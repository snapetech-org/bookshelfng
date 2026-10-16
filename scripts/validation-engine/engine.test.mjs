// Copyright (C) BookshelfNG contributors.
import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, readFileSync, rmSync, statSync } from 'node:fs';
import os from 'node:os';
import path from 'node:path';

test('validation receipt export and artifact upload share the runner temp root', () => {
  const workflow = readFileSync('.github/workflows/build.yml', 'utf8');
  const receiptPath = '$' + '{{ runner.temp }}' +
    '/bookshelf-validation/receipt.json';
  assert.ok(workflow.includes('VALIDATION_RECEIPT_EXPORT: ' + receiptPath));
  assert.ok(workflow.includes('path: ' + receiptPath));
});
import { createPlan, discoverInventory, formatValidationProgress, globRegex, isolatedChildEnvironment, parseNUnitSummary, runTaskPool, stableJson, taskOutputFiles } from './engine.mjs';

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

test('only the NUnit task receives its explicit Playwright cache path', (t) => {
  const root = mkdtempSync(path.join(os.tmpdir(), 'bookshelf-validation-browser-'));
  t.after(() => rmSync(root, { recursive: true, force: true }));
  const env = isolatedChildEnvironment({
    id: 'dotnet-unit-tests',
    kind: 'test',
    passEnv: ['PLAYWRIGHT_BROWSERS_PATH'],
  }, root, {
    PATH: '/toolchain/bin',
    HOME: '/operator/home',
    PLAYWRIGHT_BROWSERS_PATH: '/runner/temp/playwright-browsers',
    GITHUB_TOKEN: 'synthetic-token',
    NODE_OPTIONS: '--require=/operator/injected.cjs',
  });
  assert.equal(env.PLAYWRIGHT_BROWSERS_PATH, '/runner/temp/playwright-browsers');
  assert.equal(env.HOME, path.join(root, 'dotnet-unit-tests-environment', 'home'));
  assert.equal(env.GITHUB_TOKEN, undefined);
  assert.equal(env.NODE_OPTIONS, undefined);
  assert.throws(() => isolatedChildEnvironment({
    id: 'engine-contract-tests',
    passEnv: ['PLAYWRIGHT_BROWSERS_PATH'],
  }, root, { PLAYWRIGHT_BROWSERS_PATH: '/runner/temp/playwright-browsers' }),
  /unapproved inherited environment variable/);
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

test('the plan declares bounded task concurrency and repository-specific output groups', () => {
  const plan = createPlan({ testsOnly: true });
  assert.equal(plan.maxConcurrentTasks, 2);
  assert.deepEqual(plan.tasks.filter((task) => task.selected).map((task) => [task.id, task.stage, task.concurrencyGroup]), [
    ['engine-contract-tests', 'tests', 'engine-contract-output'],
    ['dotnet-unit-tests', 'tests', 'nunit-output'],
  ]);
});

test('task output files are private to each task', () => {
  const nodeFiles = taskOutputFiles('/private/run', 'engine-contract-tests');
  const dotnetFiles = taskOutputFiles('/private/run', 'dotnet-unit-tests');
  assert.equal(nodeFiles.logFile, '/private/run/engine-contract-tests.log');
  assert.equal(dotnetFiles.testLogFile, '/private/run/dotnet-unit-tests-TestLog.txt');
  assert.equal(dotnetFiles.nunitResultsFile, '/private/run/dotnet-unit-tests-TestResult.xml');
  assert.notEqual(nodeFiles.testLogFile, dotnetFiles.testLogFile);
  assert.notEqual(nodeFiles.nunitResultsFile, dotnetFiles.nunitResultsFile);
  assert.throws(() => taskOutputFiles('/private/run', '../outside'), /safe lowercase identifier/);
});

test('the task pool runs independent tasks concurrently up to its configured bound', async () => {
  let active = 0;
  let maximum = 0;
  let releaseBatch;
  let signalTwoStarted;
  const batchGate = new Promise((resolve) => { releaseBatch = resolve; });
  const twoStarted = new Promise((resolve) => { signalTwoStarted = resolve; });
  const tasks = ['first', 'second', 'third'].map((id) => ({ id, stage: 'tests' }));
  const running = runTaskPool(tasks, {
    maxConcurrentTasks: 2,
    runTask: async (task) => {
      active += 1;
      maximum = Math.max(maximum, active);
      if (active === 2) signalTwoStarted();
      await batchGate;
      active -= 1;
      return { taskId: task.id, status: 'passed' };
    },
  });
  await twoStarted;
  assert.equal(maximum, 2);
  releaseBatch();
  const result = await running;
  assert.equal(maximum, 2);
  assert.equal(result.results.size, 3);
  assert.ok([...result.results.values()].every((receipt) => receipt.status === 'passed'));
  assert.ok([...result.results.values()].every((receipt) => receipt.stage === 'tests'));
});

test('the task pool serializes shared groups and waits for earlier stages and dependencies', async () => {
  const started = [];
  const activeGroups = new Set();
  const completed = new Set();
  const tasks = [
    { id: 'first-build', stage: 'build' },
    { id: 'dependent-test', stage: 'test', dependsOn: ['first-build'] },
    { id: 'other-test', stage: 'test', concurrencyGroup: 'test-output' },
    { id: 'same-output', stage: 'test', concurrencyGroup: 'test-output' },
  ];
  const result = await runTaskPool(tasks, {
    maxConcurrentTasks: 3,
    runTask: async (task) => {
      assert.equal(activeGroups.has(task.concurrencyGroup ?? task.id), false);
      if (task.stage === 'test') assert.ok(completed.has('first-build'));
      activeGroups.add(task.concurrencyGroup ?? task.id);
      started.push(task.id);
      await Promise.resolve();
      activeGroups.delete(task.concurrencyGroup ?? task.id);
      completed.add(task.id);
      return { taskId: task.id, status: 'passed' };
    },
  });
  assert.deepEqual(started, ['first-build', 'dependent-test', 'other-test', 'same-output']);
  assert.equal(result.results.size, tasks.length);
  assert.ok([...result.results.values()].every((receipt) => receipt.status === 'passed'));
});

test('a failed task blocks later batches, while tasks already in its batch finish', async () => {
  const started = [];
  const tasks = [
    { id: 'failure', stage: 'tests', concurrencyGroup: 'failure' },
    { id: 'parallel', stage: 'tests', concurrencyGroup: 'parallel' },
    { id: 'later', stage: 'tests', concurrencyGroup: 'later' },
  ];
  const result = await runTaskPool(tasks, {
    maxConcurrentTasks: 2,
    runTask: async (task) => {
      started.push(task.id);
      return { taskId: task.id, status: task.id === 'failure' ? 'failed' : 'passed' };
    },
  });
  assert.deepEqual(started, ['failure', 'parallel']);
  assert.equal(result.results.get('failure').status, 'failed');
  assert.equal(result.results.get('parallel').status, 'passed');
  assert.equal(result.results.get('later').status, 'blocked');
});

test('a source change during a concurrent batch invalidates its passes and blocks pending tasks', async () => {
  let checks = 0;
  const tasks = ['first', 'second', 'pending'].map((id) => ({ id, stage: 'tests' }));
  const result = await runTaskPool(tasks, {
    maxConcurrentTasks: 2,
    checkSource: () => { checks += 1; return checks === 1; },
    runTask: async (task) => ({ taskId: task.id, status: 'passed' }),
  });
  assert.equal(result.sourceChanged, true);
  assert.equal(result.results.get('first').status, 'blocked');
  assert.equal(result.results.get('second').status, 'blocked');
  assert.equal(result.results.get('pending').status, 'blocked');
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
    failedTestNames: [],
    failedTestNamesTruncated: false,
  });
});

