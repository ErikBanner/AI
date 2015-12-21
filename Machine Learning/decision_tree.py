import math
import matplotlib.pyplot as plt

MAX_NUM_NODE = 100
class_map = {
    "1": "alt.atheism",
    "2": "comp.graphics",
}

# information gain type
INFO_GAIN_AVG = 0
INFO_GAIN_WEIGHTED = 1

words = []
train_data_accuracy_weighted = []
test_data_accuracy_weighted = []
train_data_accuracy_avg = []
test_data_accuracy_avg = []

class DTNode:
	def __init__(self):
		"""
		Decision Tree Node
	    Attributes:
	        split_word_id: the word_id choose to split the tree (word_id for the node)
	        class_type: None if not leaf, otherwise, either class "1" or class "2"
	        docs: documents for this node
	        labels: labels corresponding to the docs
	        information_gain: information gain calculate for this word
	        left_child, right_child: DTNode
	    """
		self.split_word_id = None
		self.class_type = None
		self.docs = []
		self.labels = []
		self.information_gain = None
		self.split_word_id = None
		# word with split_word_id absent
		self.left_child = None
		# word with split_word_id present
		self.right_child = None

	def set_split_word_id(self, word_id):
		self.split_word_id = word_id

	def set_information_gain(self, ig):
		self.information_gain = ig

	def set_class_type(self, class_type):
		self.class_type = class_type

	def set_docs(self, docs):
		self.docs = docs

	def set_labels(self, labels):
		self.labels = labels

	def set_left_child(self, left_child):
		self.left_child = left_child

	def set_right_child(self, right_child):
		self.right_child = right_child

	def is_leaf(self):
		return self.class_type != None

	def get_leaves(self):
		if self.is_leaf():
			return [self]
		else:
			leaves = []
			for leaf in self.left_child.get_leaves():
				leaves.append(leaf)
			for leaf in self.right_child.get_leaves():
				leaves.append(leaf)
			return leaves

