'''
CS337 Spring 2022 - Operating Systems Prof. Al Madi
Project 5 - Multitasking
serial_code_4.py
Matthew Bass
03/13/2022

This is a file to count the words and do other functions with the the
reddit's comments data (This is to compare the speed of cleaning data,
This was done another way as compared to serial_code_3.py) From testing this
way of cleaning data is definitely quicker while leading to the same results.

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
from collections import Counter

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


def cleanAndTokenize(data : str, debug : bool = True) -> list:
    '''
    A Function to clean and tokenize the raw string
    Args:
        data (str): the raw string of the data
        debug (bool): if true debug printing statements will be output

    Returns:
        tokens (list): a list of the cleaned word tokens

    '''
    if debug:
        t_start_time = time.perf_counter()

    # Make all the characters lowercase (this is much quicker than doing it
    # after the fact when the words are split)
    data = data.lower()

    # Remove extra spaces, tabs, and line breaks
    data = " ".join(data.split())

    # keep only words
    data = re.sub(r"[^a-z\s]+", "", data).split(" ")


    if debug:
        t_end_time = time.perf_counter()
        t_total_time = t_end_time - t_start_time
        print(f"\ncleanAndTokenize is done! " + f"\n\tIt took {t_total_time} sec(s) to run in total!\n")



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


def getWordFrequencies(word_count : Counter) -> dict:
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




def getWordData(data_file: str, data_path: str, debug = True) -> dict:
    '''
    Main running function to get all the word count data
    :param data_file: the name of the file
    :param data_path: the path to the file
    :param debug: Bool if true debug staatement printed

    :return word_data: a tuple of the word counts and word frequencies

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

    # Get the word frequencies
    word_frequencies = getWordFrequencies(word_count)

    # Make the word data object
    word_data = (word_count, word_frequencies)

    return word_data


def printTopNWords(files_data: dict, top_n_words: int = 10):
    '''
    A Function to print out the top N words over the years
    Args:
        files_data (dict): the dict of word data
        top_n_words (int): the top n words to print out

    Returns:

    '''

    # Get the top words from all the years
    top_words = {}
    for file_name, data in files_data.items():
        n_words = data[0].most_common(top_n_words)

        top_words[re.sub("[^0-9]", "", file_name)] = n_words

    print(f"\nThe top {top_n_words} words for each year (word, count)")
    print(f"In Order Top: {[x+1 for x in range(top_n_words)]}")
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

        #if it isnt the frequency is 0
        else:
            word_freq[re.sub("[^0-9]", "", file_name)] = 0

    # Print the Header
    print(f"\n The frequency of {word} over the years is:")
    print(f"\t {word_freq}")
    return


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
    files_data = {}
    getWordData_start_time = time.perf_counter()
    for data_file in data_files:
        files_data[data_file] = getWordData(data_file,data_path)
    getWordData_end_time = time.perf_counter()
    getWordData_total_time = getWordData_end_time - getWordData_start_time
    print(f"\nWord Counter  is done! " +
          f"\n\tIt took {getWordData_total_time} sec(s) to run in total!\n")

    # Print the top 10 words
    printTopNWords(files_data)

    # Print word frequency of the
    printWordFrequencyOverYears(files_data,"the")

    return


# Main function to run the script
def main():



    runWordCounter()
    return


if __name__ == "__main__":
    main()
