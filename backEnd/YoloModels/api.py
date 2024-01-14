from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse,FileResponse,StreamingResponse
from fastapi.middleware import Middleware
import matplotlib.pyplot as plt 
from PIL import Image
from io import BytesIO
import cv2,uuid,os
import numpy as np 
from ultralytics import YOLO


#this file is updated
app = FastAPI()

class yoloImage(BaseModel): # i tried this base model method and this is not working unless i explicitly use upload files seperatly 
    task : str = 'det'
    varient : str = 'n'
    file :UploadFile = File(...)

# this model downloads the weights based on the task : det(detect), seg(segmentation), cls(classification), pose and obb and its varients n(nano),s(small),m(medium),l(large),x(huge) 
def Model(visionTask: str = 'det', trainedVarient: str = 'n'):
    trainedVarient = trainedVarient.lower()
    visionTask = visionTask.lower()
    if visionTask == 'det': return YOLO(f'yolov8{trainedVarient}.pt')
    else : return YOLO(f'yolov8{trainedVarient}-{visionTask}.pt')

# image process and using stream response to send data into chunks without having to increase disk and memory space 
def predict_image(model,contents):
    """
    model : we pass either yolo model or the Model function that we created 
    contents : its a binary file we will convert this binary data to array like object and process the image 
    retun -> returns the image stream response 

    """
    try:
        img = np.asarray(Image.open(BytesIO(contents))) # convert binary to image array
        result = model.predict(img) # 
        frame = result[0].plot() # returns image array with whatever config u have choosen in the model
        img_bytesio = BytesIO()
        Image.fromarray(frame).save(img_bytesio, format="JPEG")
        img_bytesio.seek(0)
        return StreamingResponse(img_bytesio, media_type="image/jpeg"),result
    except Exception as e:
        return {"error": str(e)}
# making post request where u can provide vision task and its varient weights and upload a image file 
@app.post("/image")
async def send_img(task:str='det',variant:str='n', file: UploadFile = File(...)):
    contents = await file.read()
    model = Model(visionTask=task,trainedVarient=variant)
    return predict_image(model,contents)[0]

@app.post('/detdata')
async def array(task:str='det',
                variant:str='n',
                file:UploadFile=File(...)):
    content = await file.read()
    img = np.asarray(Image.open(BytesIO(content))) # convert binary to image array
    result = Model(task,variant).predict(img)[0].boxes.data.numpy().tolist()
    return {
        'data' : result
    }

  


# ignore the below code this is only testing purpose 
@app.get("/show")
async def show():
    return FileResponse('../assects/images/cat.jpg')

@app.get("/")
async def greet():
    return {
        'Greetings' : 'Hey sup, this is machine learning solution'
    }

