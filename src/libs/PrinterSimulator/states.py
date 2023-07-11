from enum import Enum

class States(Enum):
    Idle=0
    Printing=1
    Paper_Jam=2
    Out_of_Paper=3
    Offline=4
    Low_Ink=5
    Error=6
    Busy=7
    Paused=8
    Cancelled=9
    Unknown=10

class TaskStates(Enum):
    Wating=1
    Running=2
    Finished=4

