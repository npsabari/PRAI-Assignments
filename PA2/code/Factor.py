"""
Author: Santhosh Kumar M (CS09B042)
File: Factor.py
"""

class Factor():
    """
    Class to represent factors corresponding to an undirected graphical model.
    """

    def __init__(self, name="", values=list()):
        """
        Initializes the name and values of the factor.
        For example,
        name = 'AB'
        values = [0.4, 0.2, 0.03, 0.07]
        corresponds to factor(A, B) and wherein factor(A = true, B = true) = 0.4,
        factor(A = false, B = true) = 0.03 and so on.
        """
        self.name = name
        self.values = values




