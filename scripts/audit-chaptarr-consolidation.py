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
import re
import subprocess


DISPOSITIONS = {'retained', 'ported', 'equivalent', 'retired'}


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


def unique_basename_candidate(path, target_paths_by_basename):
    """Return a review hint only when the target has one matching basename."""
    matches = target_paths_by_basename.get(pathlib.PurePosixPath(path).name, [])
    return matches[0] if len(matches) == 1 else None


def normalized(data):
    # Only establish textual rename equivalence; never infer behavior from it.
    return data.replace(b'Readarr', b'Chaptarr').replace(b'\r\n', b'\n')


_CSHARP_OPERATORS = tuple(sorted((
    '>>>=', '>>=', '<<=', '??=', '>>>', '=>', '==', '!=', '<=', '>=',
    '++', '--', '&&', '||', '??', '?.', '::', '+=', '-=', '*=', '/=',
    '%=', '&=', '|=', '^=', '<<', '>>', '->',
), key=len, reverse=True))
_CSHARP_NUMBER = re.compile(
    r'(?:0[xX][0-9A-Fa-f_]+|0[bB][01_]+|'
    r'(?:[0-9][0-9_]*(?:\.[0-9_]*)?|\.[0-9][0-9_]*)(?:[eE][+-]?[0-9_]+)?)'
    r'[uUlLfFdDmM]*'
)


def csharp_token_stream(data, include_comments=False):
    """Return C# tokens with whitespace removed, or None if unsupported.

    String and character literal text stays intact. Comments are omitted unless
    requested, in which case their text is included with whitespace collapsed.
    Interpolated and raw strings are conservatively left for manual review.
    """
    try:
        text = data.decode('utf-8-sig')
    except UnicodeDecodeError:
        return None

    tokens = []
    index = 0
    length = len(text)
    while index < length:
        char = text[index]

        if char.isspace():
            index += 1
            continue
        if text.startswith('//', index):
            newline = text.find('\n', index + 2)
            end = length if newline < 0 else newline
            if include_comments:
                tokens.append(('comment', re.sub(r'\s+', ' ', text[index:end]).strip()))
            index = length if newline < 0 else newline + 1
            continue
        if text.startswith('/*', index):
            end = text.find('*/', index + 2)
            if end < 0:
                return None
            if include_comments:
                tokens.append(('comment', re.sub(r'\s+', ' ', text[index:end + 2]).strip()))
            index = end + 2
            continue

        # C# raw strings have quote-count delimiters and interpolated strings
        # contain expression syntax. Leave both to a syntax-aware reviewer.
        prefix_end = index
        while prefix_end < length and text[prefix_end] == '$':
            prefix_end += 1
        if prefix_end < length and text[prefix_end] == '"':
            quote_end = prefix_end
            while quote_end < length and text[quote_end] == '"':
                quote_end += 1
            if quote_end - prefix_end >= 3:
                return None
            if prefix_end > index:
                return None
        if text.startswith('@$"', index) or text.startswith('$@"', index) or text.startswith('$"', index):
            return None

        # Ordinary and verbatim string literals are retained as single tokens.
        verbatim = text.startswith('@"', index)
        if char == '"' or verbatim:
            start = index
            index += 2 if verbatim else 1
            while index < length:
                if verbatim:
                    if text.startswith('""', index):
                        index += 2
                        continue
                    if text[index] == '"':
                        index += 1
                        break
                else:
                    if text[index] == '\\':
                        index += 2
                        continue
                    if text[index] == '"':
                        index += 1
                        break
                index += 1
            else:
                return None
            tokens.append(text[start:index])
            continue

        if char == "'":
            start = index
            index += 1
            while index < length:
                if text[index] == '\\':
                    index += 2
                    continue
                if text[index] == "'":
                    index += 1
                    break
                index += 1
            else:
                return None
            tokens.append(text[start:index])
            continue

        if char == '@' and index + 1 < length and (text[index + 1].isalpha() or text[index + 1] == '_'):
            start = index
            index += 2
            while index < length and (text[index].isalnum() or text[index] == '_'):
                index += 1
            tokens.append(text[start:index])
            continue

        if char.isalpha() or char == '_':
            start = index
            index += 1
            while index < length and (text[index].isalnum() or text[index] == '_'):
                index += 1
            tokens.append(text[start:index])
            continue

        if char.isdigit() or (char == '.' and index + 1 < length and text[index + 1].isdigit()):
            number = _CSHARP_NUMBER.match(text, index)
            if number is None:
                return None
            tokens.append(number.group(0))
            index = number.end()
            continue

        operator = next((candidate for candidate in _CSHARP_OPERATORS if text.startswith(candidate, index)), None)
        if operator is not None:
            tokens.append(operator)
            index += len(operator)
            continue

        if char.isascii() and not char.isalnum() and char not in '\\':
            tokens.append(char)
            index += 1
            continue
        return None

    return tokens


