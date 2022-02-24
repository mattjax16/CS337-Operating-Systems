'''
CS337 Spring 2022 - Operating Systems Prof. Al Madi
Project 2 - Preemptive CPU Scheduling Analysis
operating_system.py
Matthew Bass
02/21/2022

The operating_system.py file where processes are created, scheduler runs,
and statistics are calculated.
'''

# Importing the necessary packages and objects
import pandas as pd
import scheduler
from process import Process
from datetime import datetime as dt
import numpy as np
import random
from collections import ChainMap

# Libraries for plotting
import matplotlib as mpl

import matplotlib.pyplot as plt
import plotly.express as px


def kernal(
        selected_scheduler,
        processes=None,
        quantum=2,
        quantum2=7,
        debug=True,
        CPU_To_Csv=False,
        Processes_to_csv=False,
        save_with_date=False,
        file_proc_name=None,
        write_both_results=True):
    """
     Simulates the CPU scheduling aspects of an operating system kernel.

    :param selected_scheduler: (Function) one of the scheduling functions from scheduler.py
    :param processes: (list) a list of processes for the kernal to schuedle
    :param quantum: (int) the maximum amount of timesteps a process will
                    run for before it its put back to the waiting state (or finishes)
                    and the next process is started.
    :param quantum2: (int) the quantum for the second RR queue in the MLFQ alg
    :param debug: (Boolean) If true output messages will be printed from the selected_scheduler function
    :param CPU_To_Csv: (Boolean) if true results of CPU will be written to a csv
    :param Processes_to_csv: (Boolean) if true results of Scheduled_Processes will be written to a csv
     :param save_with_date: (Boolean) if true results of csvs will be written with timestamp
     :param file_proc_name: (String) if passed csvs will be written with the
      :param write_both_results: (Boolean) if true both results will be
      written to one csv
     end names
     with timestamp
    :return:
    """

    CPU = []  # A list to hold the data for some of the
    # scheduled process for the CPU

    Scheduled_Processes = []  # A list to hold the scheduled process for the CPU

    ready = []  # A list to hold the process scheduled ready to be scheduled

    wait = []  # A list to hold all processes with I/0 work (waiting for input)

    time = 0  # creating the intial time for the kernal

    # If there are no processes passed make a test list of 5 processes
    if processes is None:
        if debug:
            print(f"Warning no processes were passed!! Making test Processes")

        processes = [Process(1, [10, 6, 7], 0, 30), Process(2, [4, 3, 3], 3,
                                                            35),
                     Process(3, [2, 3, 4], 1, 36),
                     Process(4, [5, 2, 7], 7, 20)]

    # adding the proccesses to the ready list
    # increment time until there is one
    while len(ready) == 0:
        scheduler.add_ready(processes, ready, time)
        if len(ready) == 0:
            time += 1

    # running scheduler for all processes in ready
    while processes or ready or wait:



        if selected_scheduler == scheduler.RR_scheduler:
            time = selected_scheduler(
                processes=processes,
                ready=ready,
                wait=wait,
                CPU=CPU,
                Scheduled_Processes=Scheduled_Processes,
                time=time,
                quantum=quantum,
                debug=debug)
        elif selected_scheduler == scheduler.MLFQ_scheduler:
            time = selected_scheduler(
                processes=processes,
                ready=ready,
                wait=wait,
                CPU=CPU,
                Scheduled_Processes=Scheduled_Processes,
                time=time,
                quantum1=quantum,
                quantum2=quantum2,
                debug=debug)

        elif selected_scheduler == scheduler.SRT_scheduler or \
                selected_scheduler == scheduler.Preemptive_Priority_scheduler:
            time = selected_scheduler(
                processes=processes,
                ready=ready,
                wait=wait,
                CPU=CPU,
                Scheduled_Processes=Scheduled_Processes,
                time=time,
                debug=debug)
        else:
            time = selected_scheduler(
                processes,
                ready,
                CPU,
                Scheduled_Processes,
                time,
                debug=debug)

    # Once all the processes in the Processes have been scheduled
    # calculate their wait time and turn around time
    calc_wait_and_tunaround(Scheduled_Processes)

    # Write data to csv files if either
    # CPU_To_Csv or Processes_to_csv is True
    if CPU_To_Csv or Processes_to_csv or write_both_results:

        if save_with_date:
            # get the current time for writing the file
            time = "_" + dt.now().strftime(format="%y-%m-%d_%H-%M-%S")
        else:
            time = ""

        if file_proc_name is None:
            file_proc_name = ""
        else:
            file_proc_name = f"{file_proc_name}_"

        # get the kind of scheduler used
        if selected_scheduler == scheduler.FCFS_scheduler:
            sched = "FCFS"
        elif selected_scheduler == scheduler.SJF_scheduler:
            sched = "SJF"
        elif selected_scheduler == scheduler.Priority_scheduler:
            sched = "Priority"
        elif selected_scheduler == scheduler.Priority_Aging_scheduler:
            sched = "Priority_Aging"
        elif selected_scheduler == scheduler.Preemptive_Priority_scheduler:
            sched = "Preemptive_Priority"
        elif selected_scheduler == scheduler.Priority_Turnaround_scheduler:
            sched = "Priority_Turnaround"
        elif selected_scheduler == scheduler.SRT_scheduler:
            sched = "SRT"
        elif selected_scheduler == scheduler.MLFQ_scheduler:
            sched = "MLFQ"
        elif selected_scheduler == scheduler.RR_scheduler:
            if quantum > 0:
                sched = f"RR_Q{quantum}"
            else:
                if debug:
                    print(f"Error {quantum} is not a valid " +
                          f"Quantum Size!!")
                    exit()
        elif debug:
            print(f"Error {selected_scheduler} is not a valid " +
                  f"scheduling function!!")
            exit()

        # Writing CPU data
        if CPU_To_Csv:
            # reverse CPU so it is written to df in process order
            CPU.sort(key=lambda x: x['id'], reverse=True)
            pd.DataFrame(CPU).to_csv(
                f"data/CPU_Data/CPU_{sched}_{file_proc_name}results" +
                f"{time}.csv",
                index=False)

        # Writing Scheduled_Processes data
        if Processes_to_csv:
            Scheduled_Processes.sort(key=lambda x: x.id, reverse=True)

            # creating a list of dicts of all
            # the process attributes
            SP_dict_list = [{"id": x.id, "burst time": x.burst_time,
                             "initial burst time": x.initial_burst_time,
                             "arrival time": x.arrival_time,
                             "completion time": x.completion_time,
                             "priority": x.priority,
                             "wait time": x.wait_time,
                             "turnaround time": x.turnaround_time,
                             "times worked on": x.times_worked_on
                             } for x in Scheduled_Processes]

            # Writing the CSV file
            SP_dict_list.sort(key=lambda x: x['id'], reverse=True)
            pd.DataFrame(SP_dict_list).to_csv(
                f"data/Sched_Process_Data/Scheduled_Processes" +
                f"_{sched}_{file_proc_name}results{time}.csv",
                index=False)

        if write_both_results:

            # Unpacking data from CPU
            processes_activity = {}
            for cpu_proc in CPU:
                if f"{cpu_proc['id']}" in processes_activity:
                    processes_activity[f"{cpu_proc['id']}"] += [{'start ' +
                                                                 str(len(processes_activity[f"{cpu_proc['id']}"]) +
                                                                     1): cpu_proc['start'], 'finish ' +
                                                                 str(len(processes_activity[f"{cpu_proc['id']}"]) +
                                                                     1): cpu_proc['finish'], 'priority ' +
                                                                 str(len(processes_activity[f"{cpu_proc['id']}"]) +
                                                                     1): cpu_proc['priority']}]
                else:
                    processes_activity[f"{cpu_proc['id']}"] = [
                        {'start 1': cpu_proc['start'],
                         'finish 1': cpu_proc['finish'],
                         'priority 1': cpu_proc['priority']}]

            # making Start Stop df for all data
            # start by padding data
            padded_CPU_activities = []
            max_times_worked = max(
                [len(proc) for proc in processes_activity.values()])
            for proc_id, proc_times in processes_activity.items():
                if len(proc_times) < max_times_worked:  # padding the processes
                    for num in range(
                            len(proc_times) + 1,
                            max_times_worked + 1):
                        # making default padding stats
                        proc_times.append({f"start {num}": -1,
                                           f"finish {num}": -1,
                                           f"priority {num}": -1})

                # add the id of the process
                proc_times.reverse()
                proc_times.append({"p id": int(proc_id)})

                # concat all the dictionaries and add them to padded
                # activities
                padded_CPU_activities.append(dict(ChainMap(*proc_times)))

            # Make Process activity df
            padded_CPU_activities.sort(key=lambda x: x["p id"], reverse=True)
            cpu_df = pd.DataFrame(padded_CPU_activities)

            """
            Making IO wait times DF
            """
            io_df_list = []
            for proc in Scheduled_Processes:

                proc_io_dict = {"io id": proc.id}

                # loop through all the io waiting times
                for index, io_wait in enumerate(proc.io_waiting_times):
                    proc_io_dict[f'io start {index}'] = io_wait[0]
                    proc_io_dict[f'io end {index}'] = io_wait[1]

                io_df_list.append(proc_io_dict)

            # pad the io_df_list
            max_io_wait_times = max([len(proc) for proc in io_df_list])
            for proc_id, proc_io_times in enumerate(io_df_list):
                if len(proc_io_times) < max_io_wait_times:  # padding the processes
                    for num in range(
                            len(proc_io_times) + 1,
                            max_io_wait_times + 1):
                        # making default padding stats
                        proc_io_times[f'io start {index}'] = -1
                        proc_io_times[f'io end {index}'] = -1

            # making df
            io_df_list.sort(key=lambda x: x["io id"], reverse=True)
            io_df = pd.DataFrame(io_df_list)

            # creating a list of dicts of all
            # the process attributes
            SP_dict_list = [{"id": x.id, "burst time": x.burst_time,
                             "initial burst time": x.initial_burst_time,
                             "arrival time": x.arrival_time,
                             "final priority": x.priority,
                             "wait time": x.wait_time,
                             "turnaround time": x.turnaround_time,
                             "response time": x.response_time,
                             "total CPU time": x.total_CPU_time,
                             "total I/O time": x.total_IO_time,
                             "times worked on": x.times_worked_on
                             } for x in Scheduled_Processes]

            # making dataframe
            SP_dict_list.sort(key=lambda x: x["id"], reverse=True)
            sp_df = pd.DataFrame(SP_dict_list)

            # Combining the 2 dataframe
            main_df = pd.concat([sp_df, cpu_df, io_df], axis=1)
            main_df.drop(['p id', 'io id'], inplace=True, axis=1)

            main_df.to_csv(
                f"data/Combined_Data/All" +
                f"_{sched}_{file_proc_name}results{time}.csv",
                index=False)

    return


