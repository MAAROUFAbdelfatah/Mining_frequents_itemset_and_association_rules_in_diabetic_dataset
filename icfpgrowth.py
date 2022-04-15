import itertools

class MISNode(object):
    """
        A node in the MIS tree.
    """

    def __init__(self, value, count, parent):
        """
            Create the node.
        """
        self.value = value
        self.count = count
        self.parent = parent
        self.link = None
        self.children = []

    def has_child(self, value):
        """
            Check if node has a particular child node.
        """
        for node in self.children:
            if node.value == value:
                return True

        return False

    def get_child(self, value):
        """
            Return a child node with a particular value.
        """
        for node in self.children:
            if node.value == value:
                return node

        return None

    def add_child(self, value):
        """
            Add a node as a child node.
        """
        child = MISNode(value, 1, self)
        self.children.append(child)
        return child

class MISHeader(object):
    """
        header table of the MIS tree
    """
    def __init__(self, value, MISValue):
        self.value = value
        self.MISValue = MISValue
        self.link = None

class MISTree(object):
    """
        A minimum item support tree.
    """
    def __init__(self, transactions, MISValues, root_value, root_count):
        self.items = MISValues
        self.headers =self.build_header_table(self.items)
        self.root = self.build_mis_tree(transactions, root_value, root_count, self.items, self.headers)


    @staticmethod
    def build_header_table(MISValues):
        """
            build a header table for the MIS tree
            Input: {}: dictionary with keys -> item name , values -> minimum item support
            Output: []: list of the MISHeader object.
        """
        headers = []

        items_names = list(MISValues.keys())

        for item_name in items_names:
            header = MISHeader(item_name, MISValues[item_name])
            headers.append(header)
        
        return headers
    
    def build_mis_tree(self, transactions, root_value, root_count, items, headers):
        """
            Build the mis tree .
            Input: transactions, root_value, root_count, items, headers
            Output: MISNode object as root of MIS tree.
        """
        root = MISNode(root_value, root_count, None)
        for transaction in transactions:
            sorted_items = [x for x in transaction if x in items]
            sorted_items.sort(key=lambda x: items[x], reverse=True)
            if len(sorted_items) > 0:
                self.insert_tree(sorted_items, root, headers)

        return root
    
    def insert_tree(self, items, node, headers):
        """
            Recursively grow MIS tree.
        """
        first = items[0]
        child = node.get_child(first)
        if child is not None:
            child.count += 1
        else:
            # Add new child.
            child = node.add_child(first)

            # Link it to header structure.
            for header in headers:
                if header.value == first:
                    if header.link is None:
                        header.link = child
                    else:
                        current = header.link
                        while current.link is not None:
                            current = current.link
                        current.link = child
        # Call function recursively.
        remaining_items = items[1:]
        if len(remaining_items) > 0:
            self.insert_tree(remaining_items, child, headers)

    def find_infrequent_item(self):
        """
            finding the infrequent items in the MIS tree
            Input: the MIS tree
            Output: []: list of infrequet item value
        """
        min_mis = min(self.items.values())

        hs = self.headers

        supports = []

        for h in hs:
            current = h.link
            counter = 0
            while current is not None:
                counter += current.count
                current = current.link
            if counter < min_mis:
                supports.append(h.value)
        return supports

    def mis_pruning(self, infrequent_items):
        """
            remove infrequent items from the MIS tree
            Input: []: list of infrequent items value,  infquent items in this step is MIS(item)<min(MIS(item1), MIS(item2), ....)
            Output: MIS tree without infrequent items
        """

        hs = self.headers
        removed_items ={} 

        for h in hs:
            if h.value in infrequent_items:
                current = h.link
                while current is not None:
                    current.parent.children += current.children
                    for child in current.children:
                        child.parent = current.parent
                    current.parent.children.remove(current)
                    current = current.link
                    h.link = None
                    removed_items[h]= None
        for item in removed_items.keys():
            hs.remove(item)

    def mis_mergeing(self):
        hs = self.headers
        for h in hs:
            current = h.link
            while current is not None and current.link is not None:
                if current.link != None and current.parent == current.link.parent:
                    current.count += current.link.count
                    current.children += current.link.children 
                    for child in current.link.children:
                        child.parent = current
                    current.parent.children.remove(current.link)
                    current.link = current.link.link
                    if current.link != None and current.parent != current.link.parent:
                        current = current.link
                else:
                    current = current.link
    
    def support(self, itemName):
        support = 0
        hs = self.headers

        for h in hs:
            if h.value == itemName:
                current = h.link
                while current is not None:
                    support += current.count
                    current = current.link
                break    
        return support  

    def infrequent_leaf_node_pruning(self):
        hs = self.headers
        for h in hs:
            current = h
            while current is not None and current.link is not None:
                if current.link.children == [] and self.support(current.link.value) < self.items[current.link.value]:
                    current.link.parent.children.remove(current.link)
                    current.link = current.link.link
                if current == None:
                    break
                current = current.link

    def conditional_mis_trees(self, h):
        current = h.link
        patterns_h = {}
        while current is not None:
            current_parent = current.parent
            pattern_h = current.value,
            current_count = current.count
            while current_parent.parent is not None:
                tmp_tuple = current_parent.value ,
                pattern_h += tmp_tuple
                current_parent = current_parent.parent
            current = current.link
            patterns_h[pattern_h] = current_count
        return patterns_h 
    
    def multiply(self, pattern):
        multi_pattern = []
        keys_list = list(pattern.keys())
        for key in keys_list:
            multi_pattern += [key for _ in range(pattern[key])]
        return multi_pattern

    def conditional_patterns(self):
        hs  = self.headers
        conditional_patterns = {}
        for h in hs:
            conditional_pattern_h = []
            conditional_tree = self.conditional_mis_trees(h)
            patterns = self.multiply(conditional_tree)
            for pattern in patterns:
                pattern_len = len(pattern)
                for i in range(1, pattern_len + 1):
                    conditional_pattern_h += itertools.combinations(pattern, i)
            new_conditional_pattern_h = []
            for h_pattern in conditional_pattern_h:
                    if h.value in h_pattern:
                        new_conditional_pattern_h.append(h_pattern)
            conditional_patterns[h.value] = new_conditional_pattern_h
        return conditional_patterns

    def combine(self, liste):
        result = {}
        for item in liste:
            if item in list(result.keys()):
                result[item] +=1 
            else:
                result[item] = 1
        return result

    
    def conditional_frequent_patterns(self):

        conditional_frequent_patterns = {}
        conditional_patterns = self.conditional_patterns()

        conditional_patterns_keys = list(conditional_patterns.keys())
        for key in conditional_patterns_keys:
            mis_value = self.items[key]
            conditional_pattern = self.combine(conditional_patterns[key])
            for key_cp in conditional_pattern.keys():
                if conditional_pattern[key_cp] >= mis_value:
                    conditional_frequent_patterns[key_cp] = conditional_pattern[key_cp] 
        return conditional_frequent_patterns

