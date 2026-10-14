#!/usr/bin/env node
// Copyright (C) BookshelfNG contributors.
import { createHash, randomUUID } from 'node:crypto';
import { spawn, spawnSync } from 'node:child_process';
import {
  closeSync,
  existsSync,
  lstatSync,
  mkdirSync,
  openSync,
  readFileSync,
  readlinkSync,
  unlinkSync,
  writeSync,
} from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { validation } from './config.mjs';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const ENGINE_VERSION = 1;
const INHERITED_ENVIRONMENT_KEYS = new Set([
  'ASDF_DATA_DIR', 'ASDF_DIR', 'COMSPEC', 'DOTNET_ROOT', 'DOTNET_ROOT_X64',
  'DOTNET_ROOT_X86', 'LANG', 'LC_ALL', 'LC_CTYPE', 'MISE_DATA_DIR',
  'MISE_HOME', 'NVM_DIR', 'PATH', 'PATHEXT', 'VOLTA_HOME', 'SYSTEMROOT',
  'TZ', 'WINDIR',
]);
const APPROVED_TASK_PASS_ENVIRONMENT = new Map([
  ['dotnet-unit-tests', new Set(['PLAYWRIGHT_BROWSERS_PATH'])],
]);
const MAX_CAPTURED_OUTPUT = 1024 * 1024;
const PROGRESS_INTERVAL_MS = 60_000;

function hash(value) {
  return createHash('sha256').update(value).digest('hex');
}

function stable(value) {
  if (Array.isArray(value)) return `[${value.map(stable).join(',')}]`;
  if (value && typeof value === 'object') {
    return `{${Object.keys(value).sort().map((key) => `${JSON.stringify(key)}:${stable(value[key])}`).join(',')}}`;
  }
  return JSON.stringify(value);
}

function git(args) {
  const result = spawnSync('git', args, { cwd: ROOT, encoding: 'utf8', maxBuffer: 16 * 1024 * 1024 });
  if (result.error || result.status !== 0) {
    throw new Error(`git ${args.join(' ')} failed: ${result.error?.message ?? result.stderr?.trim()}`);
  }
  return result.stdout;
}

function allRepositoryFiles() {
  const tracked = git(['ls-files', '-z']).split('\0').filter(Boolean);
  const untracked = git(['ls-files', '--others', '--exclude-standard', '-z']).split('\0').filter(Boolean);
  return [...new Set([...tracked, ...untracked])].sort();
}

function fileDigest(relative) {
  const full = path.join(ROOT, relative);
  const info = lstatSync(full);
  if (info.isSymbolicLink()) return hash(`symlink:${readlinkSync(full)}`);
  if (!info.isFile()) return hash(`non-file:${relative}`);
  return hash(readFileSync(full));
}

export function globRegex(pattern) {
  let result = '^';
  for (let index = 0; index < pattern.length; index += 1) {
    const char = pattern[index];
    if (char === '*' && pattern[index + 1] === '*') {
      index += 1;
      if (pattern[index + 1] === '/') {
        index += 1;
        result += '(?:.*/)?';
      } else result += '.*';
    } else if (char === '*') result += '[^/]*';
    else result += char.replace(/[|\\{}()[\]^$+?.]/g, '\\$&');
  }
  return new RegExp(`${result}$`);
}

export function discoverInventory(files = allRepositoryFiles(), rules = validation.inventory) {
  const entries = [];
  const counts = {};
  const ownership = new Set();
  for (const rule of rules) {
    const patterns = (rule.patterns ?? [rule.pattern]).map(globRegex);
    const matches = files.filter((relative) => patterns.some((pattern) => pattern.test(relative)));
    if (matches.length === 0) throw new Error(`Required inventory lane is empty: ${rule.id}`);
    counts[rule.id] = matches.length;
    for (const relative of matches) {
      if (ownership.has(relative)) throw new Error(`Test source has duplicate lane ownership: ${relative}`);
      ownership.add(relative);
      const full = path.join(ROOT, relative);
      if (lstatSync(full).isSymbolicLink()) throw new Error(`Test source is a symlink: ${relative}`);
      entries.push({ file: relative, lane: rule.id, framework: rule.framework, owner: rule.owner, sha256: fileDigest(relative) });
    }
  }
  entries.sort((left, right) => left.file.localeCompare(right.file));
  return { entries, counts, digest: hash(stable(entries)) };
}

