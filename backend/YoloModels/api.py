from fastapi import FastAPI,UploadFile,File
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
from io import BytesIO,StringIO
import cv2
from ImgHandle import responsePayload,YoloPath
import pandas as pd

app = FastAPI()

development_origin = ['*']
allow_only_origins = ["http://localhost:5173"] # front end url 

app.add_middleware(
    CORSMiddleware,
    allow_origins=development_origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/image")
async def send_img(task:str='det',variant:str='n', file: UploadFile = File(...)):
    contents = await file.read()
    model = YoloPath(task,variant).getpath
    return responsePayload(BytesIO(contents),model).send_processed_img

@app.post('/detData')
async def array(task:str='det',
                variant:str='n',
                file:UploadFile=File(...)):
    content = BytesIO( await file.read())
    model = YoloPath(task,variant).getpath
    result = responsePayload(content,model).predict[0].boxes.data.numpy().tolist()
    return {
        'data' : result
    }

data = {
    'name' : ['if you are watching this message means the end point is working']
}

@app.get("/")
async def working():
    return {'hi' : 'this api is working'}

@app.get("/csv")
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
    model = YoloPath(task,variant).getpath
    result = responsePayload(content,model).boxes
    return result

@app.post("/keypoints")
async def boxes(task:str='pose',
                variant:str='n',
                file:UploadFile=File(...)):
    content = BytesIO( await file.read())
    model = YoloPath(task,variant).getpath
    result = responsePayload(content,model).keypoints
    return result

@app.post("/object/info")
async def boxes(task:str='pose',
                variant:str='n',
                file:UploadFile=File(...)):
    content = BytesIO( await file.read())
    model = YoloPath(task,variant).getpath
    result = responsePayload(content,model).imgCrop
    return {key : len(value) for key,value in result.items()}

@app.post("/countObjects")
async def boxes(task:str='pose',
                variant:str='n',
                file:UploadFile=File(...)):
    content = BytesIO(await file.read())
    model = YoloPath(task,variant).getpath
    result = responsePayload(content,model).inImageObjects
    return result

@app.post("/show/cropped/{person}/{nthImage}")
async def boxes(objectName:str,
                nthImage:int,
                task:str='pose',
                variant:str='n',
                file:UploadFile=File(...)):
    content = BytesIO(await file.read())
    model = YoloPath(task,variant).getpath
    Imgformat = responsePayload(content,model).isImageFile[1].format
    crop = responsePayload(content,model).imgCrop
    objs_in_pic = list(crop.keys())
    name = objectName
    nthobj = nthImage
    if name in objs_in_pic:
        images = crop[name]
        no_of_images = len(images)
        if 0<= nthobj <= no_of_images:
            result = images[nthobj]
        else : 
            result = {'response : ':f'there is no {nthobj} object in the {name} please provide the number from 0 to {no_of_images}'}
    else :
        result = {'response : ':f'theres no {name} in the uploaded image please try to provide the names from {objs_in_pic}'}
    return result