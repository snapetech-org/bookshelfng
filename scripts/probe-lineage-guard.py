#!/usr/bin/env python3
"""Verify a Chaptarr candidate rejects a real Bookshelf release DB unchanged."""
import argparse
import hashlib
import json
import os
import pathlib
import shutil
import subprocess
import time


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--chaptarr', required=True, type=pathlib.Path)
    parser.add_argument('--source-config', required=True, type=pathlib.Path)
    parser.add_argument('--output', required=True, type=pathlib.Path)
    args = parser.parse_args()
    app = args.output.resolve()
    app.mkdir(parents=True, exist_ok=False)
    config = app / 'config'
    shutil.copytree(args.source_config.resolve(strict=True), config)
    database = config / 'readarr.db'
    original_hash = digest(database)
    env = {k: v for k, v in os.environ.items() if k in ('PATH', 'LANG', 'LD_LIBRARY_PATH', 'DOTNET_ROOT')}
    env.update(HOME=str(app), XDG_CONFIG_HOME=str(app / 'xdg'))
    with (app / 'process.log').open('wb') as log:
        proc = subprocess.Popen([str(args.chaptarr.resolve(strict=True)), '-nobrowser', '-data=' + str(config)],
                                cwd=args.chaptarr.resolve().parent, env=env, stdin=subprocess.DEVNULL,
                                stdout=log, stderr=subprocess.STDOUT)
        try:
            deadline = time.monotonic() + 60
            while proc.poll() is None and time.monotonic() < deadline:
                log.flush()
                if 'This database uses a Readarr/Bookshelf schema, not a Chaptarr schema.' in (app / 'process.log').read_text(errors='replace'):
                    proc.terminate()
                    proc.wait(timeout=10)
                    break
                time.sleep(0.1)
            if proc.poll() is None:
                proc.terminate()
                proc.wait(timeout=10)
            code = proc.returncode
        finally:
            if proc.poll() is None:
                proc.kill()
                proc.wait()
    log_text = (app / 'process.log').read_text(errors='replace')
    after_hash = digest(database)
    expected = 'This database uses a Readarr/Bookshelf schema, not a Chaptarr schema.'
    if expected not in log_text:
        raise RuntimeError(f'Candidate did not emit the expected lineage error (exit {code}); inspect process.log')
    if original_hash != after_hash:
        raise RuntimeError('The incompatible database changed during candidate startup')
    if '*** Migrating Main database ***' in log_text:
        raise RuntimeError('The migration runner started before rejecting the incompatible database')
    result = {'candidateExitCode': code, 'originalDatabaseSha256': original_hash,
              'afterDatabaseSha256': after_hash, 'databaseUnchanged': True,
              'migrationRunnerStarted': '*** Migrating Main database ***' in log_text, 'result': 'PASS'}
    (app / 'result.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
