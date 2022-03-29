'''
CS337 Spring 2022 - Operating Systems Prof. Al Madi
Project 6 - Software Synchronization Solutions
synch_solutions.py
Matthew Bass
03/29/2022

This is the code to hold all the solutions to the project and also
to outline the abstraction class that will be used for all the "locks"
'''
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

# Abstract class for all the solutions
class SyncSolution(ABC):


    def __init__(self) -> None:
        self.name = None
        return

    @abstractmethod
    def lock(self) -> None:
        pass

    @abstractmethod
    def unlock(self) -> None:
        pass



def main():
    return


if __name__ == '__main__':
    main()