package model;

public class Node{
    Node left; 
    Node right;
    double optionValue; // Whether any money is won
    double ImmediateExerciseValue; //American option lets you excercise it at any time
    double ContinuationValue;  //European option (ignore the exercise)
    double stockValue; //Stock price given U, D
    public Node(double stockValue) {
        this.stockValue = stockValue;
        this.left = null;
        this.right = null;
    }
}