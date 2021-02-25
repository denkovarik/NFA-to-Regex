# This file runs tests for project
#
# Usage:
#   python3 runTests.py


import io
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
import unittest
from utilities import *
import graphviz
import networkx as nx
 
class executionTests(unittest.TestCase):
    def testExecution(self):
        """
        This function tests that the program is able to run and execute a 
        basic test. 
        """
        # Test Assert
        self.assertTrue(2 == 2)

    
class nfa2RexTests(unittest.TestCase):
    def testFunctionCall(self):
        """
        Tests ability to call the function nfa2Gtg
        """
        # Test Case 1 
        G = nx.DiGraph(nfaTest1) 
 
        # Convert to GTG
        GTG = nfa2Gtg(G)

        # Check that the nodes are equivalent
        for test, sol in zip(sorted(GTG), sorted(nfaSol1)):
            self.assertTrue(test == sol)

        # Check that the edges are equivalent
        for test, sol in zip(sorted(GTG.edges()), sorted(nfaSol1.edges())):
            self.assertTrue(test == sol)


        # Test Case 2
        G = nx.DiGraph(nfaTest2) 
 
        # Convert to GTG
        GTG = nfa2Gtg(G)

        # Check that the nodes are equivalent
        for test, sol in zip(sorted(GTG), sorted(nfaSol2)):
            self.assertTrue(test == sol)

        # Check that the edges are equivalent
        for test, sol in zip(sorted(GTG.edges()), sorted(nfaSol2.edges())):
            self.assertTrue(test == sol) 
    

    def testSimplifyRegexp(self):
        """
        This function tests 
        """
        # Test Case #1: Regexp with single char.
        test = 'a'
        sol = 'a'
        ans = simplifyRegexp(test)
        self.assertTrue(ans == sol)
 
        # Test Case #2: Regexp with just empty set.
        test = '\u2205'
        sol = ''
        ans = simplifyRegexp(test)
        self.assertTrue(ans == sol) 

        # Test Case #3: Regexp with 1 char concatenated with empty set
        test = 'a\u2205'
        sol = 'a'
        ans = simplifyRegexp(test)
        self.assertTrue(ans == sol) 
 
        # Test Case #4: Regexp with char concat to (empty set)*
        test = 'a\u2205*'
        sol = 'a'
        ans = simplifyRegexp(test)
        self.assertTrue(ans == sol) 
 
        # Test Case #5: Regexp with (empty set) + char
        test = '\u2205 + a'
        sol = 'a'
        ans = simplifyRegexp(test)
        self.assertTrue(ans == sol) 
 
        # Test Case #6: Regexp with (empty set) + char
        test = '\u2205 + a(bb)*a'
        sol = 'a(bb)*a'
        ans = simplifyRegexp(test)
        self.assertTrue(ans == sol) 
        
        # Test Case #7: Regexp with char + (empty set)
        test = 'a + \u2205'
        sol = 'a'
        ans = simplifyRegexp(test)
        self.assertTrue(ans == sol) 
 
        # Test Case #8: Regexp with (empty)*
        test = 'a\u2205*'
        sol = 'a'
        ans = simplifyRegexp(test)
        self.assertTrue(ans == sol) 
 
        # Test Case #9: Regexp with 'empty +' and 'empty*'
        test = '\u2205 + a\u2205*a'
        sol = 'aa'
        ans = simplifyRegexp(test)
        self.assertTrue(ans == sol) 
 
        # Test Case #10: Regexp with unnecessary parenthesis
        test = '(a)'
        sol = 'a'
        ans = simplifyRegexp(test)
        self.assertTrue(ans == sol) 
        
        # Test Case #10: Regexp with multiple unnecessary parenthesis
        test = '(a)(b)'
        sol = 'ab'
        ans = simplifyRegexp(test)
        self.assertTrue(ans == sol) 
        
        # Test Case #10: Regexp with unnecessary followed by unnecessary parenthesis
        test = '(a)*(b)'
        sol = 'a*b'
        ans = simplifyRegexp(test)
        self.assertTrue(ans == sol) 
        
        # Test Case #11
        test = '(a)*(ba)'
        sol = 'a*ba'
        ans = simplifyRegexp(test)
        self.assertTrue(ans == sol) 
        
        # Test Case #12
        test = '(ab)*(b)'
        sol = '(ab)*b'
        ans = simplifyRegexp(test)
        self.assertTrue(ans == sol) 
        
        # Test Case #13
        test = '(ab)*(a)'
        sol = '(ab)*a'
        ans = simplifyRegexp(test)
        self.assertTrue(ans == sol) 
        
        # Test Case #14
        test = '(ab)*(a)*'
        sol = '(ab)*a*'
        ans = simplifyRegexp(test)
        self.assertTrue(ans == sol) 
        
        # Test Case #14
        test = '(ab* + (a+bb)* + (ab))*(a)*'
        sol = '(ab*+(a+bb)*+ab)*a*'
        ans = simplifyRegexp(test)
        self.assertTrue(ans == sol) 
        
        # Test Case #15
        test = '(ab* + (a+bb)* + (ab))(a)*'
        sol = '(ab*+(a+bb)*+ab)a*'
        ans = simplifyRegexp(test)
        self.assertTrue(ans == sol) 
        
        # Test Case #16
        test = '(ab* + a+bb + (ab))(a)*'
        sol = '(ab*+a+bb+ab)a*'
        ans = simplifyRegexp(test)
        self.assertTrue(ans == sol) 
        
        # Test Case #17
        test = '(ab*abb(ab))(a)*'
        sol = 'ab*abbaba*'
        ans = simplifyRegexp(test)
        self.assertTrue(ans == sol) 
        
        # Test Case #18
        test = '((ab)*abb(ab))(a)*'
        sol = '(ab)*abbaba*'
        ans = simplifyRegexp(test)
        self.assertTrue(ans == sol) 
        
        # Test Case #19: Redundant addition
        test = 'a + a'
        sol = 'a'
        ans = simplifyRegexp(test)
        self.assertTrue(ans == sol) 
        
        # Test Case #20: Redundant addition
        test = '(a + a)'
        sol = 'a'
        ans = simplifyRegexp(test)
        self.assertTrue(ans == sol) 
        
        # Test Case #21: Redundant addition
        test = '(ab)* + (ab)*'
        sol = '(ab)*'
        ans = simplifyRegexp(test)
        self.assertTrue(ans == sol) 


if __name__ == '__main__':
    # Read in the test nfa
    filepath = ''
    path = os.getcwd().split('/')
    if path[len(path)-1] != 'testing':
        filepath = 'testing/'

    tempFilename = filepath + 'temp/temp.dot'
    nfaTest1Path = filepath + 'NFAs/tests/test1.gv'
    nfaSol1Path = filepath + 'NFAs/solutions/sol1.gv'
    
    nfaTest2Path = filepath + 'NFAs/tests/test2.gv'
    nfaSol2Path = filepath + 'NFAs/solutions/sol2.gv'

    # Test 1
    nfaTest1 = nx.drawing.nx_agraph.read_dot(nfaTest1Path) 
    nfaSol1 = nx.drawing.nx_agraph.read_dot(nfaSol1Path) 

    # Test 2
    nfaTest2 = nx.drawing.nx_agraph.read_dot(nfaTest2Path) 
    nfaSol2 = nx.drawing.nx_agraph.read_dot(nfaSol2Path) 

    unittest.main() 
