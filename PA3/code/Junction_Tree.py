"""
Author: Santhosh Kumar M (CS09B042)
File: Clique_Tree.py
"""

from Message import Message
from Clique import Clique
from sets import Set
import Utils

class Junction_Tree():
    """
    Class to represent a junction tree and perform message passing in it.
    """

    def __init__(self, cliques, neighbours):
        """
        Initializes the cliques and neighbours of each clique in the junction tree with the given list of Clique() objects and neighbours dictionary.
        Defines messages between all pairs of cliques which are adjacent in the clique tree.
        For example,
        cliques = [clique_1, clique_2, clique_3] wherein clique_1.name = 'AB', clique_2.name = 'BDE', clique_3.name = 'AC'
        neighbours = {clique_1 : [clique_2, clique_3], clique_2 : [clique_1], clique_3 : [clique_1]}
        """
        self.cliques = cliques
        self.neighbours = neighbours

        # Initialize messages using objects of Message() class - code goes here.
        self.message_dict = dict()
        for cliq in self.cliques:
            self.message_dict[cliq] = \
                {neigh: Message(''.join(list(Set(cliq.name) & Set(neigh.name))), cliq, neigh, []) for neigh in self.neighbours[cliq]}

    def normalize(self, clique):
        """
        Normalizes the values corresponding to the given clique and returns the normalized clique.
        """
        try:
            tmp_values = [val/sum(clique.values) for val in clique.values]
            clique.values = tmp_values
        except ZeroDivisionError:
            print ' :-o Zero probability'
        return clique

    def multiply_messages_clique(self, messages, clique):
        """
        Multiplies the given list of incoming messages and the given clique and returns the resultant clique.
        """

        # Use the predefined multiply_factor function as the prototype of
        # Clique and Factor are same
        ret_clique = Clique(clique.name, clique.values)
        for msg in messages:
            ret_clique = Utils.multiply_factors(ret_clique, msg)
        return ret_clique

    def marginalize(self, clique, variable):
        """
        Marginalizes the given clique over the given variable and returns the marginalized clique.
        """
        """
        print 'Marginalizing'
        print factor.name, factor.values
        print 'Over variable '+variable
        """
        # Sum over all possible values of the given variable in the given
        # Clique
        try:
            my_name = ''.join([i for i in clique.name if i != variable])
            my_val = [0 for i in range(1<<len(my_name))]
            mask = len(my_val)-1
            var_idx = len(clique.name)-clique.name.index(variable)-1
            tmp_sz = 0
            while mask >= 0:
                tmp_values = [((mask>>i)&1) for i in range(len(my_name)-1, -1, -1)]
                pos = [len(clique.name)-clique.name.index(i)-1 for i in my_name]
                my_val[tmp_sz] = clique.values[sum([int(not tmp_values[i])*(1<<pos[i]) for i in range(len(my_name))]) + (1<<var_idx)]
                my_val[tmp_sz] += clique.values[sum([int(not tmp_values[i])*(1<<pos[i]) for i in range(len(my_name))])]
                tmp_sz += 1
                mask -= 1
            return Clique(my_name, my_val)
        except ValueError:
            print 'Enter the function variables properly :-/'

    def message_passing(self):
        """
        Performs message passing in the junction tree.
        """

        # Computes the message between sender and receiver
        def sp_message(sender, receiver):
            my_cliq = Clique(sender.name, sender.values, [])
            for neigh in self.neighbours[sender]:
                if neigh == receiver: continue
                my_cliq = Utils.multiply_factors(my_cliq, self.message_dict[neigh][sender])
            for var in Set(sender.name) - Set(receiver.name): my_cliq = self.marginalize(my_cliq, var)
            return Message(my_cliq.name, sender, receiver, my_cliq.values)

        # Recursively performs the upward passing of message
        def recursive_msg_pass(root, parent_node):
            my_cliq = Clique(root.name, root.values)
            for neigh in self.neighbours[root]:
                if parent_node == neigh: continue
                self.message_dict[neigh][root] = recursive_msg_pass(neigh, root)
                my_cliq = Utils.multiply_factors(my_cliq, self.message_dict[neigh][root])
            for var in Set(root.name) - Set(parent_node.name): my_cliq = self.marginalize(my_cliq, var)
            return Message(my_cliq.name, root, parent_node, my_cliq.values)

        # Recursively performs the downward message passing
        def downward_pass(root, parent_node):
            my_cliq = Clique(root.name, root.values)
            for neigh in self.neighbours[root]:
                if parent_node == neigh: continue
                self.message_dict[root][neigh] = sp_message(root, neigh)
                downward_pass(neigh, root)

        # Computes the marginals and stores for efficient calculations
        def get_marginals(root, parent_node):
            my_cliq = Clique(root.name, root.values)
            for neigh in self.neighbours[root]:
                my_cliq = Utils.multiply_factors(my_cliq, self.message_dict[neigh][root])
                if neigh == parent_node: continue
                get_marginals(neigh, root)
            root.marginals = my_cliq

        # Calling the functions inside this function
        primary_root = self.cliques[0]
        recursive_msg_pass(primary_root, primary_root)
        downward_pass(primary_root, primary_root)
        get_marginals(primary_root, primary_root)

    def marginal_inference(self, variable):
        """
        Performs marginal inference, P(variable), in the junction tree and returns the marginal probability distribution as a list.
        """
        # Selects the smallest clique containing the variable and just
        # marginalize the 'marginal' to get the probability
        my_cliq = None
        for cliq in self.cliques:
            if variable in cliq.name:
                if my_cliq is None or len(my_cliq.name) > len(cliq.name):
                    my_cliq = cliq
        my_cliq = my_cliq.marginals
        my_cliq_vars = Set(my_cliq.name)
        for var in my_cliq_vars - Set(variable): my_cliq = self.marginalize(my_cliq, var)
        return my_cliq

    def joint_inference(self, variables):
        """
        Performs joint inference, P(variables), in the junction tree and returns the joint probability distribution as a list.
        """

        # Function to get subtree such that scope[sub-tree] >= variables
        def get_subtree(root, parent_node, clique_vars):
            if len(clique_vars) == 0: return None
            sub_tree_cliques = list()
            for neigh in self.neighbours[root]:
                if neigh == parent_node: continue
                clique_vars -= Set(neigh.name)
                sub_tree_cliques.append(neigh)
                if len(clique_vars) == 0: return sub_tree_cliques
            for neigh in self.neighbours[root]:
                if neigh == parent_node: continue
                child_tree = get_subtree(neigh, root, clique_vars)
                if child_tree is None: return sub_tree_cliques
                sub_tree_cliques.extend(child_tree)
            return sub_tree_cliques

        # Compute the modified factors of the subtree for VE
        def get_subtree_factors(root, parent_node):
            sub_tree_factors_tmp = []
            for neigh in self.neighbours[root]:
                if neigh == parent_node or neigh not in sub_tree_set: continue
                sub_tree_factors_tmp.append(Utils.multiply_factors(neigh.marginals, self.message_dict[neigh][root], True))
                sub_tree_factors_tmp.extend(get_subtree_factors(neigh, root))
            return sub_tree_factors_tmp

        # Does VE on the given factors for the variables to be inferenced on
        def joint_ve_inference(all_variables, _variables, factors):
            """
            Performs joint inference, P(variables), on the UGM and returns the joint probability distribution as a list.
            """
            elimination_order = Utils.get_elimination_ordering(all_variables, _variables, factors)
            list_of_factors = Set(factors)
            for elem in elimination_order:
                facs_to_multiply = list()
                for fac in list_of_factors:
                    if elem in fac.name:
                        facs_to_multiply.append(fac)

                if len(facs_to_multiply) == 0: assert(False)
                res = facs_to_multiply[0]
                for fac in facs_to_multiply[1:]:
                    res = Utils.multiply_factors(res, fac)
                res = self.marginalize(res, elem)
                list_of_factors -= Set(facs_to_multiply)
                list_of_factors.add(res)

            list_of_factors = list(list_of_factors)
            ret_fac = list_of_factors[0]
            for fac in list_of_factors[1:]:
                ret_fac = Utils.multiply_factors(ret_fac, fac)
            return self.normalize(ret_fac)

        factor_list = self.cliques
        primary_root = factor_list[0]
        _vars = Set(variables) - Set(primary_root.name)
        sub_tree = [primary_root]
        if len(_vars) != 0: sub_tree.extend(get_subtree(primary_root, primary_root, _vars))
        sub_tree_set = Set(sub_tree)
        """
        print 'subtree is'
        for node in sub_tree:
            print node.name
            print node.values
        """
        sec_root = sub_tree[0]
        sub_tree_factors = [sec_root.marginals]
        sub_tree_factors.extend(get_subtree_factors(sec_root, sec_root))
        sub_tree_factors = factor_list

        """
        print 'sub_tree factors'
        for node in sub_tree_factors:
            print node.name
            print node.values
        """
        all_vars = Set()
        for fac in sub_tree_factors: all_vars |= Set(fac.name)
        return self.normalize(joint_ve_inference(all_vars, variables, sub_tree_factors))

    def conditional_inference(self, variable_1, variable_2):
        """
        Performs conditional inference, P(variable_1 | variable_2), in the junction tree and returns the conditional probability distribution as a list.
        """
        # Exploit the joint_inference and marginal_inference methods !
        return Utils.multiply_factors(self.joint_inference([variable_1, variable_2]), self.marginal_inference(variable_2), True)
