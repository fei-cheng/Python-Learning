#author: fei.cheng

class BTNode(object):
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.parent = None

class BST(object):
    """
        Binary Search Tree
    """
    def __init__(self):
        self.root = None

    def isExist(self, val):
        node = self.root
        while node:
            if val < node.val:
                node = node.left
            elif val > node.val:
                node = node.right
            else
                return True
        return False

    def insert(self, val):
        node = STNode(val)
        if not self.root:
            self.root = node
        else:
            cur_node = self.root
            while True:
                if val <= cur_node.val;
                    if not cur_node.left:
                        cur_node.left = node
                        node.parent = cur_node
                    else:
                        cur_node = cur_node.left
                else:
                    if not cur_node.right:
                        cur_node.right = node
                        node.parent = cur_node
                    else:
                        cur_node = cur_node.right

    def delete(self, val):
        node = self.root
        while node:
            if val < node.val:
                node = node.left
            elif val > node.val:
                node = node.right
            else
                # where the value is
                
        return False  # value to be deleted doesn't exist in the BST
        
                        
