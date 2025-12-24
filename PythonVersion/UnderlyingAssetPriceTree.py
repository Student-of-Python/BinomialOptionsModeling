from typing import Optional, Union, Any
from Node import Node
import math

class PriceMovementTree:
    def __init__(self, current_price: Union[float,int], U: Union[int, float], steps: int = 5):
        """
        :param current_price: current price of the underlying asset
        :param U: Magnitude of upward or downward movement (as a decimal)
        :param steps: height of the tree
        """
        self.price = current_price
        self.U = 1 + U
        self.D = 1.0 / self.U
        self.steps = steps
        self.delta_t = 1.0 / (self.steps + 1)

        self.tree = [Node(current_price) for _ in range((2**(self.steps + 1) - 1))]
        self.mk_tree()




    def mk_tree(self, i: int = 0) -> None:
        """
        Notes:
        Given parent node with index i
        left node = list[2*i + 1]
        right node = list[2*i + 2]

        :param i:  index of tree
        :return: Binomial Tree with price action
        """
        #Base Case: Outside of Bounds
        if i*2 + 2 > len(self.tree):
            return

        #Recursive Case: Valid Index
        price = self.tree[i].stock_value

        #Left Child
        self.tree[2 * i + 1] = Node(stock_value= price * self.D)

        #Right Child
        self.tree[2 * i + 2] = Node(stock_value=price * self.U)

        #Left Tree + Right Tree
        self.mk_tree(2 * i + 1)
        self.mk_tree(2 * i + 2)


    def get_height(self) -> int:
        """
        :return: Height of the tree
        """
        return self.steps + 1



    def get_tree(self):
        return self.tree


    def get_attr(self, attr: str) -> Optional[Any]:
        if hasattr(self, attr):
            return getattr(self, attr)

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
        for i in range(self.steps + 1):
            tree_str += " ".join([f"{node.stock_value:.2f}" for node in self.tree[2**i-1: 2**(i+1) - 1]]) + "\n"
        return tree_str




