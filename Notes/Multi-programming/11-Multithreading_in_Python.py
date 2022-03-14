import threading
import time
import os

def print_cube(num):
    print(threading.current_thread().name, os.getpid())
    print("Cube: {}".format(num * num * num))


def print_square(num):
    print(threading.current_thread().name, os.getpid())
    print("Square: {}".format(num * num))

def main():

	t1 = threading.Thread(target=print_cube, args=(3,), name='t1')
	t2 = threading.Thread(target=print_square, args=(4,), name='t2')

	t1.start()
	t2.start()

	t1.join()
	t2.join()


if __name__ == '__main__':
    main()