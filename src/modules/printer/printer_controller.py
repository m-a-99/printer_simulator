from flask import request,redirect,url_for,make_response
from utils.utils import utils
class PrinterController:
    def __init__(self,app,PrinterService,mode):
        self.app=app
        self.service=PrinterService
        self.register_routes()
        self.utils=utils()
        self.__mode=mode
        
    def checkauth(self,func):
            # return func()
            if self.__mode=="test":
                return func()
            if not "Authorization" in request.headers and not "jwt"  in request.cookies:
                    return redirect('login')
            token=None
            if "Authorization" in request.headers:
                token = request.headers['Authorization'].split(' ')
            else:
                token=request.cookies.get("jwt").replace("%20"," ").split(" ")
            if len(token)==2:
                token=token[1]
            else:
                token=token[0]
            try:
                self.utils.verify(token)
                return func()
            except:
                return redirect('login')
    
    def register_routes(self):
        
        # @self.app.before_request
        # def checkjwt():
        #     print(request.endpoint)
        #     if request.endpoint == 'login':
        #     # Skip JWT verification for login page
        #       return
        #     headers = {
        #             'Access-Control-Allow-Origin': '*',
        #             'Access-Control-Allow-Methods': 'POST, GET, OPTIONS, PUT, DELETE',
        #             'Access-Control-Allow-Headers': 'Origin, Accept, Content-Type, Authorization, X-Requested-With'
        #              }
        #     if request.method == 'OPTIONS':
        #         return make_response(('OK', 200, headers))
            
        #     # if not "Authorization" in request.headers:
        #     #     return redirect(url_for('login'))
            
        #     # token = request.headers['Authorization'].split(' ')
        #     # if len(token)==2:
        #     #     token=token[1]
        #     # try:
        #     #     self.utils.verify(token)
        #     # except:
        #     #     return redirect(url_for('login'))
           
            

        @self.app.get("/ping")
        def pong():
            return "pong"
        
        @self.app.get('/')
        def home():
            return self.checkauth(lambda:self.service.index())   
        
        @self.app.post("/login")
        def login():
            data= request.json
            return self.service.login(data)
        
        @self.app.get("/test")
        def test():
            return {"message":"success"}
        
        
        @self.app.get('/login')
        def index():
            return self.service.index()
        
      
        @self.app.get("/papers")
        def getPapers():
            return self.checkauth(lambda:self.service.getPapers())

        @self.app.get("/inc")
        def getInc():
            return self.checkauth(lambda:self.service.getInc())

        @self.app.get("/pendingtasks")
        def getPendingTasks():
            return self.checkauth(lambda:self.service.getPendingTasks())

        @self.app.get("/finishedtasks")
        def getFinishedTasks():
            return self.checkauth(lambda:self.service.getFinishedTasks())

        @self.app.get("/fonts")
        def getFonts():
            return self.checkauth(lambda:self.service.getFonts())

        @self.app.get("/setting")
        def getSettings():
            return self.checkauth(lambda:self.service.getSettings())

        @self.app.get("/fontsizes")
        def getFontSizes():
            return self.checkauth(lambda:self.service.getFontSizes())


        @self.app.post("/poweron")
        def poweron():
            return self.checkauth(lambda:self.service.poweron())
            
        @self.app.post("/poweroff")
        def poweroff():
            return self.checkauth(lambda: self.service.poweroff())

        @self.app.get("/state")
        def getState():
            return self.checkauth(lambda:self.service.getState())

        @self.app.post("/fixpaperjam")
        def fixPaperJam():
            return self.checkauth(lambda:self.service.fixPaperJam())

                
            
        @self.app.put("/papers")
        def setpapers():
            data=request.json
            return self.checkauth(lambda:self.service.setpapers(data["papers"]))
                
        @self.app.post("/cartridges")
        def replace_Cartridges():
            return self.checkauth(lambda:self.service.replace_Cartridges())

        @self.app.post("/cancel")
        def cancel():
            return self.checkauth(lambda:self.service.cancel())


        @self.app.post("/canceltask")
        def cancelTask():
            data=request.json
            return self.checkauth(lambda:self.service.cancelTask(data["taskid"]))
            
        @self.app.post("/pause")
        def pause():
            return self.checkauth(lambda:self.service.pause())
         
            
        @self.app.post("/resume")
        def resume():
            return self.checkauth(lambda:self.service.resume())
          

        @self.app.post("/print")
        def printReq():
            data=request.json
            return self.checkauth(lambda:self.service.printReq(data["payload"]))
       
            
        @self.app.get("/pdf/<path:fileId>")
        def file(fileId):
            return self.checkauth(lambda:self.service.file(fileId))

        @self.app.post("/printfile")
        def printfile():
            return self.checkauth(lambda:self.service.printfile(request.files,request.form.to_dict()))

        @self.app.get("/pageformats")
        def getpageformats():
            return self.checkauth(lambda:self.service.getpageformats())

        @self.app.get("/orientations")
        def getOrientations():
            return self.checkauth(lambda:self.service.getOrientations())

        @self.app.get("/setting")
        def getsetting():
            return self.checkauth(lambda:self.service.getsetting())

        @self.app.post("/calibrate")
        def calibrate():
            data=request.json
            return self.checkauth(lambda:self.service.calibrate(data["payload"]))

        @self.app.post("/reset")
        def reset():
            return self.checkauth(lambda:self.service.reset())

        @self.app.get("/version")
        def getversion():
            return self.checkauth(lambda:self.service.getversion())
        @self.app.get("/stats")
        def getstats():
            return self.checkauth(lambda:self.service.getstats())

        @self.app.post("/firmware")
        def updatefrimware():
            files=request.files
            return self.checkauth(lambda:self.service.updatefrimware(files))
            
            
    
    

    