'''
CS337 Spring 2022 - Operating Systems Prof. Al Madi
Project 5 - Multitasking
serial_code_2.py
Matthew Bass
03/13/2022

This is a file to count the words and do other functions with the the
reddit's comments data

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

import numpy as np
from typing import Any, List

from word_count_objects import MaxWordCounts, VALID_DATA_TYPES, WordCount


'''
Helper FunctionS
'''


def checkDataType(data_type: str):
    '''
    This is a function to check the data types if the datatype is valid
    then nothing happens if it isnt the code exits

    :param data_type: string of data type being passes
    :return:
    '''
    if data_type.lower() not in VALID_DATA_TYPES:
        print(f"Error {data_type} is not a valid data type!!!\n" +
              f"Valid data_types are {VALID_DATA_TYPES}\n" +
              f"exiting from the code!!!")
        exit()


'''
Functions to parse the raw data and clean it
'''


def cleanDataList(raw_line_data: list) -> list:
    '''
    Function to clean the raw data from each file

    :param raw_line_data: list of raw data strings
    :return:
    '''

    clean_data = splitLinesList(raw_line_data)

    # making regex to look for word
    word_regex = re.compile("^[a-zA-Z]")
    # Filter out all words strings that are not begging with letters
    clean_data = list(filter(word_regex.match, clean_data))

    # Make all the filtered words lowercase
    clean_data = list(map(str.lower, clean_data))

    return clean_data


def splitLinesList(raw_line_data: list) -> list:
    '''
    This function splits the raw list of line strings into

    :param raw_line_data: list of raw data strings
    :return:
    '''
    raw_words_list = []
    for line in raw_line_data:
        raw_words_list += re.split("[^a-zA-Z0-9']", line)
    return raw_words_list


'''
Functions to create word maps and analize
'''


def createWordCountDict(data: list, debug: bool = False) -> dict:
    '''
    Create a word count dict from the data.

    :param data: a list of all the cleaned words
    :return: word_count: a word count dict of the file
    '''

    # Create a word count dict
    word_count = {}

    # Loop through the data and increment each word
    for word in data:
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1

        if debug:
            print(f"\nAdded {word} {word_count[word]}")

    return word_count


def sortWordCount(word_count: dict, sort_ord: str = "descending") -> dict:
    '''
    Sorts the word count dicts based on sort_ord
    :param word_count: the dict of word counts
    :param sort_ord: method to sort the dicts
    :return: sorted_word_count: the dictionary of sorted word counts
    '''

    word_count_list = list(word_count.items())

    # Sort the word_count_list based on sort_ord
    if sort_ord.lower() == "descending":
        word_count_list.sort(key=lambda x: x[1], reverse=True)

    sorted_word_count = dict(word_count_list)

    return sorted_word_count


def createWordCountHeap(
        data: list, sort_ord: str = "descending", debug: bool = False):
    '''
    Create a word count heap from the data.

    :param data: a list of all the cleaned words
    :param sort_ord: method to sort the dicts
    :param debug: if true debug printing will be done
    :return: word_count: a word count dict of the file
    '''

    if sort_ord == "descending":
        word_count = MaxWordCounts()

    # Loop through the data and increment each word
    for word in data:
        word_count.addWord(word)

    return word_count


def calcWordFrequencies(word_count: dict, data_type: str = "list") -> dict:
    '''
    This function calculates the word frequencies fot all the word count dicts

    :param word_count: a word count dict
    :param data_type: a str of the data type to use. Valid types list, np
    :return: word_count_freq: a dict of the word count and word frequency
    '''

    # Calculate the total number of words based on data type
    # and the frequencies
    # If base list
    if data_type == "list":

        wc_list = list(word_count.values())

        total_wc = sum(wc_list)
        word_freqs = [wc / total_wc for wc in wc_list]

        word_count_freq = {word: (count, freq) for (word, count, freq) in
                           zip(word_count.keys(), wc_list, word_freqs)}

    # If numpy
    elif data_type == "np":

        wc_array = np.array(word_count.values())

        total_wc = wc_array.sum()

        word_freqs = wc_array / total_wc

        word_count_freq = {word: (count, freq) for (word, count, freq) in
                           zip(word_count.keys(), wc_array, word_freqs)}

    return word_count_freq


def printTopWordCounts(sorted_word_counts: dict, top_n_words: int = 10):
    '''
    Prints out the top n number of words from the sorted word counts

    :param sorted_word_counts: The dictionary of sorted word counts
    :param top_n_words: the number of top words to print out
    :return:
    '''

    # Loop through each of the word count dicts and print them out
    for file_name, word_count in sorted_word_counts.items():
        printTopWords(file_name, word_count, top_n_words)

    return


def printTopWords(file_name: str, word_count: dict, top_n_words: int = 10):
    '''
    Prints tthe top N words from the wordcount file
    :param file_name: the name of the file
    :param word_count: the sorted word count data
    :param top_n_words: the top number of words to print
    :return:
    '''

    # Print out the intro for the file
    print(f"\n{file_name}'s top {top_n_words} words: ")
    print("\n\t rank.  word  :  count")

    # Loop through the top n number of words are print
    # until top_n words are printed
    words_printed = -1
    for word, count in word_count.items():

        words_printed += 1
        # If top n words have been printed return
        if top_n_words == words_printed:
            return

        print(f"\n\t {words_printed + 1}. {word} : {count}")


def printTopWordCountsFreqs(sorted_word_data: dict, top_n_words: int = 10):
    '''
    Prints out the top n number of words from the sorted word counts

    :param sorted_word_data: The dictionary of sorted word counts and
    frequencies
    :param top_n_words: the number of top words to print out
    :return:
    '''

    # Loop through each of the word count dicts and print them out
    for file_name, word_count in sorted_word_data.items():
        printTopWordsFreqs(file_name, word_count, top_n_words)

    return


def printTopWordsFreqs(
        file_name: str, sorted_word_data: dict, top_n_words: int = 10):
    '''
    Prints the top N words from the wordcount file
    :param file_name: the name of the file
    :param sorted_word_data: the sorted word  data
    :param top_n_words: the top number of words to print
    :return:
    '''

    # Print out the intro for the file
    print(f"\n{file_name}'s top {top_n_words} words: ")
    print("\n\t rank.\tword\t:\tcount\t:\tfrequency")

    # Loop through the top n number of words are print
    # until top_n words are printed
    words_printed = -1
    for word, data in sorted_word_data.items():

        words_printed += 1
        # If top n words have been printed return
        if top_n_words == words_printed:
            return

        print(f"\n\t {words_printed + 1}. {word} : {data[0]} : {data[1]}")


def printWordFreqOverYears(word_data: dict, word: str):
    '''
    Function to print the word frequency over the years
    :param word_data: the word data
    :param word: the word whos frequent you want to print
    :return:
    '''

    word = word.lower()

    # see if the word is in the word data at all
    word_in_year = [word in year_data.keys() for year_data in word_data]

    if True not in word_in_year:
        print(f"\nERROR {word} is not in any year!")
        return

    else:
        # Print the header
        print(f"\nThe frequency of {word} over the years:")

        for year, year_data, in_year in zip(word_data.keys(),
                                            word_data.values(),
                                            word_in_year):

            # get the year
            year = re.sub("[^0-9]", "", year)

            # if the word is in the year
            if in_year:
                print(f"\n\t{year}. {year_data[1]}")
            else:
                print(f"\n\t{year}. {0}")

        return


'''
Reading in Comments
'''


def readInRawDataNP(file_name: str, data_path: str) -> np.chararray:
    '''
    A function to read in the data of the file and
    returns the raw sting in a list data structure

    :param file_name: the name of the file
    :param data_path: the path to the file
    :return: raw_data: the raw data string of the file in a np char array
    '''

    with open(data_path + file_name, 'r') as file:
        data = file.readlines()
        data = np.chararray(data)
        return data


def readInRawDataList(file_name: str, data_path: str) -> List:
    '''
    A function to read in the data of the file and
    returns the raw sting in a list data structure

    :param file_name: the name of the file
    :param data_path: the path to the file
    :return: raw_data: the raw data string of the file in a List
    '''

    with open(data_path + file_name, 'r') as file:
        data = file.readlines()
        return data


def getWordData(data_file: str, data_path: str,
                data_type: str = "list"):
    '''
    Main running function to get all the word count data
    :param data_file: the name of the file
    :param data_path: the path to the file
    :param data_type: a str of the data type to use. Valid types list, np
    :return:
    '''

    # Read in data based on data type
    readInRawDataL_start_time = time.perf_counter()
    if data_type == "list":
        data = readInRawDataList(data_file, data_path)
    elif data_type == "np":
        data = readInRawDataNP(data_file, data_path)
    readInRawDataL_end_time = time.perf_counter()
    readInRawDataL_total_time = readInRawDataL_end_time - readInRawDataL_start_time
    print(f"\n{data_file} readInRawData ({data_type}) is done! " +
          f"\n\tIt took {readInRawDataL_total_time} sec(s) to run!\n")

    # Clean the data
    # TODO add ability to work with different data_types
    cleanDataList_start_time = time.perf_counter()
    data = cleanDataList(data)
    cleanDataList_end_time = time.perf_counter()
    cleanDataList_total_time = cleanDataList_end_time - cleanDataList_start_time
    print(f"\n{data_file} cleanDataList ({data_type}) is done! " +
          f"\n\tIt took {cleanDataList_total_time} sec(s) to run!\n")

    # TODO Create the word_count heap
    # word_count = createWordCountHeap(data)
    createWordCountDict_start_time = time.perf_counter()
    data = createWordCountDict(data)
    createWordCountDict_end_time = time.perf_counter()
    createWordCountDict_total_time = createWordCountDict_end_time - \
        createWordCountDict_start_time
    print(f"\n{data_file} createWordCountDict ({data_type}) is done! " +
          f"\n\tIt took {createWordCountDict_total_time} sec(s) to run!\n")

    # sort the word count
    sortWordCount_start_time = time.perf_counter()
    data = sortWordCount(data)
    sortWordCount_end_time = time.perf_counter()
    sortWordCount_total_time = sortWordCount_end_time - sortWordCount_start_time
    print(f"\n{data_file} sortWordCount ({data_type}) is done! " +
          f"\n\tIt took {sortWordCount_total_time} sec(s) to run!\n")

    # Calculate the frequencies
    calcWordFrequencies_start_time = time.perf_counter()
    data = calcWordFrequencies(data)
    calcWordFrequencies_end_time = time.perf_counter()
    calcWordFrequencies_total_time = sortWordCount_end_time - sortWordCount_start_time
    print(f"\n{data_file} calcWordFrequencies ({data_type}) is done! " +
          f"\n\tIt took {calcWordFrequencies_total_time} sec(s) to run!\n")

    # Print the top 10 words and frequencies
    printTopWordsFreqs(data_file, data)


def runWordCounter(data_type: str = "list") -> dict:
    '''
    Main function to run the word counter

    Timing of funtions will be done in nanoseconds

    :param data_type: a str of the data type to use. Valid types list, np, gpu
    :return: a dictionary of all the files raw strings
    '''

    # Check that valid data type has been passed
    data_type = data_type.lower()
    checkDataType(data_type)

    # Get the current file directory path of the file.
    dir_path = os.path.dirname(os.path.realpath(__file__))

    # Make the filepath the reddit comments (data) path

    data_path = os.path.join(dir_path, os.path.normcase("data/"))

    # Get all the data files
    data_files = os.listdir(data_path)

    # calculate the word data for each data file
    word_data = {}
    getWordData_start_time = time.perf_counter()
    for data_file in data_files:
        word_data[data_file] = getWordData(data_file, data_path, data_type)
    getWordData_end_time = time.perf_counter()
    getWordData_total_time = getWordData_end_time - getWordData_start_time
    print(f"\nWord Counter ({data_type}) is done! " +
          f"\n\tIt took {getWordData_total_time} sec(s) to run in total!\n")

    return


# Main function to run the script
def main():

    runWordCounter()
    return


if __name__ == "__main__":
    main()
