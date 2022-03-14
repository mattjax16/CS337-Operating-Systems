

import multiprocessing

def print_records(records):
    for record in records:
        print("Name: {0}\nScore: {1}\n".format(record[0], record[1]))

def insert_record(record, records):
    records.append(record)
    print("New record added!\n")


def main():
    records = [('Sam', 10), ('Adam', 9), ('Kevin',9)]
    new_record = ('Jeff', 8)

    p1 = multiprocessing.Process(target=insert_record, args=(new_record, records))
    p2 = multiprocessing.Process(target=print_records, args=(records,))
    
    p1.start()
    p1.join()
    
    p2.start()
    p2.join()


if __name__ == '__main__':
	main()