'''
CS337 Spring 2022 - Operating Systems Prof. Al Madi
Project 5 - Multitasking
serial_code_4.py
Matthew Bass
03/13/2022

This is a file to count the words and do other functions with the the
reddit's comments data

Another version much more simplified

Refactored to process all the files one at a time

It does the following:
    - Read in the Reddit comments files

    - Count each word

    - Print the 10 most common words in each file

    - Print the frequency of a given word in each year to observe word trends
      (frequency = word_count / number_of_words)

    - Time your “common word” and “word trend” code reliably for comparison
'''
import heapq
import os
import re
import time
from collections import Counter
import numpy as np
from typing import Any, List

from word_count_objects import MaxWordCounts,VALID_DATA_TYPES,WordCount


'''
Helper FunctionS
'''



'''
Functions to parse the raw data and clean it
'''


def readInData(data_file: str, data_path: str) -> str:
    '''
    A Function to read in the raw data from the file as a string

    Args:
        data_file (str): the name of the file
        data_path (str): the path to the file

    Returns:
        data (str): the raw string of the data

    '''
    with open(data_path+data_file, 'r') as file:
        data = file.read()
    return data


def cleanAndTokenize(data : str) -> list:
    '''
    A Function to clean and tokenize the raw string
    Args:
        data (str): the raw string of the data

    Returns:
        tokens (list): a list of the cleaned word tokens

    '''
    data = re.sub(r"[^A-Za-z0-9\s]+", "", data).split(" ")
    return data


def getWordCount(data_file: str, data_path: str) -> Counter:
    '''
    A Function to get the word count from specified file

    Args:
        data_file (str): the name of the file
        data_path (str): the path to the file

    Returns:
        word_count(Counter): A counter of the files word count


    '''
    data = readInData(data_file,data_path)
    data = cleanAndTokenize(data)
    return Counter(data)



def getWordData(data_file: str, data_path: str, debug = True) -> dict:
    '''
    Main running function to get all the word count data
    :param data_file: the name of the file
    :param data_path: the path to the file
    :param debug: Bool if true debug staatement printed

    :return:
    '''


    if debug:
        t_start_time = time.perf_counter()
        print(f"START getWordData {data_file}")

    # Get the word counter
    word_count = getWordCount(data_file,data_path)

    if debug:
        t_end_time = time.perf_counter()
        t_total_time = t_end_time - t_start_time
        print(f"\nEND getWordData {data_file}! " +
              f"\n\tIt took {t_total_time} sec(s) to run in total!\n")

    return word_count




def runWordCounter() -> dict:
    '''
    Main function to run the word counter

    Timing of funtions will be done in nanoseconds

    :param data_type: a str of the data type to use. Valid types list, np, gpu
    :return: a dictionary of all the files raw strings
    '''


    # Get the current file directory path of the file.
    dir_path = os.path.dirname(os.path.realpath(__file__))

    # Make the filepath the reddit comments (data) path

    data_path = os.path.join(dir_path, os.path.normcase("data/"))

    # Get all the data files
    data_files = os.listdir(data_path)

    #calculate the word data for each data file
    word_data = {}
    getWordData_start_time = time.perf_counter()
    for data_file in data_files:
        word_data[data_file] = getWordData(data_file,data_path)
    getWordData_end_time = time.perf_counter()
    getWordData_total_time = getWordData_end_time - getWordData_start_time
    print(f"\nWord Counter  is done! " +
          f"\n\tIt took {getWordData_total_time} sec(s) to run in total!\n")

    return


# Main function to run the script
def main():


    runWordCounter()
    return


if __name__ == "__main__":
    main()
