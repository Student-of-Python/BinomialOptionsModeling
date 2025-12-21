"""

"""
from typing import Optional, Union
from Node import Node

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

        self.tree = [Node(0)] * (2**(self.steps + 1) - 1)
        self.tree[0] = Node(stock_value = current_price)
        self.mk_tree()

    def mk_tree(self, i: int = 0) -> None:
        """
        Notes:
        Given parent node with index i
        left node = list[2*i + 1]
        right node = list[2*i + 2]

        :param root: root index of tree
        :return: Binomial Tree with price action
        """
        #Base Case: Outside of Bounds
        if i > 2**((self.steps + 1) - 2):
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


    def level_order(self):
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
        for i in range(self.steps):
            yield [round(node.stock_value,2) for node in self.tree[2**i-1: 2**(i+1) - 1]]


    def __str__(self) -> str:
        """
        :return: String version of the tree
        [a]
        [b,c]
        """
        gen = self.level_order()
        tree_str = ""
        for elem in gen:
            tree_str += f"{elem}\n"
        return tree_str

obj = PriceMovementTree(100 , 0.1, 5)


