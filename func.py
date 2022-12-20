import random
import math

def serviceTime(lamda):
    x = 0.0
    while x == 0.0:
        u = random.uniform(0, 1)
        x = (-1/lamda)*(math.log(u))
    return x

# My FCFS uses a list for the ready and schedule queues. For the schedule queue, it creates a list of lists.
# Events are given a title, "arrival" or "completion", and their respective times are calculated. Then,
# the simulator will append a list containing [ title, time ] to the event queue. The simulator then steps
# through each event. Arrival events add to the ready queue, completions remove from it. Every 100ms, the
# simulator generates a set of (100/lamda) processes. If lamda is 4, the simulator will create 25 processes.
def FCFS(lamda, serv):
    # Initialize variables
    clock = 0.0
    clockArr = 0.0
    readyQueue = []
    eventQueue = []
    processCounter = 0
    toSched = int((100/lamda)) # Calculate # of processes per second, rounding down
    readyAVG = [0, 0] # Calculating average ready queue size
    cpuTime = 0.0 # Calculating CPU utilization
    turnaround = [0, 0]

    # Schedule initial processes 100ms in future. (100/lamda) == processes per 1 second
    servIns = (clockArr+lamda)
    for x in range( 1, toSched+1, 1 ): # Create arrivals
        eventQueue.append(['arrival', (clockArr+(lamda*x))]) # Add process arrival to sched queue
        servIns = (servIns + serviceTime(serv))
        if servIns < (clockArr+(lamda*x)): # If next arrival hasn't happened yet
            cpuTime = cpuTime + ((clockArr + (lamda * x)) - servIns)
            servIns = (clockArr+(lamda*x)) + serviceTime(serv)
        turnaround[0] += (servIns - (clockArr+(lamda*x)))
        turnaround[1] += 1
        eventQueue.append(['completion', servIns]) # Add completion process to sched. queue
    eventQueue = sorted(eventQueue, key=lambda x: x[1]) # Sort event queue
    clock = eventQueue[0][1]

    # FCFS Simulator - Steps thru event queue
    while processCounter < 10000:
        readyAVG[0] += len(readyQueue)
        readyAVG[1] += 1

        # If event in queue is a process arrival
        if eventQueue[0][0] == 'arrival':
            clock = eventQueue[0][1]
            clockArr = clock
            readyQueue.append(eventQueue[0][1]) # Add process to ready queue
            eventQueue.pop(0) # Remove arrival event

        # If event in queue is a process completion
        if eventQueue[0][0] == 'completion':
            clock = eventQueue[0][1]
            servIns = clock
            readyQueue.pop(0) # Remove completed process from ready queue
            eventQueue.pop(0) # Remove completion event
            processCounter += 1

        # If 1 second interval has passed, schedule next 100/lamda processes
        if processCounter % toSched == 0 and len(readyQueue) == 0 and processCounter != 10000:
            for x in range(1, toSched + 1, 1):  # Create arrivals and completions
                eventQueue.append(['arrival', (clockArr + (lamda * x))])  # Add process arrival to sched. queue
                servIns = servIns + serviceTime(serv)
                if servIns < (clockArr + (lamda * x)):
                    cpuTime = cpuTime + ((clockArr + (lamda*x))-servIns) # Sum time between completion and arrival
                    servIns = (clockArr + (lamda * x)) + serviceTime(serv)
                turnaround[0] += (servIns - (clockArr + (lamda * x)))
                turnaround[1] += 1
                eventQueue.append(['completion', servIns]) # Add process completion to sched. queue
            eventQueue = sorted(eventQueue, key=lambda x: x[1]) # Sort schedule queue

    print('FCFS |', 'AVG Turnaround:', '{:.2f}'.format(((turnaround[0]/turnaround[1])/1000)),'Throughput:',
          '{:.2f}'.format(100/lamda), 'per second | CPU Util:',
          '{:.8f}'.format(((clock-cpuTime)/clock)*100.00), '% | AVG Ready Queue:',
         '{:.2f}'.format(readyAVG[0]/readyAVG[1]),'processes.' )

