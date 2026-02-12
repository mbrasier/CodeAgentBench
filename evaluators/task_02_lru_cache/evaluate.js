#!/usr/bin/env node
'use strict';
/**
 * Evaluator for Task 02: LRU Cache
 */

const path = require('path');

let LRUCache;
try {
  ({ LRUCache } = require(
    path.join(__dirname, '..', '..', 'tasks', 'task_02_lru_cache', 'lru_cache.js')
  ));
} catch (e) {
  console.log(`[FAIL] Could not load lru_cache.js: ${e.message}`);
  process.exit(1);
}

let passed = 0;
let failed = 0;

function test(name, fn) {
  try {
    const ok = fn();
    if (ok === true) {
      console.log(`[PASS] ${name}`);
      passed++;
    } else {
      console.log(`[FAIL] ${name}: assertion returned false`);
      failed++;
    }
  } catch (e) {
    if (e.message === 'Not implemented') {
      console.log(`[FAIL] ${name}: not implemented`);
    } else {
      console.log(`[FAIL] ${name}: ${e.message}`);
    }
    failed++;
  }
}

// Basic get/put
test('get returns -1 for missing key', () => {
  const c = new LRUCache(2);
  return c.get(1) === -1;
});

test('put and get basic', () => {
  const c = new LRUCache(2);
  c.put(1, 10);
  return c.get(1) === 10;
});

test('get after update returns new value', () => {
  const c = new LRUCache(2);
  c.put(1, 1);
  c.put(1, 99);
  return c.get(1) === 99;
});

// Eviction
test('evicts LRU on overflow', () => {
  const c = new LRUCache(2);
  c.put(1, 1);
  c.put(2, 2);
  c.put(3, 3);   // evicts 1
  return c.get(1) === -1 && c.get(2) === 2 && c.get(3) === 3;
});

test('get promotes entry preventing its eviction', () => {
  const c = new LRUCache(2);
  c.put(1, 1);
  c.put(2, 2);
  c.get(1);      // 1 is now MRU
  c.put(3, 3);   // evicts 2, not 1
  return c.get(1) === 1 && c.get(2) === -1;
});

test('put update promotes entry preventing its eviction', () => {
  const c = new LRUCache(2);
  c.put(1, 1);
  c.put(2, 2);
  c.put(1, 10);  // update — 1 is now MRU
  c.put(3, 3);   // evicts 2
  return c.get(1) === 10 && c.get(2) === -1 && c.get(3) === 3;
});

test('capacity 1 always evicts previous', () => {
  const c = new LRUCache(1);
  c.put(1, 1);
  c.put(2, 2);
  return c.get(1) === -1 && c.get(2) === 2;
});

// Leetcode 146 canonical example
test('leetcode 146 canonical sequence', () => {
  const c = new LRUCache(2);
  c.put(1, 1);
  c.put(2, 2);
  const r1 = c.get(1);  // 1
  c.put(3, 3);           // evicts 2
  const r2 = c.get(2);  // -1
  c.put(4, 4);           // evicts 1
  const r3 = c.get(1);  // -1
  const r4 = c.get(3);  // 3
  const r5 = c.get(4);  // 4
  return r1 === 1 && r2 === -1 && r3 === -1 && r4 === 3 && r5 === 4;
});

// Edge: capacity 3, several puts and gets
test('capacity 3 interleaved ops', () => {
  const c = new LRUCache(3);
  c.put(1, 1); c.put(2, 2); c.put(3, 3);
  c.get(1);                // order: 2,3,1
  c.put(4, 4);             // evicts 2
  return c.get(2) === -1 && c.get(1) === 1 && c.get(3) === 3 && c.get(4) === 4;
});

console.log(`\nResults: ${passed}/${passed + failed} tests passed`);
process.exit(failed > 0 ? 1 : 0);
