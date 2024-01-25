import cv2
import numpy as np

class VideoFrameDiff:
    def __init__(self, video_path: str) -> None:
        self.path = video_path
        self.video = cv2.VideoCapture(video_path)
        self.processed_frames = []

    def DiffFrame(self, f1: np.ndarray, f2: np.ndarray, threshold=30) -> np.ndarray:
        """
        Calculates the difference between two frames using a threshold. Pixels where the 
        absolute difference is greater than the threshold are set to 255, otherwise 0.
        running on gpu makes no sence since since all it is doing a simple difference between frames
        """
        return np.where(np.abs(f1 - f2) > threshold, 255, 0).astype(np.uint8)
    
    def saveDiffFrameVideo(self, saveto: str = 'diffFrameVideo',
                           threshold: float = 30.0,
                           videoFormat='mp4v',fps=None) -> None:
        """
         Saves a video of the frame differences to the given path. 
         Reads frames from the video, calculates the difference between 
         consecutive frames using DiffFrame(), and writes the difference frames 
         to an output video file.
        
        """
        ret, framei = self.video.read() # reads 1st frame of video 
        height, width, _ = framei.shape 
        fps = self.video.get(cv2.CAP_PROP_FPS) if not fps else fps # checks if video in frame if fps is none or u can provide fps ur own fps
        fourcc = cv2.VideoWriter_fourcc(*videoFormat)
        out = cv2.VideoWriter(saveto + '.' + videoFormat, fourcc, fps, (width, height))
        while ret:
            ret, framej = self.video.read()  # framej=framei+1
            if not ret:
                break
            df = self.DiffFrame(framej, framei, threshold)
            out.write(df)
            framei = framej
        out.release()

    def playVideo(self,desired_size=(640, 480),original=False,threshold=30):
        cap = self.video
        if not cap.isOpened():
            print("Error opening video file")
            return
        print('press q to quite the video')
        if not original:
            ret, framei = cap.read() # reads 1st frame of video 
            while ret:
                ret, framej = self.video.read()  # framej=framei+1
                if not ret:
                    break
                df = self.DiffFrame(framej, framei, threshold)
                resized_frame = cv2.resize(df, desired_size, interpolation=cv2.INTER_LINEAR)
                cv2.imshow('Video Player', resized_frame)
                framei=framej
                # Break the loop if 'q' is pressed
                if cv2.waitKey(3) & 0xFF == ord('q'):
                    break
        else:
            print('press q to exit video')
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                # Resize the frame to the desired size
                resized_frame = cv2.resize(frame, desired_size, interpolation=cv2.INTER_LINEAR)

                # Display the resized frame
                cv2.imshow('Video Player', resized_frame)
                # Break the loop if 'q' is pressed
                if cv2.waitKey(30) & 0xFF == ord('q'):
                    break

        # Release the VideoCapture object and close the window
        cap.release()
        cv2.destroyAllWindows()  
