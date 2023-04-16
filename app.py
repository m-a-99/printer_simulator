from flask import Flask,request,send_from_directory
from models.printerSinglton import PrinterSinglton
from flask_socketio import SocketIO
from flask_cors import CORS


app=Flask(__name__, static_url_path='/',static_folder="static")
CORS(app)
socketio=SocketIO(app,cors_allowed_origins="*")
printer=PrinterSinglton.getInstance(socketio)

@app.get("/")
def index():
    return send_from_directory("static","index.html")

@app.get("/papers")
def getPapers():
    return printer.getPapers()

@app.get("/inc")
def getInc():
    return printer.getInk()

@app.get("/pendingtasks")
def getPendingTasks():
    return printer.getPendingTasks()

@app.get("/finishedtasks")
def getFinishedTasks():
    return printer.getFinishedTasks()

@app.get("/fonts")
def getFonts():
    return printer.getFonts()

@app.get("/setting")
def getSettings():
    return printer.getSettings()

@app.get("/fontsizes")
def getFontSizes():
    return printer.getFontSizes()


@app.post("/poweron")
def poweron():
    return printer.powerOn()
    
@app.post("/poweroff")
def poweroff():
    return  printer.powerOff()

@app.get("/state")
def getState():
    return printer.getState()

@app.post("/fixpaperjam")
def fixPaperJam():
    try:
        return printer.fixPaperJam()
    except Exception as e:
        return str(e),500
        
    
@app.put("/papers")
def setpapers():
    data=request.json
    return printer.setpapers(data["papers"])
        
@app.post("/cartridges")
def replace_Cartridges():
   return printer.replace_Cartridges()

@app.post("/cancel")
def cancel():
    try:
        return printer.cancel()
    except Exception as e:
        return str(e),500

@app.post("/canceltask")
def cancelTask():
    data=request.json
    return printer.cancelTask(data["taskid"])
    
@app.post("/pause")
def pause():
    try:
        return printer.pause()
    except Exception as e:
        return str(e),500
    
@app.post("/resume")
def resume():
    try:
        return printer.resume()
    except Exception as e:
        return str(e),500

@app.post("/print")
def printReq():
    data=request.json
    try:
        return printer.printOrder(data["payload"])
    except Exception as e:
        return str(e),500
    
@app.get("/pdf/<path:fileId>")
def file(fileId):
    return send_from_directory(directory='output', path=fileId+".pdf",as_attachment=True)

@app.post("/printfile")
def printfile():
    files=request.files
    if "file" in files:
        file=files["file"]
        if file.mimetype!="text/plain" :
            return "only text file accepted ",400
        if file :
            file.save("uploads/"+ file.filename)
            payload=request.form.to_dict()
            payload["filepath"]="uploads/"+ file.filename
            try:
                return printer.printOrder(payload)
            except Exception as e:
                return str(e),500
            
    else:
        return "file required",400

@app.get("/pageformats")
def getpageformats():
    return printer.getPageFormats()

@app.get("/orientations")
def getOrientations():
    return printer.getOrientation()

@app.get("/setting")
def getsetting():
    return printer.getSettings()

@app.post("/calibrate")
def calibrate():
    data=request.json
    return printer.calibrate(data["payload"])

@app.post("/reset")
def reset():
    return printer.reset()

@app.get("/version")
def getversion():
    return printer.getversion()
@app.get("/stats")
def getstats():
    return printer.getStats()

@app.post("/firmware")
def updatefrimware():
    files=request.files
    if "file" in files:
        file=files["file"]
        if file.mimetype!="text/plain" :
            return "only text file accepted ",400
        if file :
            file.save("firmware/firmware.txt")
            return printer.getversion()
    else:
        return "file required",400
    
    
if(__name__=="__main__"):
    socketio.run(app)

