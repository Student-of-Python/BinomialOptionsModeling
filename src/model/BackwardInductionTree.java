package model;

public class BackwardInductionTree {
    //Backward Induction
    BinaryTree tree;
    double risk_free_rate;
    boolean call_option = true; 
    double strike_price;
    
    double delta_t;
    double probability;


    public BackwardInductionTree(BinaryTree tree, double risk_free_rate, boolean call_option, double strike_price){
        this.tree = tree;
        this.risk_free_rate = risk_free_rate;
        this.call_option = call_option;
        this.strike_price = strike_price;

        this.delta_t = 1.0 / (this.tree.getHeight(this.tree.root));
        this.probability = (Math.exp(this.risk_free_rate * this.delta_t) - this.tree.U) / (this.tree.U - this.tree.D);
    }
        

    public void compute_payoffs(){
        //Computes the payoff for each terminal node
        for (Node leaf: this.tree.getLeafs()){
            if (this.call_option) leaf.payoff = Math.max(leaf.value - this.strike_price, 0);

            else leaf.payoff = Math.max(this.strike_price - leaf.value, 0);
        }
    }


    public double backwardInduction(){
        return backwardInduction(this.tree.root);
    }
    
    public double backwardInduction(Node node){
        if (node == null) return 0;

        if (node.left == null && node.right == null) return node.payoff; //reached a child node, already know payoff

        double value_up = backwardInduction(node.right); 
        double value_down = backwardInduction(node.left); 

        node.value = Math.exp(-this.risk_free_rate * this.delta_t) * (this.probability*value_up + (1-this.probability)*value_down);
        return node.value;
    }

}

