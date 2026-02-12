/**
 * A simple publish/subscribe event emitter.
 */
class EventEmitter {
  constructor() {
    throw new Error('Not implemented');
  }

  /**
   * Register a listener for the named event.
   * Multiple listeners can be added for the same event.
   *
   * @param {string} event
   * @param {Function} listener
   */
  on(event, listener) {
    throw new Error('Not implemented');
  }

  /**
   * Remove a specific listener from the named event.
   * If the listener is not registered, do nothing.
   *
   * @param {string} event
   * @param {Function} listener
   */
  off(event, listener) {
    throw new Error('Not implemented');
  }

  /**
   * Invoke all listeners registered for event, passing any extra args.
   * Returns true if at least one listener was called, false otherwise.
   *
   * @param {string} event
   * @param {...*} args
   * @returns {boolean}
   */
  emit(event, ...args) {
    throw new Error('Not implemented');
  }

  /**
   * Register a listener that fires at most once, then is automatically removed.
   *
   * @param {string} event
   * @param {Function} listener
   */
  once(event, listener) {
    throw new Error('Not implemented');
  }

  /**
   * Return the number of listeners currently registered for event.
   *
   * @param {string} event
   * @returns {number}
   */
  listenerCount(event) {
    throw new Error('Not implemented');
  }
}

module.exports = { EventEmitter };
