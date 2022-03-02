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
from dataclasses import dataclass, field
from typing import Any


@dataclass(order=True)
class RBNode:
    '''
    This is a node that makes up the RB tree

    :param key: the value of the node (this will be the vruntime of a process in CFS)
    :param parent: (RBNode) Reference to parent node
    :param l_child: (RBNode) Reference to left child node
    :param r_child: (RBNode) Reference to right child node
    :param is_red: (bool) if the Node is Red (if false node is black)
    '''
    key: Any = field(compare=True)
    parent: "RBNode" = field(default=None, compare=False)
    l_child: "RBNode" = field(default=None, compare=False)
    r_child: "RBNode" = field(default=None, compare=False)
    is_red: bool = field(default=False, compare=False)


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

        self.nodes_list = []

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

    @property
    def tree_height(self):
        return self.get_height(self.root)

    # setters

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

    '''
    General functions for RBtree
    '''

    '''
    Searching and comparisons
    '''

    def search(self, val):
        '''
        Searches for the value in the RB Tree and returns till if not there
        :param val:
        :return:
        '''

        val = RBNode(val)

        node = self.root
        while node != self.nil:
            if node == val:
                break

            if node <= val:
                node = node.r_child
            else:
                node = node.l_child

        if node == self.nil:
            print("Cannot find key in the tree")

        return node

    def minimum(self, node):
        '''
        Gets minimum node of the nodes subtree
        :param node:
        :return:
        '''
        while node.l_child != self.nil:
            node = node.l_child
        return node

    def maximum(self, node):
        '''
        Gets maximum node of the nodes subtree
        :param node:
        :return:
        '''
        while node.r_child != self.nil:
            node = node.r_child
        return node


    '''
    Inserting and Deleting
    '''

    def insert(self, val):
        '''
        Insersts a RBNode in the RB tree in the correct position based on the val

        :param val: the val of the RBNode to be inserted
        :return:
        '''



        # make the val a node
        val = RBNode(val)


        self.nodes_list.append(val)

        # see if the node value is greater than the min v runtime
        # and if it is update the min v runtime
        if val < self.min_vruntime or self.min_vruntime is self.nil:
            self.min_vruntime = val

        # Set y to the nil node and node to the root
        y = self.nil
        node = self.root

        # if val is not node increment non_nil_node_amt
        if val != self.nil:
            self.non_nil_node_amt += 1

        # while the root is not nill traverse the tree
        # and compare the values of the nodes
        while node != self.nil:
            y = node

            # Now compare the key of the insertion val and node we are at
            if val.key < node.key:
                node = node.l_child
            else:
                node = node.r_child

        # set the parent after postion found
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

        # run the value through insert fixup
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
                    # if (triangle)
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

        # color the root black
        self.root.is_red = False

        return

    def delete_fix(self, fix_node):
        '''
        Helper method for delete to fix RB tree properties
        :param self:
        :param fix_node:
        :return:
        '''
        # while the fix_node is not root or red
        while fix_node != self.root and not fix_node.is_red:

            # if the fix_node is the left child
            if fix_node == fix_node.parent.l_child:

                # Get the sibling
                sib = fix_node.parent.r_child

                # Case 1: the sibling is red.
                if sib.is_red:
                    sib.is_red = False
                    fix_node.parent.is_red = True
                    self.rotate_left(fix_node.parent)
                    sib = fix_node.parent.r_child

                # Case 2: the sibling is black and its children are black.
                if not sib.l_child.is_red and not sib.r_child.is_red:
                    sib.color.is_red = True
                    fix_node = fix_node.parent

                # Cases 3 and 4: the sibling is black and one of
                # its child is red and the other is black.
                else:

                    # Case 3: the sibling is black and its left child is red.
                    if not sib.r_child.is_red:
                        sib.l_child.is_red = False
                        sib.is_red = True
                        self.rotate_right(sib)
                        sib = fix_node.parent.r_child

                    # Case 4: the sibling is black and its right child is red.
                    sib.is_red = fix_node.parent.is_red
                    fix_node.parent.is_red = False
                    sib.r_child.is_red = False
                    self.rotate_left(fix_node.parent)

                    # move to the root to terminate the loop.
                    fix_node = self.root

                # If the fix_node is the right child
            else:
                # Get the sibling
                sib = fix_node.parent.l_child

                # Case 1: the sibling is red.
                if sib.is_red:
                    sib.is_red = False
                    fix_node.parent.is_red = True
                    self.rotate_right(fix_node.parent)
                    sib = fix_node.parent.l_child

                # Case 2: the sibling is black and its children are black.
                if not sib.r_child.is_red and not sib.r_child.is_red:
                    sib.is_red = True
                    fix_node = fix_node.parent

                # Cases 3 and 4: the sibling is black and one of
                # its child is red and the other is black.
                else:

                    # Case 3: the sibling is black and its left child is red.
                    if not sib.l_child.is_red:
                        sib.r_child.is_red = False
                        sib.is_red = True
                        self.rotate_left(sib)
                        sib = fix_node.parent.l_child

                    # Case 4: the sibling is black and its right child is red.
                    sib.is_red = fix_node.parent.is_red
                    fix_node.parent.is_red = False
                    sib.l_child.is_red = False
                    self.rotate_right(fix_node.parent)

                    # move to the root to terminate the loop.
                    fix_node = self.root

        # Make the fix_node being fixed black
        fix_node.is_red = False

        return

    def delete(self, val):
        '''


        :param val:
        :return:
        '''

        delete_node = self.search(val)

        if delete_node == self.nil:
            print("Cannot find key in the tree")
            return

        #Remove the delete node from the nodes list
        self.nodes_list.remove(delete_node)

        rem_node = delete_node
        original_color = rem_node.is_red

        # Case 1: no children or Case 2a: only one right child
        if delete_node.l_child == self.nil:
            replacing_node = delete_node.r_child
            self.transplant_nodes(delete_node, delete_node.r_child)

        # Case 2b: only one left child
        elif (delete_node.r_child == self.nil):
            replacing_node = delete_node.l_child
            self.transplant_nodes(delete_node, delete_node.l_child)


        # Case 3: two children
        else:
            rem_node = self.minimum(delete_node.r_child)
            original_color = rem_node.color
            replacing_node = rem_node.r_child
            if rem_node.parent == delete_node:
                replacing_node.parent = rem_node
            else:
                self.transplant_nodes(rem_node, rem_node.r_child)
                rem_node.r_child = delete_node.r_child
                rem_node.r_child.parent = rem_node

            self.transplant_nodes(delete_node, rem_node)
            rem_node.l_child = delete_node.l_child
            rem_node.l_child.parent = rem_node
            rem_node.is_red = delete_node.is_red

        if original_color == False:
            self.delete_fix(replacing_node)

    def transplant_nodes(self, delete_node: RBNode, replacing_node: RBNode):
        '''
        This is a function to transplant the replacing node with the node to
        be deleted

        :param delete_node:
        :param replacing_node:
        :return:
        '''
        if delete_node.parent == None:
            self.root = replacing_node
        elif delete_node == delete_node.parent.l_child:
            delete_node.parent.l_child = replacing_node
        else:
            delete_node.parent.r_child = replacing_node

        replacing_node.parent = delete_node.parent

        return


    def remove_min_vruntime(self) -> int:
        '''
         method that removes the node with the smallest vruntime in the tree
         and updates min_vruntime in constant time. The method should
         maintain all the properties of a RB-Tree.

        :return: (int) min vruntime
        '''


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

    '''
    Node info functions for RBtree
    '''

    def get_level(self, node: RBNode) -> int:
        '''
        A function to find the depth (level) for any node
        in the RB Tree ()


        :param node: (RBNode) the node in the tree whos depth you want to find
        :return: (int) height of the node
        '''

        # Set depth to 0
        depth = 0

        # set the initial check node to node
        check_node = node

        # kepp moving up levels until root is reached
        while check_node.parent != self.nil:
            depth += 1
            check_node = check_node.parent

        return depth

    def get_height(self, node: RBNode) -> int:
        '''
        A function to find the height for any node(subtree)
        in the RB Tree ()


        :param node: (RBNode) the node in the tree whos height you want to find
        :return: (int) height of the node
        '''

        # If the node is not nil
        if node != self.nil:

            # If both the left and right children are nodes take the max
            # height from both subtrees
            if node.l_child != self.nil and node.r_child != self.nil:
                return (max(self.get_height(node.l_child),
                            self.get_height(node.r_child)) + 1)

            # else if the left child is a node
            elif node.l_child != self.nil:
                return self.get_height(node=node.l_child) + 1

            # else if the right child is a node
            elif node.r_child != self.nil:
                return self.get_height(node=node.r_child) + 1

            # else return 1 if only one node
            else:
                return 1

        # else return 0 if null
        return 0


    '''
    Display and output functions for RBtree
    '''

    def display_tree(self):
        '''
        This is a function to show a visualization of the tree
        :return:
        '''

        # get max nodes for all levels and
        # make a dictionary of all the nodes on each level
        max_nodes = 0
        levels = {}
        for num in range(self.get_height(self.root)):

            # add tp calculation of the max node
            max_nodes += 2**(num)

            # create a level at that depth
            levels[f"{num}"] = []

            # loop through all the nodes in the node list and add ones
            # at that depth to the level
            for node in self.nodes_list:
                depth_of_node = self.get_level(node)
                if self.get_level(node) == num:
                    levels[f"{num}"].append(node)



        # make a tree that can hold all levels of nodes
        gTree = Graph.Tree(max_nodes,
                           children = 2)
        # make the tree layout
        positions = {k: {"node": None,
                        "pos": gTree.layout("rt")[k],
                        "level":int(gTree.layout("rt")[k][1])}  for k in range(
            max_nodes)}



        # loop through all the nodes in every level
        # and add them to positions
        for level in levels:
            for node in levels[level]:

                # get the nodes already placed
                nodes_placed = [p['node'] for p in positions.values() if p[
                    'node'] is not None ]

                # get positions at levels that are available
                aval_pos = []
                for pos in positions:
                    val = positions[pos]
                    if val["level"] == int(level) and val["node"] is None:
                        aval_pos.append(pos)

                # see if the parent for the node has been placed
                # should only be true for the root
                if node.parent not in nodes_placed:

                    # ifparent doesnt exist place node in avalible level position
                    positions[aval_pos[0]]["node"] = node

                # Else if the parent does exist
                else:

                    # getting the parent node
                    parent = [(key,value) for key,value in positions.items()
                              if value['node'] == node.parent ][0]

                    # get the keys that match the level
                    parent_level_keys = [key for key,value in positions.items()
                              if value['level'] == parent[1]["level"]]

                    # get the next level keys
                    next_level_keys = [key for key, value in positions.items()
                                         if int(value['level']) == int(
                            parent[1]["level"])+1]


                    parent_pos = parent_level_keys.index(parent[0]) + 1


                    # now chose the key for the node based on if it is
                    # the right or left child of the parent
                    if node == node.parent.r_child:
                        node_tree_pos = next_level_keys[2 * parent_pos -1]
                    elif node == node.parent.l_child:
                        node_tree_pos = next_level_keys[2 * (parent_pos-1)]

                    positions[node_tree_pos]["node"] = node



        # clean the postions list to only values only with nodes
        positions = dict([(key,value) for key,value in positions.items()
                              if value['node'] is not None ])



        # Set up vars for graphing

        # Get the max level
        M = self.get_height(self.root)-1


        # Get the edges and clean them
        E = [e.tuple for e in gTree.es]
        E = list(filter(lambda x: x[0] in positions.keys() and \
                                   x[1] in positions.keys(), E))

        # set up edges for graphing
        Xe = []
        Ye = []
        for edge in E:
            Xe += [positions[edge[0]]["pos"][0], positions[edge[1]]["pos"][0],
                   None]
            Ye += [2 * M - positions[edge[0]]["level"], 2 * M - positions[edge[
                1]]["level"],
                   None]


        # making the cordinates for the nodes
        # split into red and y group
        r_positions = dict([(key,value) for key,value in positions.items()
                              if value['node'].is_red ])
        b_positions = dict([(key, value) for key, value in positions.items()
                              if not value['node'].is_red])

        r_Xn = [r_positions[k]["pos"][0] for k in r_positions.keys()]
        r_Yn = [2 * M - r_positions[k]["pos"][1] for k in r_positions.keys()]

        b_Xn = [b_positions[k]["pos"][0] for k in b_positions.keys()]
        b_Yn = [2 * M - b_positions[k]["pos"][1] for k in
                    b_positions.keys()]



        # make the labels for the plot
        b_labels = [str(val["node"].key) for val in b_positions.values()]
        r_labels = [str(val["node"].key) for val in r_positions.values()]
        labels = [str(val["node"].key) for val in positions.values()]


        # Make the plot
        fig = go.Figure()

        # plot edges
        fig.add_trace(go.Scatter(x=Xe,
                                 y=Ye,
                                 mode='lines',
                                 line=dict(color='rgb(210,210,210)', width=1),
                                 hoverinfo='none'
                                 ))

        # plot black nodes
        fig.add_trace(go.Scatter(x=b_Xn,
                                 y=b_Yn,
                                 mode='markers',
                                 name='black',
                                 marker=dict(symbol='circle-dot',
                                             size=18,
                                             color='black',  # '#DB4551',
                                             line=dict(color='rgb(50,50,50)',
                                                       width=1)
                                             ),
                                 text=b_labels,
                                 hoverinfo='text',
                                 opacity=0.8
                                 ))
        # plot red nodes
        fig.add_trace(go.Scatter(x=r_Xn,
                                 y=r_Yn,
                                 mode='markers',
                                 name='red',
                                 marker=dict(symbol='circle-dot',
                                             size=18,
                                             color='red',  # '#DB4551',
                                             line=dict(color='rgb(50,50,50)',
                                                       width=1)
                                             ),
                                 text=r_labels,
                                 hoverinfo='text',
                                 opacity=0.8
                                 ))
        axis = dict(showline=False,
                    # hide axis line, grid, ticklabels and  title
                    zeroline=False,
                    showgrid=False,
                    showticklabels=False,
                    )

        fig.update_layout(title=f'RB Tree (Height: {self.get_height(self.root)}',
                          annotations=self.make_annotations(labels,
                                                       M, positions),
                          font_size=12,
                          showlegend=False,
                          xaxis=axis,
                          yaxis=axis,
                          margin=dict(l=40, r=40, b=85, t=100),
                          hovermode='closest',
                          plot_bgcolor='rgb(248,248,248)'
                          )
        fig.show()

        print(1)
        return

    def make_annotations(self, labels, M, positions, font_size=10,
                         font_color='rgb(250,250,250)'):
        '''
        A helper function for display tree to make annotations

        :param labels: labels to be added
        :param M: (int) The max level
        :param positions: the positions list
        :param font_size:  (int) the font size
        :param font_color:(rgb) color of the text
        :return:
        '''

        if len(labels) != len(positions.keys()):
            raise ValueError('The lists pos and labels must have the same len')
        annotations = []
        for k, val in enumerate(positions.keys()):
            annotations.append(
                dict(
                    text=labels[k],
                    # or replace labels with a different list for the text within the circle
                    x=positions[val]['pos'][0], y=2 * M - positions[val]["level"],
                    xref='x1', yref='y1',
                    font=dict(color=font_color, size=font_size),
                    showarrow=False)
            )
        return annotations

    def print_tree(self):
        '''
        Printing function for RB tree that can be called
        :return:
        '''
        # nr_vertices = self.non_nil_node_amt
        # v_label = list(map(str, range(nr_vertices)))
        # G = Graph.Tree(nr_vertices, 2)  # 2 stands for children number
        # lay = G.layout('rt')

        sys.stdout.write("ROOT\n")
        return self.print_tree_helper(self.root, "", True)

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

    def __repr__(self) -> str:
        """Provie the tree representation to visualize its layout."""
        if (self.root is None) or (self.root == self.nil):
            return "empty tree"
        return (
            f"tree_height={str(self.get_height(self.root))}, Num Nodes = "
            f"{self.non_nil_node_amt}, Min_Vruntime = {self.min_vruntime.key}\n"
            f"{type(self)},\n root={self.root} "
        )






# main testing for RB tree
def main():
    test_tree = RBTree()


    test_tree.insert(val=1)

    test_tree.insert(val = 2)

    test_tree.insert(3)

    test_tree.insert(4)

    test_tree.insert(5)
    test_tree.insert(6)
    test_tree.insert(7)
    test_tree.insert(8)
    test_tree.insert(9)
    test_tree.insert(10)





    test_tree.print_tree()

    # test_tree.display_tree()

    test_tree.delete(3)

    test_tree.display_tree()

    '''Testing get level'''
    # print(test_tree.get_level(test_tree.root))
    # print(test_tree.get_level(test_tree.nodes_list[5]))
    # print(test_tree.get_level(test_tree.nodes_list[0]))
    # print(test_tree.get_level(test_tree.nodes_list[8]))
    # print(test_tree.get_level(test_tree.nodes_list[9]))

    # test_nil_node = RBNode(0)
    # test_nil1_node = RBNode(0)
    # test_2_node = RBNode(2)
    # test_3_node = RBNode(3)
    #
    # print(test_nil_node == test_nil1_node)
    # print(test_2_node == test_3_node)
    # print(test_2_node < test_3_node)
    return

if __name__ == "__main__":
    main()
