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

talk about the experience and learning 

Topics:
- memory constraints
- order of operations
- use of proper data types
- how stats were calculated.
- how multiprocessing in particular was use full
- talk about traces (used form viztrace) that were used to see where my code 
  imporoved
  - this is also a reason to why I used concurrent futures to run the 
    multiprocessing in the functions instead of `multiprocessing.Pool()`.
- Also talk about why mulitthreading here would not be that usefull in reality


Overall I found this project, in using multitasking to speed up the word 
counting python code, to be extremly rewarding in learning the limits of 
multiprocessing and mulithreading as well as using memory resources properly,
and overall strategies to optimize code (Including Traces from [viztracer](
https://viztracer.readthedocs.io/en/latest/basic_usage.html))


## Code Overview and Analysis:

To Views the traces uses the command `vizviewer viztraces/`


### serial_code_1.py:

To start out I wrote (serial_code) which read in all the data from all files 
at once (this proved to be extremely inefficient). 

When looking at the graph below along with the total runtime of the 
wordcounter from the viztrace file we can see that this was an awful 
approach to counting all the words in the reddit comments.


<img src="/Users/matthewbass/Documents/School_Colby/Colby/spring22/CS337-Operating-Systems/Projects/Proj5/pics/serial1_pycharm_call_graph.png" width="1200" height="800">

From The Trace above we can see the all the main function for running the word counter `CreateWordCounts()`
is only ran once showing that all the files are read in at the sametime (the function `readInComments()` also shows this.) 

One of the biggest issues of this code is the in total all the text files combine to arounf 4gb of data so memeory limitations and bottle necks where massive on my m1 macbook air with 8gb of ram and even on my desktopcompter with 32 gb of ram (which is why I ran my simulations on that machine).

Here is the machine at is memory limitations

<img src="/Users/matthewbass/Documents/School_Colby/Colby/spring22/CS337-Operating-Systems/Projects/Proj5/pics/sc1_mem.png">

Overall this was an afwul approached that made the counter slow taking 234.635 seconds to run in total. I used this appriach though in `multitasking_code_1.py` which I would come to regret imensly.


### multitasking_code_1.py:
Overall this code is not even worth showing the trace to because it took 
forever to run and would crash both computers because the memory constraints 
where so large,so then I wrote a new version of the serial code called 
`serial_code_2.py` which reads in the data from the files one at a time. 

Below is an example of the memory issues on mac with it not even running.

<img src="https://github.com/mattjax16/CS337-Operating-Systems/blob/master/Projects/Proj5/pics/memory_issue.png">



### serial_code_2.py:

This code is a bit more efficient in terms of memory usage but still takes 
some time to run. To improve the memory efficiency I proccesed each file one 
at a time. This can be see in the call graph below.

<img src="/Users/matthewbass/Documents/School_Colby/Colby/spring22/CS337-Operating-Systems/Projects/Proj5/pics/sc2_trace.png">

Here the word counter took 225.551 seconds to run. Which is even worse than serial_code_1.py. This is because the function `readInComments()` is called multiple times and each time it reads in the file and then calls the function `CreateWordCounts()` which is called multiple times. This wouldnt be a problem if it wasnt for the fact that I tried to get creative by making the file word_count_objects.py which had custom objects to manage the word counts using the `heapq` module. However I used this along with the `Counter` object from the `collections` module to but it was very slow and inefficent as we will see in later versions of serial codes. However for now this was enough of a solution for the memory constraints when using multiprocessing with the word counter.


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


### multitasking_code_3.py:

Next with `serial_code_3.py` I used the `multiprocessing` and `concurent 
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



  

### Resources:
- [Info on different python timers](https://www.webucator.com/article/python-clocks-explained/#:~:text=perf_counter()%20%2C%20which%20has%20a,33%2C491%20times%20faster%20than%20time.)
- [Why viztracer doesnt work with multiprocessing Pool](https://viztracer.readthedocs.io/en/latest/concurrency.html)

<br>

---

### Layout:
	.
    

