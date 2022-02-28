'''
CS337 Spring 2022 - Operating Systems Prof. Al Madi
Project 3 - Preemptive CPU Scheduling Analysis
RBTree.py
Matthew Bass
02/28/2022

A Red Black Tree in python (used here for Completely fair scheduling)
'''
import numpy as np


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
        self.nil = RBNode(0)
        self.root = self.nil
        self.min_vruntime = self.root
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

    def fix_insert(self, val):
        '''
        Helper function for insert and makes sure all the properties of an RB
        tree are still valid after insertion

        :param val: (Node) the node value to be inserted
        :return:
        '''

        return


    def rotate_left(self, node):
        '''
        Rotates the node specified in the tree to the left.

        :param node:
        :return:
        '''

        return

    def rotate_right(self, node):
        '''
        Rotates the node specified in the tree to the right.

        :param node:
        :return:
        '''

        return










def main():
    return

if __name__ == "__main__":
    main()
