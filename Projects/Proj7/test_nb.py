import threading
import random
import time
import numpy as np
from dataclasses import dataclass, field



@dataclass
class Semaphore():
    '''
    A Semaphore class that allows for the use of a counter and a condition
    variable.

    Attributes:
        counter: An integer that represents the number of threads that are
            currently waiting on the condition variable.
        condition: A condition variable that is used to signal threads that
            the counter is 0.
    '''
    counter: int = field(default=1)
    condition: threading.Condition = field(default = threading.Condition(),
                                           init=False)

    def acquire(self):
        '''
        This method acquires the lock for the condition variable before
        decrementing the counter by one, then it checks if the counter is
        below zero and sets the thread to sleep if true.  Otherwise, it
        releases the lock.

        '''

        ### TODO: Question why does not work without the context manager
        # # acquire the lock
        # self.condition.acquire()
        #
        # # decrement the counter
        # self.counter -= 1
        #
        # # check if the counter is below zero
        # # if so, set the thread to sleep
        # # otherwise, release the lock
        # if self.counter < 0:
        #     self.condition.wait()
        # else:
        #     self.condition.release()

        # acquire the lock for the condition variable with the context manager
        with self.condition:
            # decrement the counter
            self.counter -= 1

            # check if the counter is below zero
            # if so, set the thread to sleep
            # otherwise, release the lock
            if self.counter < 0:
                self.condition.wait()

        return




    def release(self):
        '''
        This method acquires the condition lock and increments the counter by
        one, notifies a single sleeping thread, and releases the lock.
        '''

        # # acquire the lock
        # self.condition.acquire()
        #
        # # increment the counter
        # self.counter += 1
        #
        # # notify a single sleeping thread
        # self.condition.notify()
        #
        # # release the lock
        # self.condition.release()

        # acquire the lock for the condition variable with the context manager
        with self.condition:
            # increment the counter
            self.counter += 1

            # notify a single sleeping thread
            self.condition.notify()

        return

    # Make the Semaphore class a context manager
    __enter__ = acquire
    __exit__ = release








#
# ACCESS = Semaphore2(counter=1)
# EMPTY = Semaphore2(counter=BUFFER_SIZE)
# FULL = Semaphore2(counter=0)


#
# ACCESS = threading.Semaphore(1)
# EMPTY = threading.Semaphore(BUFFER_SIZE)
# FULL = threading.Semaphore(0)



class Producer(threading.Thread):
    def __init__(self,
                 producer_id: int ,
                 num_produce: int,
                 buffer: list,
                 access: Semaphore,
                 empty: Semaphore,
                 full: Semaphore,
                 sleep_amt: float = 1,
                 debug: bool = False):
        '''
        The constructor for the Producer class.

        Args:
            producer_id: An integer that represents the producer number.
            num_produce: An integer that represents the number of items that
                each producer will put into the buffer.
            buffer: A list that represents the buffer.
            access: A Semaphore that represents the access lock for the buffer.
            empty: A Semaphore that represents the empty lock for the buffer.
            full: A `Semaphore` object that represents if the buffer is full or not
                (starts at 0 to represent not full and is incremented by 1
                every time the buffer is full).
            sleep_amt: A float that represents the amount of time the thread
            debug: A boolean that represents whether or not the debug mode is
        '''
        threading.Thread.__init__(self, name=f'Producer {producer_id}')
        self.producer_id = producer_id
        self.num_produce = num_produce
        self.buffer = buffer
        self.access = access
        self.empty = empty
        self.full = full
        self.sleep_amt = sleep_amt
        self.debug = debug
        return

    def run(self):
        '''
        The run method for the Producer class.  This method will produce
        numbers 0 + (producer_num * NUM_PRODUCE) - NUM_PRODUCE + (producer_num *
        NUM_PRODUCE) and put them into the buffer.
        '''
        # Make a unique data array
        data_array = np.arange(self.num_produce) + \
                     (self.producer_id * self.num_produce)

        for data in data_array:

            # Acquire the empty semaphore
            self.empty.acquire()

            # Acquire the access semaphore
            self.access.acquire()

            # Add the data to the buffer
            self.buffer.append(data)

            if self.debug:
                print(f'Producer {self.producer_id} ({threading.current_thread().name}) added {data} to the buffer')
                print(f'Buffer Size: {len(self.buffer)}')

            # Release the access semaphore
            self.access.release()

            # Release the full semaphore
            self.full.release()

            # Sleep for the amount of time specified
            if self.sleep_amt != -1:
                time.sleep(self.sleep_amt)
            else:
                time.sleep(random.random() * 3)

        return






class Consumer(threading.Thread):

    def __init__(self,
                 consumer_id: int,
                 num_consume: int,
                 buffer: list,
                 access: Semaphore,
                 empty: Semaphore,
                 full: Semaphore,
                 sleep_amt: float = 1,
                 debug: bool = False):
        '''
        The constructor for the Consumer class.

        Args:
            consumer_id: An integer that represents the consumer number.
            num_consume: An integer that represents the number of items that
                each consumer will consume from the buffer.
            buffer: A list that represents the buffer.
            access: A `Semaphore` object that represents the number of
                    threads that can access the buffer at a time (starts at 1
                     to represent only one thread can access the buffer at a
                     time).

            empty: A Semaphore that represents the empty lock for the buffer.
            full: A `Semaphore` object that represents tif the buffer is full or not
                    (starts at 0 to represent not full and is incremented by
                    1 every time the buffer is full).
            sleep_amt: A float that represents the amount of time that the
                consumer will sleep for.
            debug: A boolean that represents whether or not the debug mode is
        '''
        threading.Thread.__init__(self)
        self.consumer_id = consumer_id
        self.num_consume = num_consume
        self.buffer = buffer
        self.access = access
        self.empty = empty
        self.full = full
        self.sleep_amt = sleep_amt
        self.debug = debug
        return

    def run(self):
        '''
        The run method for the Consumer class.  This method will consume
        numbers from the buffer and print them out.
        '''
        for _ in range(self.num_consume):

            # Acquire the full semaphore
            self.full.acquire()

            # Acquire the access semaphore
            self.access.acquire()

            # Remove the data from the buffer
            data = self.buffer.pop(0)

            if self.debug:
                print(f'Consumer {self.consumer_id} ({threading.current_thread().name}) popped {data} from the buffer')
                print(f'Buffer Size: {len(self.buffer)}')

            # Release the access semaphore
            self.access.release()

            # Release the empty semaphore
            self.empty.release()

            # Sleep for set sleep amount
            if self.sleep_amt != -1:
                time.sleep(self.sleep_amt)
            else:
                time.sleep(random.random() * 3)


        return





def bufferSimulation(consumer_amt: int = 1, producer_amt: int = 1,
                     consumer_sleep: float = 1, producer_sleep: float = 1,
                     data_amt : int = 50, buffer_size = 10,
                     debug: bool = True):
    '''
    This function will simulate a buffer with a producer and consumers.
    Args:
        consumer_amt (int): The number of consumers to create.
        producer_amt (int): The number of producers to create.
        consumer_sleep (float): The amount of time that each consumer will sleep.
        producer_sleep (float): The amount of time that each producer will sleep.
        data_amt (int): The number of items that each producer will produce.
        buffer_size (int): The size of the buffer.
        debug (bool): If true, will print debug statements.

    Returns:

    '''

    # Make the variables that will be shared among the threads

    buffer = []


    # Semaphores
    access = Semaphore(counter=1)
    empty = Semaphore(counter=buffer_size)
    full = Semaphore(counter=0)

    # Calculate the consumer amount
    num_consume = data_amt // consumer_amt

    # Create the consumers
    consumers = []
    for i in range(consumer_amt):
        consumers.append(Consumer(i, num_consume, buffer, access, empty, full,
                                  consumer_sleep, debug))

    # Create the producers
    producers = []
    for i in range(producer_amt):
        producers.append(Producer(i, data_amt, buffer, access, empty, full,
                                  producer_sleep, debug))


    # Start the producer and consumer threads
    for producer in producers:
        producer.start()
    for consumer in consumers:
        consumer.start()

    # Wait for the producer and consumer threads to finish
    for producer in producers:
        producer.join()
    for consumer in consumers:
        consumer.join()


    if len(buffer) == 0:
        print('The buffer is empty after all the producers and consumers have '
              'finished')
    else:
        print('The buffer is not empty after all the producers and consumers '
              'have finished')

    print(f'Done with the simulation')
    return



def main():
    bufferSimulation(consumer_amt=1, producer_amt=1, consumer_sleep=1,
                     producer_sleep=3, data_amt=15, buffer_size=10, debug=True)
    return


if __name__ == '__main__':
    main()