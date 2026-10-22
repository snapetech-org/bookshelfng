#!/usr/bin/env python3
"""Start a released binary with throwaway configuration and retain its schema.

The output directory must not exist. Only loopback is exposed and no provider
credentials are supplied. ``--populate-bookshelf`` seeds deterministic,
synthetic linked records into a real BookshelfNG release schema and restarts
the release to verify its author/book API can read them. It is test data, not a
production database or proof that a converter is correct.
"""
import argparse
import hashlib
import json
import os
import pathlib
import re
import secrets
import socket
import sqlite3
import subprocess
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET


FIXTURE_ID = 9001
FIXTURE_DATE = '2026-10-12 12:00:00Z'
FIXTURE_TABLES = frozenset({
    'Tags', 'Config', 'RootFolders', 'AuthorMetadata', 'Authors', 'Books',
    'Editions', 'BookFiles', 'ExtraFiles', 'MetadataFiles', 'Series',
    'SeriesBookLink', 'Users', 'Notifications', 'History', 'DownloadHistory',
    'Blocklist',
})
SQL_IDENTIFIER = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*$')


def api_json(port, key, route):
    if not isinstance(route, str) or not route.startswith('/') or route.startswith('//') or '\\' in route:
        raise ValueError('Fixture API route must remain on the loopback server')
    request = urllib.request.Request(
        f'http://127.0.0.1:{port}{route}',
        headers={'X-Api-Key': key},
    )
    # nosemgrep: python.lang.security.audit.dynamic-urllib-use-detected.dynamic-urllib-use-detected -- Destination is the local fixture process on 127.0.0.1 and routes are constrained above.
    with urllib.request.urlopen(request, timeout=8) as response:
        return json.load(response)


def run_release(binary, data, output, env, port, key, routes=()):
    status = None
    api_results = {}
    with (output / 'process.log').open('ab') as log:
        process = subprocess.Popen(
            [str(binary), '-nobrowser', '-data=' + str(data)],
            cwd=binary.parent,
            env=env,
            stdin=subprocess.DEVNULL,
            stdout=log,
            stderr=subprocess.STDOUT,
        )
        try:
            deadline = time.monotonic() + 90
            while time.monotonic() < deadline:
                if process.poll() is not None:
                    raise RuntimeError('Release exited before readiness; inspect process.log')
                try:
                    status = api_json(port, key, '/api/v1/system/status')
                    break
                except (urllib.error.URLError, TimeoutError):
                    time.sleep(0.25)
            if status is None:
                raise TimeoutError('Release did not become ready')

            for route in routes:
                payload = api_json(port, key, route)
                if not isinstance(payload, list):
                    raise RuntimeError(f'Expected a JSON list from {route}')
                api_results[route] = {
                    'itemCount': len(payload),
                    'items': [
                        {
                            'id': item.get('id'),
                            'foreignId': item.get('foreignAuthorId') or item.get('foreignBookId'),
                            'title': item.get('authorName') or item.get('title'),
                        }
                        for item in payload
                    ],
                }
        finally:
            if process.poll() is None:
                process.terminate()
            try:
                process.wait(timeout=20)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
    return status, api_results


def insert_row(connection, table, row):
    if table not in FIXTURE_TABLES:
        raise ValueError(f'Unsupported fixture table: {table}')
    if any(not SQL_IDENTIFIER.fullmatch(name) for name in row):
        raise ValueError('Fixture columns must be static SQLite identifiers')

    quoted_table = '"' + table.replace('"', '""') + '"'
    columns = ', '.join('"' + name.replace('"', '""') + '"' for name in row)
    values = ', '.join('?' for _ in row)
    # Identifiers are allowlisted/validated above; all row values are bound parameters.
    # nosemgrep: python.sqlalchemy.security.sqlalchemy-execute-raw-query.sqlalchemy-execute-raw-query, python.lang.security.audit.formatted-sql-query.formatted-sql-query -- Table/column identifiers are allowlisted and quoted; every value is a bound parameter.
    connection.execute(
        f'INSERT INTO {quoted_table} ({columns}) VALUES ({values})',
        tuple(row.values()),
    )


