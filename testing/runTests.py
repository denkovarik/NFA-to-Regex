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

    
class nfa2GtgTests(unittest.TestCase):
    def testFunctionCall(self):
        """
        Tests ability to call the function nfa2Gtg
        """
        # Read in the test nfa
        path = os.getcwd().split('/')

        filepath = 'NFAs/tests/test1.gv'
        if path[len(path)-1] != 'testing':
            filepath = 'testing/' + filepath
        
        gv = graphviz.Source.from_file(filepath)
   
        # Convert to GTG
        nfa2Gtg(gv)
     
        print(gv.source)
        gv.view()

    
 
         

if __name__ == '__main__':
    unittest.main() 
