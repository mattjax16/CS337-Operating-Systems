import threading
import multiprocessing
import time
import os


def CPU_bound(numbers):

	for num in numbers:
	    for i in range(100):
	    	num * num


def main():

	numbers = list(range(0, 999999))

	multiprocessing_duration_total = 0
	multithreading_duration_total = 0

	iterations = 10

	for _ in range(iterations):
		# CPU bound comparison
		thread_count = 5
		threads = []

		chunck = len(numbers) / thread_count

		for thread in range(thread_count):

			chunck_start = int(thread * chunck)
			chunck_end = int((thread * chunck) + chunck)

			t = threading.Thread(target=CPU_bound,
				args=(numbers[chunck_start:chunck_end],))
			threads.append(t)
		
		start = time.time()
		for thread in threads:
			thread.start()

		for thread in threads:
			thread.join()

		duration = time.time() - start
		print("Threading CPU-bound duration:", duration)
		multithreading_duration_total += duration



		# multiprocessing
		process_count = 5
		processes = []

		chunck = len(numbers) / process_count

		for process in range(process_count):

			chunck_start = int(process * chunck)
			chunck_end = int((process * chunck) + chunck)

			p = multiprocessing.Process(target=CPU_bound,
				args=(numbers[chunck_start:chunck_end],))
			processes.append(p)
		
		start = time.time()
		for process in processes:
			process.start()

		for process in processes:
			process.join()

		duration = time.time() - start
		print("Multiprocessing CPU-bound duration:", duration)
		multiprocessing_duration_total += duration

	print("\n*******************************************")
	print("Threading CPU-bound duration:", 
			multithreading_duration_total / iterations)
	print("Multiprocessing CPU-bound duration:", 
			multiprocessing_duration_total / iterations)



if __name__ == '__main__':
    main()