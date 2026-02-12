# Task 16: Java Version Upgrade

The file `StringUtils.java` contains four string utility methods written in
a Java 7 style. Your task is to modernise each method to use the Java 8+
APIs described below so the file compiles and passes all tests.

There are no hint comments in the code. Read the method signatures and
implementations, then apply the required upgrades.

## Methods

### `findFirst(List<String> words, String prefix)`

Returns the first word in the list that starts with `prefix`.

**Required return type:** `Optional<String>`

Implement using `stream().filter(...).findFirst()`.
Add `import java.util.Optional;` if needed.

```java
Optional<String> result = StringUtils.findFirst(words, "b");
result.isPresent(); // true if a match was found
```

### `countLongerThan(List<String> words, int minLen)`

Counts the number of words whose length is strictly greater than `minLen`.

**Required return type:** `long`

Implement using `stream().filter(...).count()`.

```java
long n = StringUtils.countLongerThan(words, 4); // words with length > 4
```

### `sortByLength(List<String> words)`

Sorts `words` in-place by ascending length.

Return type remains `void`. Replace the anonymous `Comparator` with a lambda
or `Comparator.comparingInt(String::length)`.

### `joinStrings(List<String> words, String delimiter)`

Joins all words with `delimiter` between them and returns the result.

Return type remains `String`. Replace the `StringBuffer` loop with
`String.join(delimiter, words)`.
