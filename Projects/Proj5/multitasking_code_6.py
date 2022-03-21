'''
CS337 Spring 2022 - Operating Systems Prof. Al Madi
Project 5 - Multitasking
multitasking_code_6.py
Matthew Bass
03/13/2022

This is a file to count the words and do other functions with the the
reddit's comments data. It is based off my fastest serial code which is
serial_code_4.py In this file I attempt to make it faster than
multitasking_code_4.py and 5. This is also an experiment to see if the little
bit of multiprocessing I do is more valuable in terms of time saving when I
parallelize just cleaning the word data and not getting the word count data
from every file.


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
import numpy as np
from concurrent.futures import ProcessPoolExecutor
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
    with open(data_path + data_file, 'r') as file:
        data = file.read()
    return data


def cleanAndTokenize(data: str) -> list:
    '''
    A Function to clean and tokenize the raw string
    Args:
        data (str): the raw string of the data

    Returns:
        tokens (list): a list of the cleaned word tokens

    '''
    # Make all the filtered words lowercase
    data = list(map(str.lower, data))

    # keep only words
    data = re.sub(r"[^a-z\s]+", "", data).split(" ")



    return data


def cleanAndTokenizeMultiProcess(data: str, process_count: int = None) -> list:
    '''
    A Function to clean and tokenize the raw string
    It  uses multi processing by splitting the string data into batches
    Args:
        data (str): the raw string of the data
        process_count (int): the number of processes to use

    Returns:
        tokens (list): a list of the cleaned word tokens


    '''

    # Make process count default number of process
    # that machine has if no numbers are passed
    if process_count is None:
        print(f"\nError no process count was entered!!")
        print(f"Setting process_count to machines core count {os.cpu_count()}!")
        process_count = os.cpu_count()

    # Remove extra spaces, tabs, and line breaks
    # by splitting the data and also setting it up for multiprocessing
    data = data.split()


    # Set up data for Multiprocessing
    # set up multiprocessing  chunks to run the function
    chunck = len(data) / process_count

    mp_data = []
    for process in range(process_count):
        chunck_start = int(process * chunck)
        chunck_end = int((process * chunck) + chunck)
        mp_data.append(data[chunck_start:chunck_end])

    with ProcessPoolExecutor(process_count) as p:
        results = p.map(cleanDataList, mp_data, np.arange(len(mp_data)+1))


    # Make the cleaned data by concatting all the lists
    clean_data = list(itertools.chain.from_iterable(results))


    # keep only words
    data = re.sub(r"[^A-Za-z\s]+", "", data).split(" ")
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
    data = readInData(data_file, data_path)
    data = cleanAndTokenize(data)
    return Counter(data)


def getWordCountMultiProcess(data_file: str, data_path: str,
                             process_count: int = None) -> Counter:
    '''
    A Function to get the word count from specified file uses multiprocessing by
    splitting up the the words into batches

    Args:
        data_file (str): the name of the file
        data_path (str): the path to the file

    Returns:
        word_count(Counter): A counter of the files word count


    '''

    data = readInData(data_file, data_path)
    data = cleanAndTokenizeMultiProcess(data, process_count)
    return Counter(data)


def getWordFrequencies(word_count: Counter) -> dict:
    '''
    A Function to get the word frequency from the counter

    Args:
        word_count (Counter):

    Returns:
        word_frequencies (dict): a dict of the word frequencies
    '''
    # Initialize word frequencies dict
    word_frequencies = {}

    # Get the total word count
    total_count = sum(word_count.values())

    for word, count in word_count.items():
        word_frequencies[word] = (count / total_count)

    return word_frequencies


def getWordDataMultiProcess(data_file: str, data_path: str,
                            process_count: int = None,
                            debug: bool = True) -> dict:
    '''
    Main running function to get all the word count data
    :param data_file: the name of the file
    :param data_path: the path to the file
    :param process_count: the number of processes to use
    :param debug: Bool if true debug staatement printed

    :return word_data: a tuple of the word counts and word frequencies
    '''
    # Make process count default number of process
    # that machine has if no numbers are passed
    if process_count is None:
        print(f"\nError no process count was entered!!")
        print(f"Setting process_count to machines core count {os.cpu_count()}!")
        process_count = os.cpu_count()

    if debug:
        t_start_time = time.perf_counter()
        print(f"START getWordData {data_file} pid : {os.getpid()}")

    # Get the word counter
    word_count = getWordCountMultiProcess(data_file, data_path, process_count)

    if debug:
        t_end_time = time.perf_counter()
        t_total_time = t_end_time - t_start_time
        print(f"\nEND getWordData {data_file} pid : {os.getpid()}! " + f"\n\tIt took {t_total_time} sec(s) to run in total!\n")

    # Get the word frequencies
    word_frequencies = getWordFrequencies(word_count)

    # Make the word data object
    word_data = (word_count, word_frequencies)

    return word_data


def printTopNWords(files_data: dict, top_n_words: int = 10):
    '''
    A Function to print out the top N words over the years
    Args:
        files_data ():
        top_n_words ():

    Returns:


    '''

    # Get the top words from all the years
    top_words = {}
    for file_name, data in files_data.items():
        n_words = data[0].most_common(top_n_words)

        top_words[re.sub("[^0-9]", "", file_name)] = n_words

    print(f"\nThe top {top_n_words} words for each year (word, count)")
    print(f"In Order Top: {[x + 1 for x in range(top_n_words)]}")
    for year, tw in top_words.items():
        print(f"{year.upper()}. {tw}")

    return


def printWordFrequencyOverYears(files_data: dict, word: str):
    '''
    A Function to print out the top N words over the years
    Args:
        files_data (dict): the dict of word data
        word (str): the word whos frequency to print out

    Returns:

    '''

    # Get the word frequency from over the years
    word_freq = {}
    for file_name, data in files_data.items():
        word_freqs = data[1]

        # If the word is in the frequencies for that year add it
        if word in word_freqs.keys():

            word_freq[re.sub("[^0-9]", "", file_name)] = word_freqs[word]

        # if it isnt the frequency is 0
        else:
            word_freq[re.sub("[^0-9]", "", file_name)] = 0

    # Print the Header
    print(f"\n The frequency of {word} over the years is:")
    print(f"\t {word_freq}")
    return


def runWordCounter(thread_count: int = None, process_count: int = None,
                   debug: bool = True) -> dict:
    '''
    Main function to run the word counter

    Timing of functions will be done in seconds

    Args:
        thread_count (int): the number of threads to use
        process_count (int): the number of processes to use
        debug (bool): if true debug print statements will be displayed

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

    files_data = {}
    for data_file in data_files:
        files_data[data_file] = getWordDataMultiProcess(data_file,
                                                        data_path,
                                                        process_count)

    getWordData_end_time = time.perf_counter()
    getWordData_total_time = getWordData_end_time - getWordData_start_time
    print(f"\nWord Counter  is done! " + f"\n\tIt took {getWordData_total_time} sec(s) to run in total!\n")

    # Print the top 10 words
    printTopNWords(files_data)

    # Print word frequency of the
    printWordFrequencyOverYears(files_data, "the")

    return


# Main function to run the script
def main():
    runWordCounter()
    return


if __name__ == "__main__":
    main()