# My SRTF uses a list for ready and schedule queues. For the schedule queue, it creates a list of lists.
# Events are given a title, "arrival", and a start time. The simulator will step through each arrival.
# At each arrival, the simulator will append a process to the ready queue. The simulator will constantly
# service processes until another arrives, at which point it will append the new process to the ready queue
# and sort the queue by ascending remaining service times.
def SRTF(lamda, serv):
    # Initialize variables
    clock = 0.0
    clockArr = 0.0
    readyQueue = []
    eventQueue = []
    processCounter = 0
    toSched = int((100/lamda)) # Calculate # of processes per second, rounding down
    readyAVG = [0.0, 0.0] # Calculating average ready queue size
    cpuTime = 0.0 # Calculating CPU utilization
    turnaroundQ1 = [0, 0]
    turnaroundQ2 = [0, 0]
    
    # Schedule initial processes 100ms in future. (100/lamda) == processes per 1 second
    for x in range( 1, toSched+1, 1 ): # Create arrivals
        eventQueue.append(['arrival', (clockArr+(lamda*x))]) # Add process arrival to sched queue
    clock = eventQueue[0][1]

    while processCounter != 10000:
        readyAVG[0] += len(readyQueue) # Capture AVG ready queue size
        readyAVG[1] += 1.0

        if eventQueue[0][0] == 'arrival': # Always preempt when process arrives
            turnaroundQ1.append(eventQueue[0][1]) # Save arr. time for calc in turnaround times
            if len(readyQueue) != 0:
                readyQueue[0] = eventQueue[0][1] - readyQueue[0]  # Update current proc's remaining serv time
            readyQueue.append(serviceTime(serv)) # Append  new process
            clock = eventQueue[0][1]  # Set clock equal to current arrival time
            eventQueue.pop(0) # Remove arrival event
            readyQueue.sort() # Sort ready queue upon new arr.

            # If next arrival will occur AFTER readyQueue[0] completes, preempt
            while len(readyQueue) != 0 and clock + readyQueue[0] < eventQueue[0][1]:
                clock += readyQueue[0] # Update clock

                turnaroundQ2[0] += (clock - turnaroundQ1[0])
                turnaroundQ2[1] += 1.0
                turnaroundQ1.pop(0)

                readyQueue.pop(0)  # Process completed
                processCounter += 1
                if len(readyQueue) == 0: # If ready queue is empty, and no process has arrived...
                    cpuTime += (eventQueue[0][1] - clock) # Count idle time
                else:
                    readyQueue.sort() # Sort b/c a process completed

        #If eventQueue is empty, we need new processes
        if len(eventQueue) == 1: # Schedule (100/lamda) processes every 100ms
            clockArr += lamda
            for x in range(1, toSched + 1, 1):  # Create arrivals
                eventQueue.append(['arrival', (clockArr + (lamda * x))])  # Add process arrival to sched queue
            eventQueue = sorted(eventQueue, key=lambda x: x[1])  # Sort event queue

    print('SRTF |', 'AVG Turnaround:', '{:.2f}'.format(((turnaroundQ2[0] / turnaroundQ2[1]) / 1000)), '| Throughput:',
          '{:.2f}'.format(100 / lamda), 'per second | CPU Util:',
          '{:.8f}'.format(((clock - cpuTime) / clock) * 100.00), '% | AVG Ready Queue:',
          '{:.2f}'.format(readyAVG[0]/readyAVG[1]), 'processes.')

