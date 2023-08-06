import pytest
from comlibpy import XTree

class Node:
    def __init__(self, name, children=None):
        self.name = name
        self.children = children

def createNode(e): return Node(e["name"])
def children(e): return e.children
def level(a): return a["level"]

class TestXTree:

    def test_basic(self):
        assert( 1+2 == 3 )

    def test_from(self):
        idata = [ 
            {"name":"DP", "level":1},
            {"name":"CP", "level":1},
            {"name":"NGC", "level":1},
            {"name":"PSTM", "level":1},
        ]
        res = XTree.fromArray( idata, createNode, children, level )
        print(res)
        assert( 1 == 1 )