def populate_bookshelf_fixture(database, output):
    library = output / 'library'
    default_author_path = library / 'Jane Fixture'
    ebook_root = library / 'ebooks'
    audiobook_root = library / 'audiobooks'
    ebook_author_path = ebook_root / 'Jane Fixture'
    audiobook_author_path = audiobook_root / 'Jane Fixture'
    for folder in (default_author_path, ebook_author_path, audiobook_author_path):
        folder.mkdir(mode=0o700, parents=True, exist_ok=True)

    ebook_path = ebook_author_path / 'the-migration-atlas.epub'
    audiobook_path = audiobook_author_path / 'the-migration-atlas.m4b'
    cover_path = ebook_author_path / 'cover.jpg'
    sidecar_path = default_author_path / 'author-metadata.json'
    ebook_path.write_bytes(b'synthetic BookshelfNG EPUB fixture\n')
    audiobook_path.write_bytes(b'synthetic BookshelfNG M4B fixture\n')
    cover_path.write_bytes(b'synthetic cover fixture\n')
    sidecar_path.write_text('{"fixture":true}\n')

    with sqlite3.connect(database) as connection:
        connection.execute('PRAGMA foreign_keys = ON')
        quality_profiles = dict(connection.execute('SELECT Name, Id FROM QualityProfiles'))
        metadata_profiles = dict(connection.execute('SELECT Name, Id FROM MetadataProfiles'))
        ebook_profile = quality_profiles['eBook']
        audiobook_profile = quality_profiles['Spoken']
        standard_metadata = metadata_profiles['Standard']
        no_metadata = metadata_profiles['None']

        with connection:
            insert_row(connection, 'Tags', {'Id': FIXTURE_ID, 'Label': 'Migration Fixture'})
            for key, value in (
                ('HardcoverAuth', 'Bearer fixture-hardcover-token'),
                ('BookImportMinimumMatchPercent', '75'),
                ('MetadataCatalogSources', 'openlibrary,googlebooks'),
                ('GoogleBooksApiKey', 'fixture-key-preserved'),
                ('MetadataTitleSourcePreference', 'openlibrary'),
                ('MetadataCoverSourcePreference', 'googlebooks'),
            ):
                insert_row(connection, 'Config', {'Key': key, 'Value': value})
            insert_row(connection, 'RootFolders', {
                'Id': FIXTURE_ID,
                'Path': str(ebook_root),
                'Name': 'Migration Fixture Ebooks',
                'DefaultMetadataProfileId': standard_metadata,
                'DefaultQualityProfileId': ebook_profile,
                'DefaultMonitorOption': 0,
                'DefaultTags': json.dumps([FIXTURE_ID]),
                'IsCalibreLibrary': 0,
                'CalibreSettings': None,
                'DefaultNewItemMonitorOption': 0,
            })
            insert_row(connection, 'RootFolders', {
                'Id': FIXTURE_ID + 1,
                'Path': str(audiobook_root),
                'Name': 'Migration Fixture Audiobooks',
                'DefaultMetadataProfileId': standard_metadata,
                'DefaultQualityProfileId': audiobook_profile,
                'DefaultMonitorOption': 0,
                'DefaultTags': json.dumps([FIXTURE_ID]),
                'IsCalibreLibrary': 0,
                'CalibreSettings': None,
                'DefaultNewItemMonitorOption': 0,
            })
            insert_row(connection, 'AuthorMetadata', {
                'Id': FIXTURE_ID,
                # BookshelfNG's native Hardcover mode stores primary catalog
                # IDs as bare numbers. Keep this fixture in that real source
                # dialect so the ChaptarrNG handoff can verify mode-aware
                # provider identity conversion.
                'ForeignAuthorId': '9001',
                'TitleSlug': 'jane-fixture',
                'Name': 'Jane Fixture',
                'Overview': 'Synthetic linked-record migration fixture',
                'Disambiguation': None,
                'Gender': None,
                'Hometown': None,
                'Born': '1980-01-01',
                'Died': None,
                'Status': 0,
                'Images': '[]',
                'Links': '[]',
                'Genres': '["fiction"]',
                'Ratings': None,
                'Aliases': '["J. Fixture"]',
                'SortName': 'Fixture, Jane',
                'NameLastFirst': 'Jane Fixture',
                'SortNameLastFirst': 'Fixture, Jane',
            })
            insert_row(connection, 'Authors', {
                'Id': FIXTURE_ID,
                'CleanName': 'janefixture',
                'Path': str(default_author_path),
                'Monitored': 1,
                'LastInfoSync': FIXTURE_DATE,
                'QualityProfileId': ebook_profile,
                'Tags': json.dumps([FIXTURE_ID]),
                'Added': FIXTURE_DATE,
                'AddOptions': '{}',
                'MetadataProfileId': standard_metadata,
                'AuthorMetadataId': FIXTURE_ID,
                'MonitorNewItems': 1,
                'EbookPath': str(ebook_author_path),
                'AudiobookPath': str(audiobook_author_path),
                'EbookQualityProfileId': ebook_profile,
                'AudiobookQualityProfileId': audiobook_profile,
                'EbookMetadataProfileId': standard_metadata,
                'AudiobookMetadataProfileId': no_metadata,
            })
            insert_row(connection, 'Books', {
                'Id': FIXTURE_ID,
                'AuthorMetadataId': FIXTURE_ID,
                'ForeignBookId': '9002',
                'TitleSlug': 'the-migration-atlas-fixture',
                'Title': 'The Migration Atlas',
                'ReleaseDate': '2024-03-12',
                'Links': '[]',
                'Genres': '["fiction"]',
                'Ratings': None,
                'CleanTitle': 'themigrationatlas',
                'Monitored': 1,
                'AnyEditionOk': 0,
                'LastInfoSync': FIXTURE_DATE,
                'Added': FIXTURE_DATE,
                'AddOptions': '{}',
                'RelatedBooks': '[]',
                'LastSearchTime': None,
            })
            insert_row(connection, 'Editions', {
                'Id': FIXTURE_ID,
                'BookId': FIXTURE_ID,
                'ForeignEditionId': '9003',
                'Isbn13': '9780306406157',
                'Asin': None,
                'Title': 'The Migration Atlas (EPUB)',
                'TitleSlug': 'the-migration-atlas-epub-fixture',
                'Language': 'eng',
                'Overview': 'Synthetic ebook edition',
                'Format': 'EPUB',
                'IsEbook': 1,
                'Disambiguation': None,
                'Publisher': 'Fixture Press',
                'PageCount': 240,
                'ReleaseDate': '2024-03-12',
                'Images': '[]',
                'Links': '[]',
                'Ratings': None,
                'Monitored': 1,
                'ManualAdd': 0,
                'Narrator': None,
            })
            insert_row(connection, 'Editions', {
                'Id': FIXTURE_ID + 1,
                'BookId': FIXTURE_ID,
                'ForeignEditionId': '9004',
                'Isbn13': None,
                'Asin': 'B0FIXTURE01',
                'Title': 'The Migration Atlas (Audiobook)',
                'TitleSlug': 'the-migration-atlas-audiobook-fixture',
                'Language': 'eng',
                'Overview': 'Synthetic audiobook edition',
                'Format': 'M4B',
                'IsEbook': 0,
                'Disambiguation': None,
                'Publisher': 'Fixture Audio',
                'PageCount': None,
                'ReleaseDate': '2024-03-12',
                'Images': '[]',
                'Links': '[]',
                'Ratings': None,
                'Monitored': 0,
                'ManualAdd': 0,
                'Narrator': 'Morgan Example',
            })
            quality_ebook = json.dumps({
                'quality': 2,
                'revision': {'version': 1, 'real': 0, 'isRepack': False},
            })
            quality_audio = json.dumps({
                'quality': 10,
                'revision': {'version': 1, 'real': 0, 'isRepack': False},
            })
            for file_id, edition_id, file_path, quality in (
                (FIXTURE_ID, FIXTURE_ID, ebook_path, quality_ebook),
                (FIXTURE_ID + 1, FIXTURE_ID + 1, audiobook_path, quality_audio),
            ):
                stat = file_path.stat()
                insert_row(connection, 'BookFiles', {
                    'Id': file_id,
                    'EditionId': edition_id,
                    'CalibreId': 0,
                    'Quality': quality,
                    'Size': stat.st_size,
                    'SceneName': file_path.name,
                    'DateAdded': FIXTURE_DATE,
                    'ReleaseGroup': 'MigrationFixture',
                    'MediaInfo': None,
                    'Modified': FIXTURE_DATE,
                    'Path': str(file_path),
                    'Part': 1,
                    'OriginalFilePath': str(file_path),
                    'IndexerFlags': 0,
                    'LastRemoteSearchTime': None,
                })
            insert_row(connection, 'ExtraFiles', {
                'Id': FIXTURE_ID,
                'AuthorId': FIXTURE_ID,
                'BookId': FIXTURE_ID,
                'BookFileId': FIXTURE_ID,
                'RelativePath': 'cover.jpg',
                'Extension': '.jpg',
                'Added': FIXTURE_DATE,
                'LastUpdated': FIXTURE_DATE,
            })
            insert_row(connection, 'MetadataFiles', {
                'Id': FIXTURE_ID,
                'AuthorId': FIXTURE_ID,
                'Consumer': 'Readarr',
                'Type': 1,
                'RelativePath': 'author-metadata.json',
                'LastUpdated': FIXTURE_DATE,
                'BookId': None,
                'BookFileId': None,
                'Hash': hashlib.sha256(sidecar_path.read_bytes()).hexdigest(),
                'Added': FIXTURE_DATE,
                'Extension': '.json',
            })
            insert_row(connection, 'Series', {
                'Id': FIXTURE_ID,
                'ForeignSeriesId': '9005',
                'Title': 'Atlas Cycle',
                'Description': 'Synthetic series relationship',
                'Numbered': 1,
                'WorkCount': 3,
                'PrimaryWorkCount': 3,
            })
            insert_row(connection, 'SeriesBookLink', {
                'Id': FIXTURE_ID,
                'SeriesId': FIXTURE_ID,
                'BookId': FIXTURE_ID,
                'Position': '1',
                'IsPrimary': 1,
                'SeriesPosition': 1,
            })
            insert_row(connection, 'Users', {
                'Id': FIXTURE_ID,
                'Identifier': '00000000-0000-0000-0000-000000002329',
                'Username': 'migration-fixture-user',
                'Password': hashlib.sha256(b'migration-fixture-only').hexdigest(),
            })
            insert_row(connection, 'Notifications', {
                'Id': FIXTURE_ID,
                'Name': 'BookLore migration fixture',
                'OnGrab': 0,
                'Settings': json.dumps({
                    'baseUrl': 'http://127.0.0.1:1',
                    'username': 'fixture-only',
                    'password': 'fixture-only-not-a-credential',
                }),
                'Implementation': 'BookLore',
                'ConfigContract': 'BookLoreSettings',
                'OnUpgrade': 0,
                'Tags': '[]',
                'OnRename': 0,
                'OnReleaseImport': 1,
                'OnHealthIssue': 0,
                'IncludeHealthWarnings': 0,
                'OnDownloadFailure': 0,
                'OnImportFailure': 1,
                'OnBookRetag': 0,
                'OnAuthorDelete': 0,
                'OnBookDelete': 0,
                'OnBookFileDelete': 0,
                'OnBookFileDeleteForUpgrade': 0,
                'OnApplicationUpdate': 0,
                'OnAuthorAdded': 0,
            })
            insert_row(connection, 'History', {
                'Id': FIXTURE_ID,
                'SourceTitle': 'The Migration Atlas - Fixture EPUB',
                'Date': FIXTURE_DATE,
                'Quality': quality_ebook,
                'Data': '{"fixture":true}',
                'EventType': 1,
                'DownloadId': 'fixture-download-9001',
                'AuthorId': FIXTURE_ID,
                'BookId': FIXTURE_ID,
            })
            insert_row(connection, 'DownloadHistory', {
                'Id': FIXTURE_ID,
                'EventType': 1,
                'AuthorId': FIXTURE_ID,
                'DownloadId': 'fixture-download-9001',
                'SourceTitle': 'The Migration Atlas - Fixture EPUB',
                'Date': FIXTURE_DATE,
                'Protocol': 0,
                'IndexerId': None,
                'DownloadClientId': None,
                'Release': '{"fixture":true}',
                'Data': '{"fixture":true}',
            })
            insert_row(connection, 'Blocklist', {
                'Id': FIXTURE_ID,
                'SourceTitle': 'The Migration Atlas - Rejected Fixture',
                'Quality': quality_ebook,
                'Date': FIXTURE_DATE,
                'PublishedDate': FIXTURE_DATE,
                'Size': 12345,
                'Protocol': 0,
                'Indexer': 'Migration Fixture',
                'Message': 'Synthetic rejection record',
                'TorrentInfoHash': None,
                'AuthorId': FIXTURE_ID,
                'BookIds': json.dumps([FIXTURE_ID]),
                'IndexerFlags': 0,
            })

        counts = {}
        for table in (
            'AuthorMetadata', 'Authors', 'Books', 'Editions', 'BookFiles',
            'ExtraFiles', 'MetadataFiles', 'Series', 'SeriesBookLink', 'Users',
            'Notifications', 'History', 'DownloadHistory', 'Blocklist', 'RootFolders', 'Tags', 'Config',
        ):
            # nosemgrep: python.sqlalchemy.security.sqlalchemy-execute-raw-query.sqlalchemy-execute-raw-query, python.lang.security.audit.formatted-sql-query.formatted-sql-query -- `table` is selected from the fixed report schema tuple above.
            counts[table] = connection.execute(f'SELECT COUNT(*) FROM "{table}"').fetchone()[0]
        integrity = connection.execute('PRAGMA integrity_check').fetchall()
        if integrity != [('ok',)]:
            raise RuntimeError('Populated fixture failed SQLite integrity_check')
        foreign_key_errors = connection.execute('PRAGMA foreign_key_check').fetchall()
        if foreign_key_errors:
            raise RuntimeError(f'Populated fixture has foreign-key errors: {foreign_key_errors}')
    return counts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--binary', required=True, type=pathlib.Path)
    parser.add_argument('--output', required=True, type=pathlib.Path)
    parser.add_argument('--flavor', choices=['hardcover', 'softcover', 'chaptarr'], required=True)
    parser.add_argument('--database-name', default=None,
                        help='Set the expected native DB filename when testing ChaptarrNG.')
    parser.add_argument('--populate-bookshelf', action='store_true',
                        help='Seed linked synthetic BookshelfNG records and verify API reads.')
    args = parser.parse_args()
    if args.populate_bookshelf and args.flavor == 'chaptarr':
        parser.error('--populate-bookshelf applies only to BookshelfNG release flavors')

    binary = args.binary.resolve(strict=True)
    output = args.output.resolve()
    output.mkdir(mode=0o700, parents=True, exist_ok=False)
    data = output / 'config'
    data.mkdir(mode=0o700)
    with socket.socket() as sock:
        sock.bind(('127.0.0.1', 0))
        port = sock.getsockname()[1]
    key = secrets.token_hex(16)
    config = ET.Element('Config')
    for name, value in {'BindAddress': '127.0.0.1', 'Port': str(port),
                        'ApiKey': key, 'AuthenticationMethod': 'Forms',
                        'AuthenticationRequired': 'Enabled', 'LaunchBrowser': 'False',
                        'UpdateAutomatically': 'False', 'LogLevel': 'warn'}.items():
        ET.SubElement(config, name).text = value
    ET.ElementTree(config).write(data / 'config.xml', encoding='utf-8')
    env = {k: v for k, v in os.environ.items() if k in ('PATH', 'LANG', 'LD_LIBRARY_PATH', 'DOTNET_ROOT')}
    env.update(HOME=str(output), XDG_CONFIG_HOME=str(output / 'xdg'),
               HARDCOVER=str(args.flavor == 'hardcover').lower())
    status, _ = run_release(binary, data, output, env, port, key)

    database_name = args.database_name or ('chaptarr.db' if args.flavor == 'chaptarr' else 'readarr.db')
    database = data / database_name
    population = None
    api_probe = None
    if args.populate_bookshelf:
        population = populate_bookshelf_fixture(database, output)
        status, api_probe = run_release(
            binary,
            data,
            output,
            env,
            port,
            key,
            routes=(f'/api/v1/author', f'/api/v1/book?authorId={FIXTURE_ID}'),
        )
        authors = api_probe['/api/v1/author']
        books = api_probe[f'/api/v1/book?authorId={FIXTURE_ID}']
        if authors['itemCount'] != 1 or books['itemCount'] != 1:
            raise RuntimeError('Released app API did not return the seeded author and book')
        if books['items'][0]['title'] != 'The Migration Atlas (EPUB)':
            raise RuntimeError('Released app API returned an unexpected book title')

    with sqlite3.connect(database.as_uri() + '?mode=ro', uri=True) as connection:
        integrity = connection.execute('PRAGMA integrity_check').fetchall()
        if integrity != [('ok',)]:
            raise RuntimeError('Fixture database failed integrity check')
        schema = connection.execute("SELECT type, name, tbl_name, sql FROM sqlite_master WHERE name NOT LIKE 'sqlite_%' ORDER BY type, name").fetchall()
        versions = connection.execute('SELECT Version FROM VersionInfo ORDER BY Version').fetchall()
    result = {
        'flavor': args.flavor,
        'reportedVersion': status.get('version'),
        'binarySha256': hashlib.sha256(binary.read_bytes()).hexdigest(),
        'databaseName': database_name,
        'databaseSha256': hashlib.sha256(database.read_bytes()).hexdigest(),
        'versions': [v[0] for v in versions],
        'schema': schema,
        'population': population,
        'apiReadProbe': api_probe,
        'scope': 'Released BookshelfNG schema with deterministic synthetic linked records and source API read checks; not production conversion proof.' if args.populate_bookshelf else 'Empty released-application startup only; no conversion or populated-library proof.',
    }
    (output / 'fixture.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'schema'}, indent=2))


if __name__ == '__main__':
    main()
