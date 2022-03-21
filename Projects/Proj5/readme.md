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

### Intro:

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

### Resources:
- [Info on different python timers](https://www.webucator.com/article/python-clocks-explained/#:~:text=perf_counter()%20%2C%20which%20has%20a,33%2C491%20times%20faster%20than%20time.)
- [Why viztracer doesnt work with multiprocessing Pool](https://viztracer.readthedocs.io/en/latest/concurrency.html)

<br>

---

### Layout:
	.
    

---

<br>

### Serial output(M1 chip):

(CS337-Operating-Systems) matthewbass@Matthews-MacBook-Air Proj5 % python serial_code.py

(Serial) readInComments (list) is done! 
	It took 4221127000 ns to run!


(Serial) cleanData (list) is done! 
	It took 268855206000 ns to run!


(Serial) createWordCounts (list) is done! 
	It took 149584401000 ns to run!


(Serial) sortWordCounts (list) is done! 
	It took 72037222000 ns to run!


reddit_comments_2013.txt's top 10 words: 

	 rank.  word  :  count

	 1. the : 1483690

	 2. to : 991926

	 3. a : 952442

	 4. i : 923954

	 5. and : 802390

	 6. of : 657447

	 7. you : 588959

	 8. it : 554772

	 9. that : 534433

	 10. is : 521715

reddit_comments_2012.txt's top 10 words: 

	 rank.  word  :  count

	 1. the : 1513453

	 2. to : 1030782

	 3. a : 976736

	 4. i : 969861

	 5. and : 823087

	 6. of : 685197

	 7. you : 630253

	 8. it : 571815

	 9. that : 566004

	 10. is : 547914

reddit_comments_2010.txt's top 10 words: 

	 rank.  word  :  count

	 1. the : 1868168

	 2. to : 1232146

	 3. a : 1145806

	 4. i : 1050658

	 5. and : 959107

	 6. of : 857885

	 7. you : 726782

	 8. that : 688429

	 9. it : 663704

	 10. is : 659755

reddit_comments_2011.txt's top 10 words: 

	 rank.  word  :  count

	 1. the : 1681133

	 2. to : 1125241

	 3. a : 1064893

	 4. i : 1027712

	 5. and : 887000

	 6. of : 768539

	 7. you : 664802

	 8. that : 624812

	 9. it : 611206

	 10. is : 593622

reddit_comments_2015.txt's top 10 words: 

	 rank.  word  :  count

	 1. the : 1545152

	 2. to : 1031945

	 3. a : 967068

	 4. i : 887628

	 5. and : 836367

	 6. of : 658296

	 7. you : 599540

	 8. it : 549983

	 9. is : 536990

	 10. that : 527695

reddit_comments_2014.txt's top 10 words: 

	 rank.  word  :  count

	 1. the : 1557938

	 2. to : 1045335

	 3. a : 992264

	 4. i : 934268

	 5. and : 848627

	 6. of : 678035

	 7. you : 619181

	 8. it : 572806

	 9. is : 551114

	 10. that : 545297

reddit_comments_2008.txt's top 10 words: 

	 rank.  word  :  count

	 1. the : 715269

	 2. to : 433100

	 3. a : 382497

	 4. of : 331304

	 5. and : 320515

	 6. i : 282940

	 7. that : 264302

	 8. is : 259885

	 9. in : 219639

	 10. you : 215838

reddit_comments_2009.txt's top 10 words: 

	 rank.  word  :  count

	 1. the : 1681337

	 2. to : 1061929

	 3. a : 963575

	 4. and : 811044

	 5. i : 803004

	 6. of : 792744

	 7. that : 626146

	 8. is : 605146

	 9. you : 577384

	 10. it : 553744

(Serial) printTopWordCounts (list) is done! 
	It took 19386000 ns to run!