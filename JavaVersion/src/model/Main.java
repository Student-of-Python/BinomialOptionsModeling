package model;

public class Main {
    public static void main(String[] args) {
      
    /**
     * @param current_stock_price: The current price of the stock
     * @param price_movement: The magnitude of price movement in either direction
     * @param iterations: The amount of time steps to take
     * 
     * @param risk_free_rate: Risk free rate, or the garenteed rate of return with no risk
     * @param call_option: True is it is a call option, else it would be marked as put option
     * @param strike_price: Strike price of the option
     * 
      */

        double current_stock_price = 100.0;
        double price_movement = 0.1; 
        int iterations = 3;

        boolean call_option = false;
        boolean european_option = false; 
        double strike_price = 102.0;
        double risk_free_rate = 0.1;


        Node root = new Node(current_stock_price);
        BinaryTree tree = new BinaryTree(root, price_movement, iterations);
        
        tree.add_layers();
        
        BackwardInductionTree back_tree = new BackwardInductionTree(tree, risk_free_rate, call_option, european_option, strike_price);

        tree.printTree();
 
        System.out.println("\n Option Value: " + String.format("%.2f",  back_tree.get_fairprice()) + "\n");

        back_tree.printTree();
    }
}
