
from concurrent.futures import ThreadPoolExecutor

def square(n):
    return n*n


def main():

	my_list = [1,2,3,4,5]
	result = []

	executor = ThreadPoolExecutor()  #max_workers=4

	result = executor.map(square, my_list)
	executor.shutdown(wait=True)

	for item in result:
		print(result)


if __name__ == '__main__':
	main()