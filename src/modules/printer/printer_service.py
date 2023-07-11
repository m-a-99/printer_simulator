from flask import send_from_directory
from libs.PrinterSimulator.printerSinglton import PrinterSinglton
from utils.utils import utils
import os

class PrinterService:
    
    def __init__(self,socketio,mode):
        self.path=os.path.dirname(__file__)
        self.printer=PrinterSinglton.getInstance(socketio,mode)
        self.utils=utils()

    def index(self):
        return send_from_directory(os.path.join(self.path,"../../../static"),"index.html")
    
    def login(self,payload):
        if("username"in payload and "password" in payload ):
            if(payload["username"]==os.getenv("SERVERUSERNAME") and payload["password"]==os.getenv("SERVERPASSWORD")):
                return self.utils.signjwt({"username":payload["username"]})
            else:
                return "invalid username or password",404
        else:
            return "username and password are required",404    
    
    def getPapers(self):
        return self.printer.getPapers()

    def getInc(self):
        return self.printer.getInk()

    def getPendingTasks(self):
        return self.printer.getPendingTasks()

    def getFinishedTasks(self):
        return self.printer.getFinishedTasks()

    def getFonts(self):
        return self.printer.getFonts()

    def getSettings(self):
        return self.printer.getSettings()

    def getFontSizes(self):
        return self.printer.getFontSizes()


    def poweron(self):
        return self.printer.powerOn()
        
    def poweroff(self):
        return  self.printer.powerOff()

    def getState(self):
        return self.printer.getState()

    def fixPaperJam(self):
        try:
            return self.printer.fixPaperJam()
        except Exception as e:
            return str(e),500
            
        
    def setpapers(self,papers):
        return self.printer.setpapers(papers)
            
    def replace_Cartridges(self):
       return self.printer.replace_Cartridges()

    def cancel(self):
        try:
            return self.printer.cancel()
        except Exception as e:
            return str(e),500

    def cancelTask(self,taskid):
        
        return self.printer.cancelTask(taskid)
        
    def pause(self):
        try:
            return self.printer.pause()
        except Exception as e:
            return str(e),500
        
    def resume(self):
        try:
            return self.printer.resume()
        except Exception as e:
            return str(e),500

    def printReq(self,payload):
        try:
            return self.printer.printOrder(payload)
        except Exception as e:
            return str(e),500
        
    def file(self,fileId):
        return send_from_directory(directory=os.path.join(self.path,'../../../output'), path=fileId+".pdf",as_attachment=True)

    def printfile(self,files,payload):
        if "file" in files:
            file=files["file"]
            if file.mimetype!="text/plain" :
                return "only text file accepted ",400
            if file :
                file.save(os.path.join(self.path,"../../../uploads/")+ file.filename)
                payload["filepath"]=os.path.join(self.path,"../../../uploads/")+ file.filename
                try:
                    return self.printer.printOrder(payload)
                except Exception as e:
                    return str(e),500
        else:
            return "file required",400

    def getpageformats(self):
        return self.printer.getPageFormats()

    def getOrientations(self):
        return self.printer.getOrientation()

    def getsetting(self):
        return self.printer.getSettings()

    def calibrate(self,payload):
        return self.printer.calibrate(payload)

    def reset(self):
        return self.printer.reset()

    def getversion(self):
        return self.printer.getversion()
    def getstats(self):  
        return self.printer.getStats()

    def updatefrimware(self,files):
        if "file" in files:
            file=files["file"]
            if file.mimetype!="text/plain" :
                return "only text file accepted ",400
            if file :
                file.save(os.path.join(self.path,"../../../firmware/firmware.txt"))
                return self.printer.getversion()
        else:
            return "file required",400
        