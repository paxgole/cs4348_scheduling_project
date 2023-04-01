import csv, random, scheduling_algorithms

def generate_processes(initial_processes):

    # fields = ["name", "arrival", "service", "io_interrupts", "io_interrupt1", "io_interrupt2"]    # for my reference
    # criterion = ["start", "finish", "wait", "response", "turnaround", "ratio"]                    # for my reference

    process_table = [] # this will be returned and passed into functions for use, as it's more efficient than having each algo read the csv and reformat the data every time

    with open('process_table.csv', 'w') as process_table_file:
        writer = csv.writer(process_table_file, delimiter=',')

        fieldnames = ["name", "arrival", "service", "io_interrupts", "io_interrupt1", "io_interrupt2"]
        writer.writerow(fieldnames)
        
        for entry in initial_processes:
            writer.writerow(entry)
            process_table.append(entry)
        
        last_arrival_time = 8
        last_process = 4

        # simulation must run MINIMUM 10 simulated minutes, and min time of a process is 4 seconds, 600/4 is 150 so minimum 150 processes
        while (last_process < 150):

            last_process += 1
            name = "P" + str(last_process) # instead of having processes named by alphabets

            next_arrival_interval = random.randint(2, 5)
            last_arrival_time += next_arrival_interval

            service_time = random.randint(4, 12)

            io_interrupts = random.choices([2,1,0], weights=(2, 2, 1),k=1)[0] # weights derived from frequency in initial data

            # determine when io interrupt takes place
            if (io_interrupts == 1):
                io_interrupt_moment1 = int(service_time / 2)
                io_interrupt_moment2 = 0
            elif (io_interrupts == 2):
                io_interrupt_moment1 = int(service_time / 3)
                io_interrupt_moment2 = int(service_time / 2)
            else:
                io_interrupt_moment1 = 0
                io_interrupt_moment2 = 0
            
            entry = [name, last_arrival_time, service_time, io_interrupts, io_interrupt_moment1, io_interrupt_moment2]
            writer.writerow(entry)
            process_table.append(entry)
    
    return process_table

if __name__ == "__main__":
    
    # initial data provided in assignment document
    initial_processes = [("P0",0,6,1,3,0),
                         ("P1",2,12,2,4,8),
                         ("P2",4,8,1,4,0),
                         ("P3",6,10,0,0,0),
                         ("P4",8,4,2,1,3)]

    process_table = generate_processes(initial_processes=initial_processes)

    # create performance files for all the algorithms
    algos = ["fcfs", "rr", "srt", "hrrn"]
    
    scheduling_algorithms.fcfs_performance(process_table)
    scheduling_algorithms.srt_performance(process_table)
    scheduling_algorithms.hrrn_performance(process_table)
    scheduling_algorithms.rr_performance(process_table)

