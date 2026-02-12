#!/usr/bin/env node
'use strict';
/**
 * Evaluator for Task 06: Event Emitter
 */

const path = require('path');

let EventEmitter;
try {
  ({ EventEmitter } = require(
    path.join(__dirname, '..', '..', 'tasks', 'task_06_event_emitter', 'event_emitter.js')
  ));
} catch (e) {
  console.log(`[FAIL] Could not load event_emitter.js: ${e.message}`);
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
      console.log(`[FAIL] ${name}: assertion failed (got ${JSON.stringify(ok)})`);
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

// emit returns true when listeners exist, false when none
test('emit returns false with no listeners', () => {
  const e = new EventEmitter();
  return e.emit('noop') === false;
});

test('emit returns true with a listener', () => {
  const e = new EventEmitter();
  e.on('x', () => {});
  return e.emit('x') === true;
});

// on / emit basic
test('listener receives emitted args', () => {
  const e = new EventEmitter();
  const received = [];
  e.on('data', (a, b) => received.push(a, b));
  e.emit('data', 1, 2);
  return JSON.stringify(received) === JSON.stringify([1, 2]);
});

test('multiple listeners called in order', () => {
  const e = new EventEmitter();
  const log = [];
  e.on('ev', () => log.push('first'));
  e.on('ev', () => log.push('second'));
  e.emit('ev');
  return JSON.stringify(log) === JSON.stringify(['first', 'second']);
});

test('listener not called for different event', () => {
  const e = new EventEmitter();
  let called = false;
  e.on('a', () => { called = true; });
  e.emit('b');
  return called === false;
});

// off
test('off removes specific listener', () => {
  const e = new EventEmitter();
  let count = 0;
  const fn = () => count++;
  e.on('click', fn);
  e.emit('click');   // count = 1
  e.off('click', fn);
  e.emit('click');   // count still 1
  return count === 1;
});

test('off with unknown listener does nothing', () => {
  const e = new EventEmitter();
  e.on('x', () => {});
  e.off('x', () => {});  // different function reference — no-op
  return e.listenerCount('x') === 1;
});

test('off only removes matched listener', () => {
  const e = new EventEmitter();
  const log = [];
  const f1 = () => log.push('f1');
  const f2 = () => log.push('f2');
  e.on('ev', f1);
  e.on('ev', f2);
  e.off('ev', f1);
  e.emit('ev');
  return JSON.stringify(log) === JSON.stringify(['f2']);
});

// once
test('once listener fires exactly once', () => {
  const e = new EventEmitter();
  let count = 0;
  e.once('ping', () => count++);
  e.emit('ping');
  e.emit('ping');
  e.emit('ping');
  return count === 1;
});

test('once listener removed after firing', () => {
  const e = new EventEmitter();
  e.once('x', () => {});
  e.emit('x');
  return e.listenerCount('x') === 0;
});

// listenerCount
test('listenerCount is 0 for unknown event', () => {
  return new EventEmitter().listenerCount('ghost') === 0;
});

test('listenerCount tracks multiple adds', () => {
  const e = new EventEmitter();
  e.on('a', () => {});
  e.on('a', () => {});
  e.on('a', () => {});
  return e.listenerCount('a') === 3;
});

console.log(`\nResults: ${passed}/${passed + failed} tests passed`);
process.exit(failed > 0 ? 1 : 0);
