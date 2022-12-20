# main.py
from func import *

print('Schedulers')
print('========================================')
print('1. (FCFS), 2. (SRTF), 3. (HRRN), 4. (RR)')

scheduler = input('Pick a scheduler: 1-4: ')
while scheduler != '1' and scheduler != '2' and scheduler != '3' and scheduler != '4':
    scheduler = input('Please input a listed scheduler: ')

print('Scheduler:', scheduler)
if scheduler == '4':
    quantum = input('Please choose a quantum: (Enter 1 or 2)')
    quantum = float(quantum)

serv = input('Please input the average service rate: ')
serv = float(serv)

if scheduler == '1':
    print('=================================================================')
    print('Simulating FCFS with avg. service rate', serv)
    print('=================================================================')

    # For range ( 10 processes per second -> 30 processes per second ), run FCFS
    for x in range(10, 31, 1):
        lamda = 100.0/x
        FCFS(lamda, serv)

if scheduler == '2':
    print('=================================================================')
    print('Simulating SRTF with avg. service rate', serv)
    print('=================================================================')

    for x in range(10, 31, 1):
        lamda = 100.0/x
        SRTF(lamda, serv)

if scheduler == '3':
    print('=================================================================')
    print('Simulating HRRN with avg. service rate', serv)
    print('=================================================================')

    for x in range(10, 31, 1):
        lamda = 100.0/x
        HRRN(lamda, serv)

if scheduler == '4':

    print('=================================================================')
    print('Simulating RR with avg. service rate', serv, ', quantum', quantum)
    print('=================================================================')

    for x in range(10, 31, 1):
        lamda = 100.0/x
        RR(lamda, serv, quantum)
