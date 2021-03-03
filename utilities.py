# Contains utility functions for the project.

import graphviz
import networkx as nx


def applySimpRules(regex):
    """
    Applies the following simplifying rules:
        r + \u2205 = r
        r\u2205 = \u2205
        \u2205* = \u03BB

    :param operand1: regex for operand 1
    :param operand2: regex for operand 2
    :param op: The operation for the expression
    :return: The simplified regex expression
    """
    # Remove whitespace
    regex = regex.replace(' ', '')

    stop = 0
    pos1 = 0
    pos2 = 0
    while stop == 0:
        stop = 1
        # Remove redundant parentheses
        regex = simplifyPara(regex)

        # Apply simplifying rule (\u2205* = \u03BB)
        regex = regex.replace('\u2205*', '\u03BB')

        # Apply simplifying rule (r\u2205 = \u2205)
        i = regex.find('\u2205', pos1)
        pos1 = i + 1
        if i > -1:
            p = regex.find('+', i)
            k = regex.find(')', i)
            if p > -1 and k > -1 and k < p:
                p = k
            q = regex.rfind('+', 0, i)
            k = regex.rfind('(', 0, i)
            r = regex.rfind(')', k, i)
            if k > -1 and r == -1 and k > q:
                q = k
            if p > -1 and q > -1:            
                regex = regex[:q+1] + '\u2205' + regex[p:]
                stop = 0
            elif q > -1:
                regex = regex[:q+1] + '\u2205'
                stop = 0
            elif p > -1:
                regex = '\u2205' + regex[p:]
                stop = 0
            else:
                regex = '\u2205'
        
                stop = 0
        # Remove redundant parentheses
        regex = simplifyPara(regex)

        # Apply simplifying rule (r + \u2205 = r)
        i = regex.find('\u2205', pos2)
        pos2 = i
        p = regex.find('+', i)
        k = regex.find(')', i)
        r = regex.find('(', i, k)
        if k > -1 and r == -1 and k < p:
            p = k
        q = regex.rfind('+', 0, i)
        k = regex.rfind('(', 0, i)
        r = regex.rfind(')', k, i)
        if k > -1 and r == -1 and k > q:
            q = k
        if i > -1 and (p > -1 or q > -1):
            if p > -1 and q > -1 and regex[q+1:p] == '\u2205':
                if regex[q] != '+' and regex[p] == '+':
                    p = p + 1
                    q = q + 1
                regex = regex[:q] + regex[p:]
                stop = 0
            elif p > -1 and p < len(regex) - 1 and regex[:p] != '\u2205' and regex[p+1:] == '\u2205':
                regex = regex[:p]            
                stop = 0
            elif q > -1 and q < len(regex) - 1 and regex[0:q] != '\u2205' and regex[q+1:] == '\u2205':
                regex = regex[:q]            
                stop = 0
        
        # Remove redundant parentheses
        regex = simplifyPara(regex)

    return regex


def combineEdges(G, p, q, k):
    """
    Modifies the label for the edge from p to q for the removal of node k. The
    new edge label will combine the regexp expressions from the edges that are 
    incident to the node being removed. 

    :param p: The start node G for the edge in consideration
    :param q: The end node in G for the edge in consideration
    :param k: The node being removed from the graph
    :return: The updated regular expression for the edge from p to q when 
             removing k
    """
    # Find the necessary edges
    for e in G.edges():
        # Check for edge p -> q
        if e[0] == p and e[1] == q:
            rpq = G.get_edge_data(*e)['label']
        elif e[0] == p and e[1] == k:
            rpk = G.get_edge_data(*e)['label']
        elif e[0] == k and e[1] == k:
            rkk = G.get_edge_data(*e)['label']
        elif e[0] == k and e[1] == q:
            rkq = G.get_edge_data(*e)['label']
    
    newLabel = simplifyRegexp(rpq + "+" + rpk + rkk + "*" + rkq)
    return newLabel


def getFinalState(G):
    """
    Returns the  node of graph G.
    
    :param G: digraph object of the NFA to convert
    :return: The final state of graph G
    """
    attributes = nx.get_node_attributes(G, 'shape')
    for key in attributes:
        if attributes[key] == "doublecircle":
            return key
    
    print("Error: Final state not found")
    print("Final state is expected to have the doublecircle attribute.")
    
    return "Start Node Not Found"


def getInitialState(G):
    """
    Returns the start node of graph G.
    
    :param G: digraph object of the NFA to convert
    :return: The initial state of graph G
    """
    for n in G.edges():
        if n[0] == 'qi':
            return n[1]
    
    print("Error: Initial state not found")
    print("Initial state is expected to be neighbors with node 'qi'.")
    
    return "Start Node Not Found"


def getNumTerms(exp):
    """
    Returns the number of terms inside a string. Is mainly used to determine 
    the number of terms present inside a set of parentheses.

    :param exp: A regular expression as a string
    :return: The number of terms in exp
    """
    numTerms = 0
    # Count the number of terms
    for char in exp:
        if char != ' ' and char != '*' and char != '(' and char != ')' \
        and char != '+':
            numTerms += 1

    return numTerms


