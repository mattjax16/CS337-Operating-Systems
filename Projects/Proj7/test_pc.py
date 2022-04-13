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







# Buffer Variables
BUFFER_SIZE = 10
BUFFER = []

# The Number of Items each producer will put into the buffer
NUM_PRODUCE = 20

# The number of producer and consumer threads
NUM_PRODUCERS = 1
NUM_CONSUMERS = 1

# Semaphores
ACCESS = Semaphore(counter=1)
EMPTY = Semaphore(counter=BUFFER_SIZE)
FULL = Semaphore(counter=0)
#
# ACCESS = Semaphore2(counter=1)
# EMPTY = Semaphore2(counter=BUFFER_SIZE)
# FULL = Semaphore2(counter=0)


#
# ACCESS = threading.Semaphore(1)
# EMPTY = threading.Semaphore(BUFFER_SIZE)
# FULL = threading.Semaphore(0)


class Producer(threading.Thread):
    '''
    A Producer class that inherits from the threading.Thread class.  This
    class will produce numbers 0 + (producer_num * NUM_PRODUCE) -
    NUM_PRODUCE + (producer_num * NUM_PRODUCE) and put them into the BUFFER.
    '''

    def __init__(self,
                 producer_num: int ,
                 data_amt: int,
                 buffer: list,
                 access: Semaphore,
                 empty: Semaphore,
                 full: Semaphore,
                 sleep_amt: float = 1,
                 debug: bool = False):
        '''
        The constructor for the Producer class.

        Args:
            producer_num: An integer that represents the producer number.
            data_amt: An integer that represents the number of items that
                each producer will put into the buffer.
            buffer: A list that represents the buffer.
            access: A Semaphore that represents the access lock for the buffer.
            empty: A Semaphore that represents the empty lock for the buffer.
            full: A Semaphore that represents the full lock for the buffer.
            sleep_amt: A float that represents the amount of time the thread
            debug: A boolean that represents whether or not the debug mode is
        '''
        threading.Thread.__init__(self)
        self.producer_num = producer_num
        self.data_amt = data_amt
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
        NUM_PRODUCE) and put them into the BUFFER.
        '''
        # Make a unique data array
        data_array = np.arange(self.data_amt) + \
                     (self.producer_num * self.data_amt)

        for data in data_array:

            # Acquire the empty semaphore
            self.empty.acquire()

            # Acquire the access semaphore
            self.access.acquire()

            # Add the data to the buffer
            self.buffer.append(data)

            if self.debug:
                print(f'Producer {self.producer_num} ({threading.current_thread().name}) added {data} to the buffer')
                print(f'Buffer Size: {len(self.buffer)}')

            # Release the access semaphore
            self.access.release()

            # Release the full semaphore
            self.full.release()

            # Sleep for a random amount of time
            # time.sleep(random.randint(1,3))
            time.sleep(self.sleep_amt)

        return



def producerFunc(debug: bool = True, producerNum: int = 0):
    '''
    This function will put a unique number into the buffer.

    args:
        debug: A boolean that will print debug statements if true.
        producerNum: The number of the producer thread.
    '''

    # Get thr global variables
    global BUFFER, ACCESS, EMPTY, FULL

    # Make a unique data array
    data_array = np.arange(NUM_PRODUCE) + (producerNum * NUM_PRODUCE)

    for data in data_array:


        # Acquire the empty semaphore
        EMPTY.acquire()

        # Acquire the access semaphore
        ACCESS.acquire()

        # Add the data to the buffer
        BUFFER.append(data)

        if debug:
            print(f'Producer {producerNum} ({threading.current_thread().name}) added {data} to the buffer')
            print(f'Buffer Size: {len(BUFFER)}')

        # Release the access semaphore
        ACCESS.release()

        # Release the full semaphore
        FULL.release()

        # Sleep for set sleep amount
        time.sleep(1)

    return


class Consumer(threading.Thread):
    '''
    This is a Consumer class that inherits from the threading.Thread class.
    This class will consume NUM_PRODUCE/NUM_CONSUMERS = num_consumed numbers from
    the BUFFER and print them out.
    '''

    def __init__(self,
                 consumer_num: int,
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
            consumer_num: An integer that represents the consumer number.
            num_consume: An integer that represents the number of items that
                each consumer will consume from the buffer.
            buffer: A list that represents the buffer.
            access: A Semaphore that represents the access lock for the buffer.
            empty: A Semaphore that represents the empty lock for the buffer.
            full: A Semaphore that represents the full lock for the buffer.
            sleep_amt: A float that represents the amount of time that the
                consumer will sleep for.
            debug: A boolean that represents whether or not the debug mode is
        '''
        threading.Thread.__init__(self)
        self.consumer_num = consumer_num
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
        numbers from the BUFFER and print them out.
        '''
        for _ in range(self.num_consume):

            # Acquire the full semaphore
            self.full.acquire()

            # Acquire the access semaphore
            self.access.acquire()

            # Remove the data from the buffer
            data = self.buffer.pop(0)

            if self.debug:
                print(f'Consumer {self.consumer_num} ({threading.current_thread().name}) popped {data} from the buffer')
                print(f'Buffer Size: {len(self.buffer)}')

            # Release the access semaphore
            self.access.release()

            # Release the empty semaphore
            self.empty.release()

            # Sleep for set sleep amount
            time.sleep(self.sleep_amt)

        return

def consumerFunc(debug: bool = True, consumerNum: int = 0):
    '''
    This function will put a unique number into the buffer.

    Args:
        debug:  If true, will print debug statements.
    '''

    # Get thr global variables
    global BUFFER, ACCESS, EMPTY, FULL

    for _ in range(NUM_PRODUCE):



        # Acquire the full semaphore
        FULL.acquire()

        # Acquire the access semaphore
        ACCESS.acquire()

        # get the data from the buffer
        data = BUFFER.pop()

        if debug:
            print(f'Consumer {consumerNum} {threading.current_thread().name}'
                f' poped {data} from the buffer')
            print(f'Buffer Size: {len(BUFFER)}')


        # Release the access semaphore
        ACCESS.release()

        # Release the empty semaphore
        EMPTY.release()

        # Sleep for a random amount of time
        time.sleep(3)

    return



def bufferSimulation(num_consumers: int = 1, num_producers: int = 1,
                     consumer_sleep: float = 1, producer_sleep: float = 1,
                     data_amt : int = 50, buffer_size = 10,
                     debug: bool = True):
    '''
    This function will simulate a buffer with a producer and consumers.
    Args:
        num_consumers (int): The number of consumers to create.
        num_producers (int): The number of producers to create.
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
    num_consume = data_amt // num_consumers

    # Create the consumers
    consumers = []
    for i in range(num_consumers):
        consumers.append(Consumer(i, num_consume, buffer, access, empty, full,
                                  consumer_sleep, debug))

    # Create the producers
    producers = []
    for i in range(num_producers):
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


    if len(BUFFER) == 0:
        print('The buffer is empty after all the producers and consumers have '
              'finished')
    else:
        print('The buffer is not empty after all the producers and consumers '
              'have finished')

    print(f'Done with the simulation')


def main():
    bufferSimulation(num_consumers=1, num_producers=1, consumer_sleep=1,
                     producer_sleep=3, data_amt=50, buffer_size=10, debug=True)
    return


if __name__ == '__main__':
    main()