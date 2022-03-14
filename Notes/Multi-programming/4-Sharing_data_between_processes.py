

import os
import multiprocessing


def square_list(my_list, result):

	for index, num in enumerate(my_list):
		result[index] = num*num

	print("Result at new process:")
	for index in range(4):
		print(result[index], end=', ')
	print()


def main():
	
	numbers = [1, 2, 3, 4]
	result = multiprocessing.Array('i', 4)

	p1 = multiprocessing.Process(target=square_list, args=(numbers, result))

	p1.start()

	p1.join()

	print("Result at original process:")
	for index in range(4):
		print(result[index], end=', ')


if __name__ == '__main__':
	main()