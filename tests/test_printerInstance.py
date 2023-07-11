import pytest
import sys
sys.path.append('src')

from libs.PrinterSimulator.states import States
from libs.PrinterSimulator.printer import Printer
from libs.PrinterSimulator.printerSinglton import PrinterSinglton

@pytest.fixture
def printer():
    printer=PrinterSinglton.getInstance(None,"test")
    return printer


def test_PowerOn(printer:printer):
    printer.powerOn()
    assert printer.getState()["state"]==States.Idle.name
    

def test_Print_And_Pause(printer:Printer):
    printer.powerOn()
    printer.pause()
    
    task=printer.printOrder({
            "payload":{
                "text":"print test #1",
                "font":"Arial",
                "fontsize":12,
                "italic":True,
                "bold":True,
                "alignment":"C",
                "color":"#000000"
                }
            })
    assert printer.getState()["state"]==States.Paused.name
    assert printer.checkTaskInQueue(task["id"])
    printer.cancel()
    