# Contains utility functions for the project.

import graphviz
import networkx as nx


def nfa2Gtg(G):
    """
    Converts an NFA to an equivalent GTG.

    :param G: digraph object of the NFA to convert
    :return: An equivalent GTG to the NFA
    """

    # Create a set of known edges
    edges = {(0,0)}
    for i in sorted(G.edges()):
        edges.add(i)
   
    # Ensure there is an edge from every node to every other node 
    for n in sorted(nx.nodes(G)):
        for n2 in sorted(nx.nodes(G)):
            e = (n, n2)     # Create edge tuple
            # If no edge is already present, add one with label for phi
            if n != 'qi' and n2 != 'qi' and not (n, n2) in edges:
                G.add_edge(*e, label='\u2205')
            # Else convert the existing edge label to a regular expression
            else:
                if n != 'qi' and n2 != 'qi':
                    edgeLabel = G.get_edge_data(n, n2)
                    edgeLabel = edgeLabel.get("label")    
                    edgeLabel = edgeLabel.replace(",", "+")
                    G.add_edge(*e, label=edgeLabel)
    
    return G


def simpAddition(subRegexp):
    temp = subRegexp.split('+')
    ops = set()
    subRegexp = ''
    exp = ''
    for op in temp:
        if not op in ops:
            if exp != '':
                exp = exp + '+' + op
            else:
                exp = op
            ops.add(op)
    return exp


def simplifyPara(simPara):
    # Remove unnecessary parenthesis
    i = 0
    j = 0
    stop = 0
   
    # Removed all unnecessary ( from string
    while i < len(simPara):
        if simPara[i] == '(':
            pc = 0
            j = i + 1
            while j < len(simPara):
                if simPara[j] == '(':
                    pc += 1
                elif pc > 0 and simPara[j] == ')':
                    pc -= 1
                elif simPara[j] == ')' and pc == 0:
                    charLen = int(abs(j - i) - 1)
                    if charLen < 2:
                        # Remove ')'
                        prefix = simPara[:j]
                        suffix = simPara[(j+1):]
                        simPara = prefix + suffix
                        # Remove '('
                        prefix = simPara[:i]
                        suffix = simPara[(i+1):]
                        simPara = prefix + suffix
                        i -= 1
                        j = len(simPara)
                    elif j == len(simPara) - 1:
                        # Remove ')'
                        simPara = simPara[:j]
                        # Remove '('
                        prefix = simPara[:i]
                        suffix = simPara[(i+1):]
                        simPara = prefix + suffix
                        i -= 1
                        j = len(simPara)
                    elif j + 1 < len(simPara) and simPara[j+1] != '*' and simPara.find('+', i, j) == -1:
                        # Remove ')'
                        prefix = simPara[:j]
                        suffix = simPara[(j+1):]
                        simPara = prefix + suffix
                        # Remove '('
                        prefix = simPara[:i]
                        suffix = simPara[(i+1):]
                        simPara = prefix + suffix
                        i -= 1
                        j = len(simPara)
                j += 1
        i += 1
    return simPara


def simplifyRegexp(regexp):
    """
    Simplifies a regular expression.
    """
    regexp = regexp.replace(' ', '')            # Remove whitespace
    regexp = regexp.replace('\u2205*', '')
    regexp = regexp.replace('\u2205', '')

    # Remove '+' at beginning
    if len(regexp) > 0 and regexp[0] == '+':
        regexp = regexp[1:]

    # Remove '+' at end
    if len(regexp) > 0 and regexp[len(regexp)-1] == '+':
        regexp = regexp[:(len(regexp)-1)]

    regexp = simplifyPara(regexp)

    # Remove redundant addition

    stop = 0
    numPara = 0
    while stop == 0:
        stop = 1
        i = 0
        while i < len(regexp):
            if regexp[i] == '(':
                c = 0
                j = 0
                while j < len(regexp) and j < len(regexp):
                    if regexp[j] == ')' and c == numPara:
                        stop = 0
                        subRegexp = regexp[i+1:j]
                        subRegexp = simpAddition(subRegexp)
                        regexp = regexp[:i+1] + subRegexp + regexp[j:] 
                    else:
                        c += 1
                    j += 1
            i += 1
        numPara += 1               
    regexp = simpAddition(regexp)
    return regexp
