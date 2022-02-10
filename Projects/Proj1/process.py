# CS337 Spring 2022 - Operating Systems Prof. Al Madi
# process.py
# Matthew Bass
# 02/09/2022

# This is a file to create a Process class

class Process:
    # The Process class implements a process in the ready state for scheduling
    # and takes in the parameters: id, burst_time, arrival_time, and priority
    def __init__(self,id,burst_time, arrival_time,priority):

        # Defining private properties
        self.__id = id
        self.__burst_time = burst_time
        self.__arrival_time = arrival_time
        self.__priority = priority
        self.__wait_time = 0
        self.__turnaround_time = 0
        return

    # Defining getters
    @property
    def id(self):
        return self.__id

    @property
    def burst_time(self):
        return self.__burst_time

    @property
    def arrival_time(self):
        return self.__arrival_time

    @property
    def priority(self):
        return self.__priority

    @property
    def wait_time(self):
        return self.__wait_time

    @property
    def turnaround_time(self):
        return self.__turnaround_time


    #Defining setters

    @burst_time.setter
    def burst_time(self, val):
        self.__burst_time = val
        return

    @arrival_time.setter
    def arrival_time(self, val):
        self.__arrival_time = val
        return

    @priority.setter
    def priority(self, val):
        self.__priority = val
        return

    @wait_time.setter
    def wait_time(self, val):
        self.__wait_time = val
        return

    @turnaround_time.setter
    def turnaround_time(self,val):
        self.__turnaround_time = val
        return





# Main Testing function for Process Class
def main():
    test_proccess_1 = Process(1,4,3,6)

    print(test_proccess_1.id)
    # test_proccess_1.id = 1 # This shouldnt work becouse property is private
    # AttributeError: can't set attribute
    print(test_proccess_1.turnaround_time)

    test_proccess_1.turnaround_time+= 9
    print(test_proccess_1.turnaround_time)


if __name__ == "__main__":
    main()