def calc_wait_and_tunaround(Scheduled_Processes):
    '''
    Calculates the wait time and turn around for all the scheduled processes
    :param Scheduled_Processes: this is a list of all the process that have been scheduled
    :return:
    '''

    # Sort the Scheduled_Processes based on their id
    Scheduled_Processes.sort(key=lambda x: x.id, reverse=True)
    for proc in Scheduled_Processes:
        proc.turnaround_time = proc.completion_time - proc.arrival_time
        proc.wait_time = proc.turnaround_time - proc.total_CPU_time

    return


# defining a function to plot CPU Data
def plotCPU(cpu_results, title="CPU Results Timeline"):
    '''
    A function to plot a cpu results df from
    operating_system.py
    :param cpu_results: (dataframe) the CPU results from the kernal simulation
    :param title: (string) the title for the plot
    :return:
    '''

    # making the timeline plot
    fig = px.timeline(cpu_results, x_start="start", x_end="finish", y="id",
                      color="priority", labels={"id": "Process ID"})

    # adding the title
    fig.update_layout(title_text=title, title_x=0.5)

    # setting up the x axis by finding the delta
    cpu_results['delta'] = cpu_results['finish'] - cpu_results['start']
    fig.data[0].x = cpu_results.delta.tolist()
    fig.layout.xaxis = dict(
        tickmode='linear',
        tick0=0,
        dtick=1,
        title_text="Time (clock ticks)",
        showline=True
    )

    # setting up the yaxis
    fig.layout.yaxis = dict(
        tickmode='linear',
        tick0=0,
        dtick=1,
        title_text="Process ID",
    )
    fig.show()

    return