# build the decision tree by maintaining a priority queue of leaves
def build_decision_tree(words, train_labels, train_data_sparse, test_labels, test_data_sparse, ig_type):
	num_of_nodes = 1

	# root node
	# information_gains servers as a priority queue, use get_max(igs) to get best feature id (word_id)
	information_gains = []
	for word_id in range(len(words)):
		ig = information_gain(train_labels, word_id, train_data_sparse, ig_type)
		information_gains.append(ig)
	# best feature
	split_word_id = get_max(information_gains)
	print "Selected word : %s (%f)" % (words[split_word_id], information_gains[split_word_id])

	# create root node with two leaves (children)
	root = DTNode()
	left_child = DTNode()
	right_child = DTNode()
	root.set_split_word_id(split_word_id)
	root.set_left_child(left_child)
	root.set_right_child(right_child)
	root.set_information_gain(information_gains[split_word_id])
	
	# left child - word absent
	# right child - word present
	left_child_docs = []
	left_child_labels = []
	right_child_docs = []
	right_child_labels = []
	for doc_id in range(len(train_data_sparse)):
		doc = train_data_sparse[doc_id]
		label = train_labels[doc_id]
		if doc[split_word_id] == 0:
			left_child_docs.append(doc)
			left_child_labels.append(label)
		else:
			right_child_docs.append(doc)
			right_child_labels.append(label)

	left_child.set_labels(left_child_labels)
	left_child.set_docs(left_child_docs)
	left_child.set_class_type(predict_child_class_type(train_data_sparse, train_labels, split_word_id, 0))
	right_child.set_labels(right_child_labels)
	right_child.set_docs(right_child_docs)
	right_child.set_class_type(predict_child_class_type(train_data_sparse, train_labels, split_word_id, 1))

	# perform accuracy test with the root node
	if ig_type == INFO_GAIN_WEIGHTED:
		train_data_accuracy_weighted.append(accuracy_test(root, train_labels, train_data_sparse))
		test_data_accuracy_weighted.append(accuracy_test(root, test_labels, test_data_sparse))
	else:
		train_data_accuracy_avg.append(accuracy_test(root, train_labels, train_data_sparse))
		test_data_accuracy_avg.append(accuracy_test(root, test_labels, test_data_sparse))

	# generate MAX_NUM_NODE-1 nodes
	while num_of_nodes < MAX_NUM_NODE:
		# get all the leaves
		leaves = root.get_leaves()

		# information gains for all leaves, select the best feature from this list
		leaves_information_gains = []
		for leaf in leaves:
			if leaf.information_gain == None:
				# informaion gain for a single leaf
				information_gains = []
				for word_id in range(len(words)):
					ig = information_gain(leaf.labels, word_id, leaf.docs, ig_type)
					information_gains.append(ig)

				split_word_id = get_max(information_gains)
				leaf.set_split_word_id(split_word_id)
				leaf.set_information_gain(information_gains[split_word_id])

		leaves_information_gains = [leaf.information_gain for leaf in leaves]
		leaves_information_gains.append(leaf.information_gain)

		# selecte a leave with most information gain
		selected_leaf_index = get_max(leaves_information_gains)
		selected_leaf = leaves[selected_leaf_index]
		selected_leaf.set_class_type(None)
		print "Selected word : %s (%f)" % (words[selected_leaf.split_word_id], selected_leaf.information_gain)

		# create left and right children for the selected node
		left_child = DTNode()
		right_child = DTNode()
		selected_leaf.set_left_child(left_child)
		selected_leaf.set_right_child(right_child)

		left_child_docs = []
		left_child_labels = []
		right_child_docs = []
		right_child_labels = []
		for doc_id in range(len(selected_leaf.docs)):
			doc = selected_leaf.docs[doc_id]
			label = selected_leaf.labels[doc_id]
			if doc[selected_leaf.split_word_id] == 0:
				left_child_docs.append(doc)
				left_child_labels.append(label)
			else:
				right_child_docs.append(doc)
				right_child_labels.append(label)

		left_child.set_labels(left_child_labels)
		left_child.set_docs(left_child_docs)
		left_child.set_class_type(predict_child_class_type(left_child_docs, left_child_labels, selected_leaf.split_word_id, 0))
		right_child.set_labels(right_child_labels)
		right_child.set_docs(right_child_docs)
		right_child.set_class_type(predict_child_class_type(right_child_docs, right_child_labels, selected_leaf.split_word_id, 1))

		# perform a new accuracy test with the new tree
		if ig_type == INFO_GAIN_WEIGHTED:
			train_data_accuracy_weighted.append(accuracy_test(root, train_labels, train_data_sparse))
			test_data_accuracy_weighted.append(accuracy_test(root, test_labels, test_data_sparse))
		else:
			train_data_accuracy_avg.append(accuracy_test(root, train_labels, train_data_sparse))
			test_data_accuracy_avg.append(accuracy_test(root, test_labels, test_data_sparse))

		num_of_nodes += 1

	return root

# test the accuracy with the given sparse data and corresponding labels
def accuracy_test(root, labels, data_sparse):
	correct_count = 0
	for doc_id in range(len(data_sparse)):
		tmp_root = root
		doc = data_sparse[doc_id]
		while not tmp_root.is_leaf():
			if doc[tmp_root.split_word_id] == 0:
				tmp_root = tmp_root.left_child
			else:
				tmp_root = tmp_root.right_child

		if tmp_root.class_type == labels[doc_id]:
			correct_count += 1

	return float(correct_count) / len(labels)

def print_tree(root, level, present):
	present_str = "No:"
	if present:
		present_str = "Yes:"
	if level == 0:
		present_str = ""

	if not root.is_leaf():
		print " " * level, present_str, "%s, information gain (%f)" % (words[root.split_word_id], root.information_gain)
		print_tree(root.left_child, level+1, False)
		print_tree(root.right_child, level+1, True)
	else:
		print " " * level, present_str, "class %s (%s)" % (root.class_type, class_map[root.class_type])

# predict the leaf class type for a leaf node
def predict_child_class_type(train_data_sparse, labels, word_id, branch_value):
	class_one_count = 0
	class_two_count = 0
	for doc_id in range(len(labels)):
		if train_data_sparse[doc_id][word_id] == branch_value:
			if labels[doc_id] == '1':
				class_one_count += 1
			else:
				class_two_count += 1

	if class_one_count > class_two_count:
		return '1'
	else:
		return '2'

