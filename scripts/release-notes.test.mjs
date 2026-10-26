import assert from 'node:assert/strict';
import fs from 'node:fs';
import test from 'node:test';

import { hasExplicitNoReleaseNote } from './release-notes.mjs';

const pullRequestTemplate = fs.readFileSync(
  new URL('../.github/PULL_REQUEST_TEMPLATE.md', import.meta.url),
  'utf8'
);
const releaseNoteWorkflow = fs.readFileSync(
  new URL('../.github/workflows/release-notes.yml', import.meta.url),
  'utf8'
);

test('the default unchecked internal-only option is not an opt-out', () => {
  assert.equal(hasExplicitNoReleaseNote(pullRequestTemplate), false);
});

test('the checked internal-only option is an explicit opt-out', () => {
  const checkedTemplate = pullRequestTemplate.replace(
    '- [ ] This change is internal-only',
    '- [x] This change is internal-only'
  );

  assert.equal(hasExplicitNoReleaseNote(checkedTemplate), true);
});

test('a standalone release-note marker remains supported', () => {
  assert.equal(hasExplicitNoReleaseNote('release-note: none'), true);
});

test('a bracketed release-note marker in a commit subject is explicit', () => {
  assert.equal(
    hasExplicitNoReleaseNote(
      'docs: refresh retirement audit [release-note: none]'
    ),
    true
  );
});

test('release-note markers inside HTML comments are ignored', () => {
  assert.equal(hasExplicitNoReleaseNote('<!-- release-note: none -->'), false);
});

test('PR release-note validation uses the synthetic merge commit base', () => {
  assert.match(releaseNoteWorkflow, /validation_base_sha="\$BASE_SHA"/u);
  assert.match(
    releaseNoteWorkflow,
    /git rev-parse --verify "\$\{HEAD_SHA\}\^1"/u
  );
  assert.match(releaseNoteWorkflow, /--base "\$validation_base_sha"/u);
});

test('push release-note validation includes the head commit message with associated PR metadata', () => {
  assert.match(
    releaseNoteWorkflow,
    /printf '%s' "\$HEAD_COMMIT_MESSAGE" > "\$body_file"/u
  );
  assert.match(
    releaseNoteWorkflow,
    /printf '\\n\\n%s' "\$HEAD_COMMIT_MESSAGE" >> "\$body_file"/u
  );
});
