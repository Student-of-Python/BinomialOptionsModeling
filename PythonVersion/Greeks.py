from UnderlyingAssetPriceTree import PriceMovementTree
from BackwardInduction import BackwardInductionTree
from typing import Union, Optional
from Node import Node


class Greeks:
    def __init__(self, price_movement: PriceMovementTree , induction_tree: BackwardInductionTree) -> None:
        """
        :param price_movement: Price movement tree of the underlying asset movement
        :param induction_tree: Induction
        """
        self.p_tree = price_movement
        self.i_tree = induction_tree

        #Misc
        self.call_option = induction_tree.get_attr("call_bool")

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



