from pathlib import Path
from typing import Union
from fastapi import FastAPI,UploadFile,File
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from PIL import Image
import numpy as np
from io import BytesIO,StringIO
from ultralytics import YOLO
import cv2
from collections import Counter
from main import responsePayload
import pandas as pd

def Model(visionTask: str = 'det', trainedVarient: str = 'n'):
    trainedVarient = trainedVarient.lower()
    visionTask = visionTask.lower()
    if visionTask == 'det': return (f'yolov8{trainedVarient}.pt')
    else : return (f'yolov8{trainedVarient}-{visionTask}.pt')



app = FastAPI()



@app.post("/image")
async def send_img(task:str='det',variant:str='n', file: UploadFile = File(...)):
    contents = await file.read()
    model = Model(visionTask=task,trainedVarient=variant)
    return responsePayload(BytesIO(contents),model).send_processed_img


@app.post('/detdata')
async def array(task:str='det',
                variant:str='n',
                file:UploadFile=File(...)):
    content = BytesIO( await file.read())
    model = Model(task,variant)
    result = responsePayload(content,model).predict[0].boxes.data.numpy().tolist()
    return {
        'data' : result
    }

data = {
    'name' : ['sai','ganesh','reddy'],
    'age' : [27,28,29]
}

@app.get("/")
async def csvfile():
    df = pd.DataFrame(data)
    stream = StringIO()
    df.to_csv(stream,index=False)
    response = StreamingResponse(iter([stream.getvalue()]),media_type='text/csv')

    return response

@app.post("/boxes")
async def boxes(task:str='det',
                variant:str='n',
                file:UploadFile=File(...)):
    content = BytesIO( await file.read())
    model = Model(task,variant)
    result = responsePayload(content,model).boxes
    return result

@app.post("/keypoints")
async def boxes(task:str='det',
                variant:str='n',
                file:UploadFile=File(...)):
    content = BytesIO( await file.read())
    model = Model(task,variant)
    result = responsePayload(content,model).keypoints
    return result