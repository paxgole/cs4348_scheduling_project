def fcfs(process_table):

    # fields = ["name", "arrival", "service", "io_interrupts", "io_interrupt1", "io_interrupt2"]    # for my reference
    # criterion = ["start", "finish", "wait", "response", "turnaround", "ratio"]                    # for my reference

    number_of_processes = len(process_table)

    performance_entries = []
    for i in range(0, number_of_processes):
        performance_entries.append([i, None, None])
    performance_entries[0][1] = 0
    minute_performance_calcs = []
    current_period_processes = []

    ready_queue = []
    disk_queue = [] # processes in io queue
    current_process = None
    current_process_progress = None
    next_process = 0 # next process that will arrived to the queue
    second_counter = 0
    completion_counter = 0

    # initiate the ready queue with first process
    ready_queue = [[0,0]]
    current_process = ready_queue[0][0]
    current_process_progress = ready_queue[0][1]
    next_process = 1

    
    # loop end condition is that last process has a finish time
    # we calculate this by checking in loop since an infinite loop is better than checking the condition every cycle
    # each loop represents 1 second
    while True:

        # print("Current process: P" + str(current_process))
        # print("Process progress: ", str(current_process_progress))
        # print(ready_queue)
        # print(disk_queue)

        # check if need to next process to ready queue
        if (process_table[next_process][1] == second_counter):
            ready_queue.append([next_process, 0])
            if next_process != (number_of_processes - 1): # if that was not the last arriving process
                next_process += 1
        
        # handle disk queue
        if (len(disk_queue) != 0):
            ready_queue.append(disk_queue.pop(0)) # add to end of ready queue
        
        # handle ready queue
        if len(ready_queue) == 0:
            current_process = None
            current_process_progress = None
        else:
            # check if currents' are empty and ready queue is not
            if current_process == None:
                current_process = ready_queue[0][0]
                current_process_progress = ready_queue[0][1]
                if performance_entries[current_process][1] == None:
                    performance_entries[current_process][1] = second_counter

            current_process_progress += 1
            ready_queue[0][1] = current_process_progress

            # if progress reached io interrupt point, move to disk queue
            if (process_table[current_process][4] == current_process_progress) or (process_table[current_process][5] == current_process_progress):
                disk_queue.append(ready_queue.pop(0))
                # print("Moving to disk queue")

                if len(ready_queue) == 0: # check if sending to disk made the ready queue empty
                    current_process = None
                    current_process_progress = None
                else:
                    current_process = ready_queue[0][0]
                    current_process_progress = ready_queue[0][1]
                    if performance_entries[current_process][1] == None:
                        performance_entries[current_process][1] = second_counter
                
                # print("Current process: P" + str(current_process))
                # print("Process progress: ", str(current_process_progress))
                # print(ready_queue)
                # print(disk_queue)
            
            # if service time is complete, remove from queue and update performance_entries
            if (current_process_progress == process_table[current_process][2]):
                performance_entries[current_process][2] = second_counter
                current_period_processes.append(current_process)
                completion_counter += 1
                # print("Current process completed")
                # print("Completion count: ", str(completion_counter))

                if completion_counter == number_of_processes:
                    minute_performance_calcs.append(current_period_processes)
                    return performance_entries, minute_performance_calcs
                
                ready_queue.pop(0)
                if len(ready_queue) == 0: # check if sending to disk made the ready queue empty
                    current_process = None
                    current_process_progress = None
                else:
                    current_process = ready_queue[0][0]
                    current_process_progress = ready_queue[0][1]
                    if performance_entries[current_process][1] == None:
                        performance_entries[current_process][1] = second_counter
                
                # print("Current process: P" + str(current_process))
                # print("Process progress: ", str(current_process_progress))
                # print(ready_queue)
                # print(disk_queue)
            
            second_counter += 1

            if ((second_counter % 60) == 0):
                minute_performance_calcs.append(current_period_processes)
                current_period_processes = []
            
            # print('\n')