# This simulator schedules 100/lambda processes in advance. Then, it steps through the arrival events.
# Once an arrival event is encountered, the function will calculate HRRNs and pick the suitable process
# for CPU time. It then generates a completion event. Every time a completion event is received,
# the function will recalculate HRRNs and pick another process to generate a completion event for.
def HRRN(lamda, serv):
    # Initialize variables
    clock = 0.0
    clockArr = 0.0
    readyQueue = [] # [ service time, wait time, HRRN ]
    eventQueue = [] # [ event name, service time ]
    processCounter = 0
    toSched = int((100 / lamda))  # Calculate # of processes per second, rounding down
    readyAVG = [0.0, 0.0]  # Calculating average ready queue size
    cpuTime = 0.0  # Calculating CPU utilization
    turnaround = 0.0 # Sum of turnarounds
    turnaroundArr = 0.0

    # Schedule initial processes 100ms in future. (100/lamda) == processes per 1 second
    for x in range( 1, toSched+1, 1 ): # Create arrivals
        eventQueue.append(['arrival', (clockArr+(lamda*x))]) # Add process arrival to sched queue
    clock = eventQueue[0][1]

    while processCounter != 10000:
        readyAVG[0] += len(readyQueue)  # Capture AVG ready queue size
        readyAVG[1] += 1.0

        # If eventQueue is empty, we need new processes
        if len(eventQueue) == 1:  # Schedule (100/lamda) processes every 100ms
            clockArr += lamda
            for x in range(1, toSched + 1, 1):  # Create arrivals
                eventQueue.append(['arrival', (clockArr + (lamda * x))])  # Add process arrival to sched queue
            eventQueue = sorted(eventQueue, key=lambda x: x[1])  # Sort event queue

        if eventQueue[0][0] == 'arrival':
            clock = eventQueue[0][1]  # Set clock equal to current arrival time
            clockArr = clock # So we can generate correct # of processes per 100ms
            readyQueue.append([serviceTime(serv), clock, 0])  # Append new process to ready queue
            eventQueue.pop(0)

            if len(readyQueue) == 1:   # If ready queue has only 1 entry, no need to sort by HRRN
                turnTemp = serviceTime(serv)
                eventQueue.append(['completion', clock + turnTemp])  # Add completion event
                eventQueue = sorted(eventQueue, key=lambda x: x[1])  # Resort event queue

        elif eventQueue[0][0] == 'completion':
            clock = eventQueue[0][1] # Set clock to service time of first ready process
            eventQueue.pop(0)
            turnaroundArr = clock - (readyQueue[0][1] + readyQueue[0][0]) # Find arrival time
            readyQueue.pop(0)
            processCounter+=1

            turnaround += (clock - turnaroundArr)

            # If no other processes in ready queue, move on and wait for next arrival
            # Otherwise, sort ready queue by HRRN to determine next process that runs
            if len(readyQueue) != 0:

                for x in readyQueue:
                    wait = clock - x[1]
                    x[1] += wait  # Update wait times for ready processes
                    x[2] = (x[1]+x[0])/x[0] # calculate HRRN
                readyQueue = sorted(readyQueue, key=lambda x: x[2], reverse=True)  # Sort ready queue by HRRN
                eventQueue.append(['completion', clock+readyQueue[0][0]])   # Create new completion event
                eventQueue = sorted(eventQueue, key=lambda x: x[1])  # Resort event queue
            else:
                cpuTime += (eventQueue[0][1] - clock)

    print('HRRN |', 'AVG Turnaround:', '{:.2f}'.format(turnaround / 10000), '| Throughput:',
          '{:.2f}'.format(100 / lamda), 'per second | CPU Util:',
         '{:.8f}'.format(((clock - cpuTime) / clock)*100), '% | AVG Ready Queue:',
          '{:.2f}'.format(readyAVG[0] / readyAVG[1]), 'processes.')

