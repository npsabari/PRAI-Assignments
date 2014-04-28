"""
Author: Santhosh Kumar M (CS09B042)
File: Undirected_Graphical_Model.py
"""

from Factor import Factor
from Node import Node
from Message import Message

from sets import Set

class Undirected_Graphical_Model():
    """
    Class to construct an undirected graphical model (UGM) and perform exact inference (variable elimination) on it.
    """

    def __init__(self, factors, nodes):
        """
        Initializes the UGM with the given factors list and nodes list.
        """
        self.factors = factors
        self.nodes = nodes

    def is_chain(self):
        """
        Checks whether the given graph is a chain and returns true (or false) respectively.
        """
        # Necessary and Sufficient Condition for a list of factors to be a chain
        # 1. Exactly one factors should be made up of only one variable
        # 2. Rest of the factors should be made up of two variables
        # 3. The graph is connected

        end_factors, rest_factors = Set(), Set()
        for fac in self.factors:
            if len(fac.name) == 1: end_factors.add(fac)
            elif len(fac.name) == 2: rest_factors.add(fac)
            else:
                #print len(fac.name)
                return False

        #print len(end_factors)
        if len(end_factors) != 1: return False

        # Take any end point and generate the ordering using dfs
        end_factors = list(end_factors)
        my_factor_list = list(end_factors)
        search_var = end_factors[0].name
        node_store = list(search_var)

        # search_var is the variable shared over the edges in the dfs
        while len(rest_factors) > 0:
            candidate_factors = Set()
            for fac in rest_factors:
                if fac.name.count(search_var) == 0: continue
                elif fac.name.count(search_var) > 1: return False
                else: candidate_factors.add(fac)
            if len(candidate_factors) != 1: return False
            candidate = list(candidate_factors)[0]
            my_factor_list.append(candidate)
            if candidate.name[0] == search_var: search_var = candidate.name[1]
            elif candidate.name[1] == search_var: search_var = candidate.name[0]
            else: return False
            rest_factors -= candidate_factors
            node_store.append(search_var)

        if len(my_factor_list) != len(self.factors): return False
        self.factors = my_factor_list

        """
        print 'After is_chain'
        for fac in self.factors:
            print fac.name
            print fac.values
        for node in self.nodes:
            print node.name
        """
        self.nodes = [Node(node_name) for node_name in node_store]
        return True

    def normalize(self, factor):
        """
        Normalizes the values corresponding to the given factor and returns the normalized factor.
        """
        try:
            tmp_values = [val/sum(factor.values) for val in factor.values]
            factor.values = tmp_values
        except ZeroDivisionError:
            print ' :-o Zero probability'
        return factor


    def multiply_factors(self, factor_1, factor_2, override=False):
        """
        Multiplies the given two factors and returns the resultant factor.
        """
        """
        print 'multiplying factors '
        print factor_1.name, factor_1.values
        print factor_2.name, factor_2.values
        """
        # Does P(X) * P(Y) depending on the variable common between X and Y
        # Construct the factor 'name' from X and Y and iterate over all possible
        # values of the factor 'name' similar to truth table and multiply the
        # values of P(X) and P(Y) for the corresponding values of X and Y
        my_name = factor_1.name
        for var in factor_2.name:
            if var not in my_name: my_name += var
        #print my_name
        my_val = [0 for i in range(1<<len(my_name))]

        pos_1 = {i : len(factor_1.name)-factor_1.name.index(i)-1 for i in my_name if i in factor_1.name}
        pos_2 = {i : len(factor_2.name)-factor_2.name.index(i)-1 for i in my_name if i in factor_2.name}
        #print pos_1, pos_2

        mask = len(my_val) - 1
        tmp_sz = 0
        while tmp_sz < len(my_val):
            tmp_values = [((mask>>i)&1) for i in range(len(my_name)-1, -1, -1)]
            #print mask, tmp_values
            if not override:
                my_val[tmp_sz] = factor_1.values[sum([int(not tmp_values[i])*(1<<pos_1[my_name[i]]) for i in range(len(my_name)) if my_name[i] in factor_1.name])]
                my_val[tmp_sz] *= factor_2.values[sum([int(not tmp_values[i])*(1<<pos_2[my_name[i]]) for i in range(len(my_name)) if my_name[i] in factor_2.name])]
            else:
                try:
                    my_val[tmp_sz] = factor_1.values[sum([int(not tmp_values[i])*(1<<pos_1[my_name[i]]) for i in range(len(my_name)) if my_name[i] in factor_1.name])]
                    my_val[tmp_sz] /= factor_2.values[sum([int(not tmp_values[i])*(1<<pos_2[my_name[i]]) for i in range(len(my_name)) if my_name[i] in factor_2.name])]
                except ZeroDivisionError:
                    print 'Conditional probability is zero :-/'
            tmp_sz += 1
            mask -= 1

        fac = Factor(my_name, my_val)
        """
        print 'After multiplication'
        print fac.name, fac.values
        fac = self.normalize(fac)
        print 'After Normalization'
        print fac.name, fac.values
        """
        return fac

    def marginalize(self, factor, variable):
        """
        Marginalizes the given factor over the given variable and returns the marginalized factor.
        """
        """
        print 'Marginalizing'
        print factor.name, factor.values
        print 'Over variable '+variable
        """
        # Sum over all possible values of the variable in the given factor
        try:
            my_name = ''.join([i for i in factor.name if i != variable])
            my_val = [0 for i in range(1<<len(my_name))]
            mask = len(my_val)-1
            var_idx = len(factor.name)-factor.name.index(variable)-1
            tmp_sz = 0
            while mask >= 0:
                tmp_values = [((mask>>i)&1) for i in range(len(my_name)-1, -1, -1)]
                pos = [len(factor.name)-factor.name.index(i)-1 for i in my_name]
                my_val[tmp_sz] = factor.values[sum([int(not tmp_values[i])*(1<<pos[i]) for i in range(len(my_name))]) + (1<<var_idx)]
                my_val[tmp_sz] += factor.values[sum([int(not tmp_values[i])*(1<<pos[i]) for i in range(len(my_name))])]
                tmp_sz += 1
                mask -= 1
            return Factor(my_name, my_val)
        except ValueError:
            print 'Enter the function variables properly :-/'

    def get_elimination_ordering(self, query_variables):
        """
        Returns an elimination ordering of the random variables after removing the query variables as a list.
        For example, if random variables are 'B', 'C', 'A' and query variable is 'B', then one elimination order is ['C', 'A'].
        """
        # Simple heuristic of ordering the variables in the increasing order of
        # number of factors being affected by the given variable
        to_ret = list(Set([node.name for node in self.nodes]) - Set(query_variables))
        count_fac_list = [0 for i in range(len(to_ret))]
        for i, var in enumerate(to_ret):
            for fac in self.factors:
                if var in fac.name:
                    count_fac_list[i] += 1
        def compare(var_1, var_2):
            return count_fac_list[to_ret.index(var_1)] - count_fac_list[to_ret.index(var_2)]
        return sorted(to_ret, cmp=compare)

    def marginal_inference(self, variable):
        """
        Performs marginal inference, P(variable), on the UGM and returns the marginal probability distribution as a list.
        """
        # Choose the variable 'x' to eliminate and select the factors from Set
        # S that contain that variable 'x' and multiply them and marginalize over
        # 'x' and add the resultant factor to S.
        # Repeat for all variables to be eliminated
        # Multiply all the factors in S and return the result
        elimination_order = self.get_elimination_ordering(variable)
        list_of_factors = Set(self.factors)
        for elem in elimination_order:
            facs_to_multiply = list()
            for fac in list_of_factors:
                if elem in fac.name:
                    facs_to_multiply.append(fac)

            if len(facs_to_multiply) == 0: assert(False)
            res = facs_to_multiply[0]
            for i in range(1, len(facs_to_multiply)):
                res = self.multiply_factors(res, facs_to_multiply[i])
            res = self.marginalize(res, elem)
            list_of_factors -= Set(facs_to_multiply)
            list_of_factors.add(res)

        list_of_factors = list(list_of_factors)
        assert(len(list_of_factors) > 0 and list_of_factors[0].name == variable)
        ret_fac = list_of_factors[0]
        for i in range(1, len(list_of_factors)):
            assert(list_of_factors[i].name == variable)
            ret_fac = self.multiply_factors(ret_fac, list_of_factors[i])
        return self.normalize(ret_fac)

    def joint_inference(self, variable_1, variable_2):
        """
        Performs joint inference, P(variable_1, variable_2), on the UGM and returns the joint probability distribution as a list.
        """
        # Procedure is same as above except that we consider two variables to
        # be marginalized
        elimination_order = self.get_elimination_ordering([variable_1, variable_2])
        list_of_factors = Set(self.factors)
        for elem in elimination_order:
            facs_to_multiply = list()
            for fac in list_of_factors:
                if elem in fac.name:
                    facs_to_multiply.append(fac)

            if len(facs_to_multiply) == 0: assert(False)
            res = facs_to_multiply[0]
            for i in range(1, len(facs_to_multiply)):
                res = self.multiply_factors(res, facs_to_multiply[i])
            res = self.marginalize(res, elem)
            list_of_factors -= Set(facs_to_multiply)
            list_of_factors.add(res)

        list_of_factors = list(list_of_factors)
        assert(len(list_of_factors) > 0 and (len(list_of_factors[0].name) >= 1 or variable_1 in list_of_factors[0].name and variable_2 in list_of_factors[0].name))
        ret_fac = list_of_factors[0]
        for i in range(1, len(list_of_factors)):
            assert(len(list_of_factors[i].name) >= 1 and (variable_1 in list_of_factors[i].name or variable_2 in list_of_factors[i].name))
            ret_fac = self.multiply_factors(ret_fac, list_of_factors[i])
        return self.normalize(ret_fac)

    def conditional_inference(self, variable_1, variable_2):
        """
        Performs conditional inference, P(variable_1 | variable_2), on the UGM and returns the conditional probability distribution as a list.
        """
        # Using conditional probability formula
        return self.multiply_factors(self.joint_inference(variable_1, variable_2), self.marginal_inference(variable_2), True)

    def forward_message_pass(self):
        """
        Performs forward message passing and fills the alpha message vector of all nodes.
        """
        # Assuming that is_chain() is called before using this function
        # Using the DP alpha[i] = factor(i)*alpha[i-1]
        for i, tmp_node in enumerate(self.nodes):
            if i == 0: tmp_node.alpha_message = Message(self.factors[0].values)
            else:
                cheat_fac = Factor(self.nodes[i-1].name,  self.nodes[i-1].alpha_message.message_vector)
                tmp_node.alpha_message = Message(self.marginalize(self.multiply_factors(self.factors[i], cheat_fac), self.nodes[i-1].name).values)
        """
        print 'Printing Alpha'
        for tmp_node in self.nodes:
            print tmp_node.name, tmp_node.alpha_message.message_vector
        """

    def backward_message_pass(self):
        """
        Performs backward message passing and fills the beta message vector of all nodes.
        """
        """
        print len(self.factors), len(self.nodes)
        """
        # Assuming that is_chain() is called before using this function
        # Using the DP beta[i] = factor(i)*alpha[i+1]
        for i, tmp_node in enumerate(self.nodes[::-1]):
            idx = len(self.nodes)-1-i
            if i == 0: tmp_node.beta_message = Message([1, 1])
            else:
                cheat_fac = Factor(self.nodes[idx+1].name, self.nodes[idx+1].beta_message.message_vector)
                tmp_node.beta_message = Message(self.marginalize(self.multiply_factors(self.factors[idx+1], cheat_fac), self.nodes[idx+1].name).values)
        """
        print 'Printing Beta'
        for tmp_node in self.nodes:
            print tmp_node.name, tmp_node.beta_message.message_vector
        """

    def chain_marginal_inference(self, variable):
        """
        Performs marginal inference, P(variable), on the chain by message passing and returns the marginal probability distribution as a list.
        """
        # P(A) = 1/Z * alpha(A) * beta(A)
        for node in self.nodes:
            if node.name == variable:
                cheat_fac1 = Factor(node.name, node.alpha_message.message_vector)
                cheat_fac2 = Factor(node.name, node.beta_message.message_vector)
                return self.normalize(self.multiply_factors(cheat_fac1, cheat_fac2))
        assert(False)

    def chain_consecutive_joint_inference(self, variable_1, variable_2):
        """
        Performs joint inference on the given consecutive nodes, P(variable_1, variable_2), on the chain by message passing and returns the joint probability distribution as a list.
        """
        # P(A, B) = 1/Z * alpha(A) * factor(A, B) * beta(B)
        return self.normalize(self.chain_non_consecutive_joint_inference(variable_1, variable_2))

    def chain_non_consecutive_joint_inference(self, variable_1, variable_2):
        """
        Performs joint inference on the given non-consecutive nodes, P(variable_1, variable_2), on the chain by message passing and returns the joint probability distribution as a list.
        """
        # P(A, B) = marginalize(1/Z * alpha(A) * factor(A, x1) * ... *
        # factor(xn, B) * beta(B)) over x1 to xn
        idx_1, idx_2 = -1, -1
        for i, node in enumerate(self.nodes):
            if idx_1 == -1 and node.name == variable_1: idx_1 = i
            if idx_2 == -1 and node.name == variable_2: idx_2 = i
        #print 'indices are %d %d' % (idx_1, idx_2)
        assert(idx_1 != -1 and idx_2 != -1)
        fac = Factor(self.factors[idx_1+1].name, self.factors[idx_1+1].values[:])
        for i in range(idx_1+2, idx_2+1): fac = self.multiply_factors(fac, self.factors[i])
        for i in range(idx_1+1, idx_2): fac = self.marginalize(fac, self.nodes[i].name)

        cheat_fac1 = Factor(self.nodes[idx_1].name, self.nodes[idx_1].alpha_message.message_vector)
        cheat_fac2 = Factor(self.nodes[idx_2].name, self.nodes[idx_2].beta_message.message_vector)
        return self.normalize(self.multiply_factors(self.multiply_factors(cheat_fac1, cheat_fac2), fac))

    def chain_conditional_inference(self, variable_1, variable_2):
        """
        Performs conditional inference, P(variable_1 | variable_2), on the chain by message passing and returns the conditional probability distribution as a list.
        """
        # using conditional probability formula
        for i, node in enumerate(self.nodes):
            if i == len(self.nodes)-1: break
            if (node.name == variable_1 and self.nodes[i+1].name == variable_2) or (node.name == variable_2 and self.nodes[i+1].name == variable_1):
                return self.multiply_factors(self.chain_consecutive_joint_inference(variable_1, variable_2), self.chain_marginal_inference(variable_2), True)
        return self.multiply_factors(self.chain_non_consecutive_joint_inference(variable_1, variable_2), self.chain_marginal_inference(variable_2), True)
