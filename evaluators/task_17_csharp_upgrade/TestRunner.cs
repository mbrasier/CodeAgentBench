using System;
using System.Collections.Generic;
using System.Linq;

public class TestRunner
{
    static int passed = 0;
    static int failed = 0;

    static void Check(string name, bool condition, string detail)
    {
        if (condition)
        {
            Console.WriteLine("[PASS] " + name);
            passed++;
        }
        else
        {
            Console.WriteLine("[FAIL] " + name + ": " + detail);
            failed++;
        }
    }

    public static void Main(string[] args)
    {
        var words = new List<string> { "apple", "fig", "banana", "kiwi", "cherry" };

        // GetLengths: requires List<int> return type
        List<int> lens = TextProcessor.GetLengths(words);
        Check("GetLengths count", lens.Count == 5,
              "expected 5, got " + lens.Count);
        Check("GetLengths values", lens.SequenceEqual(new List<int> { 5, 3, 6, 4, 6 }),
              "expected [5,3,6,4,6], got [" + string.Join(",", lens) + "]");

        // CountByFirstLetter: requires Dictionary<char,int> return type
        Dictionary<char, int> map = TextProcessor.CountByFirstLetter(words);
        Check("CountByFirstLetter distinct keys", map.Count == 5,
              "expected 5 keys, got " + map.Count);
        Check("CountByFirstLetter all ones", map.Values.All(v => v == 1),
              "expected all values == 1");

        var mixed = new List<string> { "apple", "ant", "bear" };
        Dictionary<char, int> map2 = TextProcessor.CountByFirstLetter(mixed);
        Check("CountByFirstLetter a=2",
              map2.ContainsKey('a') && map2['a'] == 2,
              "expected a=2");
        Check("CountByFirstLetter b=1",
              map2.ContainsKey('b') && map2['b'] == 1,
              "expected b=1");

        // CountShorterThan: fig(3)<5, kiwi(4)<5; apple(5) not <5
        int c1 = TextProcessor.CountShorterThan(words, 5);
        Check("CountShorterThan 5", c1 == 2, "expected 2, got " + c1);

        int c2 = TextProcessor.CountShorterThan(words, 10);
        Check("CountShorterThan 10", c2 == 5, "expected 5, got " + c2);

        // FormatEntry
        string f1 = TextProcessor.FormatEntry("Widget", 42);
        Check("FormatEntry basic", f1 == "Widget: 42",
              "expected 'Widget: 42', got '" + f1 + "'");

        string f2 = TextProcessor.FormatEntry("Score", 0);
        Check("FormatEntry zero", f2 == "Score: 0",
              "expected 'Score: 0', got '" + f2 + "'");

        Console.WriteLine("\nResults: " + passed + "/" + (passed + failed) + " tests passed");
        System.Environment.Exit(failed > 0 ? 1 : 0);
    }
}
