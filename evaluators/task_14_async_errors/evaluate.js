#!/usr/bin/env node
'use strict';
/**
 * Evaluator for Task 14: Async Error-Handling Bugs
 */

const path = require('path');

let fetchWithRetry, runParallel, withTimeout;
try {
  ({ fetchWithRetry, runParallel, withTimeout } = require(
    path.join(__dirname, '..', '..', 'tasks', 'task_14_async_errors', 'async_utils.js')
  ));
} catch (e) {
  console.log(`[FAIL] Could not load async_utils.js: ${e.message}`);
  process.exit(1);
}

let passed = 0;
let failed = 0;

async function test(name, fn) {
  try {
    const ok = await fn();
    if (ok === true) {
      console.log(`[PASS] ${name}`);
      passed++;
    } else {
      console.log(`[FAIL] ${name}: assertion failed (got ${JSON.stringify(ok)})`);
      failed++;
    }
  } catch (e) {
    console.log(`[FAIL] ${name}: unexpected rejection: ${e.message}`);
    failed++;
  }
}

async function main() {
  // -- fetchWithRetry --------------------------------------------------------

  // Bug: returns null instead of rejecting on total failure
  await test('fetchWithRetry rejects when all attempts fail', async () => {
    const alwaysFail = () => Promise.reject(new Error('network error'));
    try {
      await fetchWithRetry(alwaysFail, 2);
      return false;  // should have rejected
    } catch (e) {
      return e instanceof Error && e.message === 'network error';
    }
  });

  await test('fetchWithRetry returns value on first success', async () => {
    const alwaysSucceed = () => Promise.resolve(42);
    const result = await fetchWithRetry(alwaysSucceed, 3);
    return result === 42;
  });

  await test('fetchWithRetry succeeds after initial failures', async () => {
    let attempts = 0;
    const failThenSucceed = () => {
      attempts++;
      if (attempts < 3) return Promise.reject(new Error('not yet'));
      return Promise.resolve('done');
    };
    const result = await fetchWithRetry(failThenSucceed, 5);
    return result === 'done' && attempts === 3;
  });

  // -- runParallel -----------------------------------------------------------

  // Bug: tasks run sequentially (await in for-loop) instead of in parallel
  await test('runParallel runs tasks in parallel', async () => {
    const delay = (ms) => new Promise(r => setTimeout(r, ms));
    const t0 = Date.now();
    await runParallel([
      () => delay(50),
      () => delay(50),
      () => delay(50),
    ]);
    const elapsed = Date.now() - t0;
    // Should finish in ~50ms; sequential would take ~150ms
    return elapsed < 200;
  });

  await test('runParallel returns results in order', async () => {
    const results = await runParallel([
      () => Promise.resolve(1),
      () => Promise.resolve(2),
      () => Promise.resolve(3),
    ]);
    return JSON.stringify(results) === JSON.stringify([1, 2, 3]);
  });

  await test('runParallel with empty array', async () => {
    const results = await runParallel([]);
    return Array.isArray(results) && results.length === 0;
  });

  // -- withTimeout -----------------------------------------------------------

  // Bug: timeout Promise resolves() instead of reject(), so race resolves
  await test('withTimeout rejects with correct message when slow', async () => {
    const slow = new Promise(r => setTimeout(r, 1000));
    try {
      await withTimeout(slow, 50);
      return false;  // should have rejected
    } catch (e) {
      return e instanceof Error && e.message === 'Timed out after 50ms';
    }
  });

  await test('withTimeout resolves when promise is fast', async () => {
    const fast = new Promise(r => setTimeout(() => r('ok'), 10));
    const result = await withTimeout(fast, 500);
    return result === 'ok';
  });

  await test('withTimeout error message includes ms value', async () => {
    const slow = new Promise(r => setTimeout(r, 1000));
    try {
      await withTimeout(slow, 100);
      return false;
    } catch (e) {
      return e instanceof Error && e.message === 'Timed out after 100ms';
    }
  });

  console.log(`\nResults: ${passed}/${passed + failed} tests passed`);
}

main()
  .then(() => process.exit(failed > 0 ? 1 : 0))
  .catch(e => { console.error(e); process.exit(2); });
