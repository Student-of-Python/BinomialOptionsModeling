import { Node } from "../computations/node.js"
import { UnderlyingTree } from "../computations/forward_tree.js";

export class OptionTree{
    constructor(
        underlyingTree,
        risk_free_rate,
        strike_price,
        call_option,
        european_option
    ){

    this.tree = underlyingTree.tree;
    this.risk_rate = risk_free_rate;

    //Options
    this.strike = strike_price;
    this.call_bool = call_option;
    this.european_bool = european_option;

    //Misc
    this.height = underlyingTree.steps + 1;
    this.delta_t = 1.0 / (this.height);
    this.prob = (Math.exp(this.risk_rate * this.delta_t) - underlyingTree.D) / (underlyingTree.U - underlyingTree.D);
    

    this.backward_induction();

    }


    compute_payoff(node){
            if (this.call_bool){
                  return Math.max(0, node.underlying_value - this.strike);
               }
               else {
                //Put Option
                  return Math.max(0,  this.strike - node.underlying_value);
               }
    }

    backward_induction(){
        
        let last_parent = Math.floor((this.tree.length  - 2) / 2);
        for(let i = this.tree.length-1; i >= 0; i--){
            let node = this.tree[i];

            //Terminal Node; Get Payoffs            
            if (i > last_parent){
               node.option_value = this.compute_payoff(node)}

            else {
                //Know its a parent node
                let left = this.tree[2 * i + 1]
                let right = this.tree[2 * i + 2]

                let discount_option_value = Math.exp(-1 * this.risk_rate * this.delta_t) * (this.prob * right.option_value + (1 - this.prob) * left.option_value);
                
                //European Options
                if (this.european_bool) {
                    node.option_value = discount_option_value;
                }

                //American Option
                else{
                  node.option_value = Math.max(this.compute_payoff(node) , discount_option_value);
                }
            }
        }

    }


    print_tree(i = 0, prefix = "", isLeft = false) {
        if (i > this.tree.length - 1){
            return;
        }

        this.print_tree(
            i * 2 + 2,
            prefix + (isLeft ? "│   " : "    "),
            false
        );

        console.log(
            prefix +
            (isLeft ? "└── " : "┌── ") +
            (typeof this.tree[i].option_value === "number"
                ? this.tree[i].option_value.toFixed(2)
                : this.tree[i].option_value)
        );

        this.print_tree(
            i * 2 + 1,
            prefix + (isLeft ? "    " : "│   "),
            true
        ); 
    
    }

}


