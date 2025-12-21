from UnderlyingAssetPriceTree import PriceMovementTree
from typing import Union, Optional
from Node import Node

class BackwardInductionTree:
    def __init__(self, MovementTree: PriceMovementTree,
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

        self.tree = MovementTree.get_tree()
        self.risk_rate = risk_free_rate
        self.strike = strike_price


        #Options
        self.call_bool = bool(call_option)
        self.european_bool = bool(european_option)

        #Misc
        self.height = MovementTree.get_height()


        self.compute_terminal_payoffs()

        print([node.payoff for node in self.tree[-2**(self.height):]])
    def compute_terminal_payoffs(self) -> None:
        """
        Last 2^(n) elems are terminal nodes
        :return:
        """
        for node in self.tree[-2**(self.height):]:
            print(node.stock_value)
            node.payoff = max(node.stock_value - self.strike,0)

obj = PriceMovementTree(100 , 0.1, 3)
print(str(obj))
back = BackwardInductionTree(obj, 0.03,102)

