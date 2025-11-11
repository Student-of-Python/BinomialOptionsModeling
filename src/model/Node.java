package model;
public class Node{
    Node left; 
    Node right;
    double payoff; // Whether any money is won
    double value; //Stock price given U, D

    public Node(double value) {
        this.value = value;
        this.left = null;
        this.right = null;
    }
}