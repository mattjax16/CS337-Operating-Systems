

import os
import multiprocessing
import time

RESULT = []

def square_list(my_list):
	global RESULT

	for num in my_list:
		RESULT.append(num*num)

	print("Result at new process:", RESULT)


def main():
	
	numbers = [1, 2, 3, 4]

	p1 = multiprocessing.Process(target=square_list, args=(numbers,))

	p1.start()

	p1.join()

	print("Result at original process:", RESULT)


if __name__ == '__main__':
	main()