def generate_items_sets(transactions, mis_values):
    tree = MISTree(transactions, mis_values, None, None)
    #for header in tree.headers:
        #print("< name: "+header.value+", MIS value: "+str(header.MISValue)+", link: "+str(header.link)+" >")
    tree.mis_pruning(tree.find_infrequent_item())
    #for header in tree.headers:
        #print("< name: "+header.value+", MIS value: "+str(header.MISValue)+", link: "+str(header.link)+" >")
    tree.mis_mergeing()
    #for header in tree.headers:
        #print("< name: "+header.value+", MIS value: "+str(header.MISValue)+", link: "+str(header.link)+" >")
    tree.infrequent_leaf_node_pruning()
    return tree.conditional_frequent_patterns()

def generate_association_rules(patterns, confidence_threshold):
    """
        Given a set of frequent itemsets, return a dict
        of association rules in the form
        {(left): ((right), confidence)}
    """
    rules = {}
    for itemset in patterns.keys():
        upper_support = patterns[itemset]

        for i in range(1, len(itemset)):
            for antecedent in itertools.combinations(itemset, i):
                antecedent = tuple(sorted(antecedent))
                consequent = tuple(sorted(set(itemset) - set(antecedent)))

                if antecedent in patterns:
                    lower_support = patterns[antecedent]
                    confidence = float(upper_support) / lower_support

                    if confidence >= confidence_threshold:
                        rules[antecedent] = (consequent, confidence)

    return rules

""" def display_tree(self, root_children):
        for item in root_children:
            print([(itemm.value, itemm.count, itemm.parent.value) for itemm in root_children])
            if len(item.children) > 0:
                self.display_tree(list(item.children))
            else:
                print("--------------------")
                continue
"""
"""
    testing the headers static method 

headers = MISTree.build_header_table({'A':4, 'B':6, 'C':8, 'D':2})

for header in headers:
    print("< name: "+header.value+", MIS value: "+str(header.MISValue)+", link: "+str(header.link)+" >")
"""



"""
    testing the MIS tree before MIS_Pruning and MIS_Merge, incompact MIS tree static method.
"""
"""
tran = [['a', 'c'],
        ['a', 'c', 'b'],
        ['a', 'c', 'g'],
        ['a', 'c', 'h'],
        ['a', 'd', 'b'],
        ['f', 'e'],
        ['f', 'e'],
        ['d', 'e'],
        ['b', 'd'],
        ['b', 'd']
]

mis_values = {'a': 5, 'b': 5, 'c': 5, 'd': 4, 'f': 2, 'e': 2, 'g': 2, 'h': 2}

tree = MISTree(tran, mis_values, None, None)
print(tree.display_tree(tree.root.children))

headers = tree.headers

for header in headers:
    print("< name: "+header.value+", MIS value: "+str(header.MISValue)+", link: "+str(header.link)+" >")
  
"""
    #testing the find infrequent items method.
"""
print(tree.find_infrequent_item())

"""
    #testing the mis_pruning(self, infrequent_items) method.
"""
print("mis_pruning")
tree.mis_pruning(tree.find_infrequent_item())
print(tree.display_tree(tree.root.children))

headers = tree.headers

for header in headers:
    print("< name: "+header.value+", MIS value: "+str(header.MISValue)+", link: "+str(header.link)+" >")

"""
    #testing the def mis_mergeing(self) method.
"""
print("mis_mergeing")
tree.mis_mergeing()
print(tree.display_tree(tree.root.children))


"""
    #testing the def infrequent_leaf_node_pruning(self) method.
"""
print("infrequent_leaf_node_pruning")
tree.infrequent_leaf_node_pruning()
print(tree.display_tree(tree.root.children))


headers = tree.headers

for header in headers:
    print("< name: "+header.value+", MIS value: "+str(header.MISValue)+", link: "+str(header.link)+" >")

"""
    #testing the conditional_mis_trees(self) method.
"""
#cond = tree.conditional_mis_trees()
#print(cond)

"""
    #testing the conditional_patterns(self): method.
"""
con = tree.conditional_patterns()
print(con)

print("conditional_frequent_patterns(self)")
print(tree.conditional_frequent_patterns())

print(tree.generate_association_rules(tree.conditional_frequent_patterns(), 0))"""