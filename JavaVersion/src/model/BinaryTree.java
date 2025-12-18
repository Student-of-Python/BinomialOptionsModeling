package model;
import java.util.ArrayList;

/**
 * BinaryTree class represents the binary tree for the binary option model. It creates the branches that show the different paths the price action can take
*/
public class BinaryTree{

    Node root;
    final double U; 
    final double D;
    final int layers;


    /** Constructor
     * @param Node root: The root node
     * @param double U: the magnitude of the price action in either direction
     * @param int layers: Amount of steps (representing time) till expiration
     */


    public BinaryTree(Node root, double U, int layers) {
        assert U > 0 : "Upside cannot be negative " + U; 
        assert layers >= 0 : "Amount of layers must be greater than 0: " + layers;
        this.root = root;
        this.U = 1 + U;
        this.D = 1.0 / this.U;
        this.layers = layers;
    }
        

    /**
     * Adds the amount of layers iteratively 
    */
    
    public void add_layers(){
        for (int i = 0; i < this.layers; i++) {
            add(this.root);   
        }
        
    }

    /** add
     * Makes one layer each time iteratively
     * @param current: Current Node (creates )
     */
    public void add(Node current){
        //Base case 1 : current node is null; do nothing
        if (current == null) {
            return;}

        //Base Case 2 : current node has no children; make left and right child
        if (current.left == null && current.right == null) {
         //Node has no children, add two children
            current.left = new Node(current.stockValue * this.D);
            current.right = new Node(current.stockValue * this.U);
            return;
        }
        
        //Error Handling: Each node must always have either have {2,0} children.
        if ((current.left == null) != (current.right == null)) {
             throw new IllegalStateException("Invalid tree state: node has exactly one child");
            }
    
        // Recursive case: both children exist, keep going until base case
        add(current.left);
        add(current.right);
    }
    
    /** getHeight
     *  
     * @param node: Node at which to the find the height. 
     * @return height of the node given
     */
    public int getHeight(Node node) {
        //Base Case 1: If node is null, height is 0
        if (node == null) return 0;
        //Gets height of left and right subtree iteratively
        int leftHeight = getHeight(node.left);
        int rightHeight = getHeight(node.right);
        return Math.max(leftHeight, rightHeight) + 1;
    }

    /** getLeafs
     * 
     * @return ArrayList of all the leafs in the current binary tree
     */
    public ArrayList<Node> getLeafs(){
        ArrayList<Node> leafs = new ArrayList<>();
        getLeafs(this.root, leafs);
        return leafs;
    }

    /**getleafs
     * 
     * @param node: current Node
     * @param leafs: Arraylist to add the leafs to. 
     */
    public void getLeafs(Node node, ArrayList<Node> leafs){
        //Base Case 1: Node does not exist; do nothing
        if (node == null) return;

        //Base Case 2: leaf found; append list
        if (node.left == null && node.right == null) {
            leafs.add(node);
            return;
        }

        //Recursive case: Keep going until found leaf.
        getLeafs(node.left, leafs);
        getLeafs(node.right, leafs);
    }
    

    /**printTree
     * Prints the Tree elegantly for visual demonstration 
     */
    public void printTree(){
        printTree(this.root, "", true);
    }


    public void printTree(Node node, String prefix, boolean isLeft){
        if (node == null) return;

        // Print the right subtree first (so it appears on top visually)
        printTree(node.right, prefix + (isLeft ? "│   " : "    "), false);

        // Print current node
        String formattedValue = String.format("%.2f", node.stockValue);
        System.out.println(prefix + (isLeft ? "└── " : "┌── ") + formattedValue);

        // Print the left subtree
        printTree(node.left, prefix + (isLeft ? "    " : "│   "), true);
    }
}