def srt(process_table):
    # fields = ["name", "arrival", "service", "io_interrupts", "io_interrupt1", "io_interrupt2"]    # for my reference
    # criterion = ["start", "finish", "wait", "response", "turnaround", "ratio"]                    # for my reference

    number_of_processes = len(process_table)

    performance_entries = []
    for i in range(0, number_of_processes):
        performance_entries.append([i, None, None])
    performance_entries[0][1] = 0
    minute_performance_calcs = []
    current_period_processes = []

    ready_queue = []
    disk_queue = [] # processes in io queue
    current_process = None
    current_process_remaining_time = None
    next_process = 0 # next process that will arrived to the queue
    second_counter = 0
    completion_counter = 0

    # initiate the ready queue with first process
    ready_queue = [[0,6,(6-3),-1]]
    current_process = ready_queue[0][0]
    current_process_remaining_time = ready_queue[0][1]
    next_process = 1

    # loop end condition is that last process has a finish time
    # we calculate this by checking in loop since an infinite loop is better than checking the condition every cycle
    # each loop represents 1 second
    while True:

        # next insertion
        if (process_table[next_process][1] == second_counter):
            remaining = process_table[next_process][2]
            interrupt1 = -1 if (process_table[next_process][4] != 0) else (remaining - process_table[next_process][4])
            interrupt2 = -1 if (process_table[next_process][5] != 0) else (remaining - process_table[next_process][5])
            entry = [next_process, remaining, interrupt1, interrupt2]
            ready_queue.append(entry)
            ready_queue = sorted(ready_queue,key=lambda x: x[1])
            if ready_queue[0][0] != current_process:
                current_process = ready_queue[0][0]
                current_process_remaining_time = ready_queue[0][1]
                if performance_entries[current_process][1] == None:
                    performance_entries[current_process][1] = second_counter

            if next_process != (number_of_processes - 1): # if that was not the last arriving process
                next_process += 1

        # handle disk queue
        if (len(disk_queue) != 0):
            ready_queue.append(disk_queue.pop(0)) # add to end of ready queue
            ready_queue = sorted(ready_queue,key=lambda x: x[1])
            if ready_queue[0][0] != current_process:
                current_process = ready_queue[0][0]
                current_process_remaining_time = ready_queue[0][1]
        
        # handle ready queue
        if len(ready_queue) == 0:
            current_process = None
            current_process_remaining_time = None
        else:
             # check if currents' are empty and ready queue is not
            if current_process == None:
                current_process = ready_queue[0][0]
                current_process_remaining_time = ready_queue[0][1]
                if performance_entries[current_process][1] == None:
                    performance_entries[current_process][1] = second_counter
            
            current_process_remaining_time -= 1
            ready_queue[0][1] = current_process_remaining_time
        
            # if progress reached io interrupt point, move to disk queue
            if (current_process_remaining_time == ready_queue[0][2]) or (current_process_remaining_time == ready_queue[0][3]):
                disk_queue.append(ready_queue.pop(0))
                # print("Moving to disk queue")

                if len(ready_queue) == 0: # check if sending to disk made the ready queue empty
                    current_process = None
                    current_process_remaining_time = None
                else:
                    current_process = ready_queue[0][0]
                    current_process_remaining_time = ready_queue[0][1]
                    if performance_entries[current_process][1] == None:
                        performance_entries[current_process][1] = second_counter
            
            # if service time is complete, remove from queue and update performance_entries
            if (current_process_remaining_time == 0):
                performance_entries[current_process][2] = second_counter
                current_period_processes.append(current_process)
                completion_counter += 1
                # print("Current process completed")
                # print("Completion count: ", str(completion_counter))

                if completion_counter == number_of_processes:
                    minute_performance_calcs.append(current_period_processes)
                    return performance_entries, minute_performance_calcs
                
                ready_queue.pop(0)
                if len(ready_queue) == 0: # check if sending to disk made the ready queue empty
                    current_process = None
                    current_process_remaining_time = None
                else:
                    current_process = ready_queue[0][0]
                    current_process_remaining_time = ready_queue[0][1]
                    if performance_entries[current_process][1] == None:
                        performance_entries[current_process][1] = second_counter
        
        second_counter += 1

        if ((second_counter % 60) == 0):
            minute_performance_calcs.append(current_period_processes)
            current_period_processes = []

