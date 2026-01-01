import { Node } from "../computations/node.js";
import { OptionTree } from "../computations/backward_tree.js";
import { UnderlyingTree } from "../computations/forward_tree.js";

export class Greeks{
    constructor(
        option_tree,
        underlying_tree
    ) {

        this.underlying_tree = underlying_tree;
        this.option_tree = option_tree;
        this.tree = option_tree.tree;
        this.p_tree = underlying_tree.tree;

        //Misc
        this.strike = option_tree.strike;
        this.call_bool = option_tree.call_bool;
        this.delta_t = option_tree.delta_t;
        this.height = underlying_tree.steps + 1;



        //Contraints
        this.vega_epsilon = 0.01;
        this.rho_epsilon = 0.01;

        this.compute_greeks()
    }


    apply_delta(parent, right, left){
        //Terminal Node
        if (!right || !left){
            let delta = (parent.underlying_value > this.strike) ? 1 : (parent.underlying_value < this.strike) ? 0 : 0.5;
            
            if (!this.call_bool) {delta = -delta;}   
            parent.delta = delta;
            return;

        }

        else{
            parent.delta = (right.option_value - left.option_value) / (right.underlying_value - left.underlying_value);
            return;
            }
        }
    
    apply_gamma(parent, left, right){
        //Terminal Node
        if (!right || !left){
            parent.gamma = null;
        }
        else{
            parent.gamma = (right.delta - left.delta) / (right.underlying_value - left.underlying_value);
        }

    }

    apply_theta(parent,i){
        //Middle Index
        let mid = 2*(2*i+1) + 2 //Left Right
        
        //For all valid middle Nodes
        if (mid < this.tree.length) {
            parent.theta = (this.tree[mid].option_value - parent.option_value) / (2 * this.delta_t)
        } 
        else{
            parent.theta = null;
        }
    }


    apply_vega(){
        let vega_plus = this.vega_option_tree(this.vega_epsilon);
        let vega_minus = this.vega_option_tree(-this.vega_epsilon);

        this.tree[0].vega = (vega_plus[0].option_value - vega_minus[0].option_value) / (2*this.vega_epsilon);
    }


    apply_rho(){
        let rho_plus = this.rho_option_tree(this.rho_epsilon);
        let rho_minus = this.rho_option_tree(-this.rho_epsilon);
        
        this.tree[0].rho = (rho_plus[0].option_value - rho_minus[0].option_value) / (2*this.rho_epsilon);

    }

    rho_option_tree(epsilon){
        let risk_free_rate = this.option_tree.risk_rate + epsilon;
        
        let p_tree = new UnderlyingTree(this.underlying_tree.price, this.underlying_tree.U, this.underlying_tree.steps);

        let option_tree = new OptionTree(p_tree, risk_free_rate, this.option_tree.strike, this.call_bool, this.option_tree.european_bool);
        
        return option_tree.tree;
    
    }

    vega_option_tree(epsilon){
        let s_dev = (Math.log(this.underlying_tree.U) / Math.sqrt(this.delta_t)) + epsilon;
        let u_vega = Math.exp(s_dev * Math.sqrt(this.delta_t));

        let p_tree = new UnderlyingTree(this.underlying_tree.price, u_vega, this.underlying_tree.steps);

        let option_tree = new OptionTree(p_tree, this.option_tree.risk_rate, this.option_tree.strike, this.call_bool, this.option_tree.european_bool);

        return option_tree.tree;
    }




    compute_greeks() {

        //Tree based greeks:
        this.apply_vega()
        this.apply_rho()

        for(let i = (this.tree.length - 1); i >= 0; i--){
            let parent = this.tree[i];
            //define left + right
            let left = (2 * i + 1 <= this.tree.length - 1) ? this.tree[2 * i + 1] : null;
            let right = (2 * i + 2  <= this.tree.length - 1) ? this.tree[2 * i + 2] : null;

            // Apply Greek functions:
            this.apply_delta(parent, right, left);
            this.apply_gamma(parent, right, left);
            this.apply_theta(parent, i);

        }
    }

    print_tree(i = 0, prefix = "", isLeft = true) {
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
            (typeof this.tree[i].rho === "number"
                ? this.tree[i].rho.toFixed(2)
                : this.tree[i].rho)
        );

        this.print_tree(
            i * 2 + 1,
            prefix + (isLeft ? "    " : "│   "),
            true
        ); 
    
    }

}


