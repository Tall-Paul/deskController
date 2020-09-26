import cv2



class cameraStream:   

    def __init__(self, stream_url):
        self.stream_url = stream_url
        self.cap = cv2.VideoCapture(self.stream_url)

    def getFrame(self):
        if not self.cap.isOpened():
            self.cap.release()
            self.cap = cv2.VideoCapture(self.stream_url)
        try:
            ret, frame = self.cap.read()                        
        except:
            print("error")
        if ret:
            return frame
        else:
            return None
           


