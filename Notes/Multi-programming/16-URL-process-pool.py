import requests
import time
import multiprocessing

URL = "http://httpbin.org/uuid"

def fetch(session, url):
	with session.get(url) as response:
		print(response.json()['uuid'])


def main():

	start = time.time()
	with multiprocessing.Pool() as pool:
		with requests.Session() as session:
			
			pool.starmap(fetch, [(session, URL) for _ in range(100)])

	duration = time.time() - start
	print("multiprocessing code:", duration)

if __name__ == '__main__':
	main()