def hrrn(process_table):
    # fields = ["name", "arrival", "service", "io_interrupts", "io_interrupt1", "io_interrupt2"]    # for my reference
    # criterion = ["start", "finish", "wait", "response", "turnaround", "ratio"]                    # for my reference

    number_of_processes = len(process_table)

    performance_entries = []
    for i in range(0, number_of_processes):
        performance_entries.append([i, None, None])
    performance_entries[0][1] = 0
    minute_performance_calcs = []
    current_period_processes = []

    ready_queue = []
    disk_queue = [] # processes in io queue
    current_process = None
    current_process_progress = None
    next_process = 0 # next process that will arrived to the queue
    second_counter = 0
    completion_counter = 0

    # initiate the ready queue with first process
    ready_queue = [[0,0,0,6]]
    current_process = ready_queue[0][0]
    current_process_progress = ready_queue[0][1]
    next_process = 1

    
    # loop end condition is that last process has a finish time
    # we calculate this by checking in loop since an infinite loop is better than checking the condition every cycle
    # each loop represents 1 second
    while True:

        # print("Current process: P" + str(current_process))
        # print("Process progress: ", str(current_process_progress))
        # print(ready_queue)
        # print(disk_queue)
        # print("Completed:", completion_counter)

        # check if need to next process to ready queue
        if (process_table[next_process][1] == second_counter):
            ready_queue.append([next_process, 0, 0, process_table[next_process][2]])
            if next_process != (number_of_processes - 1): # if that was not the last arriving process
                next_process += 1
        
        # handle disk queue
        if (len(disk_queue) != 0):
            ready_queue.append(disk_queue.pop(0)) # add to end of ready queue
        
        # handle ready queue
        if len(ready_queue) == 0:
            current_process = None
            current_process_progress = None
        else:
            # check if currents' are empty and ready queue is not
            if current_process == None:
                current_process = ready_queue[0][0]
                current_process_progress = ready_queue[0][1]
                if performance_entries[current_process][1] == None:
                    performance_entries[current_process][1] = second_counter
            
            # update wait time for all
            for process in ready_queue:
                process[2] += 1

            current_process_progress += 1
            ready_queue[0][1] = current_process_progress

            # if progress reached io interrupt point, move to disk queue
            if (process_table[current_process][4] == current_process_progress) or (process_table[current_process][5] == current_process_progress):
                disk_queue.append(ready_queue.pop(0))
                # print("Moving to disk queue")

                if len(ready_queue) == 0: # check if sending to disk made the ready queue empty
                    current_process = None
                    current_process_progress = None
                    continue
                else:
                    hrrn_val = []
                    for process in ready_queue:
                        hrrn_val.append((process[2] + process[3]) / process[3])
                    min_index = hrrn_val.index(min(hrrn_val))
                    new_current_entry = ready_queue.pop(min_index)
                    ready_queue = [new_current_entry] + ready_queue

                    current_process = ready_queue[0][0]
                    current_process_progress = ready_queue[0][1]
                    if performance_entries[current_process][1] == None:
                        performance_entries[current_process][1] = second_counter
                
                # print("Current process: P" + str(current_process))
                # print("Process progress: ", str(current_process_progress))
                # print(ready_queue)
                # print(disk_queue)
            
            # if service time is complete, remove from queue and update performance_entries
            if (current_process_progress == process_table[current_process][2]):
                performance_entries[current_process][2] = second_counter
                current_period_processes.append(current_process)
                completion_counter += 1
                # print("Current process completed")
                # print("Completion count: ", str(completion_counter))

                if completion_counter == number_of_processes:
                    minute_performance_calcs.append(current_period_processes)
                    return performance_entries, minute_performance_calcs
                
                ready_queue.pop(0)
                if len(ready_queue) == 0: # check if sending to disk made the ready queue empty
                    current_process = None
                    current_process_progress = None
                else:
                    hrrn_val = []
                    for process in ready_queue:
                        hrrn_val.append((process[2] + process[3]) / process[3])
                    min_index = hrrn_val.index(min(hrrn_val))
                    new_current_entry = ready_queue.pop(min_index)
                    ready_queue = [new_current_entry] + ready_queue

                    current_process = ready_queue[0][0]
                    current_process_progress = ready_queue[0][1]
                    if performance_entries[current_process][1] == None:
                        performance_entries[current_process][1] = second_counter
                
                # print("Current process: P" + str(current_process))
                # print("Process progress: ", str(current_process_progress))
                # print(ready_queue)
                # print(disk_queue)
            
            second_counter += 1

            if ((second_counter % 60) == 0):
                minute_performance_calcs.append(current_period_processes)
                current_period_processes = []
            
            # print('\n')