test('NUnit reports without a real case total are rejected', () => {
  assert.throws(() => parseNUnitSummary('<test-run result="Passed"/>'), /aggregate counts are invalid/);
  assert.throws(() => parseNUnitSummary('<test-suite total="1"/>'), /no test-run summary/);
});

test('failed NUnit summaries retain the measured case counts for the receipt', () => {
  assert.deepEqual(parseNUnitSummary(
    '<test-run total="3" passed="2" failed="1" skipped="0" inconclusive="0" result="Failed"/>',
  ), {
    total: 3,
    passed: 2,
    failed: 1,
    skipped: 0,
    inconclusive: 0,
    result: 'Failed',
    failedTestNames: [],
    failedTestNamesTruncated: false,
  });
});

test('failed NUnit receipts include decoded case names and cap the list at 100', () => {
  const cases = Array.from({ length: 101 }, (_, index) =>
    `<test-case fullname="Fixture.case&amp;${index}" result="Failed"/>`).join('');
  const summary = parseNUnitSummary(
    `<test-run total="101" passed="0" failed="101" skipped="0" inconclusive="0" result="Failed">${cases}</test-run>`,
  );
  assert.equal(summary.failedTestNames.length, 100);
  assert.equal(summary.failedTestNames[0], 'Fixture.case&0');
  assert.equal(summary.failedTestNames[99], 'Fixture.case&99');
  assert.equal(summary.failedTestNamesTruncated, true);
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
    formatValidationProgress('sample', tasks, results, new Map([['running', 10_000]]), 75_000),
    '[validation] sample: 1/3 selected tasks complete (1 passed, 0 failed, 1 blocked, 1 pending); running Long task (1m05s)',
  );
});

test('live progress summary reports every active task with its own elapsed time', () => {
  const tasks = [
    { id: 'first', name: 'First task' },
    { id: 'second', name: 'Second task' },
  ];
  assert.equal(
    formatValidationProgress('sample', tasks, new Map(), new Map([['first', 10_000], ['second', 45_000]]), 75_000),
    '[validation] sample: 0/2 selected tasks complete (0 passed, 0 failed, 0 blocked, 2 pending); running First task (1m05s), Second task (0m30s)',
  );
});

test('plan identity serialization is stable across object insertion order', () => {
  assert.equal(stableJson({ z: 2, a: { y: 1, x: 0 } }), stableJson({ a: { x: 0, y: 1 }, z: 2 }));
});
