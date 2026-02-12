# Task 02: LRU Cache (JavaScript)

Implement an LRU (Least Recently Used) cache in `lru_cache.js`.

## Background

An LRU cache stores a limited number of key-value pairs. When the cache is full and a new item must be inserted, it evicts the **least recently used** item — the one that was accessed (via `get` or `put`) furthest in the past.

## What to implement

### `class LRUCache`

#### `constructor(capacity)`
- `capacity` (number): the maximum number of items the cache holds.

#### `get(key) → number`
- Return the cached value for `key` if it exists, and mark `key` as most-recently used.
- Return `-1` if `key` is not in the cache.

#### `put(key, value)`
- Insert or update `key` with `value`, and mark it as most-recently used.
- If inserting would exceed `capacity`, **evict the least-recently-used entry first**.

**Both `get` and `put` must run in O(1) average time.**

## Example

```javascript
const cache = new LRUCache(2);
cache.put(1, 1);   // cache: {1=1}
cache.put(2, 2);   // cache: {1=1, 2=2}
cache.get(1);      // returns 1,  cache order: 2 → 1 (1 is now MRU)
cache.put(3, 3);   // evicts key 2 (LRU), cache: {1=1, 3=3}
cache.get(2);      // returns -1 (evicted)
cache.put(4, 4);   // evicts key 1, cache: {3=3, 4=4}
cache.get(1);      // returns -1
cache.get(3);      // returns 3
cache.get(4);      // returns 4
```

## File to modify

**`lru_cache.js`** — implement the `LRUCache` class. The `module.exports` line at the bottom must remain.
