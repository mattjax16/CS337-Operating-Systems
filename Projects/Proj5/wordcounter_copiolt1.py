'''
This is a script to count all the words in the files in data/ .
It will time how long each function takes if debug is set to true
'''


# Imports
import os
import time
import sys
import re
import string




def main():
    '''
    This is the main function that will call all the other functions
    '''
    # Get the path to the data folder
    path = os.path.join(os.getcwd(), 'data')
    # Get the list of files in the data folder
    files = os.listdir(path)
    # Create a dictionary to store the word counts
    word_counts = {}
    # Loop through the files
    for file in files:
        # Get the path to the file
        file_path = os.path.join(path, file)
        # Get the word counts for the file
        word_counts[file] = get_word_counts(file_path)
    # Print the word counts
    print_word_counts(word_counts)



def get_word_counts(file_path, debug = True):
    '''
    This function will get the word counts for a file

    Args:
        file_path (object): the path to the file
        debug (bool): boolean to determine if debug is on or off
    '''
    # Get the start time
    start_time = time.time()
    # Open the file
    file = open(file_path, 'r')
    # Get the text from the file
    text = file.read()
    # Close the file
    file.close()
    # Get the word counts
    word_counts = get_word_counts_from_text(text)
    # Get the end time
    end_time = time.time()
    # Print the time taken
    if debug:
        print('Time taken to get word counts from file {}: {}'.format(file_path, end_time - start_time))
    # Return the word counts
    return word_counts



def get_word_counts_from_text(text, debug = True):
    '''
    This function will get the word counts from a text

    Args:
        text (str): the text to get the word counts from
        debug (bool): boolean to determine if debug is on or off
    '''
    # Get the start time
    start_time = time.time()
    # Get the word counts
    word_counts = get_word_counts_from_text_no_debug(text)
    # Get the end time
    end_time = time.time()
    # Print the time taken
    if debug:
        print('Time taken to get word counts from text: {}'.format(end_time - start_time))
    # Return the word counts
    return word_counts


def get_word_counts_from_text_no_debug(text):
    '''
    This function will get the word counts from a text

    Args:
        text (str): the text to get the word counts from
    '''
    # Get the word counts
    word_counts = {}
    # Split the text into words
    words = text.split()
    # Loop through the words
    for word in words:
        # Get the word count for the word
        word_count = get_word_count_from_word(word)
        # Add the word count to the word counts
        word_counts[word_count] = word_counts.get(word_count, 0) + 1
    # Return the word counts
    return word_counts



def get_word_count_from_word(word):
    '''
    This function will get the word count from a word

    Args:
        word (str): the word to get the word count from
    '''
    # Remove the punctuation from the word
    word = remove_punctuation(word)
    # Remove the numbers from the word
    word = remove_numbers(word)
    # Remove the whitespace from the word
    word = remove_whitespace(word)
    # Return the word count
    return word



def remove_punctuation(word):
    '''
    This function will remove the punctuation from a word

    Args:
        word (str): the word to remove the punctuation from
    '''
    # Remove the punctuation
    word = re.sub(r'[^\w\s]', '', word)
    # Return the word
    return word



def remove_numbers(word):
    '''
    This function will remove the numbers from a word

    Args:
        word (str): the word to remove the numbers from
    '''
    # Remove the numbers
    word = re.sub(r'\d', '', word)
    # Return the word
    return word



def remove_whitespace(word):
    '''
    This function will remove the whitespace from a word

    Args:
        word (str): the word to remove the whitespace from
    '''
    # Remove the whitespace
    word = re.sub(r'\s', '', word)
    # Return the word
    return word


def print_word_counts(word_counts, debug = True):
    '''
    This function will print the word counts

    Args:
        word_counts (dict): the word counts to print
        debug (bool): boolean to determine if debug is on or off
    '''
    # Get the start time
    start_time = time.time()
    # Print the word counts
    print_word_counts_no_debug(word_counts)
    # Get the end time
    end_time = time.time()
    # Print the time taken
    if debug:
        print('Time taken to print word counts: {}'.format(end_time - start_time))