def rr(process_table):
    # fields = ["name", "arrival", "service", "io_interrupts", "io_interrupt1", "io_interrupt2"]    # for my reference
    # criterion = ["start", "finish", "wait", "response", "turnaround", "ratio"]                    # for my reference

    number_of_processes = len(process_table)

    performance_entries = []
    for i in range(0, number_of_processes):
        performance_entries.append([i, None, None])
    performance_entries[0][1] = 0
    minute_performance_calcs = []
    current_period_processes = []

    ready_queue = []
    disk_queue = [] # processes in io queue
    current_process = None
    current_process_progress = None
    next_process = 0 # next process that will arrived to the queue
    second_counter = 0
    completion_counter = 0

    # initiate the ready queue with first process
    ready_queue = [[0,0]]
    current_process = ready_queue[0][0]
    current_process_progress = ready_queue[0][1]
    next_process = 1

    
    # loop end condition is that last process has a finish time
    # we calculate this by checking in loop since an infinite loop is better than checking the condition every cycle
    # each loop represents 1 second
    while True:

        # print("Current process: P" + str(current_process))
        # print("Process progress: ", str(current_process_progress))
        # print(ready_queue)
        # print(disk_queue)

        # check if need to next process to ready queue
        if (process_table[next_process][1] == second_counter):
            ready_queue.append([next_process, 0])
            if next_process != (number_of_processes - 1): # if that was not the last arriving process
                next_process += 1
        
        # handle disk queue
        if (len(disk_queue) != 0):
            ready_queue.append(disk_queue.pop(0)) # add to end of ready queue
        
        # handle ready queue
        if len(ready_queue) == 0:
            current_process = None
            current_process_progress = None
        else:
            # check if currents' are empty and ready queue is not
            if current_process == None:
                current_process = ready_queue[0][0]
                current_process_progress = ready_queue[0][1]
                if performance_entries[current_process][1] == None:
                    performance_entries[current_process][1] = second_counter

            current_process_progress += 1
            ready_queue[0][1] = current_process_progress

            # if progress reached io interrupt point, move to disk queue
            if (process_table[current_process][4] == current_process_progress) or (process_table[current_process][5] == current_process_progress):
                disk_queue.append(ready_queue.pop(0))
                # print("Moving to disk queue")

                if len(ready_queue) == 0: # check if sending to disk made the ready queue empty
                    current_process = None
                    current_process_progress = None
                else:
                    # simply rotate queue by 1
                    ready_queue = ready_queue[-1:] + ready_queue[:-1]

                    current_process = ready_queue[0][0]
                    current_process_progress = ready_queue[0][1]
                    if performance_entries[current_process][1] == None:
                        performance_entries[current_process][1] = second_counter
                
                # print("Current process: P" + str(current_process))
                # print("Process progress: ", str(current_process_progress))
                # print(ready_queue)
                # print(disk_queue)
            
            # if service time is complete, remove from queue and update performance_entries
            if (current_process_progress == process_table[current_process][2]):
                performance_entries[current_process][2] = second_counter
                current_period_processes.append(current_process)
                completion_counter += 1
                # print("Current process completed")
                # print("Completion count: ", str(completion_counter))

                if completion_counter == number_of_processes:
                    minute_performance_calcs.append(current_period_processes)
                    return performance_entries, minute_performance_calcs
                
                ready_queue.pop(0)
                if len(ready_queue) == 0: # check if sending to disk made the ready queue empty
                    current_process = None
                    current_process_progress = None
                else:
                    # simply rotate queue by 1
                    ready_queue = ready_queue[-1:] + ready_queue[:-1]

                    current_process = ready_queue[0][0]
                    current_process_progress = ready_queue[0][1]
                    if performance_entries[current_process][1] == None:
                        performance_entries[current_process][1] = second_counter
                
                # print("Current process: P" + str(current_process))
                # print("Process progress: ", str(current_process_progress))
                # print(ready_queue)
                # print(disk_queue)
            
            second_counter += 1

            if ((second_counter % 60) == 0):
                minute_performance_calcs.append(current_period_processes)
                current_period_processes = []
            
            # print('\n')

def performance_calculation(performance, minute_performance_calcs, process_table):
    # fields = ["name", "arrival", "service", "io_interrupts", "io_interrupt1", "io_interrupt2"]    # for my reference
    # criterion = ["start", "finish", "wait", "response", "turnaround", "ratio"]                    # for my reference
    print("# of entries:",len(performance))
    print("1st entry:",performance[0])
    print("Last entry:", performance[-1])
    print("Last inserted entry:",performance[minute_performance_calcs[-1][-1]])
    print("")
    for i in range(0,len(minute_performance_calcs)):
        print("Minute #", i)
        print("Process      Finish Time      Response Time       Turnaround Time     Ratio (Turnaround / Service)")
        for process in minute_performance_calcs[i]:
            process = performance[process][0]
            finish = performance[process][2]
            response = performance[process][1] - process_table[process][1]
            turnaround = performance[process][2] - process_table[process][1]
            ratio = turnaround / process_table[process][2]
            print(f'{process:<12}',f'{finish:<16}',f'{response:<19}',f'{turnaround:<19}',f'{ratio:<16}')
        print("")
    print("Throughput per minute:", 150/len(minute_performance_calcs), "\n")


def fcfs_performance(process_table):
    performance, minute_performance_calcs = fcfs(process_table)
    print("END OF FCFS:")
    performance_calculation(performance, minute_performance_calcs, process_table)

def srt_performance(process_table):
    performance, minute_performance_calcs = srt(process_table)
    print("END OF SRT:")
    performance_calculation(performance, minute_performance_calcs, process_table)

def hrrn_performance(process_table):
    performance, minute_performance_calcs = hrrn(process_table)
    print("END OF HRRN:")
    performance_calculation(performance, minute_performance_calcs, process_table)

def rr_performance(process_table):
    performance, minute_performance_calcs = rr(process_table)
    print("END OF RR:")
    performance_calculation(performance, minute_performance_calcs, process_table)