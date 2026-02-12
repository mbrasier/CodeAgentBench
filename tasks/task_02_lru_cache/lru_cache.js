/**
 * LRU (Least Recently Used) Cache.
 *
 * Stores up to `capacity` key-value pairs.  When full, evicts the entry that
 * was accessed least recently.  Both get() and put() must run in O(1) time.
 *
 * Hint: a doubly-linked list combined with a hash map achieves O(1) for all ops.
 */
class LRUCache {
  /**
   * @param {number} capacity  Maximum number of entries to hold.
   */
  constructor(capacity) {
    throw new Error('Not implemented');
  }

  /**
   * Return the value stored under `key`, or -1 if the key is not present.
   * Accessing a key makes it the most-recently-used entry.
   *
   * @param {number} key
   * @returns {number}
   */
  get(key) {
    throw new Error('Not implemented');
  }

  /**
   * Insert or update `key` with `value`.
   * If the cache is at capacity, evict the least-recently-used entry first.
   * After this call `key` is the most-recently-used entry.
   *
   * @param {number} key
   * @param {number} value
   */
  put(key, value) {
    throw new Error('Not implemented');
  }
}

module.exports = { LRUCache };