#defining a function to print the kernal result stats
def printKernalResultStats(kernal_results,title = None):
    '''

    :param kernal_results: (dataframe) the combined results from the kernal
    simulation
    :return:
    '''
    if not title:
        title = ""

    print( f"Average {title} Stats:\n-------\n"
            f"Wait Time "
            f"{kernal_results['turnaround time'].mean():.2f}\n" +
            f"Turn-Around Time {kernal_results['wait time'].mean():.2f}\n" +
            f"Response Time {kernal_results['response time'].mean():.2f}\n" +
            f"CPU Time {kernal_results['total CPU time'].mean():.2f}\n" +
            f"I/O Time {kernal_results['total I/O time'].mean():.2f}\n"
            f"Throughput "+
            f"{(kernal_results.shape[0]/kernal_results.filter(like='start').values.max()) :.4f}"+
            f" proc/sec\n")
    return

# defining a function to plot Scheduled_Processes data along with CPU data
def plotKernalResults(
        kernal_results,
        plot_wait_times=True,
        plot_io_times=True,
        title="Scheduled Processes Results Timeline",
        stats=True,
        stats_text_size=9,
        title_size = 12,
        linewidth = 295,
        figsize=(
            18,
            7)):
    '''
    A function to plot the kernal results df from (All data)
    operating_system.py

    :param kernal_results: (dataframe) the combined results from the kernal
    simulation
    :param title: (string) the title for the plot
    :param plot_wait_times: (bool) if true wait times when no work is being
    done will be shown
    :param plot_io_times: (bool) if true io working times will be shown
    :param stats: (bool) if true average wait and turn around time will be shown
    :param stats_text_size: (int) the text size of the stats
    :param title_size: (int) the text size of the title
    :param linewidth: (int) the width of the lines in the plot
    :param figsize: (tuple) the figure size of the plot
    :return:
    '''

    """
    Initializing the plot and figure along with
    vars used by all graphs
    """
    # making the figure and plot
    fig, ax = plt.subplots(figsize=figsize, tight_layout=True)

    # Setting up the process priority colors to normalizing them
    process_priorities = kernal_results.filter(like='priority')
    process_priorities = process_priorities.drop(
        "final priority", axis=1).replace(-1, 10000)

    # making all non entries the min
    process_priorities = process_priorities.replace(
        10000, np.min(process_priorities.values))

    processes_colors = process_priorities.values


    processes_colors_normed = (processes_colors - np.min(processes_colors)) / (np.max(
        processes_colors) - np.min(processes_colors))

    color = mpl.cm.get_cmap('plasma',
                            np.max(processes_colors))
    my_cmap = color(processes_colors_normed)  # making the color map

    # Calculating line widths
    linewidth = linewidth / kernal_results.shape[0]

    for q_work in range(1, kernal_results["times worked on"].max() + 1):

        # Getting the process offset points  and initial burst times
        processes_cpu_times = kernal_results[f"finish {q_work}"].values - \
            kernal_results[f"start {q_work}"].values
        processes_offsets = kernal_results[
            f"start {q_work}"].values + processes_cpu_times / 2

        processes_ids = kernal_results["id"].values[:, np.newaxis]

        # Making the main timeline
        main_timeline = ax.eventplot(processes_ids,
                                     orientation='vertical',
                                     lineoffsets=processes_offsets,
                                     linelengths=processes_cpu_times,
                                     linewidths=linewidth,
                                     colors=my_cmap[:, q_work - 1,: ])

        # plot the wait times
        if plot_wait_times:

            # If it is the first time the process has been worked on
            if q_work == 1:
                waiting_processes_lengths = kernal_results[f"start "
                                                           f"{q_work}"].values - kernal_results[f"arrival "
                                                                                                f"time"].values
                waiting_processes_offsets = kernal_results[
                    "arrival time"].values + \
                    (waiting_processes_lengths / 2)

            else:
                waiting_processes_lengths = (kernal_results[f"start "
                                                            f"{q_work}"] -
                                             kernal_results[f"finish "
                                                            f"{q_work-1}"]).values
                waiting_processes_offsets = kernal_results[f"finish "
                                                           f"{q_work-1}"].values\
                                                            + (waiting_processes_lengths / 2)

            #drop ids lengs and offsets where start is -1
            wait_cmap = my_cmap
            start_vals  = kernal_results[f"start {q_work}"].values
            drop_idxs = np.where(start_vals == -1)[0].tolist()
            if drop_idxs:
                waiting_processes_lengths = np.delete(
                    waiting_processes_lengths, drop_idxs,axis=0)
                processes_ids = np.delete(processes_ids, drop_idxs,axis=0)
                waiting_processes_offsets = np.delete(
                    waiting_processes_offsets, drop_idxs,axis=0)
                wait_cmap = np.delete(my_cmap, drop_idxs,axis=0)



            # Making the transparent waiting time timeline
            waiting_timeline = ax.eventplot(processes_ids,
                                            orientation='vertical',
                                            lineoffsets=waiting_processes_offsets,
                                            linelengths=waiting_processes_lengths,
                                            linewidths=linewidth,
                                            colors=wait_cmap[:, q_work - 1,: ],
                                            alpha=0.4)

    # plot the time waiting for IO
    if plot_io_times:

        # loop through all the the io start and end times
        io_starts = kernal_results.filter(like='io start')
        io_ends = kernal_results.filter(like='io end')

        for io_start, io_end in zip(io_starts, io_ends):
            # get the numpy array of the values
            io_end_vals = kernal_results[io_end].values
            io_start_vals = kernal_results[io_start].values

            io_length = io_end_vals - io_start_vals

            io_offsets = io_start_vals + (io_length / 2)

            # Making the transparent waiting time timeline
            io_timeline = ax.eventplot(kernal_results["id"].values[:,
                                       np.newaxis],
                                       orientation='vertical',
                                       lineoffsets=io_offsets,
                                       linelengths=io_length,
                                       linewidths=linewidth,
                                       color="grey",
                                       alpha=0.75)

    # making the ticks and grid
    #   Doing a labels list to get rid of padding proc ids
    # Y AXIS
    proc_id_array = np.arange(np.max(kernal_results["id"].values) + 2)
    proc_label_list = proc_id_array.tolist()
    proc_label_list[0] = ""
    proc_label_list[-1] = ""
    ax.set_yticks(proc_id_array, proc_label_list)
    ax.set_ylabel("Process ID")

    # X AXIS
    proc_max_end_time = np.max(kernal_results["turnaround time"].values +
                               kernal_results["arrival time"].values) + 6

    time_array_major = np.arange(0, proc_max_end_time, 5)
    time_array_minor = np.arange(proc_max_end_time)
    ax.set_xticks(time_array_major)
    ax.set_xticks(time_array_minor, minor=True)

    ax.xaxis.grid(True, which='minor')

    # ax.set_xticks(time_array)
    # ax.xaxis.set_minor_locator(mpl.ticker.AutoMinorLocator())
    ax.set_xlabel("Time (clock ticks)")

    ax.grid(axis="x")

    # # setting the colorbar for the timeline
    norm = mpl.colors.Normalize(vmin=np.min(processes_colors),
                                vmax=np.max(processes_colors))

    fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=color),
                 label="Priority (Higher = More Priority)")

    # Setting the title
    ax.set_title(title,size = title_size)

    # these are matplotlib.patch.Patch properties
    props = dict(boxstyle='square', facecolor='wheat', alpha=0.99)

    # Adding stats
    if stats:

        ax.text(
            0.91,
            1,
            f"Average:\n-------\n"
            f"Wait Time "
            f"{kernal_results['turnaround time'].mean():.2f}\n" +
            f"Turn-Around Time {kernal_results['wait time'].mean():.2f}\n" +
            f"Response Time {kernal_results['response time'].mean():.2f}\n" +
            f"CPU Time {kernal_results['total CPU time'].mean():.2f}\n" +
            f"I/O Time {kernal_results['total I/O time'].mean():.2f}\n"
            f"Throughput "+
            f"{(kernal_results.shape[0]/kernal_results.filter(like='start').values.max()) :.4f}"+
            f" proc/sec\n",
            transform=ax.transAxes,
            fontsize=stats_text_size,
            verticalalignment='top',
            bbox = props)

    # making the legend
    custom_lines = [mpl.lines.Line2D([0], [0], color="blue", lw=6)]
    lines_legend = [" (solid) = CPU"]
    if plot_wait_times:
        custom_lines.append(
            mpl.lines.Line2D(
                [0],
                [0],
                color="blue",
                alpha=0.4,
                lw=6))
        lines_legend.append(" (transparent) = Wait")
    if plot_io_times:
        custom_lines.append(mpl.lines.Line2D([0], [0], color="Grey",
                                             alpha=0.75, lw=6))
        lines_legend.append(" (grey) = I/O")

    ax.legend(
        custom_lines,
        lines_legend,
        loc="upper left",
        fontsize=stats_text_size,
        edgecolor = "black")

    plt.tight_layout()

    # display the plot
    plt.show()

    return


