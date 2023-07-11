import sys
# sys.path.append('/hdd/work/unitone/flask/docker/flaskproj/src')
sys.path.append('src')

import unittest
from flask import Flask

from modules.printer.printer_module import PrinterModule
from flask_socketio import SocketIO
import json
from libs.PrinterSimulator.printerSinglton import PrinterSinglton
import time
from libs.PrinterSimulator.states import States

              
class Test1(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.socketIo=SocketIO(self.app,cors_allowed_origins="*")
        PrinterModule(self.app,self.socketIo,"test")
        self.client = self.app.test_client()
        self.Printer=PrinterSinglton.getInstance(self.socketIo)

    def test_PrintJobSubmission(self):
        loginres=self.client.post("/login",headers={'Content-Type': 'application/json'},data=json.dumps({}))
        response0 = self.client.post('/poweron')
        self.assertEqual(response0.status_code,200)
        data = {
            "payload":{
                "text":"print test #1",
                "font":"Arial",
                "fontsize":12,
                "italic":True,
                "bold":True,
                "alignment":"C",
                "color":"#000000"
                }
            }
        headers = {'Content-Type': 'application/json'}
        response = self.client.post('/print', data=json.dumps(data), headers=headers)
        resjson=response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(resjson["payload"],data["payload"])
        self.assertTrue(self.Printer.checkTaskInQueue(resjson['id']))

    def tearDown(self):
        time.sleep(3)
        response0 = self.client.post('/poweroff')
        return super().tearDown()
    
class Test2(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.socketIo=SocketIO(self.app,cors_allowed_origins="*")
        PrinterModule(self.app,self.socketIo,"test")
        self.client = self.app.test_client()
        self.Printer=PrinterSinglton.getInstance(self.socketIo)
        
    def test_PrinterStatus(self):
        self.assertEqual(self.Printer.getState()["state"],States.Offline.name)
        self.client.post('/poweron')
        self.assertEqual(self.Printer.getState()["state"],States.Idle.name)
        data = {
            "payload":{
                "text":"print test #1",
                "font":"Arial",
                "fontsize":12,
                "italic":True,
                "bold":True,
                "alignment":"C",
                "color":"#000000"
                }
            }
        headers = {'Content-Type': 'application/json'}
        self.client.post('/print', data=json.dumps(data), headers=headers)
        self.client.post('/print', data=json.dumps(data), headers=headers)
        self.assertEqual(self.Printer.getState()["state"],States.Printing.name)
        time.sleep(2.8)
        self.assertEqual(self.Printer.getState()["state"],States.Busy.name)
        time.sleep(1)
        self.assertEqual(self.Printer.getState()["state"],States.Printing.name)
        self.client.post('/pause')
        self.assertEqual(self.Printer.getState()["state"],States.Paused.name)
        self.client.post('/resume')
        self.assertEqual(self.Printer.getState()["state"],States.Printing.name)
        time.sleep(2)
        self.assertEqual(self.Printer.getState()["state"],States.Idle.name)

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(Test1("test_PrintJobSubmission"))
    suite.addTest(Test2("test_PrinterStatus"))
    # suite.addTest(MyTest3('test_something3'))
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # unittest.main()





