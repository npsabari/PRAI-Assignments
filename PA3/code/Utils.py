"""
Author: Santhosh Kumar M (CS09B042)
File: Utils.py
"""

import re
from Factor import Factor
from Message import Message
from Clique import Clique
from Junction_Tree import Junction_Tree
from sets import Set

def moralize_graph(input_file):
    """
    Performs moralization of the given graph if directed and returns the list of Factor objects (factors).
    """

    # Performs some crazy file reads and gets the values correct
    lines = list()
    with open(input_file, 'r') as infile:
        # Assuming the table details starts from the fourth non-empty line
        lines = [line.strip() for line in infile if len(line.strip()) != 0][4:]
    list_of_factors, idx = list(), 0
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
        else:
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
    Returns the list of Factor() objects (factors) and the list of random variables, say, variables = ['A', 'C', 'B'], in the given graph.
    """
    list_of_factors = moralize_graph(input_file)
    list_of_variables= [fac.name[-1] for fac in list_of_factors]
    """
    for fac in list_of_factors:
        print fac.name
        print fac.values
    """
    return [list_of_factors, list_of_variables]

def factors_to_cliques(factors):
    """
    Simply creates a Clique() object for every given Factor() object and returns the list of Clique() objects.
    """
    return [Clique(fac.name, fac.values[:], []) for fac in factors]

def is_tree(factors):
    """
    Checks whether the given graph is a tree and returns true (or false) respectively.
    """
    # If a factor has more than 2 parents then it will be moralized to a cycle.
    # This is both necessary and sufficient condition for checking tree
    for fac in factors:
        if len(fac.name) > 2: return False
    return True

def compute_neighbours(cliques):
    """
    Computes the neighbours of each clique and returns the neighbours dictionary.
    For example,
    cliques = [clique_1, clique_2, clique_3] wherein clique_1.name = 'AB', clique_2.name = 'BDE', clique_3.name = 'AC'
    neighbours = {clique_1 : [clique_2, clique_3], clique_2 : [clique_1], clique_3 : [clique_1]}
    """

    # Computes the neighborhood matrix in O(n*max_name_size)

    var_map_dict = dict()
    for cliq in cliques:
        for var in cliq.name:
            if var_map_dict.has_key(var): var_map_dict[var].append(cliq)
            else: var_map_dict[var] = [cliq]
    neigh_dict = dict()
    for cliq in cliques:
        neigh_set = Set()
        for var in cliq.name: neigh_set |= Set(var_map_dict[var])
        neigh_set.remove(cliq)
        neigh_dict[cliq] = list(neigh_set)
    return neigh_dict

def get_elimination_ordering(variables, query_variables, factors = list()):
    """
    Returns an elimination ordering of the random variables after removing the query variables as a list.
    For example, if random variables are 'B', 'C', 'A' and query variable is 'B', then one elimination order is ['C', 'A'].
    """
    # Simple heuristic of ordering the variables in the increasing order of
    # number of factors being affected by the given variable
    to_ret = list(Set(variables) - Set(query_variables))
    count_fac_list = {var: 0 for var in to_ret}
    for i, var in enumerate(to_ret):
        for fac in factors:
            if var in fac.name:
                count_fac_list[var] += 1
    def compare(var_1, var_2):
        return count_fac_list[var_1] - count_fac_list[var_2]
    return sorted(to_ret, cmp=compare)

def multiply_factors(factor_1, factor_2, override=False):
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

    fac = Clique(my_name, my_val, [], None)
    """
    print 'After multiplication'
    print fac.name, fac.values
    fac = normalize(fac)
    print 'After Normalization'
    print fac.name, fac.values
    """
    return fac

def get_max_cliques(factors, elimination_order):
    """
    Given the elimination order, use node elimination to return a list of maximal elimination cliques.
    """

    # Get the list of all cliques generated during VE
    all_cliques = Set()
    list_of_factors = Set([fac.name for fac in factors])
    for elem in elimination_order:
        clique_name_set = Set()
        fac_accounted = Set()
        for fac in list_of_factors:
            if elem in fac:
                clique_name_set |= Set(fac)
                fac_accounted.add(fac)
        if len(clique_name_set) == 0: assert(False)
        clique_name = ''.join(list(clique_name_set))
        all_cliques.add(clique_name)
        clique_name = ''.join(list(Set(clique_name) - Set([elem])))
        list_of_factors -= fac_accounted
        list_of_factors.add(clique_name)

    """
    print 'after VE ordering, cliques are '
    for cliq in all_cliques: print cliq
    """

    # Removing cliques which are subsets of others
    max_cliques = Set()
    for fac in all_cliques:
        present = False
        for fac1 in (all_cliques - Set([fac])):
            if Set(fac1) >= Set(fac):
                present = True
                break
        if not present:
            max_cliques.add(fac)

    """
    print 'after removing subsets, cliques are '
    for cliq in max_cliques: print cliq
    """

    # Assign factors to the max_cliques generated, such that each factor is
    # assigned only once and each clique has at-least one factor
    max_cliques_ret = [Clique(cliq, [], []) for cliq in max_cliques]
    factors_to_assign = Set(factors)
    for i,cliq in enumerate(max_cliques_ret):
        factors_assigned = Set()
        for fac in factors_to_assign:
            if Set(cliq.name) >= Set(fac.name):
                factors_assigned.add(fac)
                max_cliques_ret[i].factors.append(fac)
        factors_to_assign -= factors_assigned

    """
    print 'after assigning factors'
    for cliq in max_cliques_ret:
        print 'for clique '+cliq.name
        for fac in cliq.factors:
            print fac.name

    """

    # Compute the values and adjust the clique name to be consistent with
    # values array for it be used in inference functions
    for cliq in max_cliques_ret:
        assert(len(cliq.factors) > 0)
        multiplied_facs = cliq.factors[0]
        for facs in cliq.factors[1:]: multiplied_facs = multiply_factors(multiplied_facs, facs)
        cliq.name = multiplied_facs.name
        cliq.values = multiplied_facs.values
    return max_cliques_ret

def get_junction_tree(max_cliques):
    """
    From the given maximal elimination cliques (nodes), compute maximum weight spanning tree.
    Return a Junction_Tree() object with nodes as cliques and edges as neighbours of each clique corresponding to the computed maximum weight spanning tree.
    """

    # Making the mapping for name to clique
    name_map = {cliq.name: cliq for cliq in max_cliques}

    # Variables for Disjoint sets
    parent_map = {cliq.name: cliq.name for cliq in max_cliques}
    rank_map = {cliq.name: 0 for cliq in max_cliques}

    # Functions for disjoint sets ( I like this DS ! )
    # Time complexity: O(inv_ack(n))
    def parent(key):
        if parent_map[key] == key:
            return key
        parent_map[key] = parent(parent_map[key])
        return parent_map[key]

    def link(key1, key2):
        par1, par2 = parent(key1), parent(key2)
        if par1 == par2: return False
        if rank_map[par1] > rank_map[par2]: parent_map[par2] = par1
        elif rank_map[par2] > rank_map[par1]: parent_map[par1] = par2
        else: parent_map[par2], rank_map[par1] = par1, rank_map[par1]+1
        return True

    neigh_dict = compute_neighbours(max_cliques)

    # Making vertex set
    vertices = name_map.keys()
    # Making edge set
    edges = Set()
    for u in neigh_dict:
        for v in neigh_dict[u]:
            edge_wt = len(Set(u.name) & Set(v.name))
            assert(edge_wt < len(u.name) and edge_wt < len(v.name))
            if edge_wt > 0: edges.add((edge_wt, u.name, v.name))

    # For sorting in decreasing order
    def compare(edge1, edge2):
        return edge2[0] - edge1[0]
    edges = sorted(edges, cmp=compare)

    # Doing kruskal Algorithm using Disjoint Sets
    max_spanning_tree_edges = list()

    # Simple three line MST algorithm !
    for edge in edges:
        u, v = edge[1], edge[2]
        if link(u, v): max_spanning_tree_edges.append(edge)

    # Constructing modified neighborhood matrix for the JT
    neigh_dict = {cliq: [] for cliq in max_cliques}
    for edge in max_spanning_tree_edges:
        neigh_dict[name_map[edge[1]]].append(name_map[edge[2]])
        neigh_dict[name_map[edge[2]]].append(name_map[edge[1]])
    return Junction_Tree(max_cliques, neigh_dict)