# function to generate processes
def generate_processes(n=10000,
                       split=0.5,
                       cpu_bound_range=[(8, 12), (1, 3)],
                       io_bound_range=[(1, 3), (8, 12)],
                       max_arrival_time=10000,
                       max_priority=10000,
                       duty_amt=3,
                       seed = None):
    '''
    This is a function to generate processes that are cpu and io bound processes

    :param n: (int) the number of processes to create
    :param split: (float) the percentage of cpu to io bound processes (higher split more CPU bound)
    :param cpu_bound_range: (list of 2 tuples with integers) holds the max
    and min ranges for the cpu and io tasks for the cpu bound processes
    :param io_bound_range: (list of 2 tuples with integers) holds the max
    and min ranges for the cpu and io tasks for the io bound processes
    :param max_arrival_time: (int) the maximum time that a process can arrive
     :param max_priority: (int) the maximum priority that a process can have
     :param duty_amt: (int) the lenght of the duty of each process
     :param seed: (int) the random seed for the function
    :return:
    '''

    #if there is a seed set the random seed
    if seed:
        np.random.seed(seed)


    # making choices 0 stands for cpu bound
    choices = np.random.choice([0, 1], size=(n,), p=[split, 1 - split])

    generated_processes = []

    for idx, choice in enumerate(choices):
        # if the choice is cpu bound
        if choice == 0:
            choice_duty = []
            for index in range(duty_amt):
                if index % 2 == 0:
                    choice_duty.append(random.randint(cpu_bound_range[0][0],
                                                      cpu_bound_range[0][1]))
                if index % 2 == 1:
                    choice_duty.append(random.randint(cpu_bound_range[1][0],
                                                      cpu_bound_range[1][1]))
        else:
            choice_duty = []
            for index in range(duty_amt):
                if index % 2 == 0:
                    choice_duty.append(random.randint(io_bound_range[0][0],
                                                      io_bound_range[0][1]))
                if index % 2 == 1:
                    choice_duty.append(random.randint(io_bound_range[1][0],
                                                      io_bound_range[1][1]))

        # Create the new Process
        new_proc = Process(idx, choice_duty,
                           random.randint(1, max_arrival_time),
                           random.randint(1, max_priority))

        generated_processes.append(new_proc)

    # return the generated processes
    return generated_processes


