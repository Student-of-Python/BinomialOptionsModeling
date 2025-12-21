"""
Node Class
--> Represents a Node
Contains
--------

Values
Stock Value
"""
from typing import Optional


class Node:
    def __init__(self, stock_value: float) -> None:
        '''
        :param stockvalue: price of underlying asset at some time
        '''
        self.stock_value = stock_value if stock_value > 0 else 0

        #Misc / To be computed
        self.option_value = None
        self.immediate_value = None
