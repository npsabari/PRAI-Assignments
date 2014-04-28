"""
Author: Santhosh Kumar M (CS09B042)
File: main.py
"""

import Undirected_Graphical_Model
import Utils
import Factor
import Node
import Message
import sys

def main():
    input_file = sys.argv[1]

    [factors, nodes] = Utils.read_file(input_file)

    ugm = Undirected_Graphical_Model.Undirected_Graphical_Model(factors, nodes)
    #print ugm.is_chain()

    if ugm.is_chain() == False:

        marginal_prob_dist = ugm.marginal_inference('J')
        print marginal_prob_dist.values
        marginal_prob_dist = ugm.marginal_inference('B')

        joint_prob_dist = ugm.joint_inference('J', 'M')
        print joint_prob_dist.values

        conditional_prob_dist = ugm.conditional_inference('B', 'J')
        print conditional_prob_dist.values
        return

    else:

        ugm.forward_message_pass()
        ugm.backward_message_pass()
        """
        chain_marginal_prob_dist = ugm.chain_marginal_inference('D')
        for value in chain_marginal_prob_dist.values:
            print value
        chain_consecutive_prob_dist = ugm.chain_consecutive_joint_inference('C', 'D')


        chain_non_consecutive_prob_dist = ugm.chain_non_consecutive_joint_inference('A', 'D')
        chain_conditional_prob_dist = ugm.chain_conditional_inference('A', 'D')
        """

if __name__ == "__main__":
    main()
