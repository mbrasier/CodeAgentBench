/**
 * Test suite for Task 04: Generic Stack
 * Run via:  ts-node test_stack.ts
 */
import { Stack } from '../../tasks/task_04_typescript_stack/stack';

let passed = 0;
let failed = 0;

function test(name: string, fn: () => boolean): void {
  try {
    const ok = fn();
    if (ok) {
      console.log(`[PASS] ${name}`);
      passed++;
    } else {
      console.log(`[FAIL] ${name}: assertion returned false`);
      failed++;
    }
  } catch (e) {
    const msg = (e as Error).message ?? String(e);
    if (msg === 'Not implemented') {
      console.log(`[FAIL] ${name}: not implemented`);
    } else {
      console.log(`[FAIL] ${name}: ${msg}`);
    }
    failed++;
  }
}

test('new stack is empty', () => new Stack<number>().isEmpty() === true);

test('new stack size is 0', () => new Stack<number>().size() === 0);

test('not empty after push', () => {
  const s = new Stack<number>();
  s.push(1);
  return !s.isEmpty();
});

test('size increases with push', () => {
  const s = new Stack<number>();
  s.push(1); s.push(2); s.push(3);
  return s.size() === 3;
});

test('pop returns last pushed (LIFO)', () => {
  const s = new Stack<number>();
  s.push(1); s.push(2); s.push(3);
  return s.pop() === 3;
});

test('pop decreases size', () => {
  const s = new Stack<number>();
  s.push(1); s.push(2);
  s.pop();
  return s.size() === 1;
});

test('pop from empty returns undefined', () => {
  return new Stack<number>().pop() === undefined;
});

test('peek returns top without removing', () => {
  const s = new Stack<number>();
  s.push(42);
  return s.peek() === 42 && s.size() === 1;
});

test('peek empty returns undefined', () => {
  return new Stack<number>().peek() === undefined;
});

test('isEmpty after all pops', () => {
  const s = new Stack<number>();
  s.push(1); s.pop();
  return s.isEmpty();
});

test('stack with strings', () => {
  const s = new Stack<string>();
  s.push('hello'); s.push('world');
  return s.pop() === 'world' && s.pop() === 'hello';
});

test('LIFO order preserved for many items', () => {
  const s = new Stack<number>();
  for (let i = 1; i <= 5; i++) s.push(i);
  const out: number[] = [];
  while (!s.isEmpty()) out.push(s.pop()!);
  return JSON.stringify(out) === JSON.stringify([5, 4, 3, 2, 1]);
});

console.log(`\nResults: ${passed}/${passed + failed} tests passed`);
process.exit(failed > 0 ? 1 : 0);
