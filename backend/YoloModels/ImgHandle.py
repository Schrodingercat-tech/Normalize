from ultralytics import YOLO
from pathlib import Path
from fastapi.responses import StreamingResponse
from PIL import Image
import numpy as np
from io import BytesIO,StringIO
from ultralytics import YOLO
import cv2
import os
import pandas as pd# Imports the pandas library for working with data frames
from collections import defaultdict

class YoloPath:
    """Initializes YoloPath with default vision task and trained variant.
    
    Args:
      visionTask (str): The vision task, default 'det' for detection.
      trainedVarient (str): The trained YOLO variant, default 'n' for nano.
    
    """
    def __init__(self,
                 visionTask: str = 'det', 
                 trainedVarient: str = 'n') -> None:
        self.task = visionTask
        self.varient = trainedVarient

    @property
    def getpath(self):
        '''
        NOTE - we have various yolov8 models for 
        det(detection), seg(segmentation), cls(classification), pose(pose detection only applied for person object) and (obb)oriented bounding boxes
        with varients like n(nano),s(small),m(medium),l(large) and x(huge)
        this function allows us to sepcify the task and its varient seperately and it makes string that is needed to initilize the yolo model
        '''
        task,varient = self.task.lower(), self.varient.lower()
        if task == 'det': return (f'yolov8{varient}.pt')
        else : return f'yolov8{varient}-{task}.pt'

class ImageData:
    """Initializes ImageData with image content and YOLO model.
    
    Args:
      content (str|BytesIO): Path to image file or image binary data.
      model (str|Path): Path to YOLO model file or name of pretrained model variant (default 'yolov8n.pt').
      task (str): YOLO task like 'det', 'seg', etc.
    """
    def __init__(self,content: str | BytesIO,
                 model:str|Path='yolov8n.pt',
                 task=None) -> None:
        self.model = YOLO(model,task)
        self.content = content
    
    @property
    def isImageFile(self)->bool:
        """
        you can explicitly pass and binary or image path in __init__,
        if its image returns True and image content
        if not false and none
        """
        content = self.content
        try: 
            if isinstance(content, str) :
                with open(content,'rb') as f:
                    image = Image.open(BytesIO(f))
            elif isinstance(content, BytesIO):
                image = Image.open(content) 
            else:
                return False,None

            return True,image
        except Exception as e: return False
        
    @property
    def imgarr(self)->np.ndarray:
        """
        converts binary image or image path to an numpy array

        """
        sucess, img = self.isImageFile
        if sucess:
            return np.asarray(img)
        
    @property
    def predict(self):
        """
        use yolo object to predict image
        it returns yolo predict object
        """
        # in predict method you can pass an image either PIL object or image path or simply numpy array
        # im choosing isimagefile since it handles error expections
        sucess, img = self.isImageFile
        if sucess:
            model = self.model.predict(img)
            return model
    @property
    def objNames(self):
        return self.predict[0].names
    
    @property
    def boxes(self): # in detetction segmention and keypoints boxes value will be present 
        Boxes = self.predict[0].boxes
        if Boxes is None:
            return {
                'response' : 'boxes value is null cant fetch csv'
            }
        else :
            Boxes = Boxes.numpy().data
            headers = ['Xmin','Ymin','Xmax','Ymax','Confidence','Name']
            df = pd.DataFrame(Boxes,columns=headers)
            df['Name'] = df['Name'].map(dict(self.objNames))
            stream = StringIO()
            df.to_csv(stream,index=False)
            return StreamingResponse(
                iter([stream.getvalue()]),
                media_type='text/csv'
            )
    @property
    def keypoints(self): # if pose is called it will display persons keypoints note : it is only trained on person
        key = self.predict[0].keypoints
        if key is None:
            return {
                'response' : 'keypoints value is null cant fetch csv'
            }
        else:
            headers = ['Object', 'X', 'Y', 'Visibility']
            key = key.data.numpy()
            data = []
            for i, k in enumerate(key):
                df = pd.DataFrame(k, columns=headers[1:])
                df.insert(0, 'Object', i)  # insert 'Object' column at the beginning
                data.append(df)
            final_df = pd.concat(data)  
            stream = StringIO()
            final_df.to_csv(stream,index=False)
            return StreamingResponse(
                iter([stream.getvalue()]),
                media_type='text/csv'
            )

                
    @property
    def masks(self): # when segmentation is called this will return the mask data 
        mask = self.predict[0].masks
        if mask is None:
            return {
                'response' : 'mask value is null cant fetch csv'
            }
            
    @property
    def obb(self): # oriented bounding boxes this method is called if there are objects that are oriented by some angle's
        mask = self.predict[0].masks
        if mask is None:
            return {
                'response' : 'mask value is null cant fetch csv'
            }
    @property 
    def imgCrop(self): 
        """Crops detected objects from image.

        This method crops the detected objects from the input image using 
        the bounding box coordinates predicted by the model. It returns
        a dictionary with the object names as keys and a list of cropped 
        images containing each detected instance of that object.

        The bounding box coordinates are extracted from model.boxes and
        used to crop the region from the input image. The cropped images
        are appended to lists grouped by the object name/class.
        """
        images = defaultdict(list)
        model = self.predict[0]
        names = self.objNames
        boxes = model.boxes.data.numpy()
        objs,cols = boxes.shape
        for obj in range(objs):
            xmin,ymin,xmax,ymax,confi,clas = boxes
            crop = self.isImageFile[1].crop((xmin,ymin,xmax,ymax))
            images[names[clas]].append(crop)
        return images
        
 
class responsePayload(ImageData):

    """
    sending files from an end point 
    since we process variety of data formats on image for example,
    sending processed image for bounding box ,mask,key ,obb or any sort of data 
    
    """
    
    def  __init__(self, content: str | BytesIO,
                   model: str | Path = 'yolov8n.pt', 
                   task=None) -> None:
        super().__init__(content, model, task)
    
    @property
    def send_processed_img(self):
        model = self.predict[0]
        _ , img = self.isImageFile
        Imgformat = img.format
        frame = cv2.cvtColor(model.plot(),cv2.COLOR_BGR2RGB)
        img_bytesio = BytesIO()
        Image.fromarray(frame).save(img_bytesio, format=f"{Imgformat}")
        img_bytesio.seek(0)
        streamResponse = StreamingResponse(img_bytesio,media_type=f'image/{Imgformat.lower()}')
        return streamResponse
    
    @property
    def file_response(self):
        pass
    @property
    def json_response(self):
        pass