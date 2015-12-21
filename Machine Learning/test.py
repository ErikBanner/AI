#!/usr/bin/python
from __future__ import division
from copy import deepcopy
import sqlite3
import math

class node(object):
    def __init__(self):
    	self.splitted = False
    	self.parent = None
        self.feature = None
        self.category = None
        self.information_gain = None
        self.reduced_contain_space = None
        self.reduced_not_contain_space = None
        self.reduced_to_features = None
        self.left = None
        self.right = None

    def print_tree(self, level=0):
    	global TRAIN_TABLE
    	global WORDID_INDEX
    	if self.splitted == True:
        	print '\t' * level + str(self.feature)
        else:
        	print '\t' * level + "category: " + repr(self.category)
        if self.left != None:
	        self.left.print_tree(level+1)
    	if self.right != None:
	        self.right.print_tree(level+1)

def foo():
	t = node()
	t.feature = 0
	t.splitted = True
	t.left = node()
	t.left.feature = 10
	t.right =node()
	t.right.feature = 100
	t.left.left = node()
	t.left.splitted = True
	t.left.left.feature = 1000
	t.left.right = node()
	t.left.right.feature = 10000
	t.right.left = node()
	t.right.splitted = True
	t.right.left.feature = 100000
	while t.splitted == True:
		t = t.left
		t.print_tree()
foo()