import requests
import time

URL = "http://httpbin.org/uuid"

def fetch(session, url):
	with session.get(url) as response:
		print(response.json()['uuid'])


def main():

	start = time.time()

	with requests.Session() as session:
		for _ in range(100):
			fetch(session, URL) 

	duration = time.time() - start
	print("serial code:", duration)

if __name__ == '__main__':
	main()