import itertools


class MISNode(object):
    """
    A node in the FP tree.
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
    

class MISTree(object):
    """
    A frequent pattern tree.
    """

    def __init__(self, transactions, mis_values, root_value, root_count):
        """
        Initialize the tree.
        """
        self.mis_values = mis_values
        self.transactions_supp = self.items_support(transactions)#self.find_frequent_items(transactions, threshold)
        self.headers = self.build_header_table(self.transactions_supp)
        self.root = self.build_mis_tree(
            transactions, root_value,
            root_count, self.transactions_supp, self.headers)
    @staticmethod
    def items_support(transactions):
        """
        Create a dictionary of items with occurrences above the threshold.
        """
        items = {}

        for transaction in transactions:
            for item in transaction:
                if item in items:
                    items[item] += 1
                else:
                    items[item] = 1

        return items

    @staticmethod
    def build_header_table(transactions):
        """
        Build the header table.
        """
        headers = {}
        for key in transactions.keys():
            headers[key] = None
        return headers

    def build_mis_tree(self, transactions, root_value,
                     root_count, mis_values, headers):
        """
        Build the FP tree and return the root node.
        """
        root = MISNode(root_value, root_count, None)

        for transaction in transactions:
            sorted_items = [x for x in transaction]
            sorted_items.sort(key=lambda x: mis_values[x], reverse=True)
            if len(sorted_items) > 0:
                self.insert_tree(sorted_items, root, headers)
        return root

    def insert_tree(self, items, node, headers):
        """
        Recursively grow FP tree.
        """
        first = items[0]
        child = node.get_child(first)
        if child is not None:
            child.count += 1
        else:
            # Add new child.
            child = node.add_child(first)

            # Link it to header structure.
            if headers[first] is None:
                headers[first] = child
            else:
                current = headers[first]
                while current.link is not None:
                    current = current.link
                current.link = child

        # Call function recursively.
        remaining_items = items[1:]
        if len(remaining_items) > 0:
            self.insert_tree(remaining_items, child, headers)

    def min_mis_value(self):
        mis_values = list(self.mis_values.values())
        return min(mis_values)

    def infrequent_items(self):
        threshold = self.min_mis_value()
        keys = list(self.transactions_supp.keys())
        return [key for key in keys if self.transactions_supp[key] < threshold]
    
    def mis_pruning(self, root_children, infrequent_item):
        
        for item in root_children:
            #print(item.value)
            #print([(itemm.value, itemm.count, itemm.parent.value) for itemm in root_children])
            if item.value == infrequent_item:
                #print("find")
                item.parent.children += item.children
                for child in item.children:
                    child.parent = item.parent
                item.parent.children.remove(item)
            if len(item.children) > 0:
                self.mis_pruning(list(item.children), infrequent_item)
            else:
                continue

    
    def mis_mergeing(self, root_children):
        for item in root_children:
            if len(item.children) > 0:
                same = self.children_same_item_name(item.children)
                item.children=self.merge(item.children, same)
                self.mis_mergeing(item.children)

    def merge(self, children, same):
        if len(children) > 0:
            keys = same.keys()
            for key in keys:
                for i in range(1, len(same[key])):
                   # print(i)
                    #print("=====")
                    #print(same[key][i])
                    children[same[key][0]].count += children[same[key][i]].count
                    children[same[key][0]].children += children[same[key][i]].children
            holder = []
            for key in keys:
                holder += same[key][1:]
            #print(same[key][1:])
            children = self.del_list_indexes(children, holder)
        return children

    def del_list_indexes(self, l, id_to_del):
        #somelist = [i for j, i in enumerate(l) if j not in id_to_del]
        counter = 0
        for i in range(len(l)):
            if i in id_to_del:
                del l[i - counter]
                counter += 1
        
        return l
        

    def children_same_item_name(self, children):
        same = {}
        children_len = len(children)
        checked = []
        for i in range(children_len - 1):
            for j in range(i + 1, children_len):
                if children[i].value == children[j].value and children[i].value not in checked:
                    if same.get(children[i].value) != None:
                        same[children[i].value] += [j] 
                    else:
                        same[children[i].value] = [i, j]
            checked += children[i].value
        return same

    def display_tree(self, root_children):
        for item in root_children:
            print([(itemm.value, itemm.count, itemm.parent.value) for itemm in root_children])
            if len(item.children) > 0:
                self.display_tree(list(item.children))
            else:
                print("--------------------")
                continue


tran = [['a', 'c', 'd', 'f'],
        ['a', 'c', 'e', 'f', 'g'],
        ['a', 'b', 'c', 'f', 'h'],
        ['b', 'f', 'g'],
        ['b', 'c']
]

mis_values = {'a': 4, 'b': 4, 'c': 4, 'd': 3, 'e': 3, 'f': 2, 'g': 2, 'h': 2}

tree = MISTree(tran, mis_values, None, None)

sup = tree.items_support(tran)
print(sup)

header = tree.build_header_table(sup)
print(header)
root = tree.build_mis_tree(tran, None,
                     None, mis_values, tree.headers)
print([(item.value, item.count, item.parent.value) for item in root.children])
print({item for item in tree.headers})
print({item.count for item in tree.headers.values()})
print(tree.min_mis_value())
print(tree.infrequent_items())
for in_item in tree.infrequent_items():
    print(tree.mis_pruning(list(root.children), in_item))
print(tree.display_tree(root.children))

node1 = MISNode('f', 1, 'e')
node2 = MISNode('t', 4, 'e')
node3 = MISNode('f', 5, 'e')
node4 = MISNode('f', 6, 'e')
node5 = MISNode('t', 4, 'e')

print(tree.children_same_item_name([node1, node2, node3, node4, node5]))

merge = tree.merge([node1, node2, node3, node4, node5], tree.children_same_item_name([node1, node2, node3, node4, node5]))

print([value.value for value in merge])

print(tree.mis_mergeing(root.children))
print(tree.display_tree(root.children))
print({item for item in tree.headers})
print({item.count for item in tree.headers.values()})