from UnderlyingAssetPriceTree import PriceMovementTree
from BackwardInduction import BackwardInductionTree
from typing import Union, Optional, Callable, List
from Node import Node
import math


class Greeks:

    def __init__(self, induction_tree: BackwardInductionTree, price_tree: PriceMovementTree) -> None:
        """
        :param induction_tree: Induction
        """
        self.i_tree = induction_tree.tree
        self.p_tree = price_tree
        self.vega_epsilon = 0.01
        self.rho_epsilon = 0.01

        #Misc
        self.call_option = bool(induction_tree.get_attr("call_bool"))
        self.strike = induction_tree.get_attr("strike")
        self.height = induction_tree.get_attr("height")

        self.type = induction_tree.get_attr("european_option")
        self.risk_rate  = induction_tree.get_attr("risk_rate")
        self.delta_t = induction_tree.get_attr("delta_t")
        self.prob = induction_tree.get_attr("prob")
        self.U = price_tree.get_attr("U")


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

            #NOTE: Gamma behaves weirdly around expiration; should I omit Gamma from last two levels?
            gamma = 0 if (parent.delta != self.strike) else -1
            parent.gamma = gamma
            return
        else:
            parent.gamma = (right.delta - left.delta) / (right.stock_value - left.stock_value)
            return

    def apply_theta(self, parent: Node, i: int):
        """
        :param parent: parent Node or leaf node
        :param i: index of the parent node
        :return: None; In-place calculation

        Notes:
        Theta is how much value time has on an option;
        more specifically, if price stays the same, but we move the option forward in time,
        how much will the price change?

        Theta = (V_Expected - V_Now) / Change in time
        V_expected = mid two steps ahead
        At Expiration Theta = 0, meaning no uncertainty.
        """

        #NOTE: Is this the correct implementation of theta?
        mid = 2*(2*i+1) + 2 #Middle Node by left then right traversal
        if mid < len(self.i_tree):
            parent.theta = (self.i_tree[mid].option_value - parent.option_value) / (2 * self.delta_t)
            return
        else:
            parent.theta = "--"

    def apply_vega(self) -> None:
        """
        :return:
        """
        vega_tree_plus = self.vega_option_tree(self.vega_epsilon)
        vega_tree_minus = self.vega_option_tree(-self.vega_epsilon)
        self.i_tree[0].vega = (vega_tree_plus[0].option_value - vega_tree_minus[0].option_value) / (
                    2 * self.vega_epsilon)

    def apply_rho(self) -> None:
        """
        :return:
        """
        rho_tree_plus = self.rho_option_tree(self.rho_epsilon)
        rho_tree_minus = self.rho_option_tree(-self.rho_epsilon)
        self.i_tree[0].rho = (rho_tree_plus[0].option_value - rho_tree_minus[0].option_value) / (
                2 * self.rho_epsilon)


    def vega_option_tree(self, epsilon: Union[float, int]) -> List[Union[float,int]]:
        """
        :param epsilon:
        :return:
        """
        s_dev = (math.log(self.U) / math.sqrt(self.delta_t)) + epsilon
        u_vega = math.exp(s_dev * math.sqrt(self.delta_t))

        price_tree = PriceMovementTree(self.p_tree.price, u_vega, self.height - 1)

        option_tree = BackwardInductionTree(price_tree, self.risk_rate, self.strike, self.call_option,
                                                 self.type)

        return option_tree.tree

    def rho_option_tree(self, epsilon: Union[float, int]) -> List[Union[float,int]]:
        """
        :param epsilon:
        :return:
        """
        risk_free_rate = self.risk_rate + epsilon

        price_tree = PriceMovementTree(self.p_tree.price, self.U, self.height - 1)

        option_tree = BackwardInductionTree(price_tree, risk_free_rate, self.strike, self.call_option,
                                                 self.type)

        return option_tree.tree






    def compute_greeks(self) -> None:
        """
        :return:
        """
        self.apply_vega()
        self.apply_rho()
        for i in range(len(self.i_tree) - 1, -1, -1): #O(N) time with 2^height - 1 elems :(
            parent = self.i_tree[i]
            right = self.i_tree[2 * i + 2] if 2 * i + 2 < len(self.i_tree) - 1 else None
            left = self.i_tree[2*i + 1] if 2*i + 1 < len(self.i_tree) - 1 else None

            #Apply functions
            self.apply_delta(parent,right, left)
            self.apply_gamma(parent, right, left)
            self.apply_theta(parent, i)




    def __str__(self) -> str:
        """
        :return: Level Order of the tree

        """
        tree_str = ""
        for i in range(self.height + 1):
            tree_str += " ".join([f"{node.rho}" for node in self.i_tree[2**i-1: 2**(i+1) - 1]]) + "\n"
        return tree_str


obj = PriceMovementTree(100 , 0.1, 5)
print(str(obj))
back = BackwardInductionTree(obj, 0.1,102,True,False)
print(str(back))
greeks = Greeks(back, obj)
print(str(greeks))