def print_word_counts_no_debug(word_counts):
    '''
    This function will print the word counts

    Args:
        word_counts (dict): the word counts to print
    '''
    # Loop through the word counts
    for word_count in word_counts:
        # Print the word count
        print('{}: {}'.format(word_count, word_counts[word_count]))



def get_top_words(word_counts, top_n, debug = True):
    '''
    This function will get the top words

    Args:
        word_counts (dict): the word counts to get the top words from
        top_n (int): the number of top words to get
        debug (bool): boolean to determine if debug is on or off
    '''
    # Get the start time
    start_time = time.time()
    # Get the top words
    top_words = get_top_words_no_debug(word_counts, top_n)
    # Get the end time
    end_time = time.time()
    # Print the time taken
    if debug:
        print('Time taken to get top words: {}'.format(end_time - start_time))
    # Return the top words
    return top_words





def get_top_words_no_debug(word_counts, top_n):
    '''
    This function will get the top words

    Args:
        word_counts (dict): the word counts to get the top words from
        top_n (int): the number of top words to get
    '''
    # Get the top words
    top_words = []
    # Loop through the word counts
    for word_count in word_counts:
        # Add the word count to the top words
        top_words.append(word_count)
    # Sort the top words
    top_words.sort(reverse = True)
    # Get the top words
    top_words = top_words[:top_n]
    # Return the top words
    return top_words



def get_top_words_from_file(file_name, top_n, debug = True):
    '''
    This function will get the top words from a file

    Args:
        file_name (str): the file name to get the top words from
        top_n (int): the number of top words to get
        debug (bool): boolean to determine if debug is on or off
    '''
    # Get the start time
    start_time = time.time()
    # Get the top words
    top_words = get_top_words_from_file_no_debug(file_name, top_n)
    # Get the end time
    end_time = time.time()
    # Print the time taken
    if debug:
        print('Time taken to get top words from file: {}'.format(end_time - start_time))
    # Return the top words
    return top_words


def get_top_words_from_file_no_debug(file_name, top_n):
    '''
    This function will get the top words from a file

    Args:
        file_name (str): the file name to get the top words from
        top_n (int): the number of top words to get
    '''
    # Get the top words
    top_words = []
    # Open the file
    with open(file_name, 'r') as file:
        # Loop through the file
        for line in file:
            # Get the words
            words = line.split()
            # Loop through the words
            for word in words:
                # Add the word to the top words
                top_words.append(word)
    # Sort the top words
    top_words.sort(reverse = True)
    # Get the top words
    top_words = top_words[:top_n]
    # Return the top words
    return top_words



def get_top_words_from_files(file_names, top_n, debug = True):
    '''
    This function will get the top words from a file

    Args:
        file_names (list): the file names to get the top words from
        top_n (int): the number of top words to get
        debug (bool): boolean to determine if debug is on or off
    '''
    # Get the start time
    start_time = time.time()
    # Get the top words
    top_words = get_top_words_from_files_no_debug(file_names, top_n)
    # Get the end time
    end_time = time.time()
    # Print the time taken
    if debug:
        print('Time taken to get top words from files: {}'.format(end_time - start_time))
    # Return the top words
    return top_words



def get_top_words_from_files_no_debug(file_names, top_n):
    '''
    This function will get the top words from a file

    Args:
        file_names (list): the file names to get the top words from
        top_n (int): the number of top words to get
    '''
    # Get the top words
    top_words = []
    # Loop through the file names
    for file_name in file_names:
        # Open the file
        with open(file_name, 'r') as file:
            # Loop through the file
            for line in file:
                # Get the words
                words = line.split()
                # Loop through the words
                for word in words:
                    # Add the word to the top words
                    top_words.append(word)
    # Sort the top words
    top_words.sort(reverse = True)
    # Get the top words
    top_words = top_words[:top_n]
    # Return the top words
    return top_words



