'''
CS337 Spring 2022 - Operating Systems Prof. Al Madi
Project 3 - Preemptive CPU Scheduling Analysis
RBTree.py
Matthew Bass
02/28/2022

A Red Black Tree in python (used here for Completely fair scheduling)
'''
import numpy as np
from igraph import Graph, EdgeSeq
import plotly.graph_objects as go
import sys


class RBNode:
    '''
    This is a node that makes up the RB tree
    '''

    def __init__(self, key, parent = None, l_child = None,
                 r_child = None, is_red = False):
        '''

        :param key: the value of the node (this will be the vruntime of a process in CFS)
        :param parent: (RBNode) Reference to parent node
        :param l_child: (RBNode) Reference to left child node
        :param r_child: (RBNode) Reference to right child node
        :param is_red: (bool) if the Node is Red (if false node is black)
        '''

        # Defining private properties
        self.__key = key
        self.__parent = parent
        self.__l_child = l_child
        self.__r_child = r_child
        self.__is_red = is_red

        return

    # Defining getters
    @property
    def key(self):
        return self.__key

    @property
    def parent(self):
        return self.__parent

    @property
    def l_child(self):
        return self.__l_child

    @property
    def r_child(self):
        return self.__r_child

    @property
    def is_red(self):
        return self.__is_red

    #making setters

    @key.setter
    def key(self, val):
        self.__key = val
        return

    @parent.setter
    def parent(self, val):
        self.__parent = val
        return

    @l_child.setter
    def l_child(self, val):
        self.__l_child = val
        return

    @r_child.setter
    def r_child(self, val):
        self.__r_child = val
        return

    @is_red.setter
    def is_red(self, val):
        self.__is_red = val
        return





