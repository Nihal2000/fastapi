from fastapi import FastAPI
from typing import Optional
import uvicorn
import requests
import os
import numpy as np
import shutil
from PIL import Image
from detect import run

# load environment variables
try:
    port = os.environ["PORT"]
except:
    port= 8000

app =  FastAPI()

@app.get("/")
async def home_view():
    return {"hello": "world"}

@app.get("/img")
async def img_echo_view(q: Optional[str]= None):
    if q == None:
        return {"query": "use /?q=(url) to submit the url."}
    else:
        if q.endswith('.jpeg') or q.endswith('.jpg') or q.endswith('.png') or 1:
            response = requests.get(q, stream=True)
            response.raw.decode_content = True
            image = Image.open(response.raw)
            #image.show()
            #print(np.array(image)[:2])
            #img = np.array(image)[:, : , :3]
            #result= ocr.run_tesseract(img)
            result= call_detect(q)
            if result:
                return result
            else:
                return {"result" : "False"}

def call_detect(q):

    json_file= {'prediction': {}}
    key=0
    name_ext=q.split("/")[-1]
    name= name_ext.split(".")[0]
    try:
        os.mkdir("/detect")
    except:
        pass
    path= "detect/"+name

    name=q.split("/")[-1].split(".")[0]
    run(weights= "yolo_signature.pt", source= q, save_txt= True, save_conf= True, name= name, project= "detect", data= "", conf_thres= 0.5)

    path_labels= path+"/labels"

    for file_name in os.listdir(path_labels):
        data= np.loadtxt(path_labels+"/"+file_name)
        try:
            for row in data:
                element= {}
                element['left']= row[1]
                element['top']= row[2]
                element['width']= row[3]
                element['height']= row[4]
                element['conf']= row[5]

                json_file['prediction'][key]= element
                key+= 1
        except:
            element= {}
            element['left']= data[1]
            element['top']= data[2]
            element['width']= data[3]
            element['height']= data[4]
            element['conf']= data[5]

            json_file['prediction'][key]= element
            key+= 1
    shutil.rmtree(path)
    os.remove(name_ext)
    return json_file

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(port), reload=True)