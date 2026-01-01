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

function buildGreeksTree(options_tree, underlying) {
    let greek_tree = new Greeks(options_tree, underlying);
    return greek_tree;
    }

function renderTree(treeType) {
    //Hide 
    const tag = document.getElementById('Instruct Params')
    tag.innerHTML = ""

    const tree = treeType.tree;
    const container = document.getElementById("tree");
    container.querySelectorAll(".node").forEach(n => n.remove());

    const levels = treeType.height; // number of levels in the tree

    container.style.display = "grid";
    container.style.gridTemplateColumns = `repeat(${levels}, 200px)`;
    container.style.justifyContent = "center";

    const rowPositions = {};

    // 1. Place leaves (leaves start at level = levels-1)
    const firstLeaf = Math.pow(2, levels - 1) - 1;
    const leafCount = Math.pow(2, levels - 1);
    const rowGap = 2;

    for (let i = 0; i < leafCount; i++) {
        rowPositions[firstLeaf + i] = i * rowGap + 1;
    }

    // 2. Work upward
    for (let i = firstLeaf - 1; i >= 0; i--) {
        rowPositions[i] =
            (rowPositions[2 * i + 1] + rowPositions[2 * i + 2]) / 2;
    }

    const maxRow = Math.max(...Object.values(rowPositions));
    container.style.gridTemplateRows = `repeat(${maxRow + 1}, 70px)`;

    // 3. Render nodes (annotate depth + semantic classes)
    tree.forEach((nodeObj, i) => {
        const depth = Math.floor(Math.log2(i + 1));

        const node = document.createElement("div");
        // mark runtime-created nodes so CSS can keep them hidden until animated
        node.className = "node dynamic";
        node.textContent = nodeObj.toString();
        node.dataset.index = i;
        node.dataset.depth = depth;

        // semantic classes
        if (i === 0) node.classList.add("root");
        const firstLeaf = Math.pow(2, levels - 1) - 1;
        if (i >= firstLeaf) node.classList.add("leaf");

        // determine numeric value if present (option tree stores e.g. option_value)
        let val = null;
        if (nodeObj && typeof nodeObj.option_value !== 'undefined') val = nodeObj.option_value;
        else if (nodeObj && typeof nodeObj.value !== 'undefined') val = nodeObj.value;

        if (typeof val === 'number') {
            if (val > 0) node.classList.add('positive');
            else if (val < 0) node.classList.add('negative');
            else node.classList.add('neutral');
        } else {
            node.classList.add('neutral');
        }

        node.style.gridColumn = depth + 1;
        node.style.gridRow = rowPositions[i];

        container.appendChild(node);
    });
}
function drawConnections(tree) {
    const svg = document.getElementById("tree-lines");
    svg.innerHTML = "";

    const container = document.getElementById("tree");
    const containerRect = container.getBoundingClientRect();

    

    // IMPORTANT: sync SVG size first
    svg.setAttribute("width", container.scrollWidth);
    svg.setAttribute("height", container.scrollHeight);

    const nodes = [...container.querySelectorAll(".node")];
    const nodeMap = {};
    nodes.forEach(n => nodeMap[n.dataset.index] = n);

    tree.forEach((_, i) => {
        const parent = nodeMap[i];
        if (!parent) return;

        const parentRect = parent.getBoundingClientRect();
        const px = parentRect.left + parentRect.width / 2 - containerRect.left;
        const py = parentRect.top + parentRect.height / 2 - containerRect.top;

        const parentDepth = Number(parent.dataset.depth || Math.floor(Math.log2(i + 1)));

        [2 * i + 1, 2 * i + 2].forEach(childIndex => {
            const child = nodeMap[childIndex];
            if (!child) return;

            const childRect = child.getBoundingClientRect();
            const cx = childRect.left + childRect.width / 2 - containerRect.left;
            const cy = childRect.top + childRect.height / 2 - containerRect.top;

            const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
            line.setAttribute("x1", px);
            line.setAttribute("y1", py);
            line.setAttribute("x2", cx);
            line.setAttribute("y2", cy);
            line.setAttribute("stroke", "#52525b");
            line.setAttribute("stroke-width", "2");

            // tag with depth; CSS controls visibility via .drawn
            line.dataset.depth = parentDepth;
            svg.appendChild(line);
        });
    });
}


function autoScaleTree() {
    const wrapper = document.getElementById("tree-wrapper");
    const scaleBox = document.getElementById("tree-scale");

    const scaleX = wrapper.clientWidth / scaleBox.scrollWidth;
    const scaleY = wrapper.clientHeight / scaleBox.scrollHeight;

    const scale = Math.min(scaleX, scaleY, 1);

    scaleBox.style.transform = `scale(${scale})`;
}

function postResult(finalTree) {
    const root = finalTree.tree[0];

    // Option value (headline)
    document.getElementById("results_option_value").textContent =
        `$${Math.max(0,root.option_value.toFixed(2))}`;

    const greeks = [
        ["delta", "Delta"],
        ["gamma", "Gamma"],
        ["theta", "Theta"],
        ["vega", "Vega"],
        ["rho", "Rho"]
    ];

    greeks.forEach(([key, label]) => {
        const el = document.getElementById(`results_${key}`);
        const value = root[key];

        let color =
            value > 0 ? "positive" :
            value < 0 ? "negative" :
            "neutral";

        el.innerHTML = `
            <span class="greek-label">${label}</span>
            <span class="greek-value ${color}">
            ${value !== null ? value.toFixed(4) : "—"}
            </span>
        `;
    });
}

function animateTreeByLevel(levelDelay = 180) {
    const nodes = Array.from(document.querySelectorAll('.node'));
    const levels = {};
    nodes.forEach(node => {
        const depth = Number(node.dataset.depth ?? (Number(node.style.gridColumn) - 1));
        if (!levels[depth]) levels[depth] = [];
        levels[depth].push(node);
    });

    const maxLevel = Math.max(...Object.keys(levels).map(Number));

    for (let level = 0; level <= maxLevel; level++) {
        setTimeout(() => {
            (levels[level] || []).forEach(n => n.classList.add('visible'));

            // after nodes show, reveal lines that originate from this depth
            setTimeout(() => {
                const svg = document.getElementById('tree-lines');
                svg.querySelectorAll(`line[data-depth="${level}"]`).forEach(l => l.classList.add('drawn'));
            }, 120);
        }, level * levelDelay);
    }
}

function update() {
    const S0 = Math.max(0,Number(current_price.value));
    const u = Math.max(0,Number(U.value));
    const n = Math.min(4, Math.max(0, Number(steps.value)));
    const r = Math.max(0,Number(risk_rate.value));
    const k = Math.max(0,Number(strike.value));
    const isCall = call_bool.checked;
    const isEuro = european_bool.checked;

    const underlying = buildUnderlyingTree(S0, u, n);

    const optionTree = buildOptionsTree(underlying, r, k, isCall, isEuro);

    const greekTree = buildGreeksTree(optionTree, underlying);
    renderTree(greekTree);
    postResult(greekTree);
    requestAnimationFrame(() => {
        drawConnections(greekTree.tree);
        animateTreeByLevel(180);
    });

}




document.querySelectorAll("input").forEach(input => {
    input.addEventListener("input", update);
});


