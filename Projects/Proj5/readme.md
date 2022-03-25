# CS337 - OPERATING SYSTEMS- Project 5 Multitasking
#### By: Matthew Bass


**Project Overview:**
    
In this assignment, you will revisit a familiar project from CS231.  We will 
write a program to process eight years of Reddit comments to find the most common words overall and in each year.  This assignment is intentionally vague to give you room to be creative in your solutions.  

You will be graded based on:
- Your choice of data structure for each part of the project (you can use any 
Python library).
- How you apply multiprocessing and multithreading to speed up your code.
- The improvement, in run time, over running the code serially.




### PREREQUISITES:
    Python 3
    Jupyter
    Matplotlib
    Pandas
    Numpy
	linecache
    autopep8

If you are on a mac will need a product such as [The Unarchiver](https://apps.apple.com/us/app/the-unarchiver/id425424353?mt=12) 
to unpack the rar files.

<br>

---

## Intro:


Overall I found this project, in using multitasking to speed up the word 
counting python code, to be extremly rewarding in learning the limits of 
multiprocessing and mulithreading as well as using memory resources properly,
and overall strategies to optimize code (Including Traces from [viztracer](
https://viztracer.readthedocs.io/en/latest/basic_usage.html))

<br>

## Code Overview and Analysis:

To Views the traces uses the command `vizviewer viztraces/`



### serial_code_1.py:

To start out I wrote (serial_code) which read in all the data from all files 
at once (this proved to be extremely inefficient). 

When looking at the graph below along with the total runtime of the 
wordcounter from the viztrace file we can see that this was an awful 
approach to counting all the words in the reddit comments.


<img src="https://github.com/mattjax16/CS337-Operating-Systems/blob/master/Projects/Proj5/pics/serial1_pycharm_call_graph.png" width="1200" height="800">

From The Trace above we can see the all the main function for running the word counter `CreateWordCounts()`
is only ran once showing that all the files are read in at the sametime (the function `readInComments()` also shows this.) 

One of the biggest issues of this code is the in total all the text files combine to arounf 4gb of data so memeory limitations and bottle necks where massive on my m1 macbook air with 8gb of ram and even on my desktopcompter with 32 gb of ram (which is why I ran my simulations on that machine).

Here is the machine at is memory limitations

<img src="https://github.com/mattjax16/CS337-Operating-Systems/blob/master/Projects/Proj5/pics/sc1_mem.png">

Overall this was an afwul approached that made the counter slow taking 234.635 seconds to run in total. I used this appriach though in `multitasking_code_1.py` which I would come to regret imensly.


<br>


### multitasking_code_1.py:
Overall this code is not even worth showing the trace to because it took 
forever to run and would crash both computers because the memory constraints 
where so large,so then I wrote a new version of the serial code called 
`serial_code_2.py` which reads in the data from the files one at a time. 

Below is an example of the memory issues on mac with it not even running.

<img src="https://github.com/mattjax16/CS337-Operating-Systems/blob/master/Projects/Proj5/pics/memory_issue.png">


<br>


### serial_code_2.py:

This code is a bit more efficient in terms of memory usage but still takes 
some time to run. To improve the memory efficiency I proccesed each file one 
at a time. This can be seen in the call graph below.

<img src="https://github.com/mattjax16/CS337-Operating-Systems/blob/master/Projects/Proj5/pics/sc2_trace.png">

Here the word counter took 225.551 seconds to run. Which is even worse than serial_code_1.py. This is because the function `readInComments()` is called multiple times and each time it reads in the file and then calls the function `CreateWordCounts()` which is called multiple times. This wouldnt be a problem if it wasnt for the fact that I tried to get creative by making the file word_count_objects.py which had custom objects to manage the word counts using the `heapq` module. However I used this along with the `Counter` object from the `collections` module to but it was very slow and inefficent as we will see in later versions of serial codes. However for now this was enough of a solution for the memory constraints when using multiprocessing with the word counter.


<br>


### multitasking_code_2.py:
In this code I used the `multiprocessing` and `concurent futures` module to 
run the word counter in parallel. At first I used the `multiprocessing.Pool()
` function to run the word counter in parallel but this was not the best 
approach because when using viztracer it can not tracess multipleprocesses 
when they are called with the `Pool()` function on windows so instead I used 
the `concurent futures` module instead which is a better approach along with 
the `multiprocessing.Manager()` object which also worked with viztracer. In 
this code I did basic multiprocessing by only running the `getWordData()` 
function. There is a process created for each file.

Here is the code snippet for multiprocessing below:

```python
# Use the process pool context manager to start multiprocess pool with
# desired number of processes
with ProcessPoolExecutor(process_count) as p:
    word_data_list = p.map(getWordData,
                           data_files,
                           repeat(data_path),
                           repeat(process_count),
                           repeat(thread_count),
                           repeat(data_type))

# Make the word count dicts
word_data = {}
for data_file, dat in zip(data_files, word_data_list):
    word_data[data_file] = dat
```

Now to go through the performance will now look at the call graph produced 
with viztracer from the `multitasking_code_2.py`. We will see the overall 
call graph then the main process and subprocesses.


##### Overall Call Graph:
<img src="https://github.com/mattjax16/CS337-Operating-Systems/blob/master/Projects/Proj5/pics/mt2_call_graph.png">

##### Main Process:

<img src="https://github.com/mattjax16/CS337-Operating-Systems/blob/master/Projects/Proj5/pics/mt2_main_process.PNG">


##### Subprocesses:

<img src="https://github.com/mattjax16/CS337-Operating-Systems/blob/master/Projects/Proj5/pics/mt2_sub_process.PNG">

##### Preformance:
From the call graohs above we can see that overall `multitasking_code_2.
  py` took around 57.5 seconds to run. That makes this basic multiprocessing 
  code using eight cores to run (The number of files to process), about 4 
  times faster than the serial code (3.92262608696 times faster to be exact).
  This of course is helped because my I9-1090K has at least eight cores to work 
  with.


<br>


### multitasking_code_3.py:

Next with `multitasking_code_3.py` I used the `multiprocessing` and `concurent 
futures`  modules to try and speed up my code even more multiprocessing to my 
code. When looking at the traces from `multitasking_code_2.py` and just from 
running it, I can see 
that the two other functions that took the most time to run were 
`cleanDataList()` and `createWordCountDict()` taking around 12 and 10 
seconds to run respectively for the large text files. I also saw that 
the `readInComments()` function took around only a little over a second to 
run so not that much time at all. Considering these facts and due to 
`readInComments()` being an I/O bound function, and `createWordCountDict()` 
and `cleanDataList()` being CPU bound functions, I decided to only implement 
more multiprocessing on the two functions `cleanDataList()` and 
`createWordCountDict()` to try and speed up the overall code instead of 
using multithreading with the function `readInComments()`.


Here is the code snippet for multiprocessing below in the main function 
using multiprocessing, `getWordData()`:

```python

# Clean the data
cleanDataList_start_time = time.perf_counter()
data = cleanDataListMuliProcess(data, process_count)
cleanDataList_end_time = time.perf_counter()
cleanDataList_total_time = cleanDataList_end_time - cleanDataList_start_time
print(f"\n{data_file} cleanDataList ({data_type}) is done! " +
      f"\n\tIt took {cleanDataList_total_time} sec(s) to run!\n")

# word_count = createWordCountHeap(data)
createWordCountDict_start_time = time.perf_counter()
data = createWordCountDictMultiProcess(data, process_count)
createWordCountDict_end_time = time.perf_counter()
createWordCountDict_total_time = createWordCountDict_end_time - \
    createWordCountDict_start_time
print(f"\n{data_file} createWordCountDict ({data_type}) is done! " +
      f"\n\tIt took {createWordCountDict_total_time} sec(s) to run!\n")

```

Here is how I added multiprocessing to the `cleanDataList()` function:
```python
def createWordCountDictMultiProcess(
        data: list, process_count: int) -> dict:
    '''
    Create a word count dict from the data. usinf mutli processing

    :param data: a list of all the cleaned words
    :param process_count: the number of process to use
    :return: word_count: a word count dict of the file
    '''

    # set up multiprocessing  chunks to run the function
    chunck = len(data) / process_count

    mp_data = []
    for process in range(process_count):
        chunck_start = int(process * chunck)
        chunck_end = int((process * chunck) + chunck)
        mp_data.append(data[chunck_start:chunck_end])

    with ProcessPoolExecutor(process_count) as p:
        results = p.map(
            createWordCountDict,
            mp_data,
            np.arange(
                len(mp_data) + 1))

    # make all dicts a counter
    results_list = [Counter(wc) for wc in results]

    # Make the cleaned data by concatting all the lists
    word_count = Counter()
    for wc in results_list:
        word_count += wc

    return word_count


def createWordCountDict(data: list, chunck_number: int,
                        debug: bool = False) -> dict:
    '''
    Create a word count dict from the data.

    :param data: a list of all the cleaned words
    :param chunck_number:int representing which chunchk is being
    processes
    :param debug: if true debug printing will occur
    :return: word_count: a word count dict of the file
    '''

    # Create a word count
    word_count = {}

    # if Debug print the function and pid
    if debug:
        print(f"\nSTART createWordCountDict {chunck_number} pid :"
              f" {os.getpid()}")

    # Loop through the data and increment each word
    for word in data:
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1

    # if Debug print the function and pid
    if debug:
        print(f"\nEND createWordCountDict {chunck_number} pid :"
              f" {os.getpid()}")
    return word_count
```

Here is the code snippet for multiprocessing below in the 
'createWordCountDict()' function:
```python
def cleanDataListMuliProcess(raw_line_data: list,
                             process_count: int) -> list:
    '''
    Function to clean the raw data from each file
    using multi processing
    :param raw_line_data: list of raw data strings
    :param process_count: the number of process to use
    :return:
    '''
    # set up multiprocessing  chunks to run the function
    chunck = len(raw_line_data) / process_count

    mp_data = []
    for process in range(process_count):
        chunck_start = int(process * chunck)
        chunck_end = int((process * chunck) + chunck)
        mp_data.append(raw_line_data[chunck_start:chunck_end])

    with ProcessPoolExecutor(process_count) as p:
        results = p.map(cleanDataList, mp_data, np.arange(len(mp_data) + 1))

    # Make the cleaned data by concatting all the lists
    clean_data = list(itertools.chain.from_iterable(results))

    return clean_data


def cleanDataList(raw_line_data: list, chunck_number: int,
                  debug: bool = False) -> list:
    '''
    Function to clean the raw data from each file

    :param raw_line_data: list of raw data strings
    :return:
    '''

    # if Debug print the function and pid
    if debug:
        print(
            f"\nSTART cleanDataList {chunck_number} pid : {os.getpid()}")

    clean_data = splitLinesList(raw_line_data)

    # making regex to look for word
    word_regex = re.compile("^[a-zA-Z]")
    # Filter out all words strings that are not begging with letters
    clean_data = list(filter(word_regex.match, clean_data))

    # Make all the filtered words lowercase
    clean_data = list(map(str.lower, clean_data))

    # if Debug print the function and pid
    if debug:
        print(
            f"\nEND cleanDataList {chunck_number} pid : {os.getpid()}")

    return clean_data
```


Now to go through the performance will now look at the call graph produced 
with viztracer from the `multitasking_code_3.py`. We will see the overall 
call graph then the main process and subprocesses.

##### Overall Call Graph:
<img src="https://github.com/mattjax16/CS337-Operating-Systems/blob/master/Projects/Proj5/pics/mt3_call_graph.PNG">


##### Main Process:

<img src="https://github.com/mattjax16/CS337-Operating-Systems/blob/master/Projects/Proj5/pics/mt3_main_process.png">


##### Subprocesses:

<img src="https://github.com/mattjax16/CS337-Operating-Systems/blob/master/Projects/Proj5/pics/mt3_sub_process.png">

##### Preformance:
From the call graohs above we can see that overall `multitasking_code_3.
  py` took around 79 seconds to run. This was surprising that it would take 
  more time than `multitasking_code_2.py` with it being about 1.4 times longer. 
  However, I guess it is due to the fact that the subprocesses take time to spin up and run and there are 
  still memory constraints.

My next thought to optimize the code even more if adding more 
multiprocessing would not do the job was to try and optimize the codes base 
functions in particular how it cleans the data, creates the word count, and 
also try and find a better data object to hold the word count data so that I 
would not need to sort the word count dictionary at the end of creating it. 
This lead me to creating the file 'serial_code_3.py'.


<br>


### serial_code_3.py:

To start in `serial_code_3.py` I first made it much simpler by removing a 
lot of functions and combining some into one. The next big change in code 
design that I made was to make the word count info and word frequency info 
into two separate data objects. This way I could create the word count with 
a `Counter` object from the `collections()` module, and then I create the word 
frequency with normal `dict ()` object. This way I could have the word count 
automatically sorted by the count of each word, and then I could just use the 
`most_common()` to print out the top 10 words. This allowed me to remove the 
function to sort the word count and also since the `Counter` object is build 
upon a priority queue heaped data structure, it was much faster to use. This 
by far was one of the biggest contributions to speeding up the code. By using dictionaries to hold the word frequencies 
for each year it made it much faster to find and print out the frequency of a word over the years since searching for a
word in a dictionary is done in constant time.

I also created a function to clean the data and split the lines into a list 
which was much faster than the previous method. Here is the function:
```python
def cleanAndTokenize(data: str, debug: bool = True) -> list:
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

    # Remove extra spaces, tabs, and line breaks
    data = " ".join(data.split())

    # keep only words
    data = re.sub(r"[^A-Za-z\s]+", "", data).split(" ")

    # Make all the filtered words lowercase
    data = list(map(str.lower, data))

    if debug:
        t_end_time = time.perf_counter()
        t_total_time = t_end_time - t_start_time
        print(f"\ncleanAndTokenize is done! " +
              f"\n\tIt took {t_total_time} sec(s) to run in total!\n")

    return data
```

Now to go through the performance will now look at the call graph produced 
with viztracer from the `serial_code_3.py`.

###### Call Graph:

<img src="https://github.com/mattjax16/CS337-Operating-Systems/blob/master/Projects/Proj5/pics/sc3_trace.png">


###### Total time to run the word counter (From another run so might be slightly different from the trace above):
```commandline
Word Counter  is done! 
	It took 110.0330921 sec(s) to run in total!
```

###### Output of the top 10 words over the years:
```commandline
The top 10 words for each year (word, count)
In Order Top: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
2008. [('the', 711513), ('to', 431563), ('a', 379813), ('of', 329578), ('and', 317301), ('i', 278455), ('that', 263598), ('is', 259208), ('in', 217093), ('you', 214583)]
2009. [('the', 1670402), ('to', 1057262), ('a', 955963), ('and', 803046), ('i', 790624), ('of', 787511), ('that', 624333), ('is', 602729), ('you', 573489), ('it', 550267)]
2010. [('the', 1856866), ('to', 1226757), ('a', 1136860), ('i', 1033577), ('and', 949769), ('of', 852237), ('you', 722363), ('that', 686378), ('it', 659562), ('is', 656993)]
2011. [('the', 1671332), ('to', 1120193), ('a', 1056315), ('i', 1006873), ('and', 878485), ('of', 763567), ('you', 660990), ('that', 622743), ('it', 607347), ('is', 590998)]
2012. [('the', 1502821), ('to', 1023874), ('a', 968789), ('i', 947775), ('and', 815605), ('of', 680333), ('you', 625966), ('it', 567488), ('that', 563968), ('is', 545467)]
2013. [('the', 1472358), ('to', 983628), ('a', 939884), ('i', 900757), ('and', 794882), ('of', 650948), ('you', 585021), ('it', 550504), ('', 538472), ('that', 532510)]
2014. [('the', 1547761), ('to', 1030803), ('a', 983303), ('i', 913603), ('and', 840100), ('of', 671992), ('', 621048), ('you', 615935), ('it', 568066), ('is', 544677)]
2015. [('the', 1534523), ('to', 1011979), ('a', 957860), ('i', 867651), ('and', 828038), ('of', 651833), ('', 644593), ('you', 596518), ('it', 546009), ('is', 531635)]
```
This confirms that the word counter is in fact working because it is common stop words (the, to, a, and, of, i, you, it, is) 
at the top of the list for each year. Also, the is the most common word in the english language, so it makes sense that it 
has the highest count in each year.

##### Performance:
From the call graph above we can see that `serial_code_3.py` took around much faster than the original serial 
code that processed each file one at a time (`serial_code_2.py`). This is due to the fact that I mentioned above. Having a
time to complete of around 108 seconds it is around 2 times faster than `serial_code_2.py` (which has a time to run of 
around 225.551 seconds). 

This had me very happy that with just a little of thought process in how I structured the code 
I was able to make it much faster. This however got me thinking could I improve how the data was cleaned and tokenized making it even faster
Here is the function in this file:
```python
def cleanAndTokenize(data: str, debug: bool = True) -> list:
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

    # Remove extra spaces, tabs, and line breaks
    data = " ".join(data.split())

    # keep only words
    data = re.sub(r"[^A-Za-z\s]+", "", data).split(" ")

    # Make all the filtered words lowercase
    data = list(map(str.lower, data))

    if debug:
        t_end_time = time.perf_counter()
        t_total_time = t_end_time - t_start_time
        print(f"\ncleanAndTokenize is done! " +
              f"\n\tIt took {t_total_time} sec(s) to run in total!\n")

    return data
```

When looking at the `cleanAndTokenize` function I can see a few way It could be imporved. To start with I know that loops in python are extremely slow 
and also that the `map` function is has approximately the same time as a for loop since the `map` function is basically a for loop under the hood. 
So my first idea was to make the initial raw string lower case and then split the string into a list of words. Then also by lower casing all the \
characters in the initial raw string I could onlt have to search for lower case characters in the regex function which could also 
improve the speed of the function. 

Here is the time it took to process `reddit_comments_2015.txt` (From another run so might be slightly different from the 
trace above):
```commandline
START getWordData reddit_comments_2015.txt

cleanAndTokenize is done there are 39380697 words! 
	It took 10.270400999999993 sec(s) to run in total!


END getWordData reddit_comments_2015.txt! 
	It took 14.4489497 sec(s) to run in total!
```



<br>



### serial_code_4.py

In `serial_code_4.py` I changed the `cleanAndTokenize` function to use the ideas that I mentioned in the performance analysis above. 

Here is the new `cleanAndTokenize` function (only the lines that are different from the original function):
```python
data = data.lower()

# Remove extra spaces, tabs, and line breaks
data = " ".join(data.split())

# keep only words
data = re.sub(r"[^a-z\s]+", "", data).split(" ")
```

Now to go through the performance will now look at the call graph produced 
with viztracer from the `serial_code_4.py`.

###### Call Graph:

<img src="https://github.com/mattjax16/CS337-Operating-Systems/blob/master/Projects/Proj5/pics/sc4_trace.png">


Here is the time it took to process `reddit_comments_2015.txt` (From another run so might be slightly different from the 
trace above):
```commandline
END getWordData reddit_comments_2014.txt! 
	It took 12.563553400000004 sec(s) to run in total!

START getWordData reddit_comments_2015.txt

cleanAndTokenize is done there are 39380697 words! 
	It took 8.325998400000003 sec(s) to run in total!


END getWordData reddit_comments_2015.txt! 
	It took 12.464330599999997 sec(s) to run in total!
```
We can see that the time to clean and tokenize the data is a little faster than it took in `serial_code_3.py` and it 
is still producing the same result (39380697 words). 

###### Total time to run the word counter (From another run so might be slightly different from the trace above):
```commandline
Word Counter  is done! 
	It took 105.5036884 sec(s) to run in total!
```

###### Output of the top 10 words over the years:
```commandline
The top 10 words for each year (word, count)
In Order Top: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
2008. [('the', 711513), ('to', 431563), ('a', 379813), ('of', 329578), ('and', 317301), ('i', 278455), ('that', 263598), ('is', 259208), ('in', 217093), ('you', 214583)]
2009. [('the', 1670402), ('to', 1057262), ('a', 955963), ('and', 803046), ('i', 790624), ('of', 787511), ('that', 624333), ('is', 602729), ('you', 573489), ('it', 550267)]
2010. [('the', 1856866), ('to', 1226757), ('a', 1136860), ('i', 1033577), ('and', 949769), ('of', 852237), ('you', 722363), ('that', 686378), ('it', 659562), ('is', 656993)]
2011. [('the', 1671332), ('to', 1120193), ('a', 1056315), ('i', 1006873), ('and', 878485), ('of', 763567), ('you', 660990), ('that', 622743), ('it', 607347), ('is', 590998)]
2012. [('the', 1502821), ('to', 1023874), ('a', 968789), ('i', 947775), ('and', 815605), ('of', 680333), ('you', 625966), ('it', 567488), ('that', 563968), ('is', 545467)]
2013. [('the', 1472358), ('to', 983628), ('a', 939884), ('i', 900757), ('and', 794882), ('of', 650948), ('you', 585021), ('it', 550504), ('', 538472), ('that', 532510)]
2014. [('the', 1547761), ('to', 1030803), ('a', 983303), ('i', 913603), ('and', 840100), ('of', 671992), ('', 621048), ('you', 615935), ('it', 568066), ('is', 544677)]
2015. [('the', 1534523), ('to', 1011979), ('a', 957860), ('i', 867651), ('and', 828038), ('of', 651833), ('', 644593), ('you', 596518), ('it', 546009), ('is', 531635)]
```
This confirms that the word counter is in fact working as expected because the top 10 words for each year are the same 
as the top 10 words from `serial_code_3.py`.

##### Performance:
  
  Since we can see that the time to clean and tokenize the data is a little faster than it took in `serial_code_4.py` and it 
is still producing the same result (39380697 words). I know that making all the characters lowercase in the initial raw 
string is faster than doing it after the fact when the words are split. This lead me to thinking that the overall time to run the word
counter would have had more of a speed increase from `serial_code_4.py` than it did, however this is not the case. With 
the overall time taking around 105 seconds to run, only a 5 second difference to the total time for `serial_code_4.py`.

This still lead me to wanting to find a even better way to clean and tokenize my data because when looking at my function
I thought it was inefficient to do split and join the data just to get rid of the tabs, whitespace, and newlines. So I looked
through the `re` module and found a function that would let me get the words from the raw lower case string all in one action.

<br>


<br>


### serial_code_5.py

In `serial_code_5.py` I changed the `cleanAndTokenize` function to use the ideas that I mentioned in the performance analysis above. 
The function that I used to get all the words in one action is `re.findall`.


Here is the new `cleanAndTokenize` function (only the lines that are different from the original function):
```python
# Make all the characters lowercase (this is much quicker than doing it
# after the fact when the words are split)
data = data.lower()

# Get all the words from the raw text
data = re.findall(r'\w+', data)
```

Now to go through the performance will now look at the call graph produced 
with viztracer from the `serial_code_5.py`.

###### Call Graph:

<img src="https://github.com/mattjax16/CS337-Operating-Systems/blob/master/Projects/Proj5/pics/sc5_trace.png">


Here is the time it took to process `reddit_comments_2015.txt` (From another run so might be slightly different from the 
trace above):
```commandline
END getWordData reddit_comments_2014.txt! 
	It took 12.563553400000004 sec(s) to run in total!

START getWordData reddit_comments_2015.txt

cleanAndTokenize is done there are 39380697 words! 
	It took 8.325998400000003 sec(s) to run in total!


END getWordData reddit_comments_2015.txt! 
	It took 12.464330599999997 sec(s) to run in total!
```
###### Total time to run the word counter (From another run so might be slightly different from the trace above):
```commandline
Word Counter  is done! 
	It took 87.05234469999999 sec(s) to run in total!
```

###### Output of the top 10 words over the years:
```commandline
The top 10 words for each year (word, count)
In Order Top: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
2008. [('the', 711513), ('to', 431563), ('a', 379813), ('of', 329578), ('and', 317301), ('i', 278455), ('that', 263598), ('is', 259208), ('in', 217093), ('you', 214583)]
2009. [('the', 1670402), ('to', 1057262), ('a', 955963), ('and', 803046), ('i', 790624), ('of', 787511), ('that', 624333), ('is', 602729), ('you', 573489), ('it', 550267)]
2010. [('the', 1856866), ('to', 1226757), ('a', 1136860), ('i', 1033577), ('and', 949769), ('of', 852237), ('you', 722363), ('that', 686378), ('it', 659562), ('is', 656993)]
2011. [('the', 1671332), ('to', 1120193), ('a', 1056315), ('i', 1006873), ('and', 878485), ('of', 763567), ('you', 660990), ('that', 622743), ('it', 607347), ('is', 590998)]
2012. [('the', 1502821), ('to', 1023874), ('a', 968789), ('i', 947775), ('and', 815605), ('of', 680333), ('you', 625966), ('it', 567488), ('that', 563968), ('is', 545467)]
2013. [('the', 1472358), ('to', 983628), ('a', 939884), ('i', 900757), ('and', 794882), ('of', 650948), ('you', 585021), ('it', 550504), ('', 538472), ('that', 532510)]
2014. [('the', 1547761), ('to', 1030803), ('a', 983303), ('i', 913603), ('and', 840100), ('of', 671992), ('', 621048), ('you', 615935), ('it', 568066), ('is', 544677)]
2015. [('the', 1534523), ('to', 1011979), ('a', 957860), ('i', 867651), ('and', 828038), ('of', 651833), ('', 644593), ('you', 596518), ('it', 546009), ('is', 531635)]
```
This confirms that the word counter is in fact working as expected because the top 10 words for each year are the same 
as the top 10 words from `serial_code_4.py`.

##### Performance:
  
  Since we can see that the time to clean and tokenize the data is a much faster than it took in `serial_code_4.py` and it 
is still producing the same result (39380697 words). I was also extremely happy with the overall time it took the word counter 
to run with it being around 87 seconds. That makes it around 26% faster than the time it took in `serial_code_3.py`. 


With this new and improved serial code I went and tried to write new and improved parallel code.
<br>

### multitasking_code_4.py:

Here in `multitasking_code_3.py` I just used multiprocessing to run the `getWordData` function in parallel and only that funciton 
since form my other experiments in parallizing the code I found that this was the fastest method.

Here is the code snippet for multiprocessing below in the main function 
using multiprocessing, `getWordData()`:

```python

# Use the concurrent futers process pool context manager to start
# multiprocess pool with desired number of processes
with ProcessPoolExecutor(process_count) as p:
    word_data_list = p.map(getWordData,
                           data_files,
                           repeat(data_path))
# Make the word count dicts
files_data = {}
for data_file, dat in zip(data_files, word_data_list):
    files_data[data_file] = dat
```



Now to go through the performance will now look at the call graph produced 
with viztracer from the `multitasking_code_4.py`. We will see the overall 
call graph then the main process and subprocesses.

##### Overall Call Graph:
<img src="https://github.com/mattjax16/CS337-Operating-Systems/blob/master/Projects/Proj5/pics/mt4_call_graph.png">


##### Main Process:

<img src="https://github.com/mattjax16/CS337-Operating-Systems/blob/master/Projects/Proj5/pics/mt4_main_process.png">


##### Subprocesses:

<img src="https://github.com/mattjax16/CS337-Operating-Systems/blob/master/Projects/Proj5/pics/mt4_sub_process.png">

##### Time it took to process `reddit_comments_2015.txt` (From another run so might be slightly different from the trace above):
```commandline
END getWordData reddit_comments_2015.txt pid : 8284!
        It took 14.160474800000001 sec(s) to run in total!
```

###### Total time to run the word counter (From another run so might be slightly different from the trace above):
```commandline
Word Counter  is done!
        It took 16.354506999999998 sec(s) to run in total!
```

##### Performance:

This by far was my best code I have written for processing all the reddit comment data as it took only about 16.4 seconds to run. 
This is a very fast time to run compared to the time it took in `serial_code_5.py` which was around 87 seconds and also proved 
to be my greatest improvement from in time with multiprocessing as this code is about 5.3 tines faster than its serial version.

<br>


## Conclusion:
  Overall I am very happy with the results of this project. I am very happy with the time it took to run the code and the fact that
I was able to go all the way from a 200+ second run time down to a 16.3 second runtime in processing the data by rewriting the code
many times. In this project I learned a ton about optimizing code and how to use multiprocessing to speed up the code. It showed me that more multiprocessing
is not always the answer to speeding up code and also that sometimes much more speed can be gained by proper use of data structures
, use of efficient functions and just overall refactoring and rethinking of every line of code to save time. It also was a great
learning experience in memory limitations and bottlenecks and how to write code tow ork within those limitations. This project also allowed me to become very
proficient at profiling code and how to use the profiler to see how much time each function took to run. (I love the viztracer library).

### Resources:
- [Dr. Al Madi](https://www.cs.colby.edu/nsalmadi/)
- [Info on different python timers](https://www.webucator.com/article/python-clocks-explained/#:~:text=perf_counter()%20%2C%20which%20has%20a,33%2C491%20times%20faster%20than%20time.)
- [Why viztracer doesnt work with multiprocessing Pool](https://viztracer.readthedocs.io/en/latest/concurrency.html)

<br>


