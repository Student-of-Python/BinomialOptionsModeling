package model;

public class BackwardInduction {
    //Backward Induction
    BinaryTree tree;
    double price;
    double time_till_expiration;
    double risk_free_rate;
    double U;
    double D;


    public BackwardInduction(BinaryTree tree, double expiration_in_years){
        this.tree = tree;
        this.price = tree.root.value;
        this.time_till_expiration = expiration_in_years;
        this.U = tree.U;    
        this.D = tree.D;
    }



    public double getProbU(Node node) {
        //Risk Nuetral probability
        // = (e^(r*n) - D) / (U - D)
        int n = tree.getHeight(tree.root);
        double delta_t = this.time_till_expiration / n;
        double numerator = Math.exp(risk_free_rate * delta_t) - D;
        double denominator = U - D;
        return numerator / denominator;}
        
}

