"""
Author: Santhosh Kumar M (CS09B042)
File: Utils.py
"""

from Factor import Factor
from Node import Node
from Message import Message

# My Imports
import re

def moralize_graph(input_file):
    """
    Performs moralization of the given graph if directed and returns the list of Factor objects (factors).
    """

    lines = list()
    with open(input_file, 'r') as infile:
        # Assuming the table details starts from the fourth non-empty line
        lines = [line.strip() for line in infile if len(line.strip()) != 0][4:]

    list_of_factors, idx= list(), 0

    while idx < len(lines):
        words = re.findall(r"[\w']+", lines[idx])
        main_var, parent_var = words[1], list()

        for i in range(3, len(words)): parent_var.append(words[i])

        if len(parent_var) == 0:
            idx += 1
            prob = float(lines[idx])
            values = [prob, 1-prob]
            list_of_factors.append(Factor(main_var, values))
            idx += 1
            continue

        # Increment by 2
        idx += 2
        tmp_idx, tt_size = 0, 1<<len(parent_var)
        values = [0 for i in range(tt_size<<1)]
        while tmp_idx < tt_size:
            prob = float(lines[idx].split()[-1])
            values[tmp_idx<<1], values[(tmp_idx<<1)|1] = prob, 1.0-prob
            tmp_idx += 1
            idx += 1

        list_of_factors.append(Factor(''.join(parent_var) + main_var, values))
    return list_of_factors

def read_file(input_file):
    """
    Reads the given input file.
    Performs moralization to convert to undirected graph if given graph is directed.
    Assigns values to factors which are stored as a list of objects (factors) of class Factor.
    Creates a list of objects (nodes) of class Node corresponding to the random variables in the graph.
    Returns the list of Factor() objects (factors) and the list of Node() objects.
    """
    list_of_factors = moralize_graph(input_file)
    list_of_nodes = [Node(fac.name[-1]) for fac in list_of_factors]
    for fac in list_of_factors:
        print fac.name
        print fac.values
    return [list_of_factors, list_of_nodes]






