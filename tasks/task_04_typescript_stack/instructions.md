# Task 04: Generic Stack (TypeScript)

Implement a generic `Stack<T>` class in `stack.ts`.

## Background

A stack is a Last-In-First-Out (LIFO) data structure. Items are pushed onto the top and popped from the top.

## What to implement

### `class Stack<T>`

#### `push(item: T): void`
Add `item` to the top of the stack.

#### `pop(): T | undefined`
Remove and return the top item.  Return `undefined` if the stack is empty.

#### `peek(): T | undefined`
Return the top item **without** removing it.  Return `undefined` if empty.

#### `isEmpty(): boolean`
Return `true` if the stack has no items.

#### `size(): number`
Return the number of items currently on the stack.

## Requirements

- The class must be **generic** — it should work for `Stack<number>`, `Stack<string>`, `Stack<MyObject>`, etc.
- All methods must run in **O(1)** time.
- Export the class: `export class Stack<T> { ... }`

## Example

```typescript
const stack = new Stack<number>();
stack.isEmpty();   // true
stack.push(10);
stack.push(20);
stack.push(30);
stack.size();      // 3
stack.peek();      // 30  (stack unchanged)
stack.pop();       // 30
stack.pop();       // 20
stack.size();      // 1
stack.isEmpty();   // false
```

## File to modify

**`stack.ts`** — implement the `Stack<T>` class.

## Running / evaluating

If `ts-node` is installed (`npm install -g ts-node typescript`), the evaluator will run automatically. Otherwise it is skipped.
