# Task 14: Async Error-Handling Bugs (JavaScript)

The file `async_utils.js` exports three async utility functions.
Each function has **one defect** in its async control flow.
Your task is to identify and fix each defect so the functions behave
as described below.

There are no hint comments in the code. Study each function's behaviour
and compare it with the specification to find what is wrong.

## Function Specifications

### `fetchWithRetry(fn, retries)`
Calls the async function `fn()`. If it throws, retries up to `retries` more
times (so the total number of attempts is `retries + 1`).

- If any attempt **succeeds** (resolves), return that resolved value.
- If **all** attempts fail, the returned promise must **reject** with the
  error from the final attempt. (It must NOT resolve with `null` or any
  other fallback value.)

### `runParallel(tasks)`
Accepts an array of zero-argument async functions and runs them **all at the
same time** (in parallel).

- Returns a promise that resolves to an array of their results, in the same
  order as `tasks`.
- All tasks must start immediately — do **not** wait for one to finish before
  starting the next.

### `withTimeout(promise, ms)`
Wraps `promise` with a timeout of `ms` milliseconds.

- If `promise` resolves before the timeout: resolve with its value.
- If the timeout fires first: the returned promise must **reject** with an
  `Error` whose message is exactly `"Timed out after " + ms + "ms"`.
  (It must NOT resolve with `undefined` or any other value.)

## Examples

```javascript
// fetchWithRetry: always-failing fn must reject
const alwaysFail = () => Promise.reject(new Error("bad"));
fetchWithRetry(alwaysFail, 2).catch(e => console.log(e.message)); // "bad"

// runParallel: all tasks run at the same time
const t0 = Date.now();
await runParallel([
  () => new Promise(r => setTimeout(r, 50)),
  () => new Promise(r => setTimeout(r, 50)),
  () => new Promise(r => setTimeout(r, 50)),
]);
console.log(Date.now() - t0); // ~50ms, not ~150ms

// withTimeout: slow promise must reject
withTimeout(new Promise(r => setTimeout(r, 1000)), 100)
  .catch(e => console.log(e.message)); // "Timed out after 100ms"
```