# Main Testing function
def main():
    # making the unfair RR processes
    unfair_rr_procs = [Process(1, [2, 35, 2], 1, 300),
                       Process(2, [5, 1, 6], 1, 24),
                       Process(3, [8, 3, 9], 5, 290),
                       Process(4, [7, 1, 6], 2, 423),
                       Process(5, [5, 3, 7], 4, 331),
                       Process(6, [9, 3, 9], 2, 389)]



    # Run the kernel with RR and unfair processes with a quantum of 10
    kernal(scheduler.RR_scheduler, processes=unfair_rr_procs,
                            quantum=10, file_proc_name="unfair", debug=False)


    # Importing the CPU results from RR unfair
    rr_unfair_results = pd.read_csv("data/Combined_Data/" +
                                    "All_RR_Q10_unfair_results.csv")

    # plotting the results
    plotKernalResults(rr_unfair_results,
                                       title="RR 10 Unfair Results Timeline",
                                       figsize=(18, 7))

    # test_processes = [Process(1, [9, 6, 7], 0, 30), Process(2, [14, 3, 7], 3,
    #                                                         35),
    #                   Process(3, [3, 3, 13], 4, 36),
    #                   Process(4, [6, 2, 7], 7, 20)]
    #
    # test_gen_procs = generate_processes(n=20, max_arrival_time=16)
    #
    # # Run the kernel with RR and base test processes
    # kernal(scheduler.Priority_scheduler, quantum=2,
    #        file_proc_name="test", CPU_To_Csv=True)

    # gen_test_results = pd.read_csv(
    #     "data/Combined_Data/All_MLFQ_test_gen_results.csv")
    # gen_test_results_cpu = pd.read_csv(
    #     "data/CPU_Data/CPU_MLFQ_test_gen_results.csv")
    #
    # # plotCPU(gen_test_results_cpu, title= "Test Gen CPU")
    # # # Plotting the Results (Enhanced Extension)
    # plotKernalResults(kernal_results=gen_test_results,
    #                   title="MLFQ Test Gen Results Timeline (Enhanced "
    #                         "Extension)")

    # Importing the results from RR test
    # rr_results_all = pd.read_csv(
    #     "data/Combined_Data/All_RR_Q2_test_results.csv")
    # rr_results_cpu = pd.read_csv("data/CPU_Data/CPU_RR_Q2_test_results.csv")

    # srt_test_results =  pd.read_csv(
    #     "data/Combined_Data/All_SRT_test_results.csv")
    # # Plotting the Results (Enhanced Extension)
    # plotKernalResults(kernal_results=srt_test_results,
    #                   title="SRT Test Results Timeline (Enhanced Extension)")

    # pp_test_results = pd.read_csv(
    #     "data/Combined_Data/All_Preemptive_Priority_test_results.csv")
    # # Plotting the Results (Enhanced Extension)
    # plotKernalResults(kernal_results=pp_test_results,
    #                   title="PP Test Results Timeline (Enhanced Extension)")

    # mlfq_test_results = pd.read_csv(
    #     "data/Combined_Data/All_MLFQ_test_1_results.csv")
    # # Plotting the Results (Enhanced Extension)
    # plotKernalResults(kernal_results=mlfq_test_results,
    # title="MLFQ Test Results Timeline (Enhanced Extension)")

    # Plotting the Results
    # plotCPU(rr_results_cpu, "RR Test Results Timeline")

    # Plotting the Results (Enhanced Extension)
    # plotKernalResults(kernal_results=rr_results_all,
    #                   title="RR Test Results Timeline (Enhanced Extension)")


if __name__ == "__main__":
    main()
