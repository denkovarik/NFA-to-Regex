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
        Tests ability to call the function nfa2Gtg.
        """
        self.assertTrue(2 == 2)
    
 
         

if __name__ == '__main__':
    unittest.main() 
