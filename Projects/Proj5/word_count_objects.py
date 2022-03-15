'''
CS337 Spring 2022 - Operating Systems Prof. Al Madi
Project 5 - Multitasking
word_count_objects.py
Matthew Bass
03/15/2022

This is a file to hold all the classes and objects for the word counter scripts
'''
from functools import total_ordering

import numpy as np

from max_min_heaps import MaxHeap, MinHeap
from dataclasses import dataclass, field

'''
GLobal variables
'''

VALID_DATA_TYPES = ["list", "np", "gpu"]

'''
Classes
'''


@total_ordering
class WordCount:
    '''
    This a class to hold the word count

    :param word: the word of the wordcount
    '''
    def __init__(self,
                 word : str = "word",
                 count : int = 1):
        self.word = word
        self.count = count
        return

    def __eq__(self, other):
        return ((self.count, self.word) == (other.count, other.word))

    def __ne__(self, other):
        return not (self == other)

    def __lt__(self, other):
        return ((self.count, self.word) > (other.count, other.word))

    def __repr__(self):
        return "WC( %s , %s )" % (self.word, self.count)


class MaxWordCounts(MinHeap):
    def __init__(self):
        self.h = []

        return

    @property
    def words(self):
        word_list = [wc.word for wc in self.h]
        return word_list


    def addWord(self ,word :str, debug : bool = False):
        '''
        Adds word to wordcount heap
        :param word:
        :return:
        '''
        if word in self.words:
            wc = self.removeWordCount(word)
            wc.count +=1
            self.heappush(wc)
            if debug:
                print(f"\nAdded {wc}")
        else:

            wc = WordCount(word)
            self.heappush(wc)
            if debug:
                print(f"\nAdded New {wc}")

        return

    def removeWordCount(self, word : str, debug : bool = True) -> WordCount:
        '''
        Functions to remove word count object based on string
        :param word:
        :return:
        '''
        # Get the words in the heap
        words = np.array(self.words)

        # Get the index
        wc_index = np.array(np.where(words == word)).min()


        return self.h.pop(wc_index)









# Main function to run the script
def main():
    return


if __name__ == "__main__":
    main()