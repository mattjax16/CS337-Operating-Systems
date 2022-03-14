

import os
import multiprocessing

def print_cube(num):
    print(os.getpid())
    print("Cube: {}".format(num * num * num))


def print_square(num):
    print(os.getpid())
    print("Square: {}".format(num * num))


def main():
	# ID of this process
	print("Main process ID:", os.getpid())

	# number of processors
	print("Processors:", multiprocessing.cpu_count())

	p1 = multiprocessing.Process(target=print_cube, args=(3,))
	p2 = multiprocessing.Process(target=print_square, args=(4,))

	p1.start()
	print("p1 alive? ", p1.is_alive())
	p2.start()

	p1.join()
	p2.join()
	print("p1 alive? ", p1.is_alive())


if __name__ == '__main__':
	main()