def infix2Postfix(regex):
    """
    Converts a regex from infix to postfix.
    
    :param regex: Regular expression in infix notation.
    :return: The regex in postfix notation.
    """
    output = ''
    ops = []
    i = 0
    # Parse the string
    while i < len(regex):
        if isOp(regex[i]):
            op = regex[i]
            if regex[i] == '(':
                ops.append(regex[i])
            elif regex[i] == ')':
                while len(ops) > 0 and ops[len(ops)-1] != '(':
                    output += ops.pop(len(ops)-1)
                ops.pop(len(ops)-1)
                # check for concatenation
                if i < len(regex) - 1 and not isOp(regex[i+1]):
                    ops.append('.')
            else:
                while len(ops) > 0 and not isHigherPriority(op, ops[len(ops)-1]) \
                and ops[len(ops)-1] != '(' and ops[len(ops)-1] != ')':
                    output += ops.pop(len(ops)-1)
                ops.append(op)
        # Check of . operation
        elif i < len(regex) - 1 and not isOp(regex[i+1]):
            while len(ops) > 0 and not isHigherPriority('.', ops[len(ops)-1]) \
            and ops[len(ops)-1] != '(' and ops[len(ops)-1] != ')':
                output += ops.pop(len(ops)-1)
            output += regex[i]
            ops.append('.')
        else:
            output += regex[i]
        i += 1

    # Pop all the operators
    while len(ops) > 0:
        output += ops.pop(len(ops)-1)

    return output


def isHigherPriority(op1, op2):
    """
    Determines if op1 has a lower priority than op2.

    :param op1: Operation 1
    :param op2: Operation 2
    :return: True if op1 has lower priority than op2
    :return: False otherwise
    """
    if op1 == '.' and op2 == '+':
        return True
    elif op1 == '*' and op2 == '+':
        return True
    elif op1 == '*.' and op2 == '+':
        return True
    elif op1 == '*+' and op2 == '+':
        return True

    return False


def isOp(char):
    """
    Determines if a character is an op or not.

    :param char: Character to determine if an op or not.
    :return: True if char is an op
    :return: False if char is not an op
    """
    if char == '+':
        return True
    elif char == '*':
        return True
    elif char == '.':
        return True
    elif char == '*.':
        return True
    elif char == '*+':
        return True
    elif char == '(':
        return True
    elif char == ')':
        return True
    return False


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


def showGraph(path):
    """
    Reads in a graph and displays it in pdf format.

    :param path: The filepath of the file containing the graph.
    """
    gv = graphviz.Source.from_file(path)
    gv.view()


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

    # Remove whitespace
    simPara = simPara.replace(' ', '')
   
    # Removed all unnecessary ( from string
    preOps = 2
    while i < len(simPara):
        if simPara[i] == '+':
            preOps = 1
        elif i == 0 and simPara[i] == '(':
            preOps = 1
        elif i > 0 and simPara[i] == '(' and simPara[i-1] == '(':
            preOps = 1
        elif simPara[i] != '+' and simPara[i] != '(' and simPara[i] != ')':
            preOps = 2

        if simPara[i] == '(':
            pc = 0
            j = i + 1
            paraOps = 2
            while j < len(simPara):
                if simPara[j] == '(':
                    pc += 1
                elif pc > 0 and simPara[j] == ')':
                    pc -= 1
                elif simPara[j] == ')' and pc == 0:
                    lastOp = 2
                    if j == len(simPara) - 1 or simPara[j+1] == '+' or simPara[j+1] == ')':
                        lastOp = 1

                    charLen = getNumTerms(simPara[i+1:j])
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
                    elif j == len(simPara) - 1 and simPara.find('+', i) == -1:
                        # Remove ')'
                        simPara = simPara[:j]
                        # Remove '('
                        prefix = simPara[:i]
                        suffix = simPara[(i+1):]
                        simPara = prefix + suffix
                        i -= 1
                        j = len(simPara)
                    elif j + 1 < len(simPara) and simPara[j+1] != '*' and preOps <= paraOps and lastOp <= paraOps:
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
                    elif j == len(simPara) - 1 and preOps <= paraOps:
                        # Remove ')'
                        simPara = simPara[:j]
                        # Remove '('
                        prefix = simPara[:i]
                        suffix = simPara[(i+1):]
                        simPara = prefix + suffix
                        i -= 1
                        j = len(simPara)
                    

                if pc == 0 and j < len(simPara) and simPara[j] == '+':
                    paraOps = 1
                j += 1
        i += 1
    return simPara


def simplifyRegexp(regexp):
    """
    Simplifies a regular expression.
    """
    regexp = regexp.replace(' ', '')            # Remove whitespace
    # Remove redundant stars
    regexp = regexp.replace("**", "*")

    regexp = applySimpRules(regexp)
            
    # Remove lambda and phi
    regexp = regexp.replace('\u03BB', '')
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
    
    # Remove redundant stars
    while(regexp.find("**") != -1):
        regexp = regexp.replace("**", "*")

    return regexp
