

import os
import multiprocessing
import time

def print_cube(num):
    #print(os.getpid())

    for i in range(99999999):
    	i * i

    #print("Cube: {}".format(num * num * num))


def print_square(num):
    #print(os.getpid())

    for i in range(99999999):
    	i * i

    #print("Square: {}".format(num * num))


def main():
	# Serial code
	start = time.time()
	print_cube(100)
	print_square(100)
	duration = time.time() - start
	print("Serial", duration)

	p1 = multiprocessing.Process(target=print_cube, args=(3,))
	p2 = multiprocessing.Process(target=print_square, args=(4,))

	# parallel code
	start = time.time()
	p1.start()
	p2.start()

	p1.join()
	p2.join()
	duration = time.time() - start
	print("Parallel", duration)


if __name__ == '__main__':
	main()