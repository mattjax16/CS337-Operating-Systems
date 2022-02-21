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

# Libraries for plotting
import matplotlib as mpl
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)
import matplotlib.pyplot as plt
import plotly.express as px
import palettable


def kernal(
        selected_scheduler,
        processes=None,
        quantum = 0,
        debug=True,
        CPU_to_csv=False,
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
    :param debug: (Boolean) If true output messages will be printed from the selected_scheduler function
    :param CPU_to_csv: (Boolean) if true results of CPU will be written to a csv
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

    time = 0  # creating the intial time for the kernal

    # If there are no processes passed make a test list of 5 processes
    if processes is None:
        if debug:
            print(f"Warning no processes were passed!! Making test Processes")

        processes = [Process(1, [5,6,7], 0, 30), Process(2, [4,3,3], 3, 35),
                     Process(3, [2,3,4], 4, 36),
                     Process(4, [5,2,7], 7, 20)]


    # adding the proccesses to the ready list
    # increment time until there is one
    while len(ready) == 0:
        scheduler.add_ready(processes, ready, time)
        if len(ready) == 0:
            time += 1

    # runnig schuedler for all processes in ready
    while processes or ready:
        if selected_scheduler != scheduler.RR_scheduler:
            time = selected_scheduler(
                processes,
                ready,
                CPU,
                Scheduled_Processes,
                time,
                quantum,
                debug=debug)
        else:
            time = selected_scheduler(
                processes,
                ready,
                CPU,
                Scheduled_Processes,
                time,
                debug=debug)


    # Once all the processes in the CPU that have finished
    # and calculate their wait time and turn around time
    calc_wait_and_tunaround(CPU, Scheduled_Processes)

    # Write data to csv files if either
    # CPU_to_csv or Processes_to_csv is True
    if CPU_to_csv or Processes_to_csv or write_both_results:

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
        elif selected_scheduler == scheduler.Priority_Turnaround_scheduler:
            sched = "Priority_Turnaround"
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

        # Writing CPU data
        if CPU_to_csv:
            # reverse CPU so it is written to df in process order
            CPU.reverse()
            pd.DataFrame(CPU).to_csv(
                f"data/CPU_Data/CPU_{sched}_{file_proc_name}results" +
                f"{time}.csv",
                index=False)

        # Writing Scheduled_Processes data
        if Processes_to_csv:
            Scheduled_Processes.reverse()

            # creating a list of dicts of all
            # the process attributes
            SP_dict_list = [{"id": x.id, "burst time": x.burst_time,
                             "inital burst time": x.inital_burst_time,
                             "arrival time": x.arrival_time,
                             "priority": x.priority,
                             "wait time": x.wait_time,
                             "turnaround time": x.turnaround_time,
                             } for x in Scheduled_Processes]

            # Writing the CSV file
            pd.DataFrame(SP_dict_list).to_csv(
                f"data/Sched_Process_Data/Scheduled_Processes" +
                f"_{sched}_{file_proc_name}results{time}.csv",
                index=False)

        if write_both_results:
            # reverse CPU so it is written to df in process order
            CPU.reverse()
            cpu_df = pd.DataFrame(CPU)

            Scheduled_Processes.reverse()

            # creating a list of dicts of all
            # the process attributes
            SP_dict_list = [{"id": x.id, "burst time": x.burst_time,
                             "initial burst time": x.initial_burst_time,
                             "arrival time": x.arrival_time,
                             "priority": x.priority,
                             "wait time": x.wait_time,
                             "turnaround time": x.turnaround_time,
                             } for x in Scheduled_Processes]

            # making dataframe
            sp_df = pd.DataFrame(SP_dict_list)

            # Combining the 2 dataframe
            main_df = pd.concat([sp_df, cpu_df], axis=1)
            main_df.drop(["Priority"], inplace=True, axis=1)

            main_df.to_csv(
                f"data/Combined_Data/All" +
                f"_{sched}_{file_proc_name}results{time}.csv",
                index=False)

    return


def calc_wait_and_tunaround(CPU, Scheduled_Processes):
    '''
    Calculates the wait tiem and turn around for all the schuedled processes

    :param CPU: this is a list that simulates the CPU by holding beginning runtime
            and end of runtime for each process. This is the same as the Gantt bar
            that we have been using in lecture slides at the bottom of each example.
    :param Scheduled_Processes: this is a list of all the process that have been scheduled
    :return:
    '''

    # Sort the CPU and Schedled_process based on their id
    CPU.sort(key=lambda x: x['id'], reverse=True)
    Scheduled_Processes.sort(key=lambda x: x.id, reverse=True)

    for cpu_info, proc in zip(CPU, Scheduled_Processes):
        proc.wait_time = cpu_info['Start'] - proc.arrival_time
        proc.turnaround_time = cpu_info['Finish'] - proc.arrival_time

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
    fig = px.timeline(cpu_results, x_start="Start", x_end="Finish", y="id",
                      color="Priority", labels={"id": "Process ID"})

    # adding the title
    fig.update_layout(title_text=title, title_x=0.5)

    # setting up the x axis by finding the delta
    cpu_results['delta'] = cpu_results['Finish'] - cpu_results['Start']
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


# defining a function to plot Scheduled_Processes data along with CPU data
def plotKernalResults(
    kernal_results,
    title="Scheduled Processes Results Timeline",
    stats = True,
    figsize=(
        10,
        6)):
    '''
    A function to plot the kernal results df from
    operating_system.py

    :param kernal_results: (dataframe) the combined results from the kernal
    simulation
    :param title: (string) the title for the plot
    :param stats: (bool) if true average wait and turn around time will be shown
    :param figsize: (tuple) the figure size of the plot
    :return:
    '''

    # making the figure and plot
    fig, ax = plt.subplots(figsize=figsize, tight_layout=True)

    # Setting up the process priority colors by normalizing them
    processes_colors = kernal_results["priority"].values
    processes_colors = (processes_colors - np.min(processes_colors)) / \
                       (np.max(processes_colors) + processes_colors / 50 - np.min(
                           processes_colors))
    color = mpl.cm.get_cmap('plasma',
                            np.max(kernal_results["priority"].values))
    my_cmap = color(processes_colors)  # making the color map

    # Getting the process avial time offset points  and turnaround times
    arrival_processes_turnaround_times = kernal_results["turnaround time"] \
        .values
    arrival_processes_offsets = kernal_results["arrival time"].values + \
        arrival_processes_turnaround_times / 2

    # Calculating line widths
    linewidth = 230 / kernal_results.shape[0]

    # Making the greyed out timeline
    arrival_timeline = ax.eventplot(kernal_results["id"].values[:,np.newaxis],
                                    orientation='vertical',
                                    lineoffsets=arrival_processes_offsets,
                                    linelengths=arrival_processes_turnaround_times,
                                    linewidths=linewidth,
                                    colors=my_cmap,
                                    alpha=0.4)

    # Getting the process offset points  and initial burst times
    processes_burst_times = kernal_results["inital burst time"].values
    processes_offsets = kernal_results[
        "Start"].values + processes_burst_times / 2

    # Making the main timeline
    main_timeline = ax.eventplot(kernal_results["id"].values[:, np.newaxis],
                                 orientation='vertical',
                                 lineoffsets=processes_offsets,
                                 linelengths=processes_burst_times,
                                 linewidths=linewidth,
                                 colors=my_cmap)

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
                               kernal_results["arrival time"].values) + 1

    time_array_major = np.arange(0, proc_max_end_time, 5)
    time_array_minor = np.arange(proc_max_end_time)
    ax.set_xticks(time_array_major)
    ax.set_xticks(time_array_minor, minor=True)

    ax.xaxis.grid(True, which='minor')

    # ax.set_xticks(time_array)
    # ax.xaxis.set_minor_locator(mpl.ticker.AutoMinorLocator())
    ax.set_xlabel("Time (clock ticks)")

    ax.grid(axis="x")

    # setting the colorbar for the timeline
    norm = mpl.colors.Normalize(vmin=np.min(kernal_results["priority"].values),
                                vmax=np.max(kernal_results["priority"].values))

    fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=color),
                 label="Priority (Higher = More Priority)")

    # Setting the title
    ax.set_title(title)


    # Adding stats
    if stats:
        ### TODO : ADD BOLDING
        ax.text(0.75, 0.95, f"Avg Wait Time: "
                            f"{kernal_results['turnaround time'].mean()}\n" +
                f"Avg Turn-Around Time: {kernal_results['wait time'].mean()}\n"
                , transform=ax.transAxes,
                fontsize=9,
                verticalalignment='top')

    # making the legend
    custom_lines = [mpl.lines.Line2D([0], [0], color="blue", lw=6),
                    mpl.lines.Line2D([0], [0], color="blue", alpha=0.4, lw=6)]
    ax.legend(custom_lines, [" (solid) = running",
                             " (transparent) = waiting"],
              loc="upper left")

    plt.tight_layout()

    # display the plot
    plt.show()

    return


# Main Testing function
def main():
    # Run the kernel with RR and base test processes
    kernal(scheduler.RR_scheduler, quantum=2,
                            file_proc_name="test"
                            , CPU_to_csv=True)



    # Importing the results from RR test
    rr_results_all = pd.read_csv("data/Combined_Data/All_RR_Q2_test_results.csv")
    rr_results_cpu = pd.read_csv("data/CPU_Data/CPU_RR_Q2_test_results.csv")


    # Plotting the Results
    plotCPU(rr_results_cpu, "RR Test Results Timeline")


if __name__ == "__main__":
    main()