def load_review_decisions(path, source, target, changed_paths, source_tree, target_tree):
    """Load exact-revision reviewed decisions for renamed or retired paths."""
    if path is None:
        return {}

    data = json.loads(path.read_text())
    if not isinstance(data, dict):
        raise ValueError('review map must be a JSON object')
    if data.get('schemaVersion') != 1:
        raise ValueError('review map schemaVersion must be 1')
    if data.get('sourceCommit') != source or data.get('targetCommit') != target:
        raise ValueError('review map sourceCommit and targetCommit must match the pinned revisions')

    entries = data.get('decisions', [])
    if not isinstance(entries, list):
        raise ValueError('review map decisions must be a JSON array')
    decisions = {}
    for decision in entries:
        if not isinstance(decision, dict):
            raise ValueError('review map decisions must contain JSON objects')
        source_path = decision.get('sourcePath')
        kind = decision.get('decision')
        if not isinstance(source_path, str) or source_path not in changed_paths:
            raise ValueError(f'review map contains an unknown or unchanged sourcePath: {source_path!r}')
        if source_path not in source_tree:
            raise ValueError(f'review map decisions require a source file present at the pinned revision: {source_path}')
        if source_path in decisions:
            raise ValueError(f'review map contains multiple decisions for: {source_path}')
        if not isinstance(decision.get('rationale'), str) or not decision['rationale'].strip():
            raise ValueError(f'review map decision requires a rationale: {source_path}')
        if not isinstance(decision.get('evidence'), str) or not decision['evidence'].strip():
            raise ValueError(f'review map decision requires evidence: {source_path}')

        if kind == 'map':
            target_path = decision.get('targetPath')
            if not isinstance(decision.get('reviewedBy'), str) or not decision['reviewedBy'].strip():
                raise ValueError(f'reviewed mapping requires reviewedBy: {source_path}')
            if not isinstance(target_path, str) or target_path not in target_tree:
                raise ValueError(f'reviewed mapping targetPath is missing from the pinned target tree: {source_path}')
        elif kind == 'retire':
            if not isinstance(decision.get('approvedBy'), str) or not decision['approvedBy'].strip():
                raise ValueError(f'approved retirement requires approvedBy: {source_path}')
            if not isinstance(decision.get('approvalReference'), str) or not decision['approvalReference'].strip():
                raise ValueError(f'approved retirement requires approvalReference: {source_path}')
        else:
            raise ValueError(f'review map decision must be "map" or "retire": {source_path}')

        decisions[source_path] = decision
    return decisions


def load_disposition_decisions(path, source, target, changed_paths, target_tree):
    """Load exact-revision feature dispositions for changed source paths."""
    if path is None:
        return {}

    data = json.loads(path.read_text())
    if not isinstance(data, dict):
        raise ValueError('disposition map must be a JSON object')
    if data.get('schemaVersion') != 1:
        raise ValueError('disposition map schemaVersion must be 1')
    if data.get('sourceCommit') != source or data.get('targetCommit') != target:
        raise ValueError('disposition map sourceCommit and targetCommit must match the pinned revisions')

    entries = data.get('dispositions', [])
    if not isinstance(entries, list):
        raise ValueError('disposition map dispositions must be a JSON array')
    decisions = {}
    for entry in entries:
        if not isinstance(entry, dict):
            raise ValueError('disposition map entries must contain JSON objects')
        source_path = entry.get('sourcePath')
        disposition = entry.get('disposition')
        if not isinstance(source_path, str) or source_path not in changed_paths:
            raise ValueError(f'disposition map contains an unknown or unchanged sourcePath: {source_path!r}')
        if source_path in decisions:
            raise ValueError(f'disposition map contains multiple decisions for: {source_path}')
        if not isinstance(disposition, str) or disposition not in DISPOSITIONS:
            raise ValueError(f'disposition must be one of {sorted(DISPOSITIONS)}: {source_path}')
        for field in ('feature', 'rationale', 'evidence'):
            if not isinstance(entry.get(field), str) or not entry[field].strip():
                raise ValueError(f'disposition requires {field}: {source_path}')

        if disposition == 'retired':
            for field in ('approvedBy', 'approvalReference'):
                if not isinstance(entry.get(field), str) or not entry[field].strip():
                    raise ValueError(f'approved retirement requires {field}: {source_path}')
            target_paths = entry.get('targetPaths', [])
            if target_paths != []:
                raise ValueError(f'retired disposition must not claim targetPaths: {source_path}')
        else:
            if not isinstance(entry.get('reviewedBy'), str) or not entry['reviewedBy'].strip():
                raise ValueError(f'reviewed disposition requires reviewedBy: {source_path}')
            target_paths = entry.get('targetPaths')
            if (not isinstance(target_paths, list) or not target_paths
                    or any(not isinstance(target_path, str) for target_path in target_paths)):
                raise ValueError(f'{disposition} disposition requires targetPaths: {source_path}')
            if len(target_paths) != len(set(target_paths)):
                raise ValueError(f'disposition targetPaths must be unique: {source_path}')
            for target_path in target_paths:
                if target_path not in target_tree:
                    raise ValueError(f'disposition targetPath is missing from the pinned target tree: {source_path}: {target_path}')

        decisions[source_path] = entry
    return decisions


