'''
CS337 Spring 2022 - Operating Systems Prof. Al Madi
Project 3 - Preemptive CPU Scheduling Analysis
process.py
Matthew Bass
02/28/2022

This is a file to create a Process class
'''


class Process:
    # The Process class implements a process for the scheduling sim
    def __init__(self, id, duty, arrival_time, priority):
        '''

        :param id: the id of the process
        :param duty: list called duty that defines CPU time and I/O time.
                     This list contains integers that alternate between CPU
                     time and I/O time
        :param arrival_time: (int) the arrival time of the process
        :param priority: (Number) the priority of the process
        '''

        # Defining private properties
        self.__id = id
        self.__duty = [work for work in duty]
        self.__initial_duty = [work for work in duty]

        self.__burst_time = int(duty[0])
        self.__initial_burst_time = int(duty[0])
        self.__arrival_time = arrival_time
        self.__completion_time = 0
        self.__priority = priority
        self.__response_time = 0
        self.__wait_time = 0
        self.__turnaround_time = 0
        self.__status = "running"
        self.__times_worked_on = 0
        self.__queue = 0
        self.__rr_num = 0
        self.__io_waiting_times = []
        self.__vruntime = 0
        self.__weight = 5
        self.__proc_type = 6
        return

    # Defining getters
    @property
    def proc_type(self):
        return self.__proc_type

    @property
    def vruntime(self):
        return self.__vruntime

    @property
    def weight(self):
        return self.__weight

    @property
    def id(self):
        return self.__id

    @property
    def duty(self):
        return self.__duty

    @property
    def arrival_time(self):
        return self.__arrival_time

    @property
    def completion_time(self):
        return self.__completion_time

    @property
    def priority(self):
        return self.__priority

    @property
    def response_time(self):
        return self.__response_time

    @property
    def wait_time(self):
        return self.__wait_time

    @property
    def turnaround_time(self):
        return self.__turnaround_time

    @property
    def initial_duty(self):
        return self.__inital_duty

    @property
    def total_CPU_time(self):
        total_cpu_time = self.__initial_duty[0::2]
        return sum(total_cpu_time)

    @property
    def current_CPU_time(self):
        cpu_times = self.__duty[0::2]
        for cpu_time in cpu_times:
            if cpu_time > 0:
                return cpu_time
        return 0

    @property
    def total_IO_time(self):
        total_io_time = self.__initial_duty[1::2]
        return sum(total_io_time)

    @property
    def num_IO_times(self):
        total_io_time = self.__initial_duty[1::2]
        return len(total_io_time)

    @property
    def io_waiting_times(self):
        return self.__io_waiting_times

    @property
    def burst_time(self):
        return self.__burst_time

    @property
    def initial_burst_time(self):
        return self.__initial_burst_time

    @property
    def status(self):
        return self.__status

    @property
    def times_worked_on(self):
        return self.__times_worked_on

    @property
    def queue(self):
        return self.__queue

    @property
    def rr_num(self):
        return self.__rr_num

    @property
    def duty_type(self):
        '''
        Indicates wether the next duty to be worked on is a
        CPU bound or I/O bound process
        :return: (string) CPU or I/O
        '''

        # Get dutties that still need to be worked on
        duties_left = []
        for duty in self.__duty:
            if duty != 0:
                duties_left.append(duty)

        # See if CPU or IO based on length
        # if even CPU and odd I/0
        if(len(duties_left) % 2 == 1):
            return "CPU"
        else:
            return "I/O"

    # Defining setters

    @proc_type.setter
    def proc_type(self, val):
        self.__proc_type = val
        return

    @vruntime.setter
    def vruntime(self, val):
        self.__vruntime = val
        return

    @weight.setter
    def weight(self, val):
        self.__weight = val
        return

    @burst_time.setter
    def burst_time(self, val):
        self.__burst_time = val
        return

    @duty.setter
    def duty(self, val):
        self.__duty = val
        return

    @arrival_time.setter
    def arrival_time(self, val):
        self.__arrival_time = val
        return

    @completion_time.setter
    def completion_time(self, val):
        self.__completion_time = val
        return

    @priority.setter
    def priority(self, val):
        self.__priority = val
        return

    @response_time.setter
    def response_time(self, val):
        self.__response_time = val
        return

    @wait_time.setter
    def wait_time(self, val):
        self.__wait_time = val
        return

    @turnaround_time.setter
    def turnaround_time(self, val):
        self.__turnaround_time = val
        return

    @times_worked_on.setter
    def times_worked_on(self, val):
        self.__times_worked_on = val
        return

    @io_waiting_times.setter
    def io_waiting_times(self, val):
        self.__io_waiting_times = val

    @queue.setter
    def queue(self, val):
        self.__queue = val

    @rr_num.setter
    def rr_num(self, val):
        self.__rr_num = val

    def process_worked_on(self):
        '''
        Increments the process' times_worked_on by one
        This is done to safely keep track of the process'
        times worked on

        :return:
        '''
        self.__times_worked_on += 1
        return

    @status.setter
    def status(self, val):

        # check for either running or waiting
        if val != "running" or val != "waiting":
            print(f"Error {val} is not a valid status!!! Chose running or "
                  f"waiting!!\n")
            return
        self.__status = val
        return

    def change_status(self):
        """
        A function to change the status of a process
        :return:
        """
        if self.status == "running":
            self.__status = "waiting"

        elif self.status == "waiting":
            self.__status = "running"

        return

    def run_process(self, debug=False):
        '''
        This function "runs" the process by subtracting 1 from
        the duty list of the left most number that is greater than 0

        :param debug: (bool) if true debug print outs will be displayed
        :return:
        '''
        for work_id, work in enumerate(self.__duty):
            if work > 0:
                self.__duty[work_id] = work - 1
                return

        if debug:
            print("Warning Nothing left to work on!!!\n")
        return

    def __repr__(self) -> str:
        """Provides the process representation its layout."""
        return f"[ID = {self.id}, Ar_T = {self.__arrival_time}," \
               f"Vr_T = {self.vruntime},P = {self.priority}]"


# Main Testing function for Process Class
def main():
    test_proccess_1 = Process(id=1, duty=[4, 1, 3], arrival_time=3,
                              priority=6)

    print(test_proccess_1.id)
    # test_proccess_1.id = 1 # This shouldnt work becouse property is private
    # AttributeError: can't set attribute
    print(test_proccess_1.status)

    print(f"Test Process Duty : {test_proccess_1.duty}")

    print(test_proccess_1.burst_time)

    test_proccess_1.change_status()
    print(test_proccess_1.status)


if __name__ == "__main__":
    main()
