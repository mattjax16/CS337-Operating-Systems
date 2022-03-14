import requests
import time
from concurrent.futures import ThreadPoolExecutor

URL = "http://httpbin.org/uuid"

def fetch(session, url):
	with session.get(url) as response:
		print(response.json()['uuid'])


def main():

	start = time.time()
	with ThreadPoolExecutor() as executor: 		#max_workers=10
		with requests.Session() as session:
			executor.map(fetch, [session] * 100, [URL] * 100)
			executor.shutdown(wait=True)

	duration = time.time() - start
	print("multithreading code:", duration)

if __name__ == '__main__':
	main()