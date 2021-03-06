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
 
class generalTests(unittest.TestCase):
    def testExecution(self):
        """
        This function tests that the program is able to run and execute a 
        basic test. 
        """
        # Test Assert
        self.assertTrue(2 == 2)


    def testGetFinalState(self):
        """
        Tests the function 'getFinalState' on its ability to return the end node
        in the graph.
        """
        G = nx.DiGraph(nfaTest1)
        finalState = getFinalState(G)
        self.assertTrue(finalState == 'q_0') 

        G = nx.DiGraph(nfaTest2)
        finalState = getFinalState(G)
        self.assertTrue(finalState == 'EO') 


    def testGetInitialState(self):
        """
        Tests the function 'getInitialState' on its ability to return the start
        node in the graph.
        """
        # Test case #1
        G = nx.DiGraph(nfaTest1)
        initState = getInitialState(G)
        self.assertTrue(initState == 'q_0')

        # Test case #2
        G = nx.DiGraph(nfaTest2)
        startNode = getInitialState(G)
        self.assertTrue(startNode == 'EE')

    
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


    def testGetNumTerms(self):
        """
        Tests function 'getNumTerms' on its ability to determine the number of 
        terms in a string.
        """
        # Test Case 1
        test = 'a'
        sol = 1
        ans = getNumTerms(test)
        self.assertTrue(ans == sol)
         
        # Test Case 2: Whitespace
        test = 'a '
        sol = 1
        ans = getNumTerms(test)
        self.assertTrue(ans == sol)
         
        # Test Case 3: *
        test = 'a*'
        sol = 1
        ans = getNumTerms(test)
        self.assertTrue(ans == sol)
         
        # Test Case 4: **
        test = 'a*'
        sol = 1
        ans = getNumTerms(test)
        self.assertTrue(ans == sol)
         
        # Test Case 5: (*)*
        test = '(a*)*'
        sol = 1
        ans = getNumTerms(test)
        self.assertTrue(ans == sol)
         
        # Test Case 6: (ab*)*
        test = '(ab*)*'
        sol = 2
        ans = getNumTerms(test)
        self.assertTrue(ans == sol)
         
        # Test Case 6: +
        test = 'a + b'
        sol = 2
        ans = getNumTerms(test)
        self.assertTrue(ans == sol)


    def testSimplifyPara(self):
        """
        Tests the function simplifyPara() on its ability to eliminate redundant
        parentheses.
        """
        # Test Case 1
        test = 'a'
        sol = 'a'
        ans = simplifyPara(test)
        self.assertTrue(ans == sol) 
       
        # Test Case 2
        test = 'ab'
        sol = 'ab'
        ans = simplifyPara(test)
        self.assertTrue(ans == sol) 
       
        # Test Case 3
        test = 'a(b)'
        sol = 'ab'
        ans = simplifyPara(test)
        self.assertTrue(ans == sol) 
       
        # Test Case 4
        test = '(a)b'
        sol = 'ab'
        ans = simplifyPara(test)
        self.assertTrue(ans == sol) 
       
        # Test Case 5
        test = '(ab)'
        sol = 'ab'
        ans = simplifyPara(test)
        self.assertTrue(ans == sol) 
       
        # Test Case 6
        test = '((ab))'
        sol = 'ab'
        ans = simplifyPara(test)
        self.assertTrue(ans == sol) 
       
        # Test Case 7
        test = '(((ab)))'
        sol = 'ab'
        ans = simplifyPara(test)
        self.assertTrue(ans == sol) 
       
        # Test Case 8
        test = '((a)b)'
        sol = 'ab'
        ans = simplifyPara(test)
        self.assertTrue(ans == sol) 
       
        # Test Case 9
        test = 'a*'
        sol = 'a*'
        ans = simplifyPara(test)
        self.assertTrue(ans == sol) 
       
        # Test Case 10
        test = '(a)*'
        sol = 'a*'
        ans = simplifyPara(test)
        self.assertTrue(ans == sol) 
       
        # Test Case 11
        test = 'a*b'
        sol = 'a*b'
        ans = simplifyPara(test)
        self.assertTrue(ans == sol) 
       
        # Test Case 12
        test = '(a*)b'
        sol = 'a*b'
        ans = simplifyPara(test)
        self.assertTrue(ans == sol) 
       
        # Test Case 13
        test = '(a)*b'
        sol = 'a*b'
        ans = simplifyPara(test)
        self.assertTrue(ans == sol) 
       
        # Test Case 14
        test = 'a*(b)'
        sol = 'a*b'
        ans = simplifyPara(test)
        self.assertTrue(ans == sol) 
       
        # Test Case 15
        test = 'ab*'
        sol = 'ab*'
        ans = simplifyPara(test)
        self.assertTrue(ans == sol) 
       
        # Test Case 16
        test = 'a(b)*'
        sol = 'ab*'
        ans = simplifyPara(test)
        self.assertTrue(ans == sol) 
       
        # Test Case 17
        test = '(ab)*'
        sol = '(ab)*'
        ans = simplifyPara(test)
        self.assertTrue(ans == sol) 
       
        # Test Case 18
        test = '(ab)*b'
        sol = '(ab)*b'
        ans = simplifyPara(test)
        self.assertTrue(ans == sol) 
       
        # Test Case 19
        test = '(ab)*(b)'
        sol = '(ab)*b'
        ans = simplifyPara(test)
        self.assertTrue(ans == sol) 
       
        # Test Case 20
        test = '(ab)*bc'
        sol = '(ab)*bc'
        ans = simplifyPara(test)
        self.assertTrue(ans == sol) 
       
        # Test Case 21
        test = '(ab)*(bc)'
        sol = '(ab)*bc'
        ans = simplifyPara(test)
        self.assertTrue(ans == sol) 
       
        # Test Case 22
        test = '(ab)c'
        sol = 'abc'
        ans = simplifyPara(test)
        self.assertTrue(ans == sol) 
       
        # Test Case 23
        test = 'a+bc+d'
        sol = 'a+bc+d'
        ans = simplifyPara(test)
        self.assertTrue(ans == sol) 
       
        # Test Case 24
        test = 'a+(bc)+d'
        sol = 'a+bc+d'
        ans = simplifyPara(test)
        self.assertTrue(ans == sol) 
       
        # Test Case 25
        test = 'a+(bc)d+e'
        sol = 'a+bcd+e'
        ans = simplifyPara(test)
        self.assertTrue(ans == sol) 
       
        # Test Case 26
        test = 'a+(bc)*d+e'
        sol = 'a+(bc)*d+e'
        ans = simplifyPara(test)
        self.assertTrue(ans == sol) 
       
        # Test Case 27
        test = 'a(bc)d'
        sol = 'abcd'
        ans = simplifyPara(test)
        self.assertTrue(ans == sol) 
       
        # Test Case 28
        test = 'a(b+cd)e'
        sol = 'a(b+cd)e'
        ans = simplifyPara(test)
        self.assertTrue(ans == sol) 
       
        # Test Case 29
        test = 'ab+(cd)e+a'
        sol = 'ab+cde+a'
        ans = simplifyPara(test)
        self.assertTrue(ans == sol) 
        
        # Test Case 30
        test = 'b+a(\u2205+r)'
        sol = 'b+a(\u2205+r)'
        ans = simplifyPara(test)
        self.assertTrue(ans == sol)
        
        # Test Case 31
        test = 'b+a(\u2205+r)+a'
        sol = 'b+a(\u2205+r)+a'
        ans = simplifyPara(test)
        self.assertTrue(ans == sol)
        
        # Test Case 32
        test = 'b+(a(\u2205+r))+a'
        sol = 'b+a(\u2205+r)+a'
        ans = simplifyPara(test)
        self.assertTrue(ans == sol)
        
        # Test Case 33
        test = 'a+(a+b)c'
        sol = 'a+(a+b)c'
        ans = simplifyPara(test)
        self.assertTrue(ans == sol)
        
        # Test Case 34
        test = 'a+(a+b)+c'
        sol = 'a+a+b+c'
        ans = simplifyPara(test)
        self.assertTrue(ans == sol)
        
        # Test Case 35
        test = 'a(b+(a+d))'
        sol = 'a(b+a+d)'
        ans = simplifyPara(test)
        self.assertTrue(ans == sol)
        
        # Test Case 36
        test = 'a(b(a+d)+c)'
        sol = 'a(b(a+d)+c)'
        ans = simplifyPara(test)
        self.assertTrue(ans == sol)
        
        # Test Case 37
        test = 'a(b(a+d))'
        sol = 'ab(a+d)'
        ans = simplifyPara(test)
        self.assertTrue(ans == sol)
        
        # Test Case 38
        test = 'a((a+d)+c)'
        sol = 'a(a+d+c)'
        ans = simplifyPara(test)
        self.assertTrue(ans == sol)
        
        # Test Case 39
        test = 'a(\u2205+r)+b'
        sol = 'a(\u2205+r)+b'
        ans = simplifyPara(test)
        self.assertTrue(ans == sol)
        
        # Test Case 40
        test = '(a + a)'
        sol = 'a+a'
        ans = simplifyPara(test)
        self.assertTrue(ans == sol)

        # Test Case 41
        test = 'aa+ab(bb)*ba'
        sol = 'aa+ab(bb)*ba'
        ans = simplifyPara(test)
        self.assertTrue(ans == sol)
        
        # Test Case 42
        test = '(aa+ab(bb)*ba)*(b+ab(bb)*a)(a(bb)*a+(b+a(bb)*ba)(aa+ab(bb)*ba)*(b+ab(bb)*a))*' 
        sol  = '(aa+ab(bb)*ba)*(b+ab(bb)*a)(a(bb)*a+(b+a(bb)*ba)(aa+ab(bb)*ba)*(b+ab(bb)*a))*' 
        ans = simplifyPara(test)
        self.assertTrue(ans == sol)
        
        # Test Case 43
        test = '\u2205+(\u2205)(\u2205)*(0+1)' 
        sol  = '\u2205+\u2205\u2205*(0+1)' 
        ans = simplifyPara(test)
        self.assertTrue(ans == sol)


    def testApplySimpRules(self):
        """
        Tests applySimpRules on its ability to apply simplifying ruls to regex.
        """
        # Test Case 1
        test = 'r'
        sol = 'r'
        ans = applySimpRules(test)
        self.assertTrue(ans == sol)
        
        # Test Case 2
        test = '\u2205*'
        sol = '\u03BB'
        ans = applySimpRules(test)
        self.assertTrue(ans == sol)
        
        # Test Case 3
        test = 'r\u2205*'
        sol = 'r\u03BB'
        ans = applySimpRules(test)
        self.assertTrue(ans == sol)
        
        # Test Case 4
        test = 'adr\u2205*'
        sol = 'adr\u03BB'
        ans = applySimpRules(test)
        self.assertTrue(ans == sol)
        
        # Test Case 5
        test = 'a*dr\u2205*'
        sol = 'a*dr\u03BB'
        ans = applySimpRules(test)
        self.assertTrue(ans == sol)
        
        # Test Case 6
        test = '(ad)*r\u2205*'
        sol = '(ad)*r\u03BB'
        ans = applySimpRules(test)
        self.assertTrue(ans == sol)
        
        # Test Case 7
        test = '\u2205*r'
        sol = '\u03BBr'
        ans = applySimpRules(test)
        self.assertTrue(ans == sol)
        
        # Test Case 8
        test = '\u2205*rds'
        sol = '\u03BBrds'
        ans = applySimpRules(test)
        self.assertTrue(ans == sol)
        
        # Test Case 9
        test = '\u2205*rd*s'
        sol = '\u03BBrd*s'
        ans = applySimpRules(test)
        self.assertTrue(ans == sol)
        
        # Test Case 10
        test = '\u2205*(rd)*s'
        sol = '\u03BB(rd)*s'
        ans = applySimpRules(test)
        self.assertTrue(ans == sol)
        
        # Test Case 11
        test = 'r\u2205'
        sol = '\u2205'
        ans = applySimpRules(test)
        self.assertTrue(ans == sol)
        
        # Test Case 12
        test = 'adr\u2205'
        sol = '\u2205'
        ans = applySimpRules(test)
        self.assertTrue(ans == sol)
        
        # Test Case 13
        test = 'ad*r\u2205'
        sol = '\u2205'
        ans = applySimpRules(test)
        self.assertTrue(ans == sol)
        
        # Test Case 14
        test = '\u2205ad*r'
        sol = '\u2205'
        ans = applySimpRules(test)
        self.assertTrue(ans == sol)
        
        # Test Case 15
        test = 'ad*r\u2205ad*r'
        sol = '\u2205'
        ans = applySimpRules(test)
        self.assertTrue(ans == sol)
        
        # Test Case 16
        test = '(ad)*r\u2205'
        sol = '\u2205'
        ans = applySimpRules(test)
        self.assertTrue(ans == sol)
        
        # Test Case 17
        test = '\u2205(ad)*r'
        sol = '\u2205'
        ans = applySimpRules(test)
        self.assertTrue(ans == sol)
        
        # Test Case 18
        test = '(ad)*r\u2205(ad)*r'
        sol = '\u2205'
        ans = applySimpRules(test)
        self.assertTrue(ans == sol)
        
        # Test Case 19
        test = '(ad)*(r\u2205+e)'
        sol = '(ad)*e'
        ans = applySimpRules(test)
        self.assertTrue(ans == sol)
        
        # Test Case 20
        test = '(r\u2205+e)(ad)*(ra)*'
        sol = 'e(ad)*(ra)*'
        ans = applySimpRules(test)
        self.assertTrue(ans == sol)
        
        # Test Case 21
        test = '(ad)*((ra)*\u2205+e)(ad)*((ra)*'
        sol = '(ad)*e(ad)*((ra)*'
        ans = applySimpRules(test)
        self.assertTrue(ans == sol)
        
        # Test Case 22
        test = 'ad(r\u2205)'
        sol = '\u2205'
        ans = applySimpRules(test)
        self.assertTrue(ans == sol)
        
        # Test Case 23
        test = 'ad*(r\u2205)'
        sol = '\u2205'
        ans = applySimpRules(test)
        self.assertTrue(ans == sol)
        
        # Test Case 24
        test = '(ad)*(r\u2205)'
        sol = '\u2205'
        ans = applySimpRules(test)
        self.assertTrue(ans == sol)
        
        # Test Case 25
        test = '\u2205r'
        sol = '\u2205'
        ans = applySimpRules(test)
        self.assertTrue(ans == sol)
        
        # Test Case 26
        test = '\u2205rda'
        sol = '\u2205'
        ans = applySimpRules(test)
        self.assertTrue(ans == sol)
        
        # Test Case 27
        test = '\u2205(ra)*'
        sol = '\u2205'
        ans = applySimpRules(test)
        self.assertTrue(ans == sol)
        
        # Test Case 28
        test = '(\u2205r)'
        sol = '\u2205'
        ans = applySimpRules(test)
        self.assertTrue(ans == sol)
        
        # Test Case 29
        test = '(\u2205r)a'
        sol = '\u2205'
        ans = applySimpRules(test)
        self.assertTrue(ans == sol)
        
        # Test Case 30
        test = '(\u2205r)a*'
        sol = '\u2205'
        ans = applySimpRules(test)
        self.assertTrue(ans == sol)
        
        # Test Case 31
        test = '(\u2205r)(ad)*'
        sol = '\u2205'
        ans = applySimpRules(test)
        self.assertTrue(ans == sol)
        
        # Test Case 32
        test = '(\u2205r)(ad*)'
        sol = '\u2205'
        ans = applySimpRules(test)
        self.assertTrue(ans == sol)
        
        # Test Case 33
        test = '(\u2205r)(ad*)*'
        sol = '\u2205'
        ans = applySimpRules(test)
        self.assertTrue(ans == sol)
        
        # Test Case 34
        test = 'r+b\u2205'
        sol = 'r'
        ans = applySimpRules(test)
        self.assertTrue(ans == sol)
        
        # Test Case 35
        test = 'r+b\u2205'
        sol = 'r'
        ans = applySimpRules(test)
        self.assertTrue(ans == sol)
        
        # Test Case 36
        test = 'r+\u2205b'
        sol = 'r'
        ans = applySimpRules(test)
        self.assertTrue(ans == sol)
        
        # Test Case 37
        test = 'b+\u2205+r'
        sol = 'b+r'
        ans = applySimpRules(test)
        self.assertTrue(ans == sol)
        
        # Test Case 38
        test = 'b+\u2205y+r'
        sol = 'b+r'
        ans = applySimpRules(test)
        self.assertTrue(ans == sol)
        
        # Test Case 39
        test = 'b+\u2205*+r'
        sol = 'b+\u03BB+r'
        ans = applySimpRules(test)
        self.assertTrue(ans == sol)
        
        # Test Case 40
        test = 'r+(ab)*\u2205+b'
        sol = 'r+b'
        ans = applySimpRules(test)
        self.assertTrue(ans == sol)
        
        # Test Case 41
        test = 'a(r+\u2205)+b'
        sol = 'ar+b'
        ans = applySimpRules(test)
        self.assertTrue(ans == sol)
        
        # Test Case 42
        test = 'a(\u2205+r)+b'
        sol = 'ar+b'
        ans = applySimpRules(test)
        self.assertTrue(ans == sol)
        
        # Test Case 43
        test = 'b+a(\u2205+r)'
        sol = 'b+ar'
        ans = applySimpRules(test)
        self.assertTrue(ans == sol)
        
        # Test Case 44
        test = 'b+a(\u2205+r)+a(\u2205+r)'
        sol = 'b+ar+ar'
        ans = applySimpRules(test)
        self.assertTrue(ans == sol)
 
        # Test Case 45: Regexp with (empty set) + char
        test = '\u2205 + a'
        sol = 'a'
        ans = applySimpRules(test)
        self.assertTrue(ans == sol) 
 
        # Test Case 46: Regexp with (empty set) + char
        test = 'a + \u2205'
        sol = 'a'
        ans = applySimpRules(test)
        self.assertTrue(ans == sol) 
 
        # Test Case 47
        test = '\u03BB\u03BB'
        sol = '\u03BB\u03BB'
        ans = applySimpRules(test)
        self.assertTrue(ans == sol) 
 
        # Test Case 48
        test = '\u03BB\u2205*'
        sol = '\u03BB\u03BB'
        ans = applySimpRules(test)
        self.assertTrue(ans == sol) 
 
        # Test Case 49
        test = '\u03BB\u2205*\u2205'
        sol = '\u2205'
        ans = applySimpRules(test)
        self.assertTrue(ans == sol) 
 
        # Test Case 50
        test = '1+\u03BB\u2205*\u2205'
        sol = '1'
        ans = applySimpRules(test)
        self.assertTrue(ans == sol) 
 
        # test case 51
        test = '(0+1)\u2205*\u2205'
        sol = '\u2205'
        ans = applySimpRules(test)
        self.assertTrue(ans == sol) 
 
        # test case 52
        test = '\u2205+(0+1)\u2205*\u2205'
        sol = '\u2205'
        ans = applySimpRules(test)
        self.assertTrue(ans == sol) 
 
        # test case 53
        test = '0+(0+1)\u2205*\u2205'
        sol = '0'
        ans = applySimpRules(test)
        self.assertTrue(ans == sol) 
 
        # test case 54
        test = '\u2205(0+1)'
        sol = '\u2205'
        ans = applySimpRules(test)
        self.assertTrue(ans == sol) 
        
        # Test Case 55
        test = '\u2205+(\u2205)\u03BB(0+1)' 
        sol = '\u2205'
        ans = applySimpRules(test)
        self.assertTrue(ans == sol) 
        
        # Test Case 56
        test = '\u2205+(\u2205)(\u2205)*(0+1)' 
        sol = '\u2205'
        ans = applySimpRules(test)
        self.assertTrue(ans == sol)

        # Test Case 57
        test = '\u03BB+\u2205+(10)*'
        sol = '\u03BB+(10)*' 
        ans = applySimpRules(test)
        self.assertTrue(ans == sol)


    def testIsOp(self):
        """
        Tests 'isOp' on its ability to determine if a character is an operation
        or not.
        """
        # Test Case 1
        ans = isOp('+')
        sol = True
        self.assertTrue(ans == sol)

        # Test Case 2
        ans = isOp('*')
        sol = True
        self.assertTrue(ans == sol)

        # Test Case 3
        ans = isOp('*.')
        sol = True
        self.assertTrue(ans == sol)

        # Test Case 4
        ans = isOp('.')
        sol = True
        self.assertTrue(ans == sol)

        # Test Case 5
        ans = isOp('a')
        sol = False
        self.assertTrue(ans == sol)

        # Test Case 6
        ans = isOp('a*')
        sol = False
        self.assertTrue(ans == sol)

        # Test Case 7
        ans = isOp('ab')
        sol = False
        self.assertTrue(ans == sol)

        # Test Case 8
        ans = isOp('a+b')
        sol = False
        self.assertTrue(ans == sol)

        # Test Case 9
        ans = isOp('a*b')
        sol = False
        self.assertTrue(ans == sol)

    
    def testIsHigherPriority(self):
        """
        Tests isLowerPriority() on its ability to determine if one operation 
        has a lower priority to another.
        """
        # Test Case 1
        op1 = '+'
        op2 = '+'
        sol = False
        ans = isHigherPriority(op1, op2)
        self.assertTrue(ans == sol)
        
        # Test Case 2
        op1 = '.'
        op2 = '+'
        sol = True
        ans = isHigherPriority(op1, op2)
        self.assertTrue(ans == sol)
        
        # Test Case 3
        op1 = '*.'
        op2 = '+'
        sol = True
        ans = isHigherPriority(op1, op2)
        self.assertTrue(ans == sol)
        
        # Test Case 4
        op1 = '*'
        op2 = '+'
        sol = True
        ans = isHigherPriority(op1, op2)
        self.assertTrue(ans == sol)
        
        # Test Case 5
        op1 = '+'
        op2 = '.'
        sol = False
        ans = isHigherPriority(op1, op2)
        self.assertTrue(ans == sol)
        
        # Test Case 6
        op1 = '.'
        op2 = '.'
        sol = False
        ans = isHigherPriority(op1, op2)
        self.assertTrue(ans == sol)
        
        # Test Case 7
        op1 = '.'
        op2 = '*'
        sol = False
        ans = isHigherPriority(op1, op2)
        self.assertTrue(ans == sol)
        
        # Test Case 8
        op1 = '.'
        op2 = '*.'
        sol = False
        ans = isHigherPriority(op1, op2)
        self.assertTrue(ans == sol)
        
        # Test Case 9
        op1 = '+'
        op2 = '*'
        sol = False
        ans = isHigherPriority(op1, op2)
        self.assertTrue(ans == sol)
        
        # Test Case 10
        op1 = '*'
        op2 = '.'
        sol = False
        ans = isHigherPriority(op1, op2)
        self.assertTrue(ans == sol)
        
        # Test Case 11
        op1 = '*'
        op2 = '*'
        sol = False
        ans = isHigherPriority(op1, op2)
        self.assertTrue(ans == sol)
        
        # Test Case 12
        op1 = '*'
        op2 = '*.'
        sol = False
        ans = isHigherPriority(op1, op2)
        self.assertTrue(ans == sol)
        
        # Test Case 13
        op1 = '+.'
        op2 = '*'
        sol = False
        ans = isHigherPriority(op1, op2)
        self.assertTrue(ans == sol)
        
        # Test Case 14
        op1 = '*.'
        op2 = '.'
        sol = False
        ans = isHigherPriority(op1, op2)
        self.assertTrue(ans == sol)
        
        # Test Case 15
        op1 = '*.'
        op2 = '*'
        sol = False
        ans = isHigherPriority(op1, op2)
        self.assertTrue(ans == sol)
        
        # Test Case 16
        op1 = '*.'
        op2 = '*.'
        sol = False
        ans = isHigherPriority(op1, op2)
        self.assertTrue(ans == sol)


    def testSimpAddition(self):
        """
        Tests simpAddition on its ability to remove redundant additions.
        """
        # Test Case #1
        test ='a'
        sol = 'a'
        ans = simpAddition(test)
        self.assertTrue(ans == sol) 
        
        # Test Case #2
        test ='a+a'
        sol = 'a'
        ans = simpAddition(test)
        self.assertTrue(ans == sol) 
        
        # Test Case #3
        test ='a+\u2205'
        sol = 'a+\u2205'
        ans = simpAddition(test)
        self.assertTrue(ans == sol) 
        
        # Test Case #4
        test ='\u2205+a'
        sol = '\u2205+a'
        ans = simpAddition(test)
        self.assertTrue(ans == sol) 
        
        # Test Case #5
        test ='\u2205+\u2205'
        sol = '\u2205'
        ans = simpAddition(test)
        self.assertTrue(ans == sol) 
        
        # Test Case #6
        test = 'a+(b+(b+cd)*)c'
        sol  = 'a+(b+(b+cd)*)c'
        ans = simpAddition(test)
        self.assertTrue(ans == sol)
        
        # Test Case #7
        test = '(ab)*+(ab)*'
        sol = '(ab)*'
        ans = simpAddition(test)
        self.assertTrue(ans == sol) 
        
        # Test Case #8
        test = '(ab)* + (ab)*'
        sol = '(ab)*'
        ans = simpAddition(test)
        self.assertTrue(ans == sol) 
        
        # Test Case #9
        test = '((ab)*+(ab)*)'
        sol = '((ab)*)'
        ans = simpAddition(test)
        self.assertTrue(ans == sol) 
        
        # Test Case #10: 
        test = 'a + a + b'
        sol = 'a+b'
        ans = simpAddition(test)
        self.assertTrue(ans == sol) 
        
        # Test Case #11
        test = '(aa+ab(bb)*ba)*(b+ab(bb)*a)(a(bb)*a+(b+a(bb)*ba)(aa+ab(bb)*ba)*(b+ab(bb)*a))*'
        sol  = '(aa+ab(bb)*ba)*(b+ab(bb)*a)(a(bb)*a+(b+a(bb)*ba)(aa+ab(bb)*ba)*(b+ab(bb)*a))*'
        ans = simpAddition(test)
        self.assertTrue(ans == sol)

        # Test Case #12
        test = '\u03BB'
        sol = '\u03BB'
        ans = simplifyRegexp(test)
        self.assertTrue(ans == sol)
    

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
        sol = '\u2205'
        ans = simplifyRegexp(test)
        self.assertTrue(ans == sol) 

        # Test Case #3: Regexp with 1 char concatenated with empty set
        test = 'a\u2205'
        sol = '\u2205'
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

        # Test Case #22: 
        test = '(a + a + b)'
        sol = 'a+b'
        ans = simplifyRegexp(test)
        self.assertTrue(ans == sol) 

        # Test Case #23: Redundant stars 
        test = 'a**'
        sol = 'a*'
        ans = simplifyRegexp(test)
        self.assertTrue(ans == sol) 

        # Test Case #24: Redundant () 
        test = '(a*)'
        sol = 'a*'
        ans = simplifyRegexp(test)
        self.assertTrue(ans == sol) 

        # Test Case #25: Redundant stars 
        test = '(a*)*'
        sol = 'a*'
        ans = simplifyRegexp(test)
        self.assertTrue(ans == sol) 

        # Test Case #26: Redundant stars 
        test = 'a***'
        sol = 'a*'
        ans = simplifyRegexp(test)
        self.assertTrue(ans == sol) 

        # Test Case #27: Redundant stars and para
        test = '((((a*)**))**)*'
        sol = 'a*'
        ans = simplifyRegexp(test)
        self.assertTrue(ans == sol) 

        # Test Case #28:
        test = '(ab*)*'
        sol = '(ab*)*'
        ans = simplifyRegexp(test)
        self.assertTrue(ans == sol) 

        # Test Case #29:
        test = 'a\u2205*'
        sol = 'a'
        ans = simplifyRegexp(test)
        self.assertTrue(ans == sol) 

        # Test Case #30:
        test = 'a\u2205*a'
        sol = 'aa'
        ans = simplifyRegexp(test)
        self.assertTrue(ans == sol) 

        # Test Case #31:
        test = '\u2205*'
        sol = '\u03BB'
        ans = simplifyRegexp(test)
        self.assertTrue(ans == sol) 

        # Test Case #32:
        test = 'a\u2205'
        sol = '\u2205'
        ans = simplifyRegexp(test)
        self.assertTrue(ans == sol) 

        # Test Case #33: Redundant stars 
        test = 'a******'
        sol = 'a*'
        ans = simplifyRegexp(test)
        self.assertTrue(ans == sol) 

        # Test Case #34 
        test = '(r+(ab)*)*+(a+(a*b))(r+\u2205)+b*b'
        sol = '(r+(ab)*)*+(a+a*b)r+b*b'
        ans = simplifyRegexp(test)
        self.assertTrue(ans == sol) 

        # Test Case #35 
        test = '(r+(ab)*)*+(a+(a*b))(r+\u2205)+b*b + (r+(ab)*)*'
        sol = '(r+(ab)*)*+(a+a*b)r+b*b'
        ans = simplifyRegexp(test)
        self.assertTrue(ans == sol) 
        
        # Test Case 36
        test = '\u2205+\u2205'
        sol = '\u2205'
        ans = simplifyRegexp(test)
        self.assertTrue(ans == sol)
        
        # Test Case 37
        test = '\u2205+\u2205\u2205*\u2205'
        sol = '\u2205'
        ans = simplifyRegexp(test)
        self.assertTrue(ans == sol)

        # Test Case 38
        test = 'aa+ab(bb)*ba'
        sol = 'aa+ab(bb)*ba'
        ans = simplifyRegexp(test)
        self.assertTrue(ans == sol)

        # Test Case 39
        test = '((aa+ab(bb)*ba)*(b+ab(bb)*a))*'
        sol = '((aa+ab(bb)*ba)*(b+ab(bb)*a))*'
        ans = simplifyRegexp(test)
        self.assertTrue(ans == sol)

        # Test Case 40
        test = '(aa+ab(bb)*ba)*(b+ab(bb)*a)(a(bb)*a+(b+a(bb)*ba)(aa+ab(bb)*ba)*(b+ab(bb)*a))*'
        sol  = '(aa+ab(bb)*ba)*(b+ab(bb)*a)(a(bb)*a+(b+a(bb)*ba)(aa+ab(bb)*ba)*(b+ab(bb)*a))*'
        ans = simplifyRegexp(test)
        self.assertTrue(ans == sol)
 
        # Test Case 41
        test = '1+\u03BB\u2205*\u2205'
        sol = '1'
        ans = simplifyRegexp(test)
        self.assertTrue(ans == sol) 
 
        # Test Case 42
        test = '\u2205+\u03BB\u2205*\u2205'
        sol = '\u2205'
        ans = simplifyRegexp(test)
        self.assertTrue(ans == sol) 
 
        # test case 43
        test = '\u2205+(0+1)\u2205*\u2205'
        sol = '\u2205'
        ans = simplifyRegexp(test)
        self.assertTrue(ans == sol) 
 
        # test case 44
        test = '0+(0+1)\u2205*\u2205'
        sol = '0'
        ans = simplifyRegexp(test)
        self.assertTrue(ans == sol) 
 
        # test case 45
        test = '\u2205(0+1)'
        sol = '\u2205'
        ans = simplifyRegexp(test)
        self.assertTrue(ans == sol) 
        
        # Test Case 46
        test = '\u2205+(\u2205)(\u2205)*(0+1)' 
        sol = '\u2205'
        ans = simplifyRegexp(test)
        self.assertTrue(ans == sol) 

        # Test Case 47
        test = '\u03BB+\u2205+(10)*'
        sol = '(10)*' 
        ans = simplifyRegexp(test)
        self.assertTrue(ans == sol) 

        # Test Case 48
        test = '\u2205+\u03BB+(10)*'
        sol = '(10)*' 
        ans = simplifyRegexp(test)
        self.assertTrue(ans == sol) 
   
 
    def testInfix2Postfix(self):
        """
        Tests 'infix2Postfix' on its ability to convert a regex in infix to
        postfix notation.
        """
        # Test Case 1
        test = 'a'
        sol = 'a'
        ans = infix2Postfix(test)
        self.assertTrue(ans == sol)
       
        # Test Case 2
        test = 'a+b'
        sol = 'ab+'
        ans = infix2Postfix(test)
        self.assertTrue(ans == sol)
       
        # Test Case 3
        test = 'aa'
        sol = 'aa.'
        ans = infix2Postfix(test)
        self.assertTrue(ans == sol)
       
        # Test Case 4
        test = 'a*b'
        sol = 'ab*'
        ans = infix2Postfix(test)
        self.assertTrue(ans == sol)
       
        # Test Case 5
        test = 'ab+c'
        sol = 'ab.c+'
        ans = infix2Postfix(test)
        self.assertTrue(ans == sol)
       
        # Test Case 6
        test = 'ab*+c'
        sol = 'ab.*c+'
        ans = infix2Postfix(test)
        self.assertTrue(ans == sol)
       
        # Test Case 7
        test = '(ab*)+c'
        sol = 'ab.*c+'
        ans = infix2Postfix(test)
        self.assertTrue(ans == sol)
       
        # Test Case 8
        test = 'a+(a*b)c'
        sol = 'aab*c.+'
        ans = infix2Postfix(test)
        self.assertTrue(ans == sol)
       
        # Test Case 9
        test = 'a+(a*b)*c'
        sol = 'aab*c*+'
        ans = infix2Postfix(test)
        self.assertTrue(ans == sol)
 
    
    def testCombineEdges(self):
        """
        Tests ability of the function 'combineEdges' to combine edges for the 
        process of removing a node from the graph.
        """
        # Test 1 
        G = nx.DiGraph(nfaTest3) 
 
        # Convert to GTG
        GTG = nfa2Gtg(G)

        # Test Case 1: Test 1 q_1 -> q_1 when removing q_2
        newEdge = combineEdges(G, 'q_1', 'q_1', 'q_2')
        sol = "e+af*b"
        self.assertTrue(newEdge == sol)

        # Test Case 2: Test 1 q_1 -> q_3 when removing q_2
        newEdge = combineEdges(G, 'q_1', 'q_3', 'q_2')
        sol = "h+af*c"
        self.assertTrue(newEdge == sol)

        # Test Case 3: Test 1 q_3 -> q_3 when removing q_2
        newEdge = combineEdges(G, 'q_3', 'q_3', 'q_2')
        sol = "g+df*c"
        self.assertTrue(newEdge == sol)

        # Test Case 4: Test 1 q_3 -> q_1 when removing q_2
        newEdge = combineEdges(G, 'q_3', 'q_1', 'q_2')
        sol = "i+df*b"
        self.assertTrue(newEdge == sol)

        
        # Test 2
        G = nx.DiGraph(nfaTest2) 
 
        # Convert to GTG
        GTG = nfa2Gtg(G)

        # Test Case 5: Test 2 EE -> EE when removing OE
        newEdge = combineEdges(G, 'EE', 'EE', 'OE')
        sol = "aa"
        self.assertTrue(newEdge == sol)

        # Test Case 6: Test 2 EE -> EO when removing OE
        newEdge = combineEdges(G, 'EE', 'EO', 'OE')
        sol = "b"
        self.assertTrue(newEdge == sol)

        # Test Case 7: Test 2 EO -> EE when removing OE
        newEdge = combineEdges(G, 'EO', 'EE', 'OE')
        sol = "b"
        self.assertTrue(newEdge == sol)
        
        # Test Case 8: Test 2 EO -> EO when removing OE
        newEdge = combineEdges(G, 'EO', 'EO', 'OE')
        sol = "\u2205"
        self.assertTrue(newEdge == sol)

        # Test Case 9: Test 2 EO -> OO when removing OE
        newEdge = combineEdges(G, 'EO', 'OO', 'OE')
        sol = "a"
        self.assertTrue(newEdge == sol)

        # Test Case 10: Test 2 OO -> EO when removing OE
        newEdge = combineEdges(G, 'OO', 'EO', 'OE')
        sol = "a"
        self.assertTrue(newEdge == sol)

        # Test Case 11: Test 2 OO -> EO when removing OE
        newEdge = combineEdges(G, 'OO', 'OO', 'OE')
        sol = "bb"
        self.assertTrue(newEdge == sol)

        # Test Case 12: Test 2 OO -> EE when removing OE
        newEdge = combineEdges(G, 'OO', 'EE', 'OE')
        sol = "ba"
        self.assertTrue(newEdge == sol)

        # Test Case 11: Test 2 EE -> OO when removing OE
        newEdge = combineEdges(G, 'EE', 'OO', 'OE')
        sol = "ab"
        self.assertTrue(newEdge == sol)
        

        # Test 3
        G = nx.DiGraph(nfaTest4)

        # Test Case 12: Test 3 EE -> EE when removing EO
        newEdge = combineEdges(G, 'EE', 'EE', 'OO')
        sol = "aa+ab(bb)*ba"
        self.assertTrue(newEdge == sol)

        # Test Case 13: Test 3 EE -> EO when removing EO
        newEdge = combineEdges(G, 'EE', 'EO', 'OO')
        sol = "b+ab(bb)*a"
        self.assertTrue(newEdge == sol)

        # Test Case 14: Test 3 EO -> EO when removing EO
        newEdge = combineEdges(G, 'EO', 'EO', 'OO')
        sol = "a(bb)*a"
        self.assertTrue(newEdge == sol)

        # Test Case 15: Test 3 EO -> EE when removing EO
        newEdge = combineEdges(G, 'EO', 'EE', 'OO')
        sol = "b+a(bb)*ba"
        self.assertTrue(newEdge == sol)

        
        # Test 4
        G = nx.DiGraph(nfaTest7) 

        # Convert to GTG
        GTG = nfa2Gtg(G)

        # Test Case 16: Test 4 q_0 -> q_1 when removing q_2
        newEdge = combineEdges(GTG, 'q_0', 'q_1', 'q_2')
        sol = "1"
        self.assertTrue(newEdge == sol)

        # Test Case 17: Test 4 q_0 -> q_0 when removing q_2
        newEdge = combineEdges(GTG, 'q_0', 'q_0', 'q_2')
        sol = "\u2205"
        self.assertTrue(newEdge == sol)

        # Test Case 18: Test 4 q_1 -> q_1 when removing q_2
        newEdge = combineEdges(GTG, 'q_1', 'q_1', 'q_2')
        sol = "\u2205"
        self.assertTrue(newEdge == sol)

        # Test Case 18: Test 4 q_1 -> q_0 when removing q_2
        newEdge = combineEdges(GTG, 'q_1', 'q_0', 'q_2')
        sol = "0"
        self.assertTrue(newEdge == sol)

        # Test Case 19: Test 4 q_0 -> q_1 when removing q_1
        newEdge = combineEdges(GTG, 'q_0', 'q_2', 'q_1')
        sol = "1(0+1)"
        self.assertTrue(newEdge == sol)

        # Test Case 20: Test 4 q_0 -> q_0 when removing q_1
        newEdge = combineEdges(GTG, 'q_0', 'q_0', 'q_1')
        sol = "10"
        self.assertTrue(newEdge == sol)

        # Test Case 21: Test 4 q_2 -> q_2 when removing q_1
        newEdge = combineEdges(GTG, 'q_2', 'q_2', 'q_1')
        sol = "\u2205"
        self.assertTrue(newEdge == sol)

        # Test Case 22: Test 4 q_2 -> q_0 when removing q_1
        newEdge = combineEdges(GTG, 'q_2', 'q_0', 'q_1')
        sol = "\u2205"
        self.assertTrue(newEdge == sol)

 
    def testCnrt2StateGTG2Regex(self):
        """
        Tests ability of the function 'combineEdges' to combine edges for the 
        process of removing a node from the graph.
        """
        # Test 1 
        G = nx.DiGraph(nfaTest5) 

        sol = '(aa+ab(bb)*ba)*(b+ab(bb)*a)(a(bb)*a+(b+a(bb)*ba)(aa+ab(bb)*ba)*(b+ab(bb)*a))*' 
        ans = cnrt2StateGTG2Regex(G, 'EE', 'EO')
        self.assertTrue(ans == sol)
        

        # Test 2
        G = nx.DiGraph(nfaTest6) 

        sol = '(e+af*b)*(h+af*c)(g+df*c+(i+df*b)(e+af*b)*(h+af*c))*' 
        ans = cnrt2StateGTG2Regex(G, 'q_1', 'q_3')
        self.assertTrue(ans == sol)

        # Test 3
        G = nx.DiGraph(nfaTest8) 

        sol = '\u03BB+(10)*' 
        ans = cnrt2StateGTG2Regex(G, 'q_0', 'q_0')
        self.assertTrue(ans == sol)


    def testNaf2Rex(self):
        """
        Tests the function nfa2Rex() on its ability to convert an nfa to a 
        regular expression.
        """
        # Test 1
        G = nx.DiGraph(nfaTest8) 
        sol = '\u03BB+(10)*' 
        ans = nfa2Rex(G)
        self.assertTrue(ans == sol)
        
        # Test 2
        G = nx.DiGraph(nfaTest1) 
        sol = '\u03BB+(10)*' 
        ans = nfa2Rex(G)
        self.assertTrue(ans == sol)
        
        # Test 3 
        G = nx.DiGraph(nfaTest3) 
        sol = '(e+af*b)*(h+af*c)(g+df*c+(i+df*b)(e+af*b)*(h+af*c))*' 
        ans = nfa2Rex(G)
        self.assertTrue(ans == sol)
        
        # Test 4
        G = nx.DiGraph(nfaTest2) 
        sol = '(aa+ab(bb)*ba)*(b+ab(bb)*a)(a(bb)*a+(b+a(bb)*ba)(aa+ab(bb)*ba)*(b+ab(bb)*a))*' 
        ans = nfa2Rex(G)
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
    
    nfaTest3Path = filepath + 'NFAs/tests/test3.gv'
    nfaSol3Path = filepath + 'NFAs/solutions/sol3.gv'
    
    nfaTest4Path = filepath + 'NFAs/tests/test4.gv'
    nfaTest5Path = filepath + 'NFAs/tests/test5.gv'
    nfaTest6Path = filepath + 'NFAs/tests/test6.gv'
    nfaTest7Path = filepath + 'NFAs/tests/test7.gv'
    nfaTest8Path = filepath + 'NFAs/tests/test8.gv'

    # Test 1
    nfaTest1 = nx.drawing.nx_agraph.read_dot(nfaTest1Path) 
    nfaSol1 = nx.drawing.nx_agraph.read_dot(nfaSol1Path) 

    # Test 2
    nfaTest2 = nx.drawing.nx_agraph.read_dot(nfaTest2Path) 
    nfaSol2 = nx.drawing.nx_agraph.read_dot(nfaSol2Path) 

    # Test 3
    nfaTest3 = nx.drawing.nx_agraph.read_dot(nfaTest3Path) 

    # Test 4
    nfaTest4 = nx.drawing.nx_agraph.read_dot(nfaTest4Path) 

    # Test 5
    nfaTest5 = nx.drawing.nx_agraph.read_dot(nfaTest5Path) 

    # Test 6
    nfaTest6 = nx.drawing.nx_agraph.read_dot(nfaTest6Path) 

    # Test 7
    nfaTest7 = nx.drawing.nx_agraph.read_dot(nfaTest7Path) 

    # Test 8
    nfaTest8 = nx.drawing.nx_agraph.read_dot(nfaTest8Path) 

    unittest.main() 
