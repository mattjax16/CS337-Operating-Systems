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
where so large so then 


### serial_code_2.py:

This code is a bit more efficient in terms of memory usage but still takes 
some time to run. To improve the memory efficiency I proccesed each file one 
at a time. This can be see in the call graph below.

<img src="/Users/matthewbass/Documents/School_Colby/Colby/spring22/CS337-Operating-Systems/Projects/Proj5/pics/sc2_trace.png">

Here the word counter took 225.551 seconds to run. Which is even worse than serial_code_1.py. This is because the function `readInComments()` is called multiple times and each time it reads in the file and then calls the function `CreateWordCounts()` which is called multiple times. This wouldnt be a problem if it wasnt for the fact that I tried to get creative by making the file word_count_objects.py which had custom objects to manage the word counts using the `heapq` module. However I used this along with the `Counter` object from the `collections` module to but it was ver slow and inefficent. So then I decided to try processesing each file one at a time in serial_code_3.py.



### Resources:
- [Info on different python timers](https://www.webucator.com/article/python-clocks-explained/#:~:text=perf_counter()%20%2C%20which%20has%20a,33%2C491%20times%20faster%20than%20time.)
- [Why viztracer doesnt work with multiprocessing Pool](https://viztracer.readthedocs.io/en/latest/concurrency.html)

<br>

---

### Layout:
	.
    