def get_top_words_from_files_with_counts(file_names, top_n, debug = True):
    '''
    This function will get the top words from a file

    Args:
        file_names (list): the file names to get the top words from
        top_n (int): the number of top words to get
        debug (bool): boolean to determine if debug is on or off
    '''
    # Get the start time
    start_time = time.time()
    # Get the top words
    top_words = get_top_words_from_files_with_counts_no_debug(file_names, top_n)
    # Get the end time
    end_time = time.time()
    # Print the time taken
    if debug:
        print('Time taken to get top words from files: {}'.format(end_time - start_time))
    # Return the top words
    return top_words


def get_relative_file_names(file_names):
    '''
    This function will get the relative file names

    Args:
        file_names (list): the file names to get the relative file names from
    '''
    # Get the relative file names
    relative_file_names = []
    # Loop through the file names
    for file_name in file_names:
        # Get the relative file name
        relative_file_name = os.path.basename(file_name)
        # Add the relative file name to the relative file names
        relative_file_names.append(relative_file_name)
    # Return the relative file names
    return relative_file_names


def get_top_words_from_files_with_counts_no_debug(file_names, top_n):
    '''
    This function will get the top words from a file

    Args:
        file_names (list): the file names to get the top words from
        top_n (int): the number of top words to get
    '''
    # Get the top words
    top_words = []

    # Get the relative file names
    file_names = get_relative_file_names(file_names)

    # Loop through the file names
    for file_name in file_names:
        # Open the file
        with open(file_name, 'r') as file:
            # Loop through the file
            for line in file:
                # Get the words
                words = line.split()
                # Loop through the words
                for word in words:
                    # Add the word to the top words
                    top_words.append(word)
    # Sort the top words
    top_words.sort(reverse = True)
    # Get the top words
    top_words = top_words[:top_n]
    # Return the top words
    return top_words




def get_top_words_from_files_with_counts_and_files(file_names, top_n, debug = True):
    '''
    This function will get the top words from a file

    Args:
        file_names (list): the file names to get the top words from
        top_n (int): the number of top words to get
        debug (bool): boolean to determine if debug is on or off
    '''
    # Get the start time
    start_time = time.time()
    # Get the top words
    top_words = get_top_words_from_files_with_counts_and_files_no_debug(file_names, top_n)
    # Get the end time
    end_time = time.time()
    # Print the time taken
    if debug:
        print('Time taken to get top words from files: {}'.format(end_time - start_time))
    # Return the top words
    return top_words


def get_top_words_from_files_with_counts_and_files_no_debug(file_names, top_n):
    '''
    This function will get the top words from a file

    Args:
        file_names (list): the file names to get the top words from
        top_n (int): the number of top words to get
    '''
    # Get the top words
    top_words = []
    # Loop through the file names
    for file_name in file_names:
        # Open the file
        with open(file_name, 'r') as file:
            # Loop through the file
            for line in file:
                # Get the words
                words = line.split()
                # Loop through the words
                for word in words:
                    # Add the word to the top words
                    top_words.append(word)
    # Sort the top words
    top_words.sort(reverse = True)
    # Get the top words
    top_words = top_words[:top_n]
    # Return the top words
    return top_words

def get_file_names(directory, extension):
    '''
    This function will get the file names

    Args:
        directory (str): the directory to get the file names from
        extension (str): the extension to get the file names from
    '''
    # Get the file names
    file_names = []
    # Get the file names
    for file_name in os.listdir(directory):
        # Check if the file name has the extension
        if file_name.endswith(extension):
            # Add the file name
            file_names.append(file_name)
    # Return the file names
    return file_names




def main():
    '''
    This function will run the main function
    '''
    # getting the file names in the data directory
    file_names = get_file_names('./data', '.txt')


    # Get the top words
    top_words = get_top_words_from_files_with_counts(file_names, 10)
    # Print the top words
    print(top_words)



if __name__ == '__main__':
    main()
