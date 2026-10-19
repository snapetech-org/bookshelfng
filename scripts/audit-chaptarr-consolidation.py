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


def unique_basename_candidate(path, target_paths_by_basename):
    """Return a review hint only when the target has one matching basename."""
    matches = target_paths_by_basename.get(pathlib.PurePosixPath(path).name, [])
    return matches[0] if len(matches) == 1 else None


def normalized(data):
    # Only establish textual rename equivalence; never infer behavior from it.
    return data.replace(b'Readarr', b'Chaptarr').replace(b'\r\n', b'\n')


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


def file_state(old, new, source_data=None, target_data=None):
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
    except (OSError, json.JSONDecodeError, ValueError) as error:
        parser.error(f'invalid review map: {error}')
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
        state = file_state(old, new, source_data, target_data)
        if reviewed is not None and reviewed['decision'] == 'retire':
            state = 'approved-retirement'
            target_path = None
            new = None
        file_entry = {'sourcePath': path, 'targetPath': target_path if new else None,
                      'state': state, 'sourceBlob': old, 'targetBlob': new}
        if reviewed is not None:
            reviewed_fields = ('decision', 'reviewedBy', 'approvedBy', 'approvalReference',
                               'targetPath', 'rationale', 'evidence')
            file_entry['reviewedDecision'] = {
                key: reviewed[key] for key in reviewed_fields if key in reviewed
            }
        if candidate_target_path is not None:
            file_entry['candidateTargetPath'] = candidate_target_path
            file_entry['candidateTargetBlob'] = candidate_target_blob
        files.append(file_entry)
    report = {
        'schemaVersion': 3,
        'scope': 'All reachable commits since the first BookshelfNG fork commit parent; includes merged upstream work. File comparison covers net changes from that parent.',
        'limitations': ['Path and text equality do not prove feature parity.',
                       'Missing mapped paths may have replacements under other names.',
                       'Unique-basename candidate paths are heuristic review hints, not confirmed mappings or evidence of equivalence.',
                       'Reviewed path mappings and approved retirements record decisions; they do not prove feature equivalence or migration safety.',
                       'No database, runtime, publisher, or upgrade validation is implied.'],
        'sourceCommit': source, 'targetCommit': target, 'forkBaseCommit': base,
        'bookshelfUpstreamCommit': upstream,
        'counts': {'commits': len(commits), 'commitsNotInUpstreamHistory': sum(not c['alsoInBookshelfUpstreamHistory'] for c in commits),
                   'netChangedPaths': len(files),
                   'uniqueBasenameCandidates': sum(f.get('candidateTargetPath') is not None for f in files),
                   'reviewedMappings': sum(f.get('reviewedDecision', {}).get('decision') == 'map' for f in files),
                   'approvedRetirements': sum(f.get('state') == 'approved-retirement' for f in files),
                   'fileStates': dict(collections.Counter(f['state'] for f in files))},
        'commits': commits, 'files': files,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'sourceCommit': source, 'targetCommit': target, **report['counts']}, indent=2))


if __name__ == '__main__':
    main()
