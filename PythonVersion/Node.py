"""
Node Class
--> Represents a Node
Contains
--------

Values
Stock Value
"""
from typing import Optional, Any


class Node:
    def __init__(self, stock_value: float) -> None:
        '''
        :param stockvalue: price of underlying asset at some time
        '''
        self.stock_value = stock_value if stock_value > 0 else 0

        #Misc / To be computed
        self.option_value = None

        self.delta = None
        self.gamma = None
        self.theta = None
        self.vega = None
        self.rho = None

    def get_attr(self, attr: str) -> Optional[Any]:
        if hasattr(self, attr):
            return getattr(self, attr)


    def __format__(self, format_spec: str) -> str:
        """
        :param format_spec: Any of the Attributes
        :return:
        """

        if not format_spec:
            return str(self)

        if hasattr(self, format_spec):
            return f"{round(getattr(self,format_spec), 2) if isinstance(getattr(self,format_spec), (float, int)) else getattr(self,format_spec)}"

        raise ValueError(f"[ERROR] Unknown format specifier: {format_spec}")

    def __str__(self) -> str:
        """
        String representation of a node
        """
        s = (f"Stock Value : {self.stock_value}\n"
             f"Option Value : {self.option_value}\n"
             f"Delta : {self.delta if self.delta else "--"}\n"
             f"Gamma : {self.gamma if self.gamma else "--"}\n" 
             f"Theta : {self.theta if self.theta else "--"}\n"
             f"Vega : {self.vega if self.vega else "--"}\n"
             f"Rho : {self.rho if self.rho else "--"}\n")

        return s