# calculate infomation gain for the word with word_id and information gain type ig_type
def information_gain(labels, word_id, train_data_sparse, ig_type):
	num_class_one = labels.count('1')
	num_class_two = labels.count('2')
	if num_class_one == 0 and num_class_two == 0:
		return 0.0

	prob_y = float(num_class_one) / (num_class_one + num_class_two) 
	total_information = entropy(prob_y)

	information_gain = total_information

	branch_value = [0,1]
	for branch in branch_value:
		child_num_class_one = 0
		child_num_class_two = 0

		for doc_id in range(len(train_data_sparse)):
			if train_data_sparse[doc_id][word_id] == branch:
				if labels[doc_id] == '1':
					child_num_class_one += 1
				else:
					child_num_class_two += 1

		Ni = child_num_class_one + child_num_class_two
		N = num_class_one + num_class_two

		if Ni != 0:
			if ig_type == INFO_GAIN_WEIGHTED:
				information_gain -= float(Ni) / N * entropy(float(child_num_class_one)/Ni)
			else:
				information_gain -= 0.5 * entropy(float(child_num_class_one)/Ni)

	return information_gain

def entropy(prob):
	if prob * (1-prob) == 0:
		return 0
	return -1 * (prob * math.log(prob, 2) + (1-prob) * math.log(1-prob, 2))

# helper function
def get_max(list):
	max_val = max(list)
	return list.index(max_val)

# load data
def load_data_and_labels():
    with open('datasets/words.txt', 'r') as f:
        for line in f:
            words.append( line.split()[0] )

    train_data = []
    with open('datasets/trainData.txt', 'r') as f:
        for line in f:
            digits = [int(x) for x in line.split()] 
            train_data.append(digits)

    train_labels = []
    with open('datasets/trainLabel.txt', 'r') as f:
        for line in f:
            train_labels.append(line.split()[0])
    
    test_data = []
    with open('datasets/testData.txt', 'r') as f:
        for line in f:
            digits = [int(x) for x in line.split()]
            test_data.append( digits )
    
    test_labels = []
    with open('datasets/testLabel.txt', 'r') as f:
        for line in f:
            test_labels.append(line.split()[0])
      
    return [words, train_data, train_labels, test_data, test_labels]

# convert trainData and testData into sparse matrices
def sparse(num_col, num_row, data):
    data_sparse = [[0] * num_col for i in range(num_row)]
    for i in data:
    	doc_id = i[0]
    	word_id = i[1]
        data_sparse[doc_id-1][word_id-1] = 1
    
    return data_sparse

def main():
	# load data and labels
	[words, train_data, train_labels, test_data, test_labels] = load_data_and_labels()
	# convert trainData and testData into sparse matrices
	train_data_sparse = sparse(len(words), len(train_labels), train_data)
	test_data_sparse = sparse(len(words), len(test_labels), test_data)

	# build tree with weighted info gain
	root = build_decision_tree(words, train_labels, train_data_sparse, test_labels, test_data_sparse, INFO_GAIN_WEIGHTED)
	print_tree(root, 0, True)

	# plot figure 2
	plt.subplot(212)
	plt.plot(test_data_accuracy_avg, 'b', label='trainData');
	plt.plot(train_data_accuracy_avg, 'g', label='testData');
	plt.ylabel('Accuracy test', fontsize = 14);
	plt.title('(a)')
	plt.legend();
	plt.axis([1, 110, 0, 1])
	# plot figure 1
	figure = plt.figure()
	plt.subplot(211)
	plt.plot(test_data_accuracy_weighted, 'b', label='trainData');
	plt.plot(train_data_accuracy_weighted, 'g', label='testData');
	plt.ylabel('accuracy test', fontsize = 14);
	plt.title('(b)')
	plt.legend();
	plt.axis([1, 110, 0, 1])

	# build tree with average info gain
	root = build_decision_tree(words, train_labels, train_data_sparse, test_labels, test_data_sparse, INFO_GAIN_AVG)
	print_tree(root, 0, True)



	# save figure
	figure.savefig('accuracy.jpg');

if __name__ == "__main__":
	main()