// Copyright (C) BookshelfNG contributors.
import test from 'node:test';
import assert from 'node:assert/strict';
import { discoverInventory, formatValidationProgress, globRegex, parseNUnitSummary, stableJson } from './engine.mjs';

test('the C# project glob includes nested test sources but not sibling trees', () => {
  const match = globRegex('src/NzbDrone.*.Test/**/*.cs');
  assert.equal(match.test('src/NzbDrone.Core.Test/Books/BookServiceTest.cs'), true);
  assert.equal(match.test('src/NzbDrone.Core.Test/Books/BookTestBase.cs'), true);
  assert.equal(match.test('src-other/NzbDrone.Core.Test/FakeTest.cs'), false);
  assert.equal(match.test('src/NzbDrone.Core/Books/BookService.cs'), false);
});

test('inventory digests identify each test file and its single native owner', () => {
  const inventory = discoverInventory();
  assert.ok(inventory.counts['csharp-unit-test-sources'] > 100);
  assert.equal(inventory.counts['validation-engine-contracts'], 1);
  assert.equal(inventory.entries.length, Object.keys(inventory.counts)
    .reduce((sum, key) => sum + inventory.counts[key], 0));
  assert.equal(new Set(inventory.entries.map((entry) => entry.file)).size, inventory.entries.length);
  assert.ok(inventory.entries.every((entry) => /^[a-f0-9]{64}$/.test(entry.sha256)));
});

test('NUnit aggregate counts retain pass, fail, skip, inconclusive and total values', () => {
  const summary = parseNUnitSummary(
    '<?xml version="1.0"?><test-run id="2" total="3448" passed="3304" failed="0" inconclusive="37" skipped="107" result="Passed"></test-run>',
  );
  assert.deepEqual(summary, {
    total: 3448,
    passed: 3304,
    failed: 0,
    skipped: 107,
    inconclusive: 37,
    result: 'Passed',
  });
});

test('NUnit reports without a real case total are rejected', () => {
  assert.throws(() => parseNUnitSummary('<test-run result="Passed"/>'), /aggregate counts are invalid/);
  assert.throws(() => parseNUnitSummary('<test-suite total="1"/>'), /no test-run summary/);
});

test('failed NUnit summaries retain the measured case counts for the receipt', () => {
  assert.deepEqual(parseNUnitSummary(
    '<test-run total="3" passed="2" failed="1" skipped="0" inconclusive="0" result="Failed"/>',
  ), { total: 3, passed: 2, failed: 1, skipped: 0, inconclusive: 0, result: 'Failed' });
});

test('live progress summary reports completed, blocked, pending, and running tasks', () => {
  const tasks = [
    { id: 'passed', name: 'Passed task' },
    { id: 'blocked', name: 'Blocked task' },
    { id: 'running', name: 'Long task' },
  ];
  const results = new Map([
    ['passed', { status: 'passed', startedAt: '2026-10-12T00:00:00.000Z' }],
    ['blocked', { status: 'blocked' }],
  ]);
  assert.equal(
    formatValidationProgress('sample', tasks, results, tasks[2], 65_000),
    '[validation] sample: 1/3 selected tasks complete (1 passed, 0 failed, 1 blocked, 1 pending); running Long task (1m05s)',
  );
});

test('plan identity serialization is stable across object insertion order', () => {
  assert.equal(stableJson({ z: 2, a: { y: 1, x: 0 } }), stableJson({ a: { x: 0, y: 1 }, z: 2 }));
});
