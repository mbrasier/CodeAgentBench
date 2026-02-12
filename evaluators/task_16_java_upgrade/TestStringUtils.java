import java.util.Arrays;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

public class TestStringUtils {

    static int passed = 0;
    static int failed = 0;

    static void check(String name, boolean condition, String detail) {
        if (condition) {
            System.out.println("[PASS] " + name);
            passed++;
        } else {
            System.out.println("[FAIL] " + name + ": " + detail);
            failed++;
        }
    }

    public static void main(String[] args) {
        List<String> words = Arrays.asList(
            "apple", "fig", "banana", "kiwi", "cherry", "plum", "date"
        );

        // findFirst: requires Optional<String> return type
        Optional<String> r1 = StringUtils.findFirst(words, "b");
        check("findFirst present", r1.isPresent(), "expected non-empty Optional");
        check("findFirst value", r1.isPresent() && r1.get().equals("banana"),
              "expected banana, got " + r1.orElse("(empty)"));

        Optional<String> r2 = StringUtils.findFirst(words, "z");
        check("findFirst absent", !r2.isPresent(), "expected empty Optional");

        // countLongerThan: requires long return type
        // words longer than 3: apple(5), banana(6), kiwi(4), cherry(6), plum(4), date(4) = 6
        long c0 = StringUtils.countLongerThan(words, 3);
        check("countLongerThan 3", c0 == 6L, "expected 6, got " + c0);

        // words longer than 4: apple(5), banana(6), cherry(6) = 3
        long c1 = StringUtils.countLongerThan(words, 4);
        check("countLongerThan 4", c1 == 3L, "expected 3, got " + c1);

        // words longer than 5: banana(6), cherry(6) = 2
        long c2 = StringUtils.countLongerThan(words, 5);
        check("countLongerThan 5", c2 == 2L, "expected 2, got " + c2);

        // words longer than 10: none = 0
        long c3 = StringUtils.countLongerThan(words, 10);
        check("countLongerThan 10", c3 == 0L, "expected 0, got " + c3);

        // sortByLength
        List<String> toSort = new ArrayList<>(Arrays.asList("apple", "fig", "banana"));
        StringUtils.sortByLength(toSort);
        check("sortByLength first",  toSort.get(0).equals("fig"),
              "expected fig, got " + toSort.get(0));
        check("sortByLength second", toSort.get(1).equals("apple"),
              "expected apple, got " + toSort.get(1));
        check("sortByLength third",  toSort.get(2).equals("banana"),
              "expected banana, got " + toSort.get(2));

        // joinStrings
        List<String> abc = Arrays.asList("a", "b", "c");
        String j1 = StringUtils.joinStrings(abc, ", ");
        check("joinStrings comma", j1.equals("a, b, c"),
              "expected 'a, b, c', got '" + j1 + "'");

        List<String> single = Arrays.asList("hello");
        String j2 = StringUtils.joinStrings(single, "-");
        check("joinStrings single", j2.equals("hello"),
              "expected 'hello', got '" + j2 + "'");

        List<String> two = Arrays.asList("foo", "bar");
        String j3 = StringUtils.joinStrings(two, " | ");
        check("joinStrings two", j3.equals("foo | bar"),
              "expected 'foo | bar', got '" + j3 + "'");

        System.out.println("\nResults: " + passed + "/" + (passed + failed) + " tests passed");
        System.exit(failed > 0 ? 1 : 0);
    }
}
