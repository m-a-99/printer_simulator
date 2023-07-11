import pytest
import sys
sys.path.append('src')
import threading
import requests
from app import app
from time import sleep


baseurl="http://0.0.0.0:5000"

def post(route="",token="",json=""):
    url=str(baseurl+route)
    headers={}
    if(token!=""):
        headers["Authorization"]="Barear "+token
    return requests.post(url,json=json,headers=headers)

def put(route="",token="",json=""):
    url=str(baseurl+route)
    headers={}
    if(token!=""):
        headers["Authorization"]="Barear "+token
    return requests.put(url,json=json,headers=headers)

def get(route="",token=""):
    url=str(baseurl+route)
    headers={}
    if(token!=None):
        headers["Authorization"]="Barear "+token    
    return requests.get(url,headers=headers)
    
    
@pytest.fixture(scope="module")
def printerClient():
    server_thread = threading.Thread(target=app.run,daemon=True)  
    server_thread.start()
    while True:
        
        try:
            response = get("/ping")
            print(response.text)
            if response.status_code == 200:
                break
        except requests.exceptions.ConnectionError:
            pass
    yield  server_thread


@pytest.fixture(scope="module")
def loginToken(printerClient):
        res=post("/login",json={"username":"Admin","password":"Admin"}) 
        assert "jwt" in res.text
        return res.json()['jwt']  


def test_poweron(loginToken):
    res=post("/poweron",token=loginToken)
    assert res.text.strip()=="Printer Powerdon Successfully"


     
def test_Ink(loginToken):
    res=post("/cartridges",token=loginToken)
    assert res.text=="Cartridges Replaced Successfully"
    
    res=get("/inc",token=loginToken)
    assert res.json()["inc"]==1.0
    
def test_pages(loginToken):
    res=put("/papers",token=loginToken,json={"papers":20})
    assert res.json()["papers"]==20


def test_printreq(loginToken):
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
    res=post("/print",token=loginToken,json=data)
    assert data['payload']==res.json()['payload']
    res=get("/state",token=loginToken)
    if(res.json()["state"]=="Paper_Jam"):
        post("/fixpaperjam",token=loginToken)   
    sleep(5)
    res=get("/finishedtasks",token=loginToken)
    assert len(res.json()["finishedTasks"])==1
    
    
def test_pause(loginToken):
    res=post("/pause",token=loginToken)
    assert res.text=="Printer Paused"
    
def test_resume(loginToken):
    res=post("/resume",token=loginToken)
    assert res.text=="Printer Resumed"



def test_cancel(loginToken):
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
    res=post("/print",token=loginToken,json=data)
    assert data['payload']==res.json()['payload']
    res=get("/state",token=loginToken)
    if(res.json()["state"]==""):
        post("/fixpaperjam",token=loginToken)
    res=post("/cancel",token=loginToken)
    assert res.text=="Task Canceld"
    

def test_poweroff(loginToken):
     res=post("/poweroff",token=loginToken)
     assert res.text.strip()=="Printer Powerdoff Successfully"