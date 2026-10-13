#!/usr/bin/env python3
"""Inventory fork history and compare tracked source at pinned Git revisions.

This is a review inventory, not a semantic equivalence or migration proof.
No working-tree files, credentials, or database contents enter the report.
"""
import argparse
import collections
import hashlib
import json
import pathlib
import subprocess


def git(repo, *args):
    return subprocess.check_output(['git', '-C', str(repo), *args])


def revision(repo, ref):
    return git(repo, 'rev-parse', '--verify', ref + '^{commit}').decode().strip()


def tree(repo, ref):
    result = {}
    for record in git(repo, 'ls-tree', '-r', '-z', ref).split(b'\0'):
        if not record:
            continue
        meta, path = record.split(b'\t', 1)
        mode, kind, oid = meta.decode().split()
        if kind == 'blob':
            result[path.decode()] = {'mode': mode, 'oid': oid}
    return result


def mapped_path(path):
    return (path.replace('Readarr', 'Chaptarr')
            .replace('NzbDrone.Core.Test/', 'Chaptarr.Core.Test/'))


def normalized(data):
    # Only establish textual rename equivalence; never infer behavior from it.
    return data.replace(b'Readarr', b'Chaptarr').replace(b'\r\n', b'\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bookshelf', type=pathlib.Path, default=pathlib.Path('.'))
    parser.add_argument('--chaptarr', type=pathlib.Path, required=True)
    parser.add_argument('--source', default='HEAD')
    parser.add_argument('--target', default='HEAD')
    parser.add_argument('--fork-base', default='bde894431^')
    parser.add_argument('--upstream', default='refs/remotes/audit-bookshelf/develop')
    parser.add_argument('--output', type=pathlib.Path, required=True)
    args = parser.parse_args()
    source = revision(args.bookshelf, args.source)
    target = revision(args.chaptarr, args.target)
    base = revision(args.bookshelf, args.fork_base)
    upstream = revision(args.bookshelf, args.upstream)
    source_tree = tree(args.bookshelf, source)
    target_tree = tree(args.chaptarr, target)
    changed = set(git(args.bookshelf, 'diff', '--name-only', '-z', base, source).decode().split('\0')) - {''}
    upstream_history = set(git(args.bookshelf, 'rev-list', upstream).decode().splitlines())
    commits = []
    for line in git(args.bookshelf, 'log', '--reverse', '--format=%H%x09%ad%x09%s', '--date=short', base + '..' + source).decode().splitlines():
        sha, date, subject = line.split('\t', 2)
        paths = git(args.bookshelf, 'diff-tree', '--root', '--no-commit-id', '--name-only', '-r', '-m', '-z', sha).decode().split('\0')
        commits.append({'commit': sha, 'date': date, 'subject': subject,
                        'alsoInBookshelfUpstreamHistory': sha in upstream_history,
                        'paths': sorted(set(paths) - {''})})
    files = []
    for path in sorted(changed):
        candidate = mapped_path(path)
        target_path = candidate if candidate in target_tree else path
        old = source_tree.get(path)
        new = target_tree.get(target_path)
        state = 'deleted-in-bookshelf' if old is None else 'no-mapped-target-file'
        if old and new:
            state = 'identical' if old == new else 'different-review-required'
            if state != 'identical':
                a = git(args.bookshelf, 'cat-file', 'blob', old['oid'])
                b = git(args.chaptarr, 'cat-file', 'blob', new['oid'])
                if old['mode'] == new['mode'] and normalized(a) == normalized(b):
                    state = 'text-equivalent-after-brand-and-newline-normalization'
        files.append({'sourcePath': path, 'targetPath': target_path if new else None,
                      'state': state, 'sourceBlob': old, 'targetBlob': new})
    report = {
        'schemaVersion': 1,
        'scope': 'All reachable commits since the first BookshelfNG fork commit parent; includes merged upstream work. File comparison covers net changes from that parent.',
        'limitations': ['Path and text equality do not prove feature parity.',
                       'Missing mapped paths may have replacements under other names.',
                       'No database, runtime, publisher, or upgrade validation is implied.'],
        'sourceCommit': source, 'targetCommit': target, 'forkBaseCommit': base,
        'bookshelfUpstreamCommit': upstream,
        'counts': {'commits': len(commits), 'commitsNotInUpstreamHistory': sum(not c['alsoInBookshelfUpstreamHistory'] for c in commits),
                   'netChangedPaths': len(files), 'fileStates': dict(collections.Counter(f['state'] for f in files))},
        'commits': commits, 'files': files,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'sourceCommit': source, 'targetCommit': target, **report['counts']}, indent=2))


if __name__ == '__main__':
    main()
