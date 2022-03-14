import threading
import multiprocessing
import time
import os


def IO_bound(numbers):

	for i in numbers:
		file = open("text.txt", "a")
		file.write("Hi")
		file.close()


def main():

	numbers = list(range(0, 99999))

	# IO_bound comparison
	thread_count = 5
	threads = []

	chunck = len(numbers) / thread_count

	for thread in range(thread_count):

		chunck_start = int(thread * chunck)
		chunck_end = int((thread * chunck) + chunck)

		t = threading.Thread(target=IO_bound,
			args=(numbers[chunck_start:chunck_end],))
		threads.append(t)
	
	start = time.time()
	for thread in threads:
		thread.start()

	for thread in threads:
		thread.join()

	duration = time.time() - start
	print("Threading IO_bound duration:", duration)
	time.sleep(1)



	# multiprocessing
	process_count = 5
	processes = []

	chunck = len(numbers) / process_count

	for process in range(process_count):

		chunck_start = int(process * chunck)
		chunck_end = int((process * chunck) + chunck)

		p = multiprocessing.Process(target=IO_bound,
			args=(numbers[chunck_start:chunck_end],))
		processes.append(p)
	
	start = time.time()
	for process in processes:
		process.start()

	for process in processes:
		process.join()

	duration = time.time() - start
	print("Multiprocessing IO_bound duration:", duration)




if __name__ == '__main__':
    main()