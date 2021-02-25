import sys
import graphviz
import networkx as nx

if len(sys.argv[1]) > 1:
    gv = graphviz.Source.from_file(sys.argv[1])
    gv.view()
