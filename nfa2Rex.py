################################################################################
 # File:    nfa2Rex.py
 #
 # Author: Dennis Kovarik
 # Date: 3/5/2021
 # Class Assignment: Midterm exam
 # 
 # Purpose: Converts a NFA graph described in dot notation and converts it to a
 # regular expression. This program expects 1 command line arguement, which is
 # the filepath to the NFA. The program will display the graph that is to be 
 # converted as a pdf. It will then convert the nfa to to a regular expression 
 # and display it to the screen.
 #   
 # Run: 
 #      python nfa2Rex.py path/to/nfa.gv
 #
 # Input:   Filepath for NFA described in dot notation
 # Output:  Regular expression for NFA and pdf of the original graph
 #
 # Notes:
 # 1. As currently written, the program removes all lambda expressions, but it
 #    has not been tested if this works in all cases. 
 # 2. The algorithm for converting an NFA to a regular expression assumes that
 #    the final state is distinct from the initial state. The case for when 
 #    the final state is the same as the initial state has been special cased,
 #    but the correctness of this special case has not be thoroughly tested.
 ##############################################################################

import sys
import graphviz
import networkx as nx
from utilities import *


# Check for the filepath passed in
if len(sys.argv) < 2:
    print("Incorrect number of command line arguments")
    print("Usage: ")
    print("\tpython nfa2Rex.py path/to/nfa.gv\n")

filepath = sys.argv[1]

# Read in the NFA
nfa = nx.drawing.nx_agraph.read_dot(filepath)
G = nx.DiGraph(nfa) 
gv = graphviz.Source.from_file(filepath)

stop = 0
# Run program
while stop == 0:
    # Display menu
    print("-------------------------------------------------------------------")
    print("Menu")
    print("\t1: Display NFA")
    print("\t2: Convert NFA to a Regular Expression")
    print("\t3: Exit")
    print()
    choice = input("Enter choice: ")

    # Run the options
    if choice == "1":
        gv.view()
        print("-------------------------------------------------------------------")
        print()
    elif choice == "2":
        regex = nfa2Rex(G)
        print()
        print("Regular Expression for NFA: " + regex)
        print("-------------------------------------------------------------------")
        print()
    else:
        print("Goodbye")
        break
    
        

    