function captureCandidate(inventory) {
  const commit = git(['rev-parse', 'HEAD']).trim();
  const tree = git(['rev-parse', 'HEAD^{tree}']).trim();
  const diffSha256 = hash(git(['diff', '--binary', 'HEAD']));
  const status = git(['status', '--porcelain=v1', '--untracked-files=all']);
  const inputs = validation.inputs.map((file) => ({ file, sha256: fileDigest(file) }));
  const artifacts = validation.testAssemblies.map((file) => ({
    file,
    available: existsSync(path.join(ROOT, file)) && lstatSync(path.join(ROOT, file)).isFile(),
    sha256: existsSync(path.join(ROOT, file)) && lstatSync(path.join(ROOT, file)).isFile()
      ? fileDigest(file)
      : null,
  }));
  const artifactSha256 = hash(stable(artifacts));
  const sourceSha256 = hash(stable({ commit, tree, diffSha256, inputs, inventorySha256: inventory.digest, artifactSha256 }));
  return {
    commit,
    tree,
    diffSha256,
    sourceSha256,
    inventorySha256: inventory.digest,
    inputDigests: inputs,
    testArtifactSha256: artifactSha256,
    testArtifacts: artifacts,
    dirty: status.length > 0,
    untrackedCount: git(['ls-files', '--others', '--exclude-standard', '-z']).split('\0').filter(Boolean).length,
  };
}

function inspectRuntime(runtime) {
  const result = spawnSync(runtime.command, runtime.args ?? ['--version'], {
    cwd: ROOT,
    encoding: 'utf8',
    timeout: 10000,
    maxBuffer: 1024 * 1024,
    env: { ...inheritedToolchainEnvironment(), NO_COLOR: '1' },
  });
  const text = `${result.stdout ?? ''}${result.stderr ?? ''}`.trim();
  const version = text.split(/\r?\n/, 1)[0] ?? '';
  const available = !result.error && result.status === 0;
  const expected = process.env.GITHUB_ACTIONS === 'true'
    ? (runtime.githubVersionPattern ?? runtime.versionPattern)
    : runtime.versionPattern;
  const compatible = available && new RegExp(expected).test(version);
  return { command: runtime.command, expected, available, compatible, version, exitCode: result.status };
}

function inheritedToolchainEnvironment(inherited = process.env) {
  const values = new Map();
  for (const [key, value] of Object.entries(inherited)) {
    const normalized = key.toUpperCase();
    if (!INHERITED_ENVIRONMENT_KEYS.has(normalized) || typeof value !== 'string') continue;
    if (!values.has(normalized) || key === normalized) values.set(normalized, value);
  }
  return Object.fromEntries(values);
}

function executionContext(candidate) {
  const platform = process.platform === 'win32' ? 'windows' : process.platform === 'darwin' ? 'macos' : 'linux';
  return {
    executor: process.env.GITHUB_ACTIONS === 'true' ? 'github-actions' : 'local',
    platform,
    architecture: process.arch,
    nodeVersion: process.version,
    runner: process.env.RUNNER_NAME ?? os.hostname(),
    nodeId: process.env.VALIDATION_NODE_ID ?? `bookshelf-${platform}-${process.arch}`,
    github: process.env.GITHUB_ACTIONS === 'true' ? {
      runId: process.env.GITHUB_RUN_ID ?? null,
      runAttempt: process.env.GITHUB_RUN_ATTEMPT ?? null,
      sha: process.env.GITHUB_SHA ?? null,
    } : null,
    candidateCommit: candidate.commit,
  };
}

