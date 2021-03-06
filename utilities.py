# File: utilities.py
# Author: Dennis Kovarik
# Purpose: Contains utility functions for the project.

import graphviz
import networkx as nx


def applySimpRules(regex):
    """
    Applies the following simplifying rules:
        r + \u2205 = r
        r\u2205 = \u2205
        \u2205* = \u03BB

    :param regex: The regular expression to apply the simplifying ruls to
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
        regex = applySimpRule2(regex)    
              
        # Remove redundant parentheses
        regex = simplifyPara(regex)

        # Apply simplifying rule (r + \u2205 = r)
        regex, stop = applySimpRule1(regex)       
        
        # Apply simplifying rule (\u2205* = \u03BB)
        regex = regex.replace('\u2205*', '\u03BB')
 
        # Remove redundant parentheses
        regex = simplifyPara(regex)

    return regex


def applySimpRule1(regex):
    """
    Applies the following simplifying rules:
        r + \u2205 = r

    :param regex: The regular expression to apply the simplifying ruls to
    :return: The simplified regex expression
    """
    stop = 1
    i = regex.find('\u2205')
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
        elif p > -1 and p < len(regex) - 1 and regex[:p] != '\u2205' \
        and regex[p+1:] == '\u2205':
            regex = regex[:p]            
            stop = 0
        elif p > -1 and p < len(regex) - 1 and regex[:p] == '\u2205' \
        and regex[p+1:] != '\u2205':
            regex = regex[p+1:]            
            stop = 0
        elif q > -1 and q < len(regex) - 1 and regex[0:q] != '\u2205' \
        and regex[q+1:] == '\u2205':
            regex = regex[:q]            
            stop = 0

    return regex, stop


def applySimpRule2(regex):
    """
    Applies the following simplifying rules:
        r\u2205 = \u2205

    :param regex: The regular expression to apply the simplifying ruls to
    :return: The simplified regex expression
    """
    i = regex.find('\u2205')
    pos1 = i + 1
    if i == -1:
        return regex
    
    s = i
    e = i
    pcs = 0
    pce = 0
            
    # Determine if in para
    inPara = inParentheses(regex, i)
                         
    # Parse string backwards
    while s > 0:
        if regex[s] == ')':
            pcs += 1
        elif regex[s] == '(' and pcs != 0:
            pcs -= 1
        elif regex[s] == '(' and pcs == 0:
            break
        elif regex[s] == '+' and pcs == 0:
            s += 1
            break
        s -= 1

    # Pase string forwards
    while e < len(regex):
        if regex[e] == '(':
            pce += 1
        elif regex[e] == ')' and pce != 0:
            pce -= 1
        elif regex[e] == ')' and pce == 0:
            break
        elif regex[e] == '+' and pce == 0:
            break
        e += 1

    if inPara > 0 and regex[s] == '(':
        s += 1
      
    regex = regex[:s] + '\u2205' + regex[e:]
    return regex


def combineEdges(G, p, q, k):
    """
    Modifies the label for the edge from p to q for the removal of node k. The
    new edge label will combine the regexp expressions from the edges that are 
    incident to the node being removed. 

    :param G: digraph object of the NFA to convert
    :param p: The start node G for the edge in consideration
    :param q: The end node in G for the edge in consideration
    :param k: The node being removed from the graph
    :return: The updated regular expression for the edge from p to q when 
             removing k
    """
    # Make sure the graph has more than 2 states
    if G.number_of_nodes() - 1 < 2:
        return ""

    # Find the necessary edges
    for e in G.edges():
        # Check for edge p -> q
        if e[0] == p and e[1] == q:
            rpq = G.get_edge_data(*e)['label']
        # Check for edge p -> k
        elif e[0] == p and e[1] == k:
            rpk = G.get_edge_data(*e)['label']
        # Check for edge k -> k
        elif e[0] == k and e[1] == k:
            rkk = G.get_edge_data(*e)['label']
        # Check for edge k -> q
        elif e[0] == k and e[1] == q:
            rkq = G.get_edge_data(*e)['label']
    
    newLabel = rpq + '+' + '(' + rpk + ')' + '(' + rkk + ')' + "*" + '(' + rkq +')'
    newLabel = simplifyRegexp(newLabel)
    return newLabel


def countNodes(G):
    """
    Counts the number of nodes in graph G.

    :param G: digraph object of the NFA to convert
    :return: The number of nodes in the graph
    """
    c = 0
    for i in G.nodes():
        if i != 'qi':
            c += 1
    return c


def cnrt2StateGTG2Regex(G, p, q):
    """
    Converts a graph with only 2 states to a regular expression

    :param G: digraph object of the NFA to convert
    :param p: The initial state for G
    :param q: The final state for G
    :return: The associated regular expression for G
    """
    # Make sure the graph has more than 2 states
    if G.number_of_nodes() - 1 > 2:
        return ""
    
    if p == q:
        for n in G.nodes():
            if n == p and n == q:
                pq = n
            else:
                k = n
        for e in G.edges():
            # Check for edge p -> p
            if e[0] == pq and e[1] == pq:
                rpp = G.get_edge_data(*e)['label']
            # Check for edge p -> k
            elif e[0] == pq and e[1] == k:
                rpk = G.get_edge_data(*e)['label']
            # Check for edge k -> p
            elif e[0] == k and e[1] == pq:
                rkp = G.get_edge_data(*e)['label']
            # Check for edge k -> k
            elif e[0] == k and e[1] == k:
                rkk = G.get_edge_data(*e)['label']

        newRegex = '(' + rpp + ')*' + '+' + '((' + rpk + ')' \
        + '(' + rkk + ')*' + '(' + rkp + '))*'
        newRegex = simplifyRegexp(newRegex)

        return '\u03BB+' + newRegex


    # Find the necessary edges
    for e in G.edges():
        # Check for edge p -> p
        if e[0] == p and e[1] == p:
            rii = G.get_edge_data(*e)['label']
        # Check for edge p -> q
        elif e[0] == p and e[1] == q:
            rij = G.get_edge_data(*e)['label']
        # Check for edge q -> q
        elif e[0] == q and e[1] == q:
            rjj = G.get_edge_data(*e)['label']
        # Check for edge q -> p
        elif e[0] == q and e[1] == p:
            rji = G.get_edge_data(*e)['label']

    regex = '(' + rii + ')*' + '(' + rij + ')(' + rjj + '+' + '(' + rji + ')' \
    + '(' + rii + ')*' + '(' + rij + ')' + ')*' 
    regex = simplifyRegexp(regex)
    return regex


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


def inParentheses(regex, i):
    """
    Determines if character at index i is inside a set of parentheses.

    :param regex: The regular expression
    :param i: The index of the reference character
    :return: 1 if character at index i is inside a set of parentheses
    :return: 0 otherwise
    """
    s = i
    e = i
    pcs = 0
    pce = 0
    inPara = 0

    # Determine if in parentheses
    while s >= 0:
        if regex[s] == ')':
            pcs += 1
        elif regex[s] == '(' and pcs != 0:
            pcs -= 1
        elif regex[s] == '(' and pcs == 0:
            while e < len(regex):
                if regex[e] == '(':
                    pce += 1
                elif regex[e] == ')' and pce != 0:
                    pce -= 1
                elif regex[e] == ')' and pce == 0:
                    inPara = 1
                    return 1
                e += 1
        s -= 1
    return 0


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


def nfa2Rex(G):
    """
    Converts an NFA to an equivalent regular expression.

    :param G: digraph object of the NFA to convert
    :return: An equivalent GTG to the NFA
    """
    p = getInitialState(G)
    q = getFinalState(G)

    G = nfa2Gtg(G)
    init = getInitialState(G)
    final = getFinalState(G)

    for k in sorted(G.nodes()):
        if k != 'qi' and k != init and k != final and G.number_of_nodes() > 3:
            nodes = set()
            edges = [] 
            for p in sorted(G.nodes()):
                for q in sorted(G.nodes()):
                    if p != 'qi' and q != 'qi' and p != k and q != k:
                        e = combineEdges(G, p, q, k)
                        nodes.add(p)
                        nodes.add(q)
                        edges.append([(p, q), e])
            
            # Remove k
            G.remove_node(k)
            edges2Remove = []
            for e in G.edges():
                if e[0] != 'qi':
                    edges2Remove.append(e)

            for edge in edges2Remove:
                G.remove_edge(*edge)
            for e in edges:
                G.add_edge(*e[0], label=e[1])
 
    rex = cnrt2StateGTG2Regex(G, init, final)
    return rex


def removeDupAdditions(subRegexp):
    """
    Removes duplicate additions from a regular expression to simplify it. This
    function serves as a helper function for simpAddition()

    :param subRegexp: Regular expretion to simplify
    :return: Simplified regular expression with duplicate additions removed
    """
    # Search for duplicate terms separated by +
    ops = set()
    i = 0
    plusI = -1
    plusJ = -1
    pc = 0
    exp = ''
    while i < len(subRegexp):
        if subRegexp[i] == '(':
            pc += 1
        elif subRegexp[i] == ')':
            pc -= 1

        if pc == 0 and subRegexp[i] == '+':
            if plusI == -1:
                ops.add(subRegexp[:i])
                plusI = i
                exp = exp + subRegexp[:i]
            elif plusI + 1 < len(subRegexp) and i > plusI:
                op = subRegexp[plusI+1:i]
                if not op in ops:
                    ops.add(op)
                    exp = exp + subRegexp[plusI:i]
                plusI = i
        i += 1

    if plusI == -1:
        ops.add(subRegexp[:i])
        plusI = i
        exp = exp + subRegexp[:i]
    else:
        op = subRegexp[plusI+1:i]
        if not op in ops:
            ops.add(op)
            exp = exp + subRegexp[plusI:i]
            plusI = i

    return exp


def showGraph(path):
    """
    Reads in a graph and displays it in pdf format.

    :param path: The filepath of the file containing the graph.
    """
    gv = graphviz.Source.from_file(path)
    gv.view()


def simpAddition(subRegexp):
    """
    Removes duplicate additions from a regular expression to simplify it.

    :param subRegexp: Regular expretion to simplify
    :return: Simplified regular expression with duplicate additions removed
    """
    pc = 0
    subRegexp = subRegexp.replace(' ', '')
    i = 0

    # search for terms enclosed by ()
    while i < len(subRegexp):
        if subRegexp[i] == '(':
            pc += 1
            j = i + 1
            while j < len(subRegexp):
                if subRegexp[j] == '(':
                    pc += 1
                elif subRegexp[j] == ')':
                    pc -= 1
                    if pc == 0:
                        subRegexp = subRegexp[:i+1] + removeDupAdditions(subRegexp[i+1:j]) + subRegexp[j:]
                j += 1
        i += 1
        
    subRegexp = removeDupAdditions(subRegexp)
    
    return subRegexp


def simplifyPara(simPara):
    """
    Removes redundant parentheses from a regular expression..

    :param simPara: Regular expretion to simplify
    :return: Simplified regular expression with redundant parentheses removed
    """
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
                elif pc == 0 and j < len(simPara) and simPara[j] == ')':
                    j = len(simPara)
                
                if pc > 0 and simPara[j] == ')':
                    pc -= 1

                j += 1
        i += 1
    return simPara


def simplifyRegexp(regexp):
    """
    Simplifies a regular expression by applying simplifying rules to it in
    addition to removing redundant parentheses and additions.

    :param regexp: Regular expretion to simplify
    :return: Simplified regular expression with duplicate additions removed
    """
    # Remove redundant addition
    stop = 0
    numPara = 0
    while stop == 0:
        stop = 1
        # Remove whitespace
        regexp = regexp.replace(' ', '')
        # Remove redundant stars
        regexp = regexp.replace("**", "*")

        regexp = simplifyPara(regexp)
        regexp = applySimpRules(regexp)
            
        # Remove lambda
        regexp = regexp.replace('\u03BB', '') 

        # Remove '+' at beginning
        if len(regexp) > 0 and regexp[0] == '+':
            regexp = regexp[1:]

        # Remove '+' at end
        if len(regexp) > 0 and regexp[len(regexp)-1] == '+':
            regexp = regexp[:(len(regexp)-1)]

        regexp = simplifyPara(regexp)

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

    # Check is regexp is empty
    if regexp == '':
        regexp = '\u03BB'
        
    # Remove whitespace
    regexp = regexp.replace(' ', '')

    return regexp
