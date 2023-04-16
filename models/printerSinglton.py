from models.printer import Printer
from abc import ABC

class PrinterSinglton(ABC):
    __instance=None
    def __init__(self,socketio):
        PrinterSinglton.__instance=Printer(socketio)
    @staticmethod
    def getInstance(socketio):
        if PrinterSinglton.__instance==None:
            PrinterSinglton(socketio)
        return PrinterSinglton.__instance