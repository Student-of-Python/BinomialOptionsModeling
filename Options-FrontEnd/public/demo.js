import { Node } from "../computations/node.js";
import { OptionTree } from "../computations/backward_tree.js";
import { UnderlyingTree } from "../computations/forward_tree.js";
import { Greeks } from "../public/computations/greeks.js";

//Vars
//Underlying Tree Vars
const current_price = document.getElementById("current_price");
const U = document.getElementById("U");
const steps = document.getElementById("steps");

//Options Vars
const risk_rate = document.getElementById("risk_rate");
const strike = document.getElementById("strike");
const call_bool = document.getElementById("call_bool");
const european_bool = document.getElementById("european_bool");




//Build Trees
function buildUnderlyingTree(current_price, U, steps) {
    let underlying = new UnderlyingTree(current_price, U, steps);
    return underlying;
    }

function buildOptionsTree(underlying_tree, risk_rate, strike, call_bool, european_bool) {
    let option_tree = new OptionTree(underlying_tree, risk_rate, strike, call_bool, european_bool);
    return option_tree;
    }

function buildGreeksTree(underlying_tree, options_tree) {
    let greek_tree = new Greeks(underlying_tree, options_tree);
    return greek_tree;
    }

function renderTree(treeType){
    //Clear
    let tree = treeType.tree
    const container = document.getElementById("tree");
    container.innerHTML = "";

    //Reconstruct by level (Tree is an array)
    for(let i = 0; i <= treeType.height; i ++){
        const row = document.createElement("div");
        row.className = "flex justify-between gap-6 my-4"
        let level = tree.slice(2**i - 1, 2**(i+1)-1)
        level.forEach(node_obj => {
            const node = document.createElement("div")
            node.className = "node";
            node.textContent = node_obj.toString();
            row.appendChild(node);
            }
        );
        container.appendChild(row);
    }

}

function update() {
    const S0 = Number(current_price.value);
    const u = Number(U.value);
    const n = Number(steps.value);
    const r = Number(risk_rate.value);
    const k = Number(strike.value);
    const isCall = call_bool.checked;
    const isEuro = european_bool.checked;
    
    const underlying = buildUnderlyingTree(S0, u, n);

    const optionTree = buildOptionsTree(underlying, r, k, isCall, isEuro);

    renderTree(optionTree);
}

document.querySelectorAll("input").forEach(input => {
    input.addEventListener("input", update);
});