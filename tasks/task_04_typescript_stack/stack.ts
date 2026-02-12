/**
 * A generic Last-In-First-Out (LIFO) stack.
 *
 * All operations must run in O(1) time.
 */
export class Stack<T> {
  // Add your private fields here

  /**
   * Add an item to the top of the stack.
   */
  push(item: T): void {
    throw new Error('Not implemented');
  }

  /**
   * Remove and return the top item.
   * Returns undefined if the stack is empty.
   */
  pop(): T | undefined {
    throw new Error('Not implemented');
  }

  /**
   * Return the top item without removing it.
   * Returns undefined if the stack is empty.
   */
  peek(): T | undefined {
    throw new Error('Not implemented');
  }

  /**
   * Return true if the stack contains no items.
   */
  isEmpty(): boolean {
    throw new Error('Not implemented');
  }

  /**
   * Return the number of items in the stack.
   */
  size(): number {
    throw new Error('Not implemented');
  }
}
