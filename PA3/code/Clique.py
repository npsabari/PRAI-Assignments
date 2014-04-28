"""
Author: Santhosh Kumar M (CS09B042)
File: Clique.py
"""

class Clique():
    """
    Class to represent a clique in a clique tree.
    """

    def __init__(self, name, values = list(), factors = list(), marginals = None):
        """
        Initializes the name and values of the clique.
        For example,
        name = 'AB'
        values = [0.4, 0.2, 0.03, 0.07]
        corresponds to clique(A, B) and wherein clique(A = true, B = true) = 0.4, clique(A = false, B = true) = 0.03 and so on.
        """
        self.name = name
        self.values = values
        self.factors = factors
        self.marginals = marginals

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name
