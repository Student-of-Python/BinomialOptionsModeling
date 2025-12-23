from UnderlyingAssetPriceTree import PriceMovementTree
from BackwardInduction import BackwardInductionTree
from typing import Union, Optional, Callable
from Node import Node


class Greeks:
    def __init__(self, induction_tree: BackwardInductionTree) -> None:
        """
        :param induction_tree: Induction
        """
        self.i_tree = induction_tree.tree

        #Misc
        self.call_option = bool(induction_tree.get_attr("call_bool"))
        self.strike = induction_tree.get_attr("strike")
        self.height = induction_tree.get_attr("height")

        self.compute_greeks()


    def apply_delta(self, parent: Node, right: Optional[Node] , left: Optional[Node]) -> None:
        """
        :param parent: parent Node or leaf node
        :param right: Right node (If applicable)
        :param left: Left node (If applicable)
        :return: None; In-place calculation

        Notes:
        Delta = Change in Option Value  / Change in Stock Price
            --> V_U - V_D / S_U - S_D

        For Terminal Nodes:
        Delta = 1 --> ITM
        Delta = 0 --> OTM
        Delta = 0.5 --> ATM
        """
        if not right or not left:
            #leaf Node
            delta = 1 if (parent.stock_value > self.strike) else 0 if (parent.stock_value < self.strike) else 0.5
            if not self.call_option:
                delta = -delta
            parent.delta = delta
            return
        else:
            parent.delta = (right.option_value - left.option_value) / (right.stock_value - left.stock_value)
            return

    def apply_gamma(self, parent: Node, right: Optional[Node] , left: Optional[Node]):
        """
        :param parent: parent Node or leaf node
        :param right: Right node (If applicable)
        :param left: Left node (If applicable)
        :return: None; In-place calculation

        Notes:
        Gamma = Change in Delta / Change in Stock Price
            --> D_U - D_D / S_U - S_D
        For Terminal Nodes:
        Gamma = 0 --> ITM
        Gamma = 0 --> OTM
        Gamma = inf. --> ATM
        (ITM, OTM delta is solidified, with inf at ATM since it switches from 0-1 in instantly)
        """


        if not right or not left:
            # leaf Node

            #TODO: Gamma behaves weirdly around expiration; should I omit Gamma from last two levels?
            gamma = 0 if (parent.delta != self.strike) else -1
            parent.gamma = gamma
            return
        else:

            parent.gamma = (right.delta - left.delta) / (right.stock_value - left.stock_value)
            return


    def compute_greeks(self) -> None:
        """
        :return:
        """

        for i in range(len(self.i_tree) - 1, -1, -1): #O(N) time with 2^height - 1 elems :(
            parent = self.i_tree[i]
            right = self.i_tree[2 * i + 2] if 2 * i + 2 < len(self.i_tree) - 1 else None
            left = self.i_tree[2*i + 1] if 2*i + 1 < len(self.i_tree) - 1 else None

            #Apply functions
            self.apply_delta(parent,right, left)
            self.apply_gamma(parent, right, left)



    def __str__(self) -> str:
        """
        :return: Level Order of the tree

        """
        tree_str = ""
        for i in range(self.height + 1):
            tree_str += " ".join([f"{node.gamma:.2f}" for node in self.i_tree[2**i-1: 2**(i+1) - 1]]) + "\n"
        return tree_str


obj = PriceMovementTree(100 , 0.1, 3)
print(str(obj))
back = BackwardInductionTree(obj, 0.1,102,True,False)
print(str(back))
greeks = Greeks(back)
print(str(greeks))




