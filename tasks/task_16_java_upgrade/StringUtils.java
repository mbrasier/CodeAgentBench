import java.util.List;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;

public class StringUtils {

    public static String findFirst(List<String> words, String prefix) {
        for (String w : words) {
            if (w.startsWith(prefix)) {
                return w;
            }
        }
        return null;
    }

    public static int countLongerThan(List<String> words, int minLen) {
        int count = 0;
        for (String w : words) {
            if (w.length() > minLen) {
                count++;
            }
        }
        return count;
    }

    public static void sortByLength(List<String> words) {
        Collections.sort(words, new Comparator<String>() {
            @Override
            public int compare(String a, String b) {
                return Integer.compare(a.length(), b.length());
            }
        });
    }

    public static String joinStrings(List<String> words, String delimiter) {
        StringBuffer sb = new StringBuffer();
        for (int i = 0; i < words.size(); i++) {
            if (i > 0) {
                sb.append(delimiter);
            }
            sb.append(words.get(i));
        }
        return sb.toString();
    }
}
