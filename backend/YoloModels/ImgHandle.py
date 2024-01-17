from ultralytics import YOLO
from pathlib import Path
from fastapi.responses import StreamingResponse
from PIL import Image
import numpy as np
from io import BytesIO,StringIO
from ultralytics import YOLO
import cv2
import os
import pandas as pd
from collections import defaultdict

class YoloPath:
    """Initializes YoloPath class to handle YOLOv8 model paths.
    
    The YoloPath class provides methods to generate the path to different 
    YOLOv8 models based on the task (detection, segmentation, etc.) and
    variant (nano, small, etc.). This allows easy initialization of YOLOv8
    models by just specifying the task and variant separately.
    
    Attributes:
        task (str): The vision task (detection, segmentation, etc). Defaults to 'det'.
        variant (str): The model variant (nano, small, etc.). Defaults to 'n'.
    
    """
    def __init__(self,
                 visionTask: str = 'det', 
                 trainedVarient: str = 'n') -> None:
        self.task = visionTask
        self.varient = trainedVarient

    @property
    def getpath(self):
        # Returns the path to the YOLOv8 model file based on the task and variant.
        # The task and variant are converted to lowercase. 
        # For detection, returns yolov8{variant}.pt.
        # For other tasks, returns yolov8{variant}-{task}.pt.
        task,varient = self.task.lower(), self.varient.lower()
        if task == 'det': return (f'yolov8{varient}.pt')
        else : return f'yolov8{varient}-{task}.pt'

class ImageData:
    def __init__(self,content: str | BytesIO,
                 model:str|Path='yolov8n.pt',
                 task=None) -> None:
        self.model = YOLO(model,task)
        self.content = content
    
    @property
    def isImageFile(self)->bool:
        """Checks if the content passed to ImageData is a valid image file.
        
        This method attempts to open the content as an image using PIL. If the content 
        is a valid image file path or binary data, it will return True and the opened 
        Image object. Otherwise it will return False and None.
        
        Returns:
            bool: True if content is a valid image, False otherwise.
            Image: The opened Image object if content is valid, None otherwise.
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
        """Converts the image content to a numpy array.
        
        This method checks if the content is a valid image using isImageFile. 
        If valid, the image is converted to a numpy array and returned.
        
        Returns:
            numpy.ndarray: The image content as a numpy array.
        """
        sucess, img = self.isImageFile
        if sucess:
            return np.asarray(img)
        
    @property
    def predict(self):
        """Gets predictions from the YOLO model on the image content.
        
        This method checks if the content is a valid image using isImageFile.
        If valid, it runs model prediction and returns the prediction output.
        
        Returns:
            YOLO model prediction output for the given image content.
        """
        # in predict method you can pass an image either PIL object or image path or simply numpy array
        # im choosing isimagefile since it handles error expections
        sucess, img = self.isImageFile
        if sucess:
            model = self.model.predict(img)
            return model
    @property
    def objNames(self):
        """Gets the object class names from the model prediction.
        
        This returns the list of class names the model can detect, obtained 
        from the model prediction output.
        
        Returns:
            list: The list of object class names detected by the model.
        """
        return self.predict[0].names
    
    @property
    def boxes(self): # in detetction segmention and keypoints boxes value will be present 
        """Gets bounding box coordinates predicted by model.
        
        This method extracts the bounding box coordinates from the model prediction output.
        It returns a CSV response containing the coordinates and confidence for each detected object.
        
        Returns:
            Response: StreamingResponse returning a CSV with bounding box info.
        """
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
        """Gets keypoints predicted by model.
        
        This method extracts the keypoints from the model prediction output.
        It returns a CSV response containing the coordinates and visibility 
        for each detected keypoint per object instance.
        
        Returns:
            Response: StreamingResponse returning a CSV with keypoint info.
        """
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
    
    def  __init__(self, content: str | BytesIO,
                   model: str | Path = 'yolov8n.pt', 
                   task=None) -> None:
        super().__init__(content, model, task)
    
    @property
    def send_processed_img(self):
        """Sends the processed image as a response.
        
        Converts the model plot to RGB, saves it to a BytesIO object, 
        seeks to start, and returns a StreamingResponse containing the image bytes 
        and appropriate media type.
        """
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