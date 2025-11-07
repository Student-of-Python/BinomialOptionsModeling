package model;
public class Node{
    Node left;
    Node right;
    Node parent;
    boolean payoff;
    double value;

    public Node(Node parent, double value, double price) {
        this.parent = parent;
        this.value = value;
        this.left = null;
        this.right = null;
        this.payoff = value > price;
    }
}