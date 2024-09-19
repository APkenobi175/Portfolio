import java.util.Arrays;
import java.util.Random;


public class TreeTester {
    // Test program
    public static void main(String[] args) {
        final String ENDLINE = "\n";

        Integer[] list1 = {25, 10, 60, 55, 58, 56, 14, 63, 8, 50, 6, 9, 15,27,29,61};
        Tree treeOne = new Tree(list1, "TreeOne:",true);

        //Problem 1
        //System.out.println(treeOne.toString());  Print so it looks like a tree
        System.out.println(treeOne.toString2());

        Integer[] list2 = {4,5,6,8,33,16,80,121,22,25, 36};
        Tree treeTwo = new Tree(list2, "TreeTwo:", false);
        System.out.println(treeTwo.toString());

        //Problem 2
        treeTwo.flip();
        treeTwo.changeName("Tree Two Now flipped");
        System.out.println( treeTwo.toString());
        treeTwo.flip();   //Flip back
        treeTwo.changeName("TreeTwo");
        System.out.println(treeTwo.toString());

        final int SIZE = 10;
        Integer[] list3 = {111, 176, 67, 77, 112, 119, 120, 70, 92, 153};
        Tree treeThree = new Tree(list3, "TreeThree:", true);
        System.out.println(treeThree.toString());

        //Problem 3
        System.out.println("Deepest Node of treeOne " + treeOne.deepestNode());
        System.out.println("Deepest Node of treeThree " + treeThree.deepestNode());


        //Problem 4
        int mylevel=3;
        System.out.println("Number nodes at level " + mylevel + " is " + treeThree.nodesInLevel(mylevel));
        mylevel=4;
        System.out.println("Number nodes at level " + mylevel + " is " + treeThree.nodesInLevel(mylevel));

        //Problem 5
        System.out.println("All paths from treeThree");
        treeThree.printAllPaths();


        Integer[] list4= {21, 8, 25, 6, 7, 19, 10, 40, 43, 52, 64, 80};
        Tree treeFour = new Tree(list4, "treeFour", false);
        //Problem 6
        treeFour.pruneK(60);
        treeFour.changeName("treeFour after pruning 60");
        System.out.println(treeFour.toString());

        System.out.println(treeTwo.toString());
        treeTwo.pruneK(290);
        treeTwo.changeName("treeTwo after pruning 290");
        System.out.println(treeTwo.toString());

        //Problem 7
        System.out.println(treeOne.toString());
        System.out.println("treeOne Least Common Ancestor of (10,15) " + treeOne.lca((Integer) 10, 15) );
        System.out.println("treeOne Least Common Ancestor of (55,61) " + treeOne.lca(55, 61) );
        System.out.println("treeOne Least Common Ancestor of (9,50) " + treeOne.lca(9, 50) );
        System.out.println("treeOne Least Common Ancestor of (29,62) " + treeOne.lca(29, 62) );

        //Problem 8
        Integer[] v5 = {15, 1,2,3,5,10, 65, 66,67,68,83, 70, 90,69,6,8};
        Tree treeFive = new Tree(v5, "TreeFive:",true);
        System.out.println(treeFive.toString());
        treeFive.balanceTree();
        treeFive.changeName("treeFive after balancing");
        System.out.println(treeFive.toString());

        //Problem 9
        System.out.println(treeOne.toString());
        treeOne.keepRange(14, 50);
        treeOne.changeName("treeOne after keeping only nodes between 14 and 50");
        System.out.println(treeOne.toString());


        treeFive.changeName("treeFive");
        System.out.println(treeFive.toString());
        treeFive.keepRange(3, 69);
        treeFive.changeName("treeFive after keeping only nodes between 3  and 69");
        System.out.println(treeFive.toString());

        // Problem 10
        treeTwo = new Tree (list2, "TreeTwo:", false);
        System.out.println(treeTwo.toString());
        System.out.println("treeTwo Contains BST: " + treeTwo.countBST());

        treeFour = new Tree (list4, "treeFour", false);
        System.out.println(treeFour.toString());
        System.out.println("treeFour Contains BST: " + treeFour.countBST());

        //Bonus

        Integer[] inorder = {4, 2, 1, 7, 5, 8, 3, 6};
        Integer[] preorder = {1, 2, 4, 3, 5, 7, 8, 6};
        Tree treeBonus = new Tree("TreeBonus");
        treeBonus.buildTreeFromTraversals(inorder, preorder);
        treeBonus.changeName("TreeBonus built from inorder and preorder traversals");
        System.out.println(treeBonus.toString());

    }
}
