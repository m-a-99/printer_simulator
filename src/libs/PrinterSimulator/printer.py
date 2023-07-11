import time
import threading
# from . import States,TaskStates,PDF

from .states import States
from .states import TaskStates 
from .Fpdf import PDF
import math
import random
from . import printer
import uuid
import json 
import pickle
from datetime import datetime
import os

class Printer():
    def __init__(self,socketio,mode):
        self.socketio=socketio
        self.__Papers=100
        self.__Inc=8
        self.__PaperJam_prev_state=States.Unknown
        self.__Pause_prev_state=States.Unknown
        self.__state=States.Offline
        self.__thread=False
        self.__Queue=[]
        self.__finished=[]
        self.__mode=mode
        
        self.isPageFormatCustom=False
        self.pageFormat="A4"
        self.pageWidth=210
        self.pageHeight=297
        self.leftMargin=25.4
        self.rightMargin=25.4
        self.topMargin=25.4
        self.orientation="P"
        self.autoPageBreak=True
        
        self.path=os.path.dirname(__file__)

    def printOrder(self,payload):
        if(self.__state==States.Offline):
            raise Exception("Printer Is Offline")
        task={
            "id":self.__truncated_uuid4(),
            "payload":payload,
            "state":TaskStates.Wating
        }
        self.__Queue.append(task)
        self.__updateTaskQueue()
        self.__checkQueue()
        return json.loads(json.dumps(task,default=lambda x: x.name))
        
    def __setNextState(self):
        if(self.__Inc<=0):
            self.__setState(States.Low_Ink)
            
        elif(self.__Papers<=0):
            self.__setState(States.Out_of_Paper)
            
        else:
            if(len(self.__Queue)>0):
                self.__setState(States.Busy)
                time.sleep(1)
            else:
                self.__setState(States.Idle)

    def __checkQueue(self):  
        if(self.__thread==False and len(self.__Queue)>0 ):
            pdf=PDF(self.isPageFormatCustom,self.pageFormat,self.pageWidth,self.pageHeight,self.leftMargin,self.rightMargin,self.topMargin ,self.orientation,self.autoPageBreak,self.__Queue[0])
            x= threading.Thread(target=self.__print, daemon=True,args=(pdf,))
            x.start()
            
    def __print(self,pdf):
        self.__thread=True
       
        while(self.__state==States.Paused or self.__state==States.Low_Ink or self.__state==States.Out_of_Paper):
            if(self.__state==States.Cancelled or self.__state==States.Offline):
                break
        self.__Queue[0]["state"]=TaskStates.Running
        self.__updateTaskQueue()
        if(self.__state==States.Idle or self.__state==States.Busy):
            self.__setState(States.Printing)
        
        self.__randomPaperJam()        
        while( self.__state==States.Paper_Jam):
            if(self.__state==States.Cancelled or self.__state==States.Offline):
                break
        start_time = time.monotonic()
        while(time.monotonic()-start_time<2 ): 
            if(self.__state==States.Paused):
                passed=time.monotonic()-start_time
                while(self.__state==States.Paused):
                    if(self.__state==States.Cancelled or self.__state==States.Offline):
                        break
                start_time=time.monotonic()-passed
            if(self.__state==States.Cancelled or self.__state==States.Offline):
                break
        if(self.__state!=States.Offline):
            task=self.__Queue.pop(0)
            if(self.__state!=States.Cancelled):
                self.__setPapers(self.__Papers-1)
                self.__setInc(self.__Inc-1)
                # print=PDF(text,size,font,alignment,color,isItalic,isBold)
                pdf.print()
                self.__setLastPrint()
                self.__setCount()
                task["state"]=TaskStates.Finished
                self.__updateTaskQueue()
                self.__finished.append(task)
                self.__updateFinishedTasks()
            else:
                self.__updateTaskQueue()
            self.__setNextState()
            self.__thread=False
            self.__checkQueue()   
        else:
            self.__updateTaskQueue()
        
            
    def __truncated_uuid4(self):
        return str(uuid.uuid4())[:8]
    
    def __randomPaperJam(self):
        if(self.__Inc>0 and self.__Papers>0):
            rand=math.trunc(random.random()*3)
            if(rand==1 and self.__mode!="test"):
                self.__PaperJam_prev_state=self.__state
                self.__setState(States.Paper_Jam)
            
    def fixPaperJam(self):
        if(self.__state!=States.Paper_Jam):
            raise Exception("There is No Paper_Jam")
        self.__setState(self.__PaperJam_prev_state)
        return "paperjam fixed Successfully"
        
        
    def __setState(self,state):
        self.__state=state
        if(self.__mode!="test"):
            self.socketio.emit('stateUpdate', {'state': self.__state.name})
        
    def __setPapers(self,papers):
        self.__Papers=papers
        if(self.__mode!="test"):
            self.socketio.emit('paperUpdate', {'papers': self.__Papers})
        
    def __setInc(self,inc):
        self.__Inc=inc
        if(self.__mode!="test"):
            self.socketio.emit('incUpdate', {'inc': self.__Inc/1000})
        
        
    def __updateTaskQueue(self):
        if(self.__mode!="test"):
            self.socketio.emit('updateTaskQueue', {'queue':json.loads(json.dumps(self.__Queue,default=lambda x: x.name))})
        
    def __updateFinishedTasks(self):
        if(self.__mode!="test"):
            self.socketio.emit('updateFinishedTasks', {'finishedTasks':json.loads(json.dumps(self.__finished,default=lambda x: x.name))})


    def getState(self):
        return {"state":self.__state.name}


    def setpapers(self,papers):
        if(papers>1000):
            raise Exception("Maximum Paper Capacity 1000")
        self.__setPapers(papers)
        self.__setNextState()
        return {"papers":self.__Papers}
        

    def replace_Cartridges(self):
        self.__setInc(1000)
        self.__setNextState()
        return "Cartridges Replaced Successfully"
    
    def cancelTask(self,id):
        for task in self.__Queue:
            if(task["id"]==id):
                self.__Queue.remove(task)
                self.__updateTaskQueue()
        return "Task With Id "+ id +" Canceld"
    def cancel(self):
         if(self.__state==States.Offline):
             raise Exception("Printer Is Offline")
         
         if self.__thread or len(self.__Queue)>0 :
            self.__setState(States.Cancelled)
            return "Task Canceld"
         else:
             raise Exception("No Task To Cancel")
    
    def pause(self):
        if(self.__state==States.Offline):
            raise Exception("Printer Is Offline")
        self.__Pause_prev_state=self.__state
        self.__setState(States.Paused)
        return "Printer Paused"
    
    def resume(self):
        if(self.__state==States.Offline):
            raise Exception("Printer Is Offline")
        self.__setState(self.__Pause_prev_state)
        return  "Printer Resumed"
    
    def powerOn(self):
        if(self.__state==States.Offline):
            self.__setState(States.Idle)
        self.__setLastRun()
        return "Printer Powerdon Successfully"
    def powerOff(self):
        self.__setState(States.Offline)
        self.__Queue=[]
        self.__updateTaskQueue()
        return "Printer Powerdoff Successfully"
        
    def getPendingTasks(self):
        return {'queue':json.loads(json.dumps(self.__Queue,default=lambda x: x.name))}
    
    def getFinishedTasks(self):
        return {'finishedTasks':json.loads(json.dumps(self.__finished,default=lambda x: x.name))}
    
    def getPapers(self):
        return {"papers":self.__Papers}
    
    def getInk(self):
        return {"inc":self.__Inc/1000}
    
    def getFonts(self):
        return ["Arial","Times","Symbol","ZapfDingbats"]
        
    def getSettings(self):
        return {
        "isPageFormatCustom":self.isPageFormatCustom,
        "pageFormat":self.pageFormat,
        "pageWidth":self.pageWidth,
        "pageHeight":self.pageHeight,
        "leftMargin":self.leftMargin,
        "rightMargin":self.rightMargin,
        "topMargin":self.topMargin,
        "orientation":self.orientation,
        "autoPageBreak":self.autoPageBreak,
        }
    def getOrientation(self):
        return ["L","P"]
    
    def getPageFormats(self):
        return ["A3","A4","A5","Letter","Legal"]
    
    def calibrate(self,payload):
        if("isPageFormatCustom" in payload):
            self.isPageFormatCustom=payload["isPageFormatCustom"]
        if self.isPageFormatCustom:
            if("pageWidth" in payload):
                self.pageWidth=payload["pageWidth"]
            if("pageHeight" in payload):
                self.pageHeight=payload["pageHeight"]
        else:   
            if("pageFormat" in payload):
                self.pageFormat=payload["pageFormat"]
        
        if("leftMargin" in payload):
            self.leftMargin=payload["leftMargin"]
        if("rightMargin" in payload):
            self.rightMargin=payload["rightMargin"]
        if("topMargin" in payload):
            self.topMargin=payload["topMargin"]
        if("orientation" in payload):
            self.orientation=payload["orientation"]
        if("autoPageBreak" in payload):
            self.autoPageBreak=payload["autoPageBreak"]
        return self.getSettings()

    def getFontSizes(self):
        return {"from":8,"to":32}
    
    def getversion(self):
        with open(os.path.join(self.path,"../../../firmware/firmware.txt")) as f:
            return f.readline()

    def __setStats(self,db):
        with open(os.path.join(self.path,'../../../stats/stats.dump'), 'ab') as file:
                file.seek(0)
                file.truncate()
                pickle.dump(db, file) 
        if(self.__mode!="test"):
            self.socketio.emit("updateStats",db)
            
        
    
    def __getStats(self):
        with open(os.path.join(self.path,'../../../stats/stats.dump'), 'rb') as file:
            db={}
            try:
                db = pickle.load(file)
            except EOFError:
                pass    
            return db
    
    def __setLastRun(self):
        db=self.__getStats()
        db["LastRun"]=datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.__setStats(db)

        
    def __setLastPrint(self):
        db=self.__getStats()
        db["LastPrint"]=datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.__setStats(db)
        
    def __setCount(self):
        db=self.__getStats()
        if"Count" in db:
            db["Count"]=db["Count"]+1
        else:
            db["Count"]=1
        self.__setStats(db)
        
    def getStats(self):
        return self.__getStats()
    
    def checkTaskInQueue(self,id):
        for task in self.__Queue:
            if(task["id"]==id):
                return True
        return False
    
    def reset(self):
        self.isPageFormatCustom=False
        self.pageFormat="A4"
        self.pageWidth=210
        self.pageHeight=297
        self.leftMargin=25.4
        self.rightMargin=25.4
        self.topMargin=25.4
        self.orientation="P"
        self.autoPageBreak=True
        return self.getSettings()


    