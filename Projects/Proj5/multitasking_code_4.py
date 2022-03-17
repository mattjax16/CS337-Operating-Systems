'''
CS337 Spring 2022 - Operating Systems Prof. Al Madi
Project 5 - Multitasking
multitasking_code_4.py
Matthew Bass
03/13/2022

This is a file to count the words and do other functions with the the
reddit's comments data. It is based off my fastest serial code which is
serial_code_4.py

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

import os
import re
import time
import multiprocessing
from collections import Counter
from itertools import repeat

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




def runWordCounter(thread_count: int = None,
                   process_count: int = None,
                   debug: bool = True) -> dict:
    '''
    Main function to run the word counter

    Timing of funtions will be done in nanoseconds

    :param data_type: a str of the data type to use. Valid types list, np, gpu
    :return: a dictionary of all the files raw strings
    '''

    # Check that process number and thread count are there
    if thread_count is None:
        print(f"\nError no thread count was entered!!")
        print(f"Setting thread_count to machines core count {os.cpu_count()}!")
        thread_count = os.cpu_count()
    if process_count is None:
        print(f"\nError no process count was entered!!")
        print(f"Setting process_count to machines core count {os.cpu_count()}!")
        process_count = os.cpu_count()

    # if Debug print the function and pid
    if debug: print(f"\nrunWordCounter pid : {os.getpid()}")


    # Get the current file directory path of the file.
    dir_path = os.path.dirname(os.path.realpath(__file__))

    # Make the filepath the reddit comments (data) path

    data_path = os.path.join(dir_path, os.path.normcase("data/"))

    # Get all the data files
    data_files = os.listdir(data_path)

    getWordData_start_time = time.perf_counter()

    # Set up data for starmap pool function
    proc_args = list(zip(data_files, repeat(data_path)))

    # Use the process pool context manager to start multiprocess pool with
    # desired number of processes
    with multiprocessing.Pool(process_count) as p:
        word_data_list = p.starmap(getWordData, proc_args)

    # Make the word count dicts
    word_data = {}
    for data_file, dat in zip(data_files, word_data_list):
        word_data[data_file] = dat


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
