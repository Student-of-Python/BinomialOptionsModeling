package model;

public class Main {
    public static void main(String[] args) {
        Node root = new Node(100.0);
        BinaryTree tree = new BinaryTree(root, 0.1);

        // Add two levels
        tree.add();
        tree.add();
        tree.add();
        
        BackwardInductionTree back_tree = new BackwardInductionTree(tree, 0, true, 102);

        back_tree.compute_payoffs();
        back_tree.backwardInduction();

        tree.printTree();
    }
}