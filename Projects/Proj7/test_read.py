import threading
import random
import time
import contextlib
import io
import sys
import numpy as np
import networkx as nx
from dataclasses import dataclass, field

class Tests (threading.Thread):
    '''
    Test Class Parrent class
    '''
    is_running = True

    def __init__(self, name):
        threading.Thread.__init__(self, name=name)

class TestWrite(Tests):
    '''
    Test class for writing output
    '''

    def __init__(self):
        Tests.__init__(self, name='TestWrite')

    def run(self):
        '''
        Run test
        '''
        count = 0
        while self.is_running:
            print(f"{self.name} is running {count}")
            time.sleep(random.uniform(0.2, 0.6))
            count += 1


class TestRead(Tests):
    '''
    Test class for reading input
    '''

    def __init__(self):
        Tests.__init__(self, name='TestRead')

    def run(self):
        '''
        Run test
        '''
        captured_output = io.StringIO()  # Create StringIO object
        last_line_amt = 1
        while self.is_running:
            with contextlib.redirect_stdout(captured_output):

                time.sleep(0.1)

            lines = captured_output.getvalue().split('\n')

            if len(lines) > last_line_amt:

                print(f"READ {self.name} is running {lines[-2]}")
                last_line_amt = len(lines)


class TestRead2(Tests):
    '''
    Test class for reading input
    '''

    def __init__(self):
        Tests.__init__(self, name='TestRead2')

    def run(self):
        '''
        Run test
        '''
        old_stdout = sys.stdout
        sys.stdout = mystdout = io.StringIO()  # Create StringIO object
        while self.is_running:
            pass
        sys.stdout = old_stdout


        # split all the string into lines
        lines = mystdout.getvalue().split('\n')
        # Print the lines
        for line in lines:
            print(f"READ {self.name} is running {line}")


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
    condition: threading.Condition = field(default=threading.Condition(),
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



def test_ct():

    # Create test threads
    test_write = TestWrite()
    test_read = TestRead2()

    # Start test threads
    test_write.start()
    test_read.start()

    time.sleep(10)
    Tests.is_running = False

    # Wait for test threads to finish
    test_write.join()

    print(f"Done running test")


def main():
    test_ct()

    return


if __name__ == '__main__':
    main()