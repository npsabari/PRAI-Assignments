"""
Author: Santhosh Kumar M (CS09B042)
File: main.py
"""

import Utils
import Factor
import Message
import sys
import Clique
import Junction_Tree

def main():
    input_file = sys.argv[1]

    [factors, variables] = Utils.read_file(input_file)

    junction_tree = None

    if Utils.is_tree(factors) == True:
        elimination_order = Utils.get_elimination_ordering(variables, [], factors)
        max_cliques = Utils.get_max_cliques(factors, elimination_order)
        """
        for cliq in max_cliques:
            print cliq.name
            print cliq.values
        """
        # Create a junction tree
        junction_tree = Utils.get_junction_tree(max_cliques)
        """
        for node in junction_tree.cliques:
            print node.name+" "
            print node.values
        for node in junction_tree.neighbours:
            print 'node is '+str(node.name)
            for neigh in junction_tree.neighbours[node]:
                print 'nodes are '+str(neigh.name)
        """

    else:
        elimination_order = Utils.get_elimination_ordering(variables, [], factors)

        # Form a set of maximal elimination cliques
        max_cliques = Utils.get_max_cliques(factors, elimination_order)
        """
        for cliq in max_cliques:
            print cliq.name
            print cliq.values
        """
        # Create a clique tree over maximal elimination cliques.
        junction_tree = Utils.get_junction_tree(max_cliques)
        """
        for node in junction_tree.cliques:
            print node.name+" "
            print node.values
        for node in junction_tree.neighbours:
            print 'node is '+str(node.name)
            for neigh in junction_tree.neighbours[node]:
                print 'nodes are '+str(neigh.name)
        """
    # Message passing
    junction_tree.message_passing()
    """
    for node in junction_tree.cliques:
        print node.marginals.name
        print node.marginals.values
    """
    # Marginal inference
    marginal_prob_dist = junction_tree.marginal_inference('G')
    print marginal_prob_dist.name
    print marginal_prob_dist.values

    # Joint inference
    joint_prob_dist = junction_tree.joint_inference(['G', 'S'])
    print joint_prob_dist.name
    print joint_prob_dist.values

    # Conditional inference
    conditional_prob_dist = junction_tree.conditional_inference('L', 'I')
    print conditional_prob_dist.name
    print conditional_prob_dist.values

if __name__ == "__main__":
    main()
