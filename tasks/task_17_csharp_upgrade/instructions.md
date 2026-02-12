# Task 17: C# Version Upgrade

The file `TextProcessor.cs` contains four text utility methods written in
an older C# style using non-generic collections. Your task is to modernise
each method to use the C# 6+/LINQ APIs described below so the file compiles
and passes all tests.

There are no hint comments in the code. Read the method signatures and
implementations, then apply the required upgrades. You will need to add
`using System.Linq;` at the top of the file for LINQ methods.

## Methods

### `GetLengths(List<string> words)`

Returns the length of each word as a typed collection.

**Required return type:** `List<int>`

Implement using `.Select(s => s.Length).ToList()`.

```csharp
List<int> lengths = TextProcessor.GetLengths(words);
// lengths[0] == words[0].Length
```

### `CountByFirstLetter(List<string> words)`

Groups words by their first character and counts how many words start
with each letter.

**Required return type:** `Dictionary<char, int>`

Implement using `.GroupBy(s => s[0]).ToDictionary(g => g.Key, g => g.Count())`.

```csharp
Dictionary<char, int> map = TextProcessor.CountByFirstLetter(words);
// map['a'] == number of words starting with 'a'
```

### `FormatEntry(string name, int value)`

Formats a name-value pair as `"name: value"`.

Return type remains `string`. Replace `string.Format(...)` with a string
interpolation expression: `$"{name}: {value}"`.

### `CountShorterThan(List<string> words, int maxLen)`

Counts the number of words whose length is strictly less than `maxLen`.

Return type remains `int`. Replace the `foreach` loop with
`.Count(s => s.Length < maxLen)`.
