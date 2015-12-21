#!/usr/bin/python
from __future__ import division
from copy import deepcopy
import math
import linecache
import matplotlib.pyplot as plot


#---------------------------------------------------Basic Knowledges--------------------------------------------------#

# a set of input features X_1, ..., X_n
# a set of target features Y_1, ..., Y_n
# a set of training examples where input and target feature values are given
# a new example where only input feature values are given
# Predict values for the new example's target feature
# classification when Y_i are discrete
# regression when Y_i are continuous
# val(e,F) = value of feature F for example e
# pval(e,F) = predicted value of feature F for example e

# Decision Tree:
#	nodes are input features
#	branches are labeled with input feature values
#	leaves are predictions for target features

# Need -logP(x) bits to encode x
# Each symbol requires on avg -P(x)logP(x) bits
# To transmit an entire sequence distributed according to P(x) need on avg
#	sum -P(x)logP(x) bits

# Given a set E of N training examples, if the number of examples with output feature Y = y_i is N_i , then
# P(Y = y_i) = P(y_i) = N_i / N

# Total information content for the set E is:
# I(E) = -sumP(y_i)logP(y_i)

# So after splitting E into E_1 and E_2 (size N_1, N_2) based on input features X_i, the information content is
# I(E_split) = N_1/N * I(E_1) + N_2/N * I(E_2)
# and we want the X_i that maximizes the information gain: I(E) - I(E_split)

# //X is input features, Y is output features, //E is training examples
# //output is a decision tree, which is either
# //	- a point estimate of Y, or
# //	- of the form < Xi,T1,...,TN > where
# //	Xi is an input feature and T1, ..., TN are decision trees 
#
# procedure DecisionTreeLearner(X,Y,E) 
# if stopping criteria is met then
# 	return pointEstimate(Y,E)
# else
# 	select feature Xi in X
# 	for each value xi of Xi do
# 		Ei = all examples in E where Xi = xi
# 		Ti =DecisionTreeLearner(X\{Xi},Y,Ei) 
# 	end for
# 	return < Xi,T1,...,TN > 
# end procedure

#---------------------------------------------------------------------------------------------------------------------#


class Node(object):
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
    	feature_str = TRAIN_TABLE[WORDID_INDEX][self.feature]
    	if self.splitted == True:
        	print '\t' * level + str(self.feature) + ": " + feature_str + ", ig: " + str(self.information_gain)
        else:
        	print '\t' * level + "category: " + repr(self.category)
        if self.left != None:
	        self.left.print_tree(level+1)
    	if self.right != None:
	        self.right.print_tree(level+1)

TYPE = True
WORDID_INDEX = 0
CATEGORY_INDEX = 0
TRAIN_TABLE = None
TEST_TABLE = None
ACCURACY = []
WORD_FILE = "words.txt"
LABEL_FILE = "trainLabel.txt"
DATA_FILE = "trainData.txt"
TEST_LABEL_FILE = "testLabel.txt"
TEST_DATA_FILE = "testData.txt"

#---------------------------------------------------------------------------------------------------------------------#

def load_train_data():
	global TRAIN_TABLE
	global WORDID_INDEX
	global CATEGORY_INDEX
	num_words = sum(1 for line in open(WORD_FILE, "r"))
	num_docs = sum(1 for line in open(LABEL_FILE, "r"))
	train_table = [[0] * (num_words+1) for doc in xrange(num_docs+1)]

	counter = 1
	with open(WORD_FILE, "r") as w:
		for line in w:
			(word,) = line.split()
			train_table[WORDID_INDEX][counter] = str(word)
			counter += 1

	counter = 1
	with open(LABEL_FILE, "r") as tl:
		for line in tl:
			(category,) = line.split()
			train_table[counter][CATEGORY_INDEX] = int(category)
			counter += 1

	with open(DATA_FILE, "r") as td:
		for line in td:
			splitted_line = line.split()
			docID = int(splitted_line[0])
			wordID = int(splitted_line[1])
			train_table[docID][wordID] = 1

	TRAIN_TABLE = train_table

	num_words = sum(1 for line in open(WORD_FILE, "r"))
	num_docs = sum(1 for line in open(LABEL_FILE, "r"))
	test_table = [[0] * (num_words+1) for doc in xrange(num_docs+1)]

	counter = 1
	with open(WORD_FILE, "r") as w:
		for line in w:
			(word,) = line.split()
			test_table[WORDID_INDEX][counter] = str(word)
			counter += 1

	counter = 1
	with open(TEST_LABEL_FILE, "r") as tl:
		for line in tl:
			(category,) = line.split()
			test_table[counter][CATEGORY_INDEX] = int(category)
			counter += 1

	with open(TEST_DATA_FILE, "r") as td:
		for line in td:
			splitted_line = line.split()
			docID = int(splitted_line[0])
			wordID = int(splitted_line[1])
			test_table[docID][wordID] = 1

	TEST_TABLE = test_table

