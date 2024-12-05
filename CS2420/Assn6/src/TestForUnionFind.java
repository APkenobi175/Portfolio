import java.util.ArrayList;
import java.util.List;

public class TestForUnionFind {
    // Playing with color options yippee
    public static final String ANSI_RESET = "\u001B[0m";
    public static final String ANSI_GREEN = "\u001B[32m";
    public static final String ANSI_RED = "\u001B[31m";
    public static void main(String[] args) {
        UnionFind unionFind = new UnionFind(121);
        List<String> failedTests = new ArrayList<>();
        int testCount = 0;
        System.out.println("Running Test Cases For Union Find....");
        // Unions
        unionFind.union(1, 2);
        unionFind.union(2, 3);

        // Test out the finds to trigger the path compression and make sure it works
        unionFind.find(2);
        unionFind.find(3);

        // Test 1: Make sure parent[2] and parent[3] are the same
        System.out.print("Test #1: Union(1,2) and Union(2,3) Testing that parent[2] and parent[3] match...");
        testCount++;
        if (unionFind.getParent(2) == unionFind.getParent(3)) {
            System.out.println(ANSI_GREEN + "Test Passed" + ANSI_RESET);
        } else {
            System.out.println(ANSI_RED + "Test Failed" + ANSI_RESET);
            failedTests.add("Test #" + testCount + " failed");
        }

        // Test 2: Path Compression Check
        testCount++;
        System.out.print("Test #2: Checking path compression by unioning 1 through 10, then making sure all of them have the same root... ");
        for (int i = 1; i < 10; i++) {
            unionFind.union(i, i + 1);
        }
        unionFind.find(10); // path compression
        boolean pathCompressionPassed = true;
        for (int i = 1; i <= 10; i++) {
            if (unionFind.find(i) != unionFind.find(1)) {
                pathCompressionPassed = false;
                break;
            }
        }

        if(pathCompressionPassed){
            System.out.println(ANSI_GREEN + "Test Passed" + ANSI_RESET);
        }else {
            System.out.println(ANSI_RED + "Test Failed" + ANSI_RESET);
            failedTests.add("Test #" + testCount + " failed");
        }

        // Test 3: Union by Size Check
        testCount++;
        System.out.print("Test #3: Checking union by size with union(1, 4) and union(3, 4), then checking parent[4] and root... ");
        unionFind.union(1, 4);
        unionFind.union(3, 4);
        if (unionFind.getParent(2) == unionFind.getParent(4) && unionFind.getParent(3) == unionFind.getParent(4)) {
            System.out.println(ANSI_GREEN + "Test Passed" + ANSI_RESET);
        } else {
            System.out.println(ANSI_RED + "Test Failed" + ANSI_RESET);
            failedTests.add("Test #" + testCount + " failed");
        }

        // Print out final results:

        if (failedTests.isEmpty()) {
            System.out.println(ANSI_GREEN + "All Tests Passed" + ANSI_RESET);

        }else{
            System.out.println(ANSI_RED + "Failed the following tests:" + ANSI_RESET);
            for (String failedTest : failedTests) {
                System.out.println(ANSI_RED + failedTest + ANSI_RESET);
            }
        }
        System.out.println("Printing out the parent size and arrays:");
        unionFind.printTheArrays();
    }

}