function expandTasks(selection, inventory, candidate) {
  const maxConcurrentTasks = validation.maxConcurrentTasks ?? 1;
  if (!Number.isInteger(maxConcurrentTasks) || maxConcurrentTasks < 1 || maxConcurrentTasks > 8) {
    throw new Error('Validation maxConcurrentTasks must be an integer from 1 through 8');
  }
  const taskById = new Map();
  for (const task of validation.tasks) {
    if (typeof task.id !== 'string' || !/^[a-z0-9][a-z0-9-]*$/.test(task.id)) {
      throw new Error('Validation task ID must be a safe lowercase identifier.');
    }
    if (taskById.has(task.id)) throw new Error(`Duplicate validation task ID: ${task.id}`);
    taskById.set(task.id, task);
    const stage = task.stage ?? 'default';
    const concurrencyGroup = task.concurrencyGroup ?? task.id;
    if (typeof stage !== 'string' || stage.trim() === '' || typeof concurrencyGroup !== 'string' || concurrencyGroup.trim() === '') {
      throw new Error(`Validation task stage and concurrency group must be nonempty strings: ${task.id}`);
    }
    const passEnv = task.passEnv ?? [];
    if (!Array.isArray(passEnv) || passEnv.some((name) =>
      typeof name !== 'string' || !APPROVED_TASK_PASS_ENVIRONMENT.get(task.id)?.has(name))) {
      throw new Error('Task requests an unapproved inherited environment variable: ' + task.id);
    }
  }
  for (const task of validation.tasks) {
    if (!Array.isArray(task.dependsOn ?? []) || (task.dependsOn ?? []).some((dependency) => typeof dependency !== 'string' || !taskById.has(dependency))) {
      throw new Error(`Validation task has an invalid dependency list: ${task.id}`);
    }
  }
  const visiting = new Set();
  const visited = new Set();
  const visit = (taskId) => {
    if (visiting.has(taskId)) throw new Error(`Validation task dependency cycle includes ${taskId}`);
    if (visited.has(taskId)) return;
    visiting.add(taskId);
    for (const dependency of taskById.get(taskId).dependsOn ?? []) visit(dependency);
    visiting.delete(taskId);
    visited.add(taskId);
  };
  for (const task of validation.tasks) visit(task.id);

  const selectedIds = new Set(validation.tasks.filter((task) => selection.task
    ? task.id === selection.task
    : task.kind === 'test').map((task) => task.id));
  const dependencyQueue = [...selectedIds];
  while (dependencyQueue.length) {
    const task = taskById.get(dependencyQueue.pop());
    for (const dependency of task.dependsOn ?? []) {
      if (selectedIds.has(dependency)) continue;
      selectedIds.add(dependency);
      dependencyQueue.push(dependency);
    }
  }
  const runtimeMap = new Map();
  for (const runtime of [
    ...validation.runtimes,
    ...validation.tasks.filter((task) => selectedIds.has(task.id)).flatMap((task) => task.runtimes ?? []),
  ]) runtimeMap.set(`${runtime.command} ${stable(runtime.args ?? [])}`, runtime);
  const runtimes = [...runtimeMap.values()].map(inspectRuntime);
  const missingArtifacts = selectedIds.has('dotnet-unit-tests')
    ? candidate.testArtifacts.filter((item) => !item.available).map((item) => item.file)
    : [];
  const tasks = validation.tasks.map((task) => ({
    id: task.id,
    name: task.name,
    kind: task.kind,
    stage: task.stage ?? 'default',
    concurrencyGroup: task.concurrencyGroup ?? task.id,
    selected: selectedIds.has(task.id),
    dependsOn: task.dependsOn ?? [],
    inventory: (task.inventory ?? []).map((lane) => ({ lane, count: inventory.counts[lane] })),
    timeoutSeconds: task.timeoutSeconds,
  }));
  const body = {
    schemaVersion: ENGINE_VERSION,
    repository: validation.repository,
    selection: selection.task ?? (selection.testsOnly ? 'tests-only' : 'complete'),
    candidate,
    inventoryCounts: inventory.counts,
    inventorySha256: inventory.digest,
    runtimes,
    missingArtifacts,
    maxConcurrentTasks,
    executionContext: executionContext(candidate),
    tasks,
  };
  return { ...body, planSha256: hash(stable(body)) };
}

function currentCandidate(inventoryRules) {
  return captureCandidate(discoverInventory(allRepositoryFiles(), inventoryRules));
}

export function isolatedChildEnvironment(task, runRoot, inherited = process.env) {
  if (typeof task?.id !== 'string' || !/^[a-z0-9][a-z0-9-]*$/.test(task.id)) {
    throw new Error('Validation task ID must be a safe lowercase identifier.');
  }
  const output = inheritedToolchainEnvironment(inherited);
  const approvedPassEnv = APPROVED_TASK_PASS_ENVIRONMENT.get(task.id) ?? new Set();
  const passEnv = task.passEnv ?? [];
  if (!Array.isArray(passEnv) || passEnv.some((name) =>
    typeof name !== 'string' || !approvedPassEnv.has(name))) {
    throw new Error('Task requests an unapproved inherited environment variable: ' + task.id);
  }
  for (const name of passEnv) {
    const match = Object.entries(inherited).find(([key]) => key.toUpperCase() === name.toUpperCase());
    if (match && typeof match[1] === 'string') output[name] = match[1];
  }
  for (const [key, value] of Object.entries(task.env ?? {})) {
    if (typeof value === 'string') output[key] = value;
  }

  const environmentRoot = path.join(runRoot, `${task.id}-environment`);
  const directories = {
    HOME: path.join(environmentRoot, 'home'),
    USERPROFILE: path.join(environmentRoot, 'home'),
    TMPDIR: path.join(environmentRoot, 'tmp'),
    TMP: path.join(environmentRoot, 'tmp'),
    TEMP: path.join(environmentRoot, 'tmp'),
    XDG_CONFIG_HOME: path.join(environmentRoot, 'xdg-config'),
    XDG_CACHE_HOME: path.join(environmentRoot, 'xdg-cache'),
    APPDATA: path.join(environmentRoot, 'AppData', 'Roaming'),
    LOCALAPPDATA: path.join(environmentRoot, 'AppData', 'Local'),
    DOTNET_CLI_HOME: path.join(environmentRoot, 'dotnet-home'),
    NUGET_PACKAGES: path.join(runRoot, 'nuget-packages'),
  };
  for (const directory of new Set(Object.values(directories))) {
    mkdirSync(directory, { recursive: true, mode: 0o700 });
  }
  Object.assign(output, directories, {
    CI: 'true',
    NO_COLOR: '1',
    DOTNET_CLI_TELEMETRY_OPTOUT: '1',
    DOTNET_NOLOGO: '1',
    DOTNET_SKIP_FIRST_TIME_EXPERIENCE: '1',
  });
  if (task.kind === 'test') output.NODE_ENV = 'test';
  return output;
}

