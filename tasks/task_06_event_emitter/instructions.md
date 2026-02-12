# Task 06: Event Emitter (JavaScript)

Implement an `EventEmitter` class in `event_emitter.js`.

## Background

An event emitter is a publish/subscribe mechanism.  Code can register listener functions for named events, and other code can fire those events to invoke all registered listeners.

## What to implement

### `class EventEmitter`

#### `on(event, listener)`
Register `listener` as a handler for `event`.  Multiple listeners can be registered for the same event.

#### `off(event, listener)`
Remove a specific `listener` from `event`.  If the listener is not registered, do nothing.

#### `emit(event, ...args)`
Call every listener registered for `event`, passing `...args` to each.
Returns `true` if there was at least one listener, `false` otherwise.
Listeners are called in the order they were registered.

#### `once(event, listener)`
Register `listener` for `event`, but automatically remove it after it fires once.

#### `listenerCount(event)`
Return the number of active listeners registered for `event`.

## Example

```javascript
const emitter = new EventEmitter();

const greet = (name) => console.log(`Hello, ${name}!`);
emitter.on('greet', greet);
emitter.emit('greet', 'Alice');   // logs "Hello, Alice!"
emitter.emit('greet', 'Bob');     // logs "Hello, Bob!"
emitter.off('greet', greet);
emitter.emit('greet', 'Carol');   // nothing happens, returns false

emitter.once('done', () => console.log('fired once'));
emitter.emit('done');   // logs "fired once"
emitter.emit('done');   // nothing — listener was removed
```

## File to modify

**`event_emitter.js`** — implement the `EventEmitter` class. The `module.exports` line must remain.
