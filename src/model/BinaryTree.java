package model;
import java.util.ArrayList;

public class BinaryTree{
    Node root;
    final double U; 
    final double D;
    public BinaryTree(Node root, double U, double D) {
        this.root = root;
        this.U = U;
        this.D = D; }

    
    public void add(double stock_price){
        add(this.root, stock_price);
    }

    public void add(Node current, double stock_price){
        //Recursively add nodes to the tree
        //Base base --> leaf has no children, add children
        //Case 2: Node has children, recurse down the tree until hit leaf, then add children
        //Since no node has exactly 1 child, this simplifies the logic
        

        //Adds two children for each leave
        if (current == null) {
            return;}

        if (current.left == null && current.right == null) {
         //Node has no children, add two children
            current.left = new Node(current,current.value * this.U, stock_price);
            current.right = new Node(current,current.value * this.D, stock_price);
            return;
        }
        
        if ((current.left == null) != (current.right == null)) {
             throw new IllegalStateException("Invalid tree state: node has exactly one child");
            }
    
        // Recursive case - both children exist
        add(current.left, stock_price);
        add(current.right, stock_price);
    }


    

    public int getHeight(Node node) {
        //If node is null, height is 0
        if (node == null) return 0;
        int leftHeight = getHeight(node.left);
        int rightHeight = getHeight(node.right);
        return Math.max(leftHeight, rightHeight) + 1;
    }

    public ArrayList<Node> getLeafs(){
        ArrayList<Node> leafs = new ArrayList<>();
        getLeafs(this.root, leafs);
        return leafs;
    }



    public ArrayList<Double> getTerminalValues(){
        //Get all the ending values of the leafs
        ArrayList<Double> terminalValues = new ArrayList<>();
        for (Node leaf : getLeafs()) {
            terminalValues.add(leaf.value);
        }
        return terminalValues;
    }

    public void getLeafs(Node node, ArrayList<Node> leafs){
        //Iterates and gets all the children
        if (node == null) return;

        if (node.left == null && node.right == null) {
            leafs.add(node);
            return;
        }

        getLeafs(node.left, leafs);
        getLeafs(node.right, leafs);
    }

    public void printTree(){
        printTree(this.root, "", true);
    }


    public void printTree(Node node, String prefix, boolean isLeft){
        if (node == null) return;

        // Print the right subtree first (so it appears on top visually)
        printTree(node.right, prefix + (isLeft ? "│   " : "    "), false);

        // Print current node
        String formattedValue = String.format("%.2f", node.value);
        System.out.println(prefix + (isLeft ? "└── " : "┌── ") + formattedValue);

        // Print the left subtree
        printTree(node.left, prefix + (isLeft ? "    " : "│   "), true);
    }
}