function killChild(child) {
  if (child.pid && process.platform !== 'win32') {
    try { process.kill(-child.pid, 'SIGTERM'); return; } catch { /* child may already have exited */ }
  }
  child.kill('SIGTERM');
}

export function taskOutputFiles(runRoot, taskId) {
  if (typeof taskId !== 'string' || !/^[a-z0-9][a-z0-9-]*$/.test(taskId)) {
    throw new Error('Validation task ID must be a safe lowercase identifier.');
  }
  return {
    logFile: path.join(runRoot, `${taskId}.log`),
    testLogFile: path.join(runRoot, `${taskId}-TestLog.txt`),
    nunitResultsFile: path.join(runRoot, `${taskId}-TestResult.xml`),
  };
}

async function runCommand(task, runRoot) {
  const startedAt = new Date().toISOString();
  const started = Date.now();
  const outputFiles = taskOutputFiles(runRoot, task.id);
  const logPath = outputFiles.logFile;
  const logFd = openSync(logPath, 'wx', 0o600);
  const stdoutParts = [];
  const stderrParts = [];
  let outputBytes = 0;
  const append = (parts, chunk) => {
    writeSync(logFd, chunk);
    outputBytes += chunk.length;
    parts.push(chunk.toString('utf8'));
    while (parts.reduce((size, part) => size + part.length, 0) > MAX_CAPTURED_OUTPUT) parts.shift();
  };
  const testResults = outputFiles.nunitResultsFile;
  const taskConfig = validation.tasks.find((item) => item.id === task.id);
  const env = isolatedChildEnvironment({
    ...taskConfig,
    env: {
      ...taskConfig.env,
      TEST_LOG_FILE: outputFiles.testLogFile,
      ...(task.id === 'dotnet-unit-tests' ? { TEST_RESULTS_FILE: testResults } : {}),
    },
  }, runRoot);
  const child = spawn(taskConfig.command[0], taskConfig.command.slice(1), {
    cwd: ROOT,
    env,
    stdio: ['ignore', 'pipe', 'pipe'],
    detached: process.platform !== 'win32',
    windowsHide: true,
  });
  child.stdout.on('data', (chunk) => append(stdoutParts, chunk));
  child.stderr.on('data', (chunk) => append(stderrParts, chunk));
  let timedOut = false;
  const timer = setTimeout(() => { timedOut = true; killChild(child); }, task.timeoutSeconds * 1000);
  const result = await new Promise((resolve) => {
    child.once('error', (error) => resolve({ code: null, signal: null, error }));
    child.once('close', (code, signal) => resolve({ code, signal, error: null }));
  }).finally(() => clearTimeout(timer));
  closeSync(logFd);

  const output = `${stdoutParts.join('')}\n${stderrParts.join('')}`;
  let activeCases = null;
  let passedCases = null;
  let failedCases = null;
  let skippedCases = null;
  let inconclusiveCases = null;
  let failedTestNames = [];
  let failedTestNamesTruncated = false;
  let parseError = null;
  if (task.id === 'engine-contract-tests') {
    const pass = output.match(/# pass (\d+)/);
    const fail = output.match(/# fail (\d+)/);
    activeCases = pass ? Number(pass[1]) : 0;
    passedCases = activeCases;
    failedCases = fail ? Number(fail[1]) : 0;
  } else {
    try {
      const xml = readFileSync(testResults, 'utf8');
      const summary = parseNUnitSummary(xml);
      activeCases = summary.total;
      passedCases = summary.passed;
      failedCases = summary.failed;
      skippedCases = summary.skipped;
      inconclusiveCases = summary.inconclusive;
      failedTestNames = summary.failedTestNames;
      failedTestNamesTruncated = summary.failedTestNamesTruncated;
      if (summary.result && summary.result !== 'Passed') parseError = `NUnit reported ${summary.result}`;
    } catch (error) { parseError = error.message; }
  }
  const status = timedOut || result.error || result.code !== 0 || parseError ||
    activeCases === null || activeCases < 1 || failedCases > 0 ? 'failed' : 'passed';
  const logSha256 = hash(readFileSync(logPath));
  return {
    taskId: task.id,
    status,
    startedAt,
    durationMs: Date.now() - started,
    exitCode: result.code,
    signal: result.signal,
    error: result.error?.message ?? parseError,
    timedOut,
    outputBytes,
    logSha256,
    logFile: path.basename(logPath),
    activeCases,
    passedCases,
    failedCases,
    failedTestNames,
    failedTestNamesTruncated,
    skippedCases,
    inconclusiveCases,
    inventory: task.inventory,
  };
}

function acquireLock() {
  const lockPath = path.join(os.tmpdir(), `bookshelf-validation-${hash(ROOT).slice(0, 16)}.lock`);
  const fd = openSync(lockPath, 'wx', 0o600);
  const contents = JSON.stringify({ pid: process.pid, startedAt: new Date().toISOString() });
  writeSync(fd, contents);
  closeSync(fd);
  return () => {
    try { unlinkSync(lockPath); } catch { /* lock may already be removed */ }
  };
}

function safeExportPath(value) {
  const target = path.resolve(value);
  const bases = [os.tmpdir(), process.env.RUNNER_TEMP].filter(Boolean).map((base) => path.resolve(base));
  if (!bases.some((base) => target.startsWith(`${base}${path.sep}`))) {
    throw new Error('Receipt exports must be beneath the system or runner temporary directory');
  }
  return target;
}

function exportEvidence(receipt, runRoot) {
  const receiptTarget = process.env.VALIDATION_RECEIPT_EXPORT;
  if (receiptTarget) {
    const target = safeExportPath(receiptTarget);
    mkdirSync(path.dirname(target), { recursive: true });
    const fd = openSync(target, 'w', 0o600);
    writeSync(fd, JSON.stringify(receipt, null, 2));
    closeSync(fd);
  }
  const nunitTarget = process.env.VALIDATION_NUNIT_EXPORT;
  const nunitResults = path.join(runRoot, 'dotnet-unit-tests-TestResult.xml');
  if (nunitTarget && existsSync(nunitResults)) {
    const target = safeExportPath(nunitTarget);
    mkdirSync(path.dirname(target), { recursive: true });
    const fd = openSync(target, 'w', 0o600);
    writeSync(fd, readFileSync(nunitResults));
    closeSync(fd);
  }
}

export function parseNUnitSummary(xml) {
  const root = xml.match(/<test-run\b[^>]*>/)?.[0];
  if (!root) throw new Error('NUnit XML has no test-run summary element');
  const attrs = Object.fromEntries([...root.matchAll(/([A-Za-z][A-Za-z0-9_-]*)="([^"]*)"/g)].map((match) => [match[1], match[2]]));
  const total = Number(attrs.total ?? attrs.testcasecount);
  const passed = Number(attrs.passed);
  const failed = Number(attrs.failed);
  const skipped = Number(attrs.skipped ?? 0);
  const inconclusive = Number(attrs.inconclusive ?? 0);
  if (![total, passed, failed, skipped, inconclusive].every(Number.isFinite)) throw new Error('NUnit XML aggregate counts are invalid');
  if (total < 1 || [passed, failed, skipped, inconclusive].some((count) => count < 0)) throw new Error('NUnit XML aggregate counts are invalid');
  const failedTestNames = [];
  let failedTestCount = 0;
  for (const match of xml.matchAll(/<test-case\b([^>]*)\/?\s*>/g)) {
    const caseAttrs = Object.fromEntries([...match[1].matchAll(/([A-Za-z][A-Za-z0-9_-]*)="([^"]*)"/g)]
      .map((attribute) => [attribute[1], decodeXmlAttribute(attribute[2])]));
    if (caseAttrs.result !== 'Failed') continue;
    failedTestCount += 1;
    if (failedTestNames.length < 100) failedTestNames.push(caseAttrs.fullname ?? caseAttrs.name ?? 'unknown test case');
  }
  return {
    total,
    passed,
    failed,
    skipped,
    inconclusive,
    result: attrs.result ?? null,
    failedTestNames,
    failedTestNamesTruncated: failedTestCount > failedTestNames.length,
  };
}

function decodeXmlAttribute(value) {
  return value.replace(/&(#x[0-9a-f]+|#\d+|amp|lt|gt|quot|apos);/gi, (entity, code) => {
    const normalized = code.toLowerCase();
    if (normalized === 'amp') return '&';
    if (normalized === 'lt') return '<';
    if (normalized === 'gt') return '>';
    if (normalized === 'quot') return '"';
    if (normalized === 'apos') return "'";
    const number = normalized[1] === 'x' ? Number.parseInt(normalized.slice(2), 16) : Number.parseInt(normalized.slice(1), 10);
    return Number.isInteger(number) && number >= 0 && number <= 0x10ffff && !(number >= 0xd800 && number <= 0xdfff)
      ? String.fromCodePoint(number)
      : entity;
  });
}

function formatElapsed(milliseconds) {
  const seconds = Math.floor(milliseconds / 1000);
  return `${Math.floor(seconds / 60)}m${String(seconds % 60).padStart(2, '0')}s`;
}

export function formatValidationProgress(repository, tasks, results, runningTasks = new Map(), now = Date.now()) {
  const receipts = tasks.map((task) => results.get(task.id)).filter(Boolean);
  const passed = receipts.filter((receipt) => receipt.status === 'passed').length;
  const failed = receipts.filter((receipt) => ['failed', 'incomplete'].includes(receipt.status)).length;
  const blocked = receipts.filter((receipt) => ['blocked', 'not-run'].includes(receipt.status)).length;
  const completed = passed + failed;
  const pending = Math.max(0, tasks.length - completed - blocked);
  const activeTasks = [...runningTasks].map(([taskId, startedAt]) => {
    const task = tasks.find((item) => item.id === taskId);
    return `${task?.name ?? taskId} (${formatElapsed(now - startedAt)})`;
  });
  const active = activeTasks.length ? `; running ${activeTasks.join(', ')}` : '';
  return `[validation] ${repository}: ${completed}/${tasks.length} selected tasks complete (${passed} passed, ${failed} failed, ${blocked} blocked, ${pending} pending)${active}`;
}

function writeValidationProgress(tasks, results, runningTasks = new Map(), state = null) {
  const summary = formatValidationProgress(
    validation.repository,
    tasks,
    results,
    runningTasks,
  );
  if (state?.last === summary) return;
  if (state) state.last = summary;
  process.stderr.write(`${summary}\n`);
}

export async function runTaskPool(tasks, {
  maxConcurrentTasks = 1,
  results = new Map(),
  runTask,
  checkSource = () => true,
  onTaskStart = () => {},
  onTaskFinish = () => {},
  onProgress = () => {},
} = {}) {
  if (!Number.isInteger(maxConcurrentTasks) || maxConcurrentTasks < 1 || maxConcurrentTasks > 8) {
    throw new Error('maxConcurrentTasks must be an integer from 1 through 8');
  }
  if (typeof runTask !== 'function' || typeof checkSource !== 'function') {
    throw new Error('runTask and checkSource must be functions');
  }

  const pending = [...tasks];
  const taskMetadata = (task) => ({
    stage: task.stage ?? 'default',
    concurrencyGroup: task.concurrencyGroup ?? task.id,
    dependsOn: task.dependsOn ?? [],
  });
  const blockedReceipt = (task, reason) => ({
    taskId: task.id,
    ...taskMetadata(task),
    status: 'blocked',
    reason,
    required: true,
  });
  let sourceChanged = false;
  while (pending.length) {
    const sourceMatches = checkSource();
    if (!sourceMatches) {
      sourceChanged = true;
      for (const task of pending.splice(0)) {
        results.set(task.id, blockedReceipt(task, 'candidate changed before task stage started'));
      }
      onProgress();
      break;
    }

    const stage = pending[0].stage ?? 'default';
    const batch = [];
    const groups = new Set();
    for (const task of pending) {
      if ((task.stage ?? 'default') !== stage) continue;
      if ((task.dependsOn ?? []).some((dependency) => results.get(dependency)?.status !== 'passed')) continue;
      const group = task.concurrencyGroup ?? task.id;
      if (groups.has(group)) continue;
      batch.push(task);
      groups.add(group);
      if (batch.length === maxConcurrentTasks) break;
    }
    if (batch.length === 0) {
      for (const task of pending.splice(0)) {
        results.set(task.id, blockedReceipt(task, 'required dependency did not pass or task stage is not runnable'));
      }
      onProgress();
      break;
    }

    for (const task of batch) pending.splice(pending.indexOf(task), 1);
    const startedAt = new Map(batch.map((task) => [task.id, Date.now()]));
    for (const task of batch) onTaskStart(task, startedAt.get(task.id));
    onProgress();

    await Promise.all(batch.map(async (task) => {
      let result;
      try {
        result = await runTask(task);
        if (!result || result.taskId !== task.id || !['passed', 'failed', 'blocked', 'not-run'].includes(result.status)) {
          throw new Error('task runner returned an invalid receipt');
        }
      } catch (error) {
        result = { taskId: task.id, status: 'failed', error: error.message, required: true };
      }
      results.set(task.id, { ...result, ...taskMetadata(task) });
      onTaskFinish(task, result);
      onProgress();
    }));

    const sourceStillMatches = checkSource();
    if (!sourceStillMatches) {
      sourceChanged = true;
      for (const task of batch) {
        const result = results.get(task.id);
        if (result.status === 'passed') results.set(task.id, {
          ...result,
          status: 'blocked',
          error: 'candidate source or compiled test artifact changed during concurrent execution',
        });
      }
      for (const task of pending.splice(0)) {
        results.set(task.id, blockedReceipt(task, 'candidate changed during task stage'));
      }
      onProgress();
      break;
    }

    if (batch.some((task) => results.get(task.id)?.status !== 'passed')) {
      for (const task of pending.splice(0)) {
        results.set(task.id, blockedReceipt(task, 'an earlier required task did not pass'));
      }
      onProgress();
      break;
    }
  }
  return { results, sourceChanged };
}

export function stableJson(value) {
  return stable(value);
}

export function createPlan(options = {}) {
  const inventory = discoverInventory();
  const candidate = captureCandidate(inventory);
  return expandTasks(options, inventory, candidate);
}

async function execute(plan) {
  const runRoot = path.join(os.tmpdir(), `bookshelf-validation-${randomUUID()}`);
  mkdirSync(runRoot, { mode: 0o700 });
  const releaseLock = acquireLock();
  const taskReceipts = new Map();
  let sourceChanged = false;
  try {
    const missingRuntimes = plan.runtimes.filter((runtime) => !runtime.available || !runtime.compatible);
    const missingArtifacts = plan.missingArtifacts;
    const selected = plan.tasks.filter((task) => task.selected);
    const progressState = {};
    if (missingRuntimes.length || missingArtifacts.length || (plan.executionContext.github && plan.executionContext.github.sha !== plan.candidate.commit)) {
      for (const task of selected) taskReceipts.set(task.id, {
        taskId: task.id, status: 'not-run', reason: 'required runtime, build artifact, or GitHub SHA is unavailable', required: true,
      });
    } else {
      const runningTasks = new Map();
      const updateProgress = () => writeValidationProgress(selected, taskReceipts, runningTasks, progressState);
      const heartbeat = setInterval(updateProgress, PROGRESS_INTERVAL_MS);
      heartbeat.unref();
      try {
        const pool = await runTaskPool(selected, {
          maxConcurrentTasks: plan.maxConcurrentTasks,
          results: taskReceipts,
          checkSource: () => captureCandidate(discoverInventory()).sourceSha256 === plan.candidate.sourceSha256,
          runTask: (task) => runCommand(task, runRoot),
          onTaskStart: (task, startedAt) => runningTasks.set(task.id, startedAt),
          onTaskFinish: (task) => runningTasks.delete(task.id),
          onProgress: updateProgress,
        });
        sourceChanged = pool.sourceChanged;
      } finally {
        clearInterval(heartbeat);
      }
    }
    for (const task of plan.tasks) {
      if (!taskReceipts.has(task.id)) taskReceipts.set(task.id, {
        taskId: task.id,
        status: task.selected ? 'blocked' : 'excluded',
        reason: task.selected ? 'an earlier required task did not pass' : plan.selection,
        required: true,
      });
    }
    writeValidationProgress(selected, taskReceipts, new Map(), progressState);
    const tasks = plan.tasks.map((task) => ({
      ...taskReceipts.get(task.id),
      stage: task.stage,
      concurrencyGroup: task.concurrencyGroup,
      dependsOn: task.dependsOn,
    }));
    const totals = {
      planned: plan.tasks.filter((task) => task.selected).length,
      executed: tasks.filter((task) => task.startedAt).length,
      passed: tasks.filter((task) => task.status === 'passed').length,
      failed: tasks.filter((task) => task.status === 'failed').length,
      blocked: tasks.filter((task) => task.status === 'blocked' || task.status === 'not-run').length,
      excluded: tasks.filter((task) => task.status === 'excluded').length,
      activeCases: tasks.reduce((sum, task) => sum + (task.activeCases ?? 0), 0),
      passedCases: tasks.reduce((sum, task) => sum + (task.passedCases ?? 0), 0),
      failedCases: tasks.reduce((sum, task) => sum + (task.failedCases ?? 0), 0),
      skippedCases: tasks.reduce((sum, task) => sum + (task.skippedCases ?? 0), 0),
      inconclusiveCases: tasks.reduce((sum, task) => sum + (task.inconclusiveCases ?? 0), 0),
    };
    const status = sourceChanged || totals.failed > 0 || totals.blocked > 0 || totals.passed !== totals.planned ? 'failed' : 'passed';
    const receipt = {
      schemaVersion: ENGINE_VERSION,
      repository: validation.repository,
      runId: randomUUID(),
      startedAt: new Date().toISOString(),
      completedAt: new Date().toISOString(),
      planSha256: plan.planSha256,
      candidate: plan.candidate,
      inventoryCounts: plan.inventoryCounts,
      inventorySha256: plan.inventorySha256,
      executionContext: plan.executionContext,
      sourceChanged,
      status,
      runtimes: plan.runtimes,
      missingArtifacts: plan.missingArtifacts,
      tasks,
      totals,
      evidenceDirectory: runRoot,
    };
    const receiptPath = path.join(runRoot, 'receipt.json');
    const fd = openSync(receiptPath, 'w', 0o600);
    writeSync(fd, JSON.stringify(receipt, null, 2));
    closeSync(fd);
    exportEvidence(receipt, runRoot);
    return { receipt, runRoot, exitCode: status === 'passed' ? 0 : 1 };
  } finally { releaseLock(); }
}

function printHelp() {
  process.stdout.write([
    'BookshelfNG validation engine',
    '',
    'Usage:',
    '  node scripts/validation-engine/engine.mjs --plan [--json]',
    '  node scripts/validation-engine/engine.mjs --tests-only',
    '  node scripts/validation-engine/engine.mjs --task <task-id>',
    '',
    'Run after ./build.sh --backend --frontend so the pinned Linux test assemblies exist.',
    'Evidence is private under the system temporary directory; GitHub exports are optional.',
    '',
  ].join('\n'));
}

async function main(argv = process.argv.slice(2)) {
  if (argv.includes('--help')) { printHelp(); return 0; }
  const options = { testsOnly: argv.includes('--tests-only') };
  const taskIndex = argv.indexOf('--task');
  if (taskIndex !== -1) options.task = argv[taskIndex + 1];
  const known = new Set(['--plan', '--json', '--tests-only', '--task']);
  for (let index = 0; index < argv.length; index += 1) {
    if (argv[index] === '--task') index += 1;
    else if (!known.has(argv[index])) throw new Error(`Unknown argument: ${argv[index]}`);
  }
  const plan = createPlan(options);
  if (options.task && !validation.tasks.some((task) => task.id === options.task)) throw new Error(`Unknown task: ${options.task}`);
  if (argv.includes('--plan')) {
    if (argv.includes('--json')) process.stdout.write(`${JSON.stringify(plan, null, 2)}\n`);
    else {
      process.stdout.write(`Repository: ${plan.repository}\nCandidate: ${plan.candidate.sourceSha256}\n`);
      process.stdout.write(`Inventory: ${JSON.stringify(plan.inventoryCounts)}\n`);
      for (const runtime of plan.runtimes) process.stdout.write(`Runtime ${runtime.command}: ${runtime.version} (${runtime.compatible ? 'ready' : 'unavailable or mismatched'})\n`);
      if (plan.missingArtifacts.length) process.stdout.write(`Missing built assemblies: ${plan.missingArtifacts.join(', ')}\n`);
      for (const task of plan.tasks) process.stdout.write(`${task.selected ? '[selected]' : '[excluded]'} ${task.id}: ${task.name}\n`);
    }
    return 0;
  }
  const result = await execute(plan);
  process.stdout.write(`${JSON.stringify({ repository: validation.repository, status: result.receipt.status, totals: result.receipt.totals, evidenceDirectory: result.runRoot }, null, 2)}\n`);
  return result.exitCode;
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  main().then((code) => { process.exitCode = code; }).catch((error) => {
    process.stderr.write(`${error.stack ?? error.message}\n`);
    process.exitCode = 2;
  });
}
