using System;
using System.Collections;
using System.Collections.Generic;

public class TextProcessor
{
    public static ArrayList GetLengths(List<string> words)
    {
        ArrayList result = new ArrayList();
        foreach (string w in words)
        {
            result.Add(w.Length);
        }
        return result;
    }

    public static Hashtable CountByFirstLetter(List<string> words)
    {
        Hashtable result = new Hashtable();
        foreach (string w in words)
        {
            char key = w[0];
            if (result.ContainsKey(key))
            {
                result[key] = (int)result[key] + 1;
            }
            else
            {
                result[key] = 1;
            }
        }
        return result;
    }

    public static string FormatEntry(string name, int value)
    {
        return string.Format("{0}: {1}", name, value);
    }

    public static int CountShorterThan(List<string> words, int maxLen)
    {
        int count = 0;
        foreach (string w in words)
        {
            if (w.Length < maxLen)
            {
                count++;
            }
        }
        return count;
    }
}
