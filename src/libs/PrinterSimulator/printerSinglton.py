from .printer import Printer
from abc import ABC

class PrinterSinglton(ABC):
    __instance=None
    def __init__(self,socketio,mode):
        PrinterSinglton.__instance=Printer(socketio,mode)
    @staticmethod
    def getInstance(socketio,mode="dev"):
        if PrinterSinglton.__instance==None:
            PrinterSinglton(socketio,mode)
        return PrinterSinglton.__instance