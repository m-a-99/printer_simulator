from flask import Flask
from flask_socketio import SocketIO
from dotenv import load_dotenv
from flask_cors import CORS
from modules.printer.printer_module import PrinterModule
import os


load_dotenv()
app=Flask(__name__,static_url_path='/',static_folder="../static")
# @app.after_request
# def add_cors_headers(response):
#     response.headers['Access-Control-Allow-Origin'] = '*'
#     response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
#     response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
#     response.headers['Access-Control-Expose-Headers'] = 'Location'
#     return response
CORS(app)

socketio=SocketIO(app,cors_allowed_origins="*")

PrinterModule(app,socketio,"dev")

    
if(__name__=="__main__"):
    app_mode = os.environ.get('MODE', 'dev')
    print(app_mode)
    if(app_mode=="dev"):
        socketio.run(app)
    else:
        socketio.run(app,host="0.0.0.0",allow_unsafe_werkzeug=True)