def file_state(old, new, source_data=None, target_data=None, source_path=None):
    if old is None:
        return 'deleted-in-bookshelf'
    if new is None:
        return 'no-mapped-target-file'
    if old == new:
        return 'identical'
    if (source_data is not None and target_data is not None
            and old['mode'] == new['mode']
            and normalized(source_data) == normalized(target_data)):
        return 'text-equivalent-after-brand-and-newline-normalization'
    if (source_path is not None and source_path.endswith('.cs')
            and source_data is not None and target_data is not None):
        source_tokens = csharp_token_stream(source_data)
        target_tokens = csharp_token_stream(target_data)
        source_comments = csharp_token_stream(source_data, include_comments=True)
        target_comments = csharp_token_stream(target_data, include_comments=True)
        if (source_tokens is not None and source_tokens == target_tokens
                and source_comments is not None and source_comments == target_comments):
            return 'code-equivalent-after-csharp-trivia-normalization'
    return 'different-review-required'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bookshelf', type=pathlib.Path, default=pathlib.Path('.'))
    parser.add_argument('--chaptarr', type=pathlib.Path, required=True)
    parser.add_argument('--source', default='HEAD')
    parser.add_argument('--target', default='HEAD')
    parser.add_argument('--fork-base', default='bde894431^')
    parser.add_argument('--upstream', default='refs/remotes/audit-bookshelf/develop')
    parser.add_argument('--output', type=pathlib.Path, required=True)
    parser.add_argument('--review-map', type=pathlib.Path,
                        help='Optional JSON file with exact-revision reviewed path decisions')
    parser.add_argument('--disposition-map', type=pathlib.Path,
                        help='Optional JSON file with exact-revision feature dispositions for changed paths')
    parser.add_argument('--require-complete-dispositions', action='store_true',
                        help='Fail unless the disposition map covers every changed source path')
    args = parser.parse_args()
    source = revision(args.bookshelf, args.source)
    target = revision(args.chaptarr, args.target)
    base = revision(args.bookshelf, args.fork_base)
    upstream = revision(args.bookshelf, args.upstream)
    source_tree = tree(args.bookshelf, source)
    target_tree = tree(args.chaptarr, target)
    target_paths_by_basename = collections.defaultdict(list)
    for target_path in target_tree:
        target_paths_by_basename[pathlib.PurePosixPath(target_path).name].append(target_path)
    changed = set(git(args.bookshelf, 'diff', '--name-only', '-z', base, source).decode().split('\0')) - {''}
    try:
        reviewed_decisions = load_review_decisions(
            args.review_map, source, target, changed, source_tree, target_tree)
        disposition_decisions = load_disposition_decisions(
            args.disposition_map, source, target, changed, target_tree)
        for source_path in reviewed_decisions.keys() & disposition_decisions.keys():
            review_retired = reviewed_decisions[source_path]['decision'] == 'retire'
            disposition_retired = disposition_decisions[source_path]['disposition'] == 'retired'
            if review_retired != disposition_retired:
                raise ValueError(f'review and disposition maps disagree about retirement: {source_path}')
    except (OSError, json.JSONDecodeError, ValueError) as error:
        parser.error(f'invalid review or disposition map: {error}')
    if args.require_complete_dispositions:
        if args.disposition_map is None:
            parser.error('--require-complete-dispositions requires --disposition-map')
        missing_dispositions = changed - set(disposition_decisions)
        if missing_dispositions:
            examples = ', '.join(sorted(missing_dispositions)[:5])
            parser.error(f'disposition map is incomplete: {len(missing_dispositions)} changed paths have no disposition; examples: {examples}')
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
        reviewed = reviewed_decisions.get(path)
        if reviewed is not None and reviewed['decision'] == 'map':
            target_path = reviewed['targetPath']
        new = target_tree.get(target_path)
        candidate_target_path = None
        if old is not None and new is None:
            candidate_target_path = unique_basename_candidate(path, target_paths_by_basename)
        candidate_target_blob = target_tree.get(candidate_target_path)
        source_data = target_data = None
        if old is not None and new is not None and old != new:
            source_data = git(args.bookshelf, 'cat-file', 'blob', old['oid'])
            target_data = git(args.chaptarr, 'cat-file', 'blob', new['oid'])
        state = file_state(old, new, source_data, target_data, path)
        disposition = disposition_decisions.get(path)
        retired = (
            (reviewed is not None and reviewed['decision'] == 'retire')
            or (disposition is not None and disposition['disposition'] == 'retired')
        )
        if retired:
            state = 'approved-retirement'
            target_path = None
            new = None
            candidate_target_path = None
            candidate_target_blob = None
        file_entry = {'sourcePath': path, 'targetPath': target_path if new else None,
                      'state': state, 'sourceBlob': old, 'targetBlob': new}
        if reviewed is not None:
            reviewed_fields = ('decision', 'reviewedBy', 'approvedBy', 'approvalReference',
                               'targetPath', 'rationale', 'evidence')
            file_entry['reviewedDecision'] = {
                key: reviewed[key] for key in reviewed_fields if key in reviewed
            }
        if disposition is not None:
            file_entry['reviewedDisposition'] = {
                key: disposition[key] for key in (
                    'disposition', 'feature', 'reviewedBy', 'approvedBy',
                    'approvalReference', 'targetPaths', 'rationale', 'evidence')
                if key in disposition
            }
        if candidate_target_path is not None:
            file_entry['candidateTargetPath'] = candidate_target_path
            file_entry['candidateTargetBlob'] = candidate_target_blob
        files.append(file_entry)
    report = {
        'schemaVersion': 4,
        'scope': 'All reachable commits since the first BookshelfNG fork commit parent; includes merged upstream work. File comparison covers net changes from that parent.',
        'limitations': ['Path and text equality do not prove feature parity.',
                       'Missing mapped paths may have replacements under other names.',
                       'Unique-basename candidate paths are heuristic review hints, not confirmed mappings or evidence of equivalence.',
                       'Reviewed path mappings and approved retirements record decisions; they do not prove feature equivalence or migration safety.',
                       'C# token equivalence is limited to files with supported literal syntax and matching comment text after whitespace normalization; it does not prove project inclusion, runtime behavior, or feature parity.',
                       'Recorded feature dispositions are maintainer decisions at the pinned revisions; they do not prove runtime or migration behavior.',
                       'No database, runtime, publisher, or upgrade validation is implied.'],
        'sourceCommit': source, 'targetCommit': target, 'forkBaseCommit': base,
        'bookshelfUpstreamCommit': upstream,
        'counts': {'commits': len(commits), 'commitsNotInUpstreamHistory': sum(not c['alsoInBookshelfUpstreamHistory'] for c in commits),
                   'netChangedPaths': len(files),
                   'uniqueBasenameCandidates': sum(f.get('candidateTargetPath') is not None for f in files),
                   'reviewedMappings': sum(f.get('reviewedDecision', {}).get('decision') == 'map' for f in files),
                   'approvedRetirements': sum(f.get('state') == 'approved-retirement' for f in files),
                   'reviewedDispositions': len(disposition_decisions),
                   'undispositionedPaths': len(changed) - len(disposition_decisions),
                   'dispositionStates': dict(collections.Counter(d['disposition'] for d in disposition_decisions.values())),
                   'fileStates': dict(collections.Counter(f['state'] for f in files)),
                   'undispositionedFileStates': dict(collections.Counter(
                       f['state'] for f in files if 'reviewedDisposition' not in f))},
        'commits': commits, 'files': files,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'sourceCommit': source, 'targetCommit': target, **report['counts']}, indent=2))


if __name__ == '__main__':
    main()
