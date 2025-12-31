import { Node } from "../computations/node.js"

export class UnderlyingTree{
    constructor(
        current_price,
        U,
        steps
    ){
        // Initialize
        this.price = current_price;
        this.U = 1 + U;
        this.D = 1.0 / this.U;
        this.steps =  Math.min(Math.max(1,steps), 5); //Confined to range [1,5]
        this.height = steps + 1;


        this.tree = [];
        // Creating amount of nodes
        for(let i = 0; i < 2**(this.steps + 1) - 1; i++){
            this.tree.push(new Node(this.price));
        }

        this.init_tree()
    }

    init_tree(i = 0) {
        if (2 * i + 1 > this.tree.length - 1){
           return;
        }

        let price  = this.tree[i].underlying_value;

        // Left Node
        this.tree[2 * i + 1].underlying_value = price * this.D;

        // Right Node
        this.tree[2 * i + 2].underlying_value =  price * this.U;

        // Traverse
        this.init_tree(i * 2 + 1);
        this.init_tree(i * 2 + 2);

    }

    get_tree(){
        return this.tree;
    }

    get_height(){
        return this.steps + 1;
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
            (typeof this.tree[i].underlying_value === "number"
                ? this.tree[i].underlying_value.toFixed(2)
                : this.tree[i].underlying_value)
        );

        this.print_tree(
            i * 2 + 1,
            prefix + (isLeft ? "    " : "│   "),
            true
        );
    
    }

}

// let obj = new UnderlyingTree(100, 0.1, 2)
// obj.print_tree()
// console.log(obj.tree)