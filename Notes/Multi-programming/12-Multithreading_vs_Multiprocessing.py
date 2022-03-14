import threading
import multiprocessing
import time
import os

def CPU_bound(num):

    for i in range(100):
    	num * num

def CPU_bound_thread(numbers):

	for num in numbers:
	    for i in range(100):
	    	num * num


def IO_bound(num):

	time.sleep(0.1)
	file = open("text.txt", "a")
	file.write("Hi")
	file.close()

def IO_bound_thread(num):

	for i in num:
		time.sleep(0.1)
		file = open("text.txt", "a")
		file.write("Hi")
		file.close()

def main():

	numbers = list(range(0, 999999))

	# CPU bound comparison
	start = time.time()
	t1 = threading.Thread(target=CPU_bound_thread, args=(numbers,))
	t1.start()
	t1.join()
	duration = time.time() - start
	print("Threading CPU-bound duration:", duration)
	time.sleep(3)

	# multiprocessing
	start = time.time()
	p = multiprocessing.Pool()
	p.map(CPU_bound, numbers)
	duration = time.time() - start
	print("Multiprocessing CPU-bound duration:", duration)
	time.sleep(3)


	# I/O bound comparison
	repeats = list(range(0, 1000))

	start = time.time()
	t1 = threading.Thread(target=IO_bound_thread, args=(repeats,))
	t1.start()
	t1.join()
	duration = time.time() - start
	print("Threading IO-bound duration:", duration)
	time.sleep(3)

	# multiprocessing
	start = time.time()
	p1 = multiprocessing.Process(target=IO_bound_thread, args=(repeats,))
	p1.start()
	p1.join()
	duration = time.time() - start
	print("Multiprocessing IO-bound duration:", duration)
	time.sleep(3)



if __name__ == '__main__':
    main()