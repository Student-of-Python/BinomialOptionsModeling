from unittest.mock import right

from UnderlyingAssetPriceTree import PriceMovementTree
from BackwardInduction import BackwardInductionTree
from typing import Union, Optional, Callable
from Node import Node


class Greeks:
    def __init__(self, price_movement: PriceMovementTree , induction_tree: BackwardInductionTree) -> None:
        """
        :param price_movement: Price movement tree of the underlying asset movement
        :param induction_tree: Induction
        """
        self.p_tree = price_movement.tree
        self.i_tree = induction_tree.tree

        #Misc
        self.call_option = bool(induction_tree.get_attr("call_bool"))
        self.strike = induction_tree.get_attr("strike")
        self.height = induction_tree.get_attr("height")

        self.init_delta()

    def init_delta(self):
        """
        :return:
        Delta = Change in Option Value  / Change in Stock Price
        --> V_U - V_D / S_U - S_D

        For Terminal Nodes:
        Delta = 1 --> ITM
        Delta = 0 --> OTM
        Delta = 0.5 --> ATM
        """
        #Compute Terminal Delta
        self.apply_terminal_func(self.terminal_delta)

        last_parent_index = (len(self.i_tree) - 2) // 2
        for i in range(last_parent_index, -1, -1):
            parent = self.i_tree[i]
            left = self.i_tree[i * 2 + 1]
            right = self.i_tree[i * 2 + 2]
            parent.delta = (right.option_value - left.option_value) / (right.stock_value - left.stock_value)


    def apply_terminal_func(self, func: Callable) -> None:
        for leaf in self.i_tree[-2**(self.height-1):]:
            func(leaf)



    def terminal_delta(self, leaf: Node) -> None:
        """
        :param leaf: Terminal Node
        :return: None; Computes Delta for Node obj.
        """
        delta = 1 if (leaf.stock_value > self.strike) else 0 if (leaf.stock_value < self.strike) else 0.5
        if not self.call_option:
            delta = -delta

        leaf.delta = delta


    def __str__(self) -> str:
        """
        :return: Level Order of the tree

        """
        tree_str = ""
        for i in range(self.height + 1):
            tree_str += " ".join([f"{node.delta:.2f}" for node in self.i_tree[2**i-1: 2**(i+1) - 1]]) + "\n"
        return tree_str


obj = PriceMovementTree(100 , 0.1, 3)
print(str(obj))
back = BackwardInductionTree(obj, 0.1,102,True,False)
print(str(back))
greeks = Greeks(obj, back)
print(str(greeks))