class RBTree:
    '''
       This is the main RB Tree
       '''

    def __init__(self):
        '''
        Initilizes an RB Tree with a nil node with value zero, and color
        black (self.nil = RBNode(0)). nil as the root and min_vruntime
        '''
        self.__non_nil_node_amt = int(0)

        self.__nil = RBNode(0)
        self.__root = self.nil
        self.__min_vruntime = self.root


        return

    # getters
    @property
    def nil(self):
        return self.__nil
    @nil.setter
    def nil(self, val):
        self.__nil = val
        return

    @property
    def root(self):
        return self.__root

    @property
    def min_vruntime(self):
        return self.__min_vruntime

    @property
    def non_nil_node_amt(self):
        return self.__non_nil_node_amt

    #setters

    @root.setter
    def root(self, val):
        self.__root = val
        return


    @min_vruntime.setter
    def min_vruntime(self, val):
        self.__min_vruntime = val
        return



    @non_nil_node_amt.setter
    def non_nil_node_amt(self, val):
        self.__non_nil_node_amt = val
        return






    def insert(self, val):
        '''
        Insersts a RBNode in the RB tree in the correct position based on the val

        :param val: the val of the RBNode to be inserted
        :return:
        '''



        #make the val a node
        val = RBNode(val)

        # Set y to the nil node and x to the root
        y = self.nil
        x = self.root

        #if x is not node increment non_nil_node_amt
        if x != self.nil:
            self.non_nil_node_amt += 1

        # while the root is not nill traverse the tree
        # and compare the values of the nodes
        while x != self.nil:
            y = x

            # Now compare the key of the insertion val and node we are at
            if val.key < x.key:
                x = x.l_child
            else:
                x = x.r_child

        #set the parent after postion found
        val.parent = y

        # Set root based on y
        if y == self.nil:
            self.root = val
        else:
            if val.key < y.key:
                y.l_child = val
            else:
                y.r_child = val

        # Set val left and right child and color
        val.l_child = self.nil
        val.r_child = self.nil
        val.is_red = True

        #run the value through insert fixup
        self.fix_insert(val)


        return

    def fix_insert(self, node):
        '''
        Helper function for insert and makes sure all the properties of an RB
        tree are still valid after insertion

        :param node: (Node) the node value to be inserted
        :return:
        '''

        # while(node's parent is Red)
        while node.parent.is_red:

            # cases change slightly depending on if the uncle is left or right
            if node.parent == node.parent.parent.l_child:

                # get the nodes uncle
                uncle = node.parent.parent.r_child

                # if the uncle is red
                if uncle.is_red:
                    # color parent and uncle black
                    uncle.is_red = False
                    node.parent.is_red = False

                    # color grandparent red
                    node.parent.parent = True

                    # set node to grandparent
                    node = node.parent.parent

                # else if it black
                else:
                    #if (triangle)
                    if node == node.parent.r_child:
                        # set node to parent
                        node = node.parent

                        # rotate to parent
                        self.rotate_left(node)


                    # color parent of node black
                    node.parent.is_red = False

                    # color grandparent of node red
                    node.parent.parent.is_red = True

                    # rotate grand parent of node
                    self.rotate_right(node.parent.parent)


            else:

                # get the nodes uncle
                uncle = node.parent.parent.l_child

                # if the uncle is red
                if uncle.is_red:
                    # color parent and uncle black
                    uncle.is_red = False
                    node.parent.is_red = False

                    # color grandparent red
                    node.parent.parent.is_red = True

                    # set node to grandparent
                    node = node.parent.parent

                # else if it black
                else:
                    # if (triangle)
                    if node == node.parent.l_child:
                        # set node to parent
                        node = node.parent

                        # rotate to parent
                        self.rotate_right(node)

                    # color parent of node black
                    node.parent.is_red = False

                    # color grandparent of node red
                    node.parent.parent.is_red = True

                    # rotate grand parent of node
                    self.rotate_left(node.parent.parent)

            if node == self.root:
                break

        #color the root black
        self.root.is_red = False

        return


    def rotate_left(self, node):
        '''
        Rotates the node specified in the tree to the left.

        :param node: (Node) The node to be rotates
        :return:
        '''

        # Y = Right child of node
        y = node.r_child
        # Change right child of node to left child of y
        node.r_child = y.l_child
        if y.l_child != self.nil:
            y.l_child.parent = node

        # Change parent of y as parent of x
        y.parent = node.parent

        # If parent of node == nil ie. root node
        if node.parent == self.nil:

            # Set y as root
            self.root = y
        else:
            # if node is a left child then adjust x's parent's left child
            if node == node.parent.l_child:
                node.parent.l_child = y
            # adjust nodes's parent's right child
            else:
                node.parent.r_child = y

        y.l_child = node

        # the parent of node is now y
        node.parent = y

        return

    def rotate_right(self, node):
        '''
        Rotates the node specified in the tree to the right.

        :param node: (Node) The node to be rotates
        :return:
        '''

        # y now points to node to left of node
        y = node.l_child

        # y's right subtree becomes nodes's left subtree
        y.r_child = node.l_child

        # right subtree of y gets a new parent
        if y.r_child != self.nil:
            y.r_child.parent = node

        # y's parent is now node's parent
        y.parent = node.parent

        # set root based on the node parent
        if node.parent == self.nil:
            self.root = y
        else:
            # if node is a left child then adjust x's parent's left child
            if node == node.parent.l_child:
                node.parent.l_child = y
            # adjust nodes's parent's right child
            else:
                node.parent.r_child = y

        # the right child of y is now node
        y.r_child = node

        # the parent of node is now y
        node.parent = y

        return


    def __repr__(self):
        '''
        Printing function for RB_tree
        :return:
        '''

        return self.print_tree()



    def print_tree(self):
        '''
        Printing function for RB tree that can be called
        :return:
        '''
        # nr_vertices = self.non_nil_node_amt
        # v_label = list(map(str, range(nr_vertices)))
        # G = Graph.Tree(nr_vertices, 2)  # 2 stands for children number
        # lay = G.layout('rt')

        self.print_tree_helper(self.root, "", True)

        return

    def print_tree_helper(self, node, indent, last):
        '''
        Recursive helper function for print tree
        :param node: (RBNode) node that is being printed
        :param indent: (string) sting representation of tree to be printed
        :param last: (Bool) if the code is the last node in the tree
        :return:
        '''
        if node != self.nil:
            sys.stdout.write(indent)
            if last:
                sys.stdout.write("R----")
                indent += "     "
            else:
                sys.stdout.write("L----")
                indent += "|    "

            s_color = "RED" if node.is_red else "BLACK"
            print(str(node.key) + "(" + s_color + ")")
            self.print_tree_helper(node.l_child, indent, False)
            self.print_tree_helper(node.r_child, indent, True)
        return




#main testing for RB tree
def main():
    test_tree = RBTree()

    test_tree.insert(val=1)
    test_tree.insert(val = 2)
    test_tree.insert(3)
    test_tree.insert(4)
    test_tree.insert(7)
    test_tree.insert(6)
    test_tree.insert(8)
    test_tree.insert(9)
    test_tree.insert(10)

    print(test_tree)

    return

if __name__ == "__main__":
    main()
