# File: showGraph.py
# Author: Dennis Kovarik
# Purpose: Displays an NFA discribed in dot notation
#
# Description:
# This program simply just displays an NFA described in dot notation to the 
# screen as a pdf. This program expects the file path to the NFA described in
# dot notation to be passed in on the command line.
#
# Usage:
#       python showGraph.py path/to/graphviv/nfa.gv

import sys
import graphviz
import networkx as nx

if len(sys.argv[1]) > 1:
    gv = graphviz.Source.from_file(sys.argv[1])
    gv.view()