# This simulator starts by creating 100/quantum quantums, and 100/lambda processes. It then steps thru
# each quantum. At each quantum, it determines if any events arrive during the quantum. If they do
# it adds the new arrival to the ready Queue. If a process will complete before the quantum ends,
# the function will continue to remove processes from the ready queue, incrementing the clock, until
# it comes across a process that will not finish before the next quantum. Then, it proceeds to the
# next quantum. When all arrivals are processed, the simulator creates another set of arrivals
# and quantums.
def RR(lamda, serv, quantum):
    clock = 0.0
    processCounter = 0.0
    eventQueue = []
    readyQueue = []
    quantStep = int(100/quantum)
    toSched = int((100 / lamda))  # Calculate # of processes per second, rounding down
    lastQuant = 0.0
    readyAVG = [0.0, 0.0] # Sum of ready queue length, # of times checked
    turnArr = [0.0] # Time proc arrives
    turnaround = 0.0
    cpuTime = 0.0


    # Generate either 100 or 50 quantums
    if quantum == 1:
        for x in range(1, 101, 1):
            eventQueue.append(['quantum',  float(x)])
    if quantum == 2:
        for x in range(0, 101, 2):
            eventQueue.append(['quantum',  float(x)])

    # Schedule initial arrivals 100ms in future. (100/lamda) == arrivals per 100ms
    for x in range(1, toSched + 1, 1):  # Create arrivals
        eventQueue.append(['arrival', ((lamda * x))])  # Add process arrival to sched queue
    eventQueue = sorted(eventQueue, key=lambda x: x[1])  # Sort event queue
    clock = eventQueue[0][1]

    #'''
    while processCounter != 10000:
        readyAVG[0] += len(readyQueue)  # Capture AVG ready queue size
        readyAVG[1] += 1.0

        if eventQueue[0][0] == 'quantum':
            clock = eventQueue[0][1]
            lastQuant = clock
            eventQueue.pop(0)

            # If eventQueue will be empty
            if len(eventQueue) == 1:

                # Calculate CPU idle time
                if len(readyQueue) == 0:
                    if eventQueue[0][0] == arrival: cpuTime += (eventQueue[0][1] - clock)
                    else: cpuTime += 1.0

                # Generate either 100 or 50 quantums
                if quantum == 1:
                    for x in range(1, 101, 1):
                        eventQueue.append(['quantum', lastQuant + float(x)])
                if quantum == 2:
                    for x in range(0, 101, 2):
                        eventQueue.append(['quantum', lastQuant + float(x)])
                # Schedule initial arrivals 100ms in future. (100/lamda) == arrivals per 100ms
                for x in range(1, toSched + 1, 1):  # Create arrivals
                    eventQueue.append(['arrival', (clock + (lamda * x))])  # Add process arrival to sched queue
                eventQueue = sorted(eventQueue, key=lambda x: x[1])  # Sort event queue

            # Check for any arrivals that occur during quantum
            if eventQueue[0][0] == 'arrival':
                clock = eventQueue[0][1]
                eventQueue.pop(0) # Remove arrival event
                readyQueue.append(serviceTime(serv)) # Generate service time and add to ready queue
                turnArr.append(clock)

            # Check if readyQueue has processes
            if len(readyQueue) != 0:
                # Check if ready process can finish within quantum
                while len(readyQueue) != 0 and (clock+readyQueue[0]) < eventQueue[0][1]:
                    clock += readyQueue[0]
                    readyQueue.pop(0)
                    turnaround += (clock-turnArr[0])
                    turnArr.pop(0)
                    processCounter += 1
                if len(readyQueue) != 0:
                    readyQueue[0] -= (eventQueue[0][1]-clock) # Update readyQueue[0] remaining service time
                    temp = readyQueue[0] # Save readyQueue[0] value
                    readyQueue.pop(0)
                    readyQueue.append(temp) # Put it in back of queue


    print('HRRN |', 'AVG Turnaround:', '{:.2f}'.format(turnaround/10000), '| Throughput:',
          '{:.2f}'.format(100 / lamda), 'per second | CPU Util:',
          '{:.8f}'.format(((clock-cpuTime)/clock)*100), '% | AVG Ready Queue:',
          '{:.2f}'.format(readyAVG[0]/readyAVG[1]), 'processes.')