#---------------------------------------------------------------------------------------------------------------------#

def entropy(feature_value_counts):
	entropy = 0
	count_total = sum(feature_value_counts)
	for count in feature_value_counts:
		if count == 0:
			continue
		else:
			entropy -= (count / count_total) * math.log(count / count_total, 2)
	return entropy

#---------------------------------------------------------------------------------------------------------------------#	
# Not yet generalized to n feature value, only binary values.

def information_gain(from_space, to_feature):
	global TYPE
	global TRAIN_TABLE
	global WORDID_INDEX
	global CATEGORY_INDEX
	category_one_count = 0
	category_two_count = 0
	category_one_contain = 0
	category_two_contain = 0
	category_one_not_contain = 0
	category_two_not_contain = 0
	reduced_contain_space = []
	reduced_not_contain_space = []
	for doc in from_space:
		if TRAIN_TABLE[doc][CATEGORY_INDEX] == 1:
			category_one_count += 1
		else:
			category_two_count += 1

		if TRAIN_TABLE[doc][to_feature] == 1: 			# contain the word
			reduced_contain_space.append(doc)
			if TRAIN_TABLE[doc][CATEGORY_INDEX] == 1: 	# the doc is in category 1
				category_one_contain += 1
			else:										# the doc is in category 2
				category_two_contain += 1
		else:											# doesn't contain the word
			reduced_not_contain_space.append(doc)
			if TRAIN_TABLE[doc][CATEGORY_INDEX] == 1:	# the doc is in category 1
				category_one_not_contain += 1
			else:										# the doc is in category 2
				category_two_not_contain += 1	
	
	if category_one_count + category_two_count != 0:
		if TYPE:
			from_space_entropy = entropy([category_one_count, category_two_count])
			to_feature_entropy = (
				(category_one_contain + category_two_contain) /
				(category_one_count + category_two_count) * 
				entropy([category_one_contain, category_two_contain]) +
				(category_one_not_contain + category_two_not_contain) /
				(category_one_count + category_two_count) *
				entropy([category_one_not_contain, category_two_not_contain])
				)
		else:
			from_space_entropy = entropy([category_one_count, category_two_count])
			to_feature_entropy = (
				0.5 * entropy([category_one_contain, category_two_contain]) + 
				0.5 * entropy([category_one_not_contain, category_two_not_contain])
				)

	return (from_space_entropy - to_feature_entropy, reduced_contain_space, reduced_not_contain_space)

#---------------------------------------------------------------------------------------------------------------------#

def point_estimate(space, feature):
	global TRAIN_TABLE
	category_one = 0
	category_two = 0
	for doc in space:
		if TRAIN_TABLE[doc][CATEGORY_INDEX] == 1:
			category_one += 1
		else:
			category_two += 1
	if category_one > category_two:
		return 1
	else:
		return 2

#---------------------------------------------------------------------------------------------------------------------#

def DTL():
	global TRAIN_TABLE
	global TEST_TABLE
	global ACCURACY
	load_train_data()
	decision_tree = None
	current_node = None
	accuracy = []

	max_information_gain = -1
	feature_for_max_ig = 0
	reduced_contain_space = []
	reduced_not_contain_space = []
	features = list(xrange(1, len(TRAIN_TABLE[WORDID_INDEX])))
	from_space = list(xrange(1, len(TRAIN_TABLE)))
	for feature in features:
		(ig, rcs, rncs) = information_gain(from_space, feature)
		if ig > max_information_gain:
			max_information_gain = ig
			reduced_contain_space = rcs
			reduced_not_contain_space = rncs
			feature_for_max_ig = feature
	root = Node()
	root.parent = Node()
	root.parent.feature = 9999
	root.feature = feature_for_max_ig
	root.category = point_estimate(from_space, feature_for_max_ig)
	root.information_gain = max_information_gain
	root.reduced_contain_space = reduced_contain_space
	root.reduced_not_contain_space = reduced_not_contain_space
	features_copy = list(features)
	features_copy.remove(feature_for_max_ig)
	root.reduced_to_features = features_copy
	priority_queue = [root]
	expanded_nodes = 0
	while expanded_nodes != 10:
		max_information_gain_left = -1
		feature_for_max_ig_left = 0
		reduced_contain_space_left = []
		reduced_not_contain_space_left = []
		max_information_gain_right = -1
		feature_for_max_ig_right = 0
		reduced_contain_space_right = []
		reduced_not_contain_space_right = []
		leaf_to_split = priority_queue[0]
		print "expanding: " + str(leaf_to_split.feature) + " with ig: " + str(leaf_to_split.information_gain)
		for to_feature in leaf_to_split.reduced_to_features:
			(igl, rcsl, rncsl) = information_gain(leaf_to_split.reduced_contain_space, to_feature)
			if igl > max_information_gain_left:
				max_information_gain_left = igl
				feature_for_max_ig_left = to_feature
				reduced_contain_space_left = rcsl
				reduced_not_contain_space_left = rncsl
			(igr, rcsr, rncsr) = information_gain(leaf_to_split.reduced_not_contain_space, to_feature)
			if igr > max_information_gain_right:
				max_information_gain_right = igr
				feature_for_max_ig_right = to_feature
				reduced_contain_space_right = rcsr
				reduced_not_contain_space_right = rncsr
		left_child = Node()
		left_child.parent = leaf_to_split
		left_child.feature = feature_for_max_ig_left
		left_child.category = point_estimate(leaf_to_split.reduced_contain_space, feature_for_max_ig_left)
		left_child.information_gain = max_information_gain_left
		left_child.reduced_contain_space = reduced_contain_space_left
		left_child.reduced_not_contain_space = reduced_not_contain_space_left
		features_copy = list(leaf_to_split.reduced_to_features)
		features_copy.remove(feature_for_max_ig_left)
		left_child.reduced_to_features = features_copy
		right_child = Node()
		right_child.parent = leaf_to_split
		right_child.feature = feature_for_max_ig_right
		right_child.category = point_estimate(leaf_to_split.reduced_not_contain_space, feature_for_max_ig_right)
		right_child.information_gain = max_information_gain_right
		right_child.reduced_contain_space = reduced_contain_space_right
		right_child.reduced_not_contain_space = reduced_not_contain_space_right
		features_copy = list(leaf_to_split.reduced_to_features)
		features_copy.remove(feature_for_max_ig_right)
		right_child.reduced_to_features = features_copy

		leaf_to_split.splitted = True
		leaf_to_split.left = left_child
		leaf_to_split.right = right_child
		expanded_nodes += 1

		test_outcome = test(root)
		print test_outcome
		ACCURACY.append(test_outcome)

		priority_queue.remove(leaf_to_split)
		priority_queue.append(left_child)
		priority_queue.append(right_child)
		priority_queue.sort(key = lambda leaf: leaf.information_gain, reverse = True)

	return root

#---------------------------------------------------------------------------------------------------------------------#

def test(dt):
	global TRAIN_TABLE
	global CATEGORY_INDEX
	correct = 0
	for doc in list(xrange(1, len(TRAIN_TABLE))):
		dt_copy = dt
		while dt_copy.splitted == True:
			if TRAIN_TABLE[doc][dt_copy.feature] == 0:
				dt_copy = dt_copy.right
			else:
				dt_copy = dt_copy.left
		if dt_copy.category == TRAIN_TABLE[doc][CATEGORY_INDEX]:
			correct += 1
	return correct / (len(TRAIN_TABLE)-1)

#---------------------------------------------------------------------------------------------------------------------#

def plot_graph():
	global ACCURACY
	graph = plot.figure()
	plot.plot(ACCURACY, 'r', label='Training Data')
	# plot.plot(test_data_accuracy_weighted, 'b', label='Test Data');
	plot.ylabel('Accuracy', fontsize = 16)
	plot.title('Information Gain')
	plot.legend()
	plot.axis([1, 100, 0.5, 1])
	graph.savefig('accuracy.jpg')

t = DTL()
plot_graph()