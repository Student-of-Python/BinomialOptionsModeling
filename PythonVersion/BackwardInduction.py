from UnderlyingAssetPriceTree import PriceMovementTree
from typing import Union, Optional
from Node import Node
import math
class BackwardInductionTree:
    def __init__(self, movement_tree: PriceMovementTree,
                 risk_free_rate: Union[float, int],
                 strike_price: Union[float, int],
                 call_option: Union[True, False] = True,
                 european_option: Union[True, False] = True,
                 ):
        """
        :param MovementTree: Price Action Movement Tree
        :param risk_free_rate: rate of return at no risk
        :param call_option: Call option if true, put if false
        :param European_option: European Option if true, American Option if false
        :param strike_price: strike price of the option
        """
        self.tree = movement_tree.get_tree()
        self.risk_rate = risk_free_rate
        self.strike = strike_price


        #Options
        self.call_bool = bool(call_option)
        self.european_bool = bool(european_option)

        #Misc
        self.height = movement_tree.get_height()
        self.delta_t = 1.0 / self.height
        self.prob = (math.exp(self.risk_rate * self.delta_t) - movement_tree.D) / (movement_tree.U - movement_tree.D)

        self.compute_terminal_payoffs()

        self.backwardinduction()


    def compute_terminal_payoffs(self) -> None:
        """
        Last 2^(n) elems are terminal nodes
        :return: Computes payoff of the terminal nodes
        """
        for leaf in self.tree[-2**self.height:]:
            self.compute_payoff(leaf)

    def compute_payoff(self, leaf: Node) -> None:
        """
        :param Leaf: Leaf (For American Options, it would be any node to find the immediate payoff)
        :return:
        """
        if self.call_bool:
            leaf.option_value = max(leaf.stock_value - self.strike, 0)
        else: # Put Option
            leaf.option_value = max(0, self.strike - leaf.stock_value)


    def backwardinduction(self) -> None:
        """
        :return:
        """
        last_parent = (len(self.tree) - 2) // 2
        for i in range(last_parent, -1, -1):
            parent = self.tree[i]
            left = self.tree[2 * i + 1]
            right = self.tree[2 * i + 2]

            discounted_price_value = math.exp(-self.risk_rate * self.delta_t) * (
                        self.prob * right.option_value + (1 - self.prob) * left.option_value
                )

            if self.european_bool:
                parent.option_value = discounted_price_value
            else:
                #American Options
                self.compute_payoff(parent)
                parent.option_value = max(parent.option_value, discounted_price_value)


    def __str__(self) -> str:
        """
        :return: Level Order of the tree

        [1,2,3,4,5,6,7]
        [0,1,2,3,4,5,6]
        Logic:
            0th Level: [1] --> [0:1]

            1st Level: [2,3] --> [1:3]

            3rd Level: [4,5,6,7] --> [3 : 7]

            nth Level: [2**(i) -1 : 2^(i + 1) - 1]
            steps --> height
        """
        tree_str = ""
        for i in range(self.height + 1):
            tree_str += " ".join([f"{node.option_value:.2f}" for node in self.tree[2**i-1: 2**(i+1) - 1]]) + "\n"
        return tree_str




obj = PriceMovementTree(100 , 0.1, 3)
print(str(obj))
back = BackwardInductionTree(obj, 0.1,102,False,False)
print(str(back))

