from .printer_controller import PrinterController
from .printer_service import PrinterService

class PrinterModule:
    def __init__(self,app,socketio,mode):
        service=PrinterService(socketio,mode)
        PrinterController(app,service,mode)
        