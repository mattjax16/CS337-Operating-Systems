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

        # Sleep for a random amount of time
        # time.sleep(random.randint(1,3))
        time.sleep(1)

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



def bufferSimulation():

    # Create the producer and consumer threads
    producer = threading.Thread(target=producerFunc)
    consumer = threading.Thread(target=consumerFunc)

    # Start the producer and consumer threads
    producer.start()
    consumer.start()

    # Wait for the producer and consumer threads to finish
    producer.join()
    consumer.join()

    if len(BUFFER) == 0:
        print('The buffer is empty')
    else:
        print('The buffer is not empty')

    print(f'Done with the simulation')


def main():
    bufferSimulation()
    return


if __name__ == '__main__':
    main()