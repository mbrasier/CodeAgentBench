'use strict';
/**
 * Task 14: Async Error-Handling Bugs
 *
 * Each function below has one defect in its async control flow.
 * Fix every defect so the functions behave according to instructions.md.
 */

/**
 * Call fn(); retry up to `retries` more times on failure.
 * Rejects with the last error if all attempts fail.
 */
async function fetchWithRetry(fn, retries) {
  let lastErr;
  for (let i = 0; i <= retries; i++) {
    try {
      return await fn();
    } catch (e) {
      lastErr = e;
    }
  }
  return null;
}

/**
 * Run all tasks in parallel and resolve with an array of results.
 */
async function runParallel(tasks) {
  const results = [];
  for (const task of tasks) {
    results.push(await task());
  }
  return results;
}

/**
 * Resolve with promise's value, or reject after ms milliseconds.
 */
function withTimeout(promise, ms) {
  const timeout = new Promise((resolve) => {
    setTimeout(() => resolve(), ms);
  });
  return Promise.race([promise, timeout]);
}

module.exports = { fetchWithRetry, runParallel, withTimeout };
