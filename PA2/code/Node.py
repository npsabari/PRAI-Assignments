"""
Author: Santhosh Kumar M (CS09B042)
File: Node.py
"""

from Message import Message

class Node():
    """
    Class to represent nodes in the graph.
    """

    def __init__(self, name, alpha_message=Message(), beta_message=Message()):
        """
        Initializes the name, alpha message vector and beta message vector for the concerned node.
        For example,
        name = 'A'
        alpha_message = Message() object
        beta_message = Message() object
        """
        self.name = name
        self.alpha_message = alpha_message
        self.beta_message = beta_message





