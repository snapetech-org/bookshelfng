// Copyright (C) BookshelfNG contributors.
import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, rmSync, statSync } from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { createPlan, discoverInventory, formatValidationProgress, globRegex, isolatedChildEnvironment, parseNUnitSummary, stableJson } from './engine.mjs';

test('task environments use an allowlist and run-owned user and temporary directories', (t) => {
  const root = mkdtempSync(path.join(os.tmpdir(), 'bookshelf-validation-env-'));
  t.after(() => rmSync(root, { recursive: true, force: true }));
  assert.throws(() => isolatedChildEnvironment({ id: 'fixture', passEnv: ['GITHUB_TOKEN'] }, root, {
    GITHUB_TOKEN: 'synthetic-token',
  }), /unapproved inherited environment variable/);
  assert.throws(() => isolatedChildEnvironment({ id: '../outside' }, root), /safe lowercase identifier/);
  const env = isolatedChildEnvironment({
    id: 'fixture',
    kind: 'test',
    env: { FIXTURE_SETTING: 'expected' },
  }, root, {
    PATH: '/toolchain/bin',
    DOTNET_ROOT: '/toolchain/dotnet',
    HOME: '/operator/home',
    TMP: '/operator/tmp',
    NODE_OPTIONS: '--require=/operator/injected.cjs',
    NUGET_AUTH_TOKEN: 'synthetic-token',
    RANDOM_PRIVATE_VALUE: 'synthetic-private-value',
    XDG_CONFIG_HOME: '/operator/config',
  });
  const environmentRoot = path.join(root, 'fixture-environment');
  assert.equal(env.PATH, '/toolchain/bin');
  assert.equal(env.DOTNET_ROOT, '/toolchain/dotnet');
  assert.equal(env.HOME, path.join(environmentRoot, 'home'));
  assert.equal(env.USERPROFILE, env.HOME);
  assert.equal(env.TMP, path.join(environmentRoot, 'tmp'));
  assert.equal(env.XDG_CONFIG_HOME, path.join(environmentRoot, 'xdg-config'));
  assert.equal(env.XDG_CACHE_HOME, path.join(environmentRoot, 'xdg-cache'));
  assert.equal(env.NODE_ENV, 'test');
  assert.equal(env.CI, 'true');
  assert.equal(env.FIXTURE_SETTING, 'expected');
  for (const key of ['GITHUB_TOKEN', 'NODE_OPTIONS', 'NUGET_AUTH_TOKEN', 'RANDOM_PRIVATE_VALUE']) assert.equal(env[key], undefined);
  if (process.platform !== 'win32') {
    assert.equal(statSync(env.HOME).mode & 0o777, 0o700);
    assert.equal(statSync(env.TMP).mode & 0o777, 0o700);
  }
});

test('only the .NET unit task receives its explicit Playwright browser cache path', (t) => {
  const root = mkdtempSync(path.join(os.tmpdir(), 'bookshelf-playwright-env-'));
  t.after(() => rmSync(root, { recursive: true, force: true }));
  const cache = '/toolchain/playwright-browsers';
  const env = isolatedChildEnvironment({
    id: 'dotnet-unit-tests',
    kind: 'test',
    passEnv: ['PLAYWRIGHT_BROWSERS_PATH'],
  }, root, { PATH: '/toolchain/bin', PLAYWRIGHT_BROWSERS_PATH: cache });
  assert.equal(env.PLAYWRIGHT_BROWSERS_PATH, cache);
  assert.equal(env.HOME, path.join(root, 'dotnet-unit-tests-environment', 'home'));
  assert.throws(() => isolatedChildEnvironment({
    id: 'engine-contract-tests',
    passEnv: ['PLAYWRIGHT_BROWSERS_PATH'],
  }, root, { PLAYWRIGHT_BROWSERS_PATH: cache }), /unapproved inherited environment variable/);
});

test('runtime probes do not inherit credentials or loader options', () => {
  const previous = new Map(['GITHUB_TOKEN', 'NODE_OPTIONS'].map((name) => [name, process.env[name]]));
  process.env.GITHUB_TOKEN = 'synthetic-runtime-token';
  process.env.NODE_OPTIONS = '--require=/nonexistent-bookshelf-runtime-module.cjs';
  try {
    const plan = createPlan({ testsOnly: true });
    const nodeRuntime = plan.runtimes.find((runtime) => runtime.command === process.execPath);
    assert.ok(nodeRuntime);
    assert.equal(nodeRuntime.version, process.version);
  } finally {
    for (const [name, value] of previous) {
      if (value === undefined) delete process.env[name];
      else process.env[name] = value;
    }
  }
});

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
