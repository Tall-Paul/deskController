from Desk import *
from tkinter import *
from tkinter import ttk
import tkinter as tk
import requests
from Camera import cameraStream
from Lights import lightController
import cv2
from PIL import Image, ImageTk

from gpiozero import Button as gpioButton

#I use motioneye, so this just points at my motioneye stream...but it should work with anything that opencv supports
VIDEO_URL = 'http://192.168.100.1:8082/'

#uses an esp8266 with the code from here on it: https://randomnerdtutorials.com/esp32-esp8266-rgb-led-strip-web-server/
LIGHTS_URL = "http://192.168.100.226/"


cameraButton = gpioButton(18)
deskButton = gpioButton(23)
lightButton = gpioButton(24)

def switchTabCamera():
    global root
    root.tab_control.select(root.tab1)

def switchTabDesk():
    global root
    root.tab_control.select(root.tab2)

def switchTabLights():
    global root
    root.tab_control.select(root.tab3)

def standingCallback():
    global root
    root.lights.set_red()  
    root.Desk.moveTo(1100)
    root.lights.set_white()

def sittingCallback():
    global root
    root.lights.set_red()       
    root.Desk.moveTo(800)
    root.lights.set_white()

def redCallBack():
    root.lights.set_red()

def greenCallBack():
    root.lights.set_green()

def blueCallBack():
    root.lights.set_blue()

def blackCallBack():
    root.lights.set_black()

def whiteCallBack():
    root.lights.set_white()


class Root(Tk):
    def __init__(self):
        super(Root, self).__init__()
        self.geometry("480x800+0+0")
        self.overrideredirect(True)

        tabControl = ttk.Notebook(self)
        self.tab1 = ttk.Frame(tabControl)
        tabControl.add(self.tab1, text='Camera')
        self.tab2 = ttk.Frame(tabControl)
        tabControl.add(self.tab2, text='Desk')
        self.tab3 = ttk.Frame(tabControl)
        tabControl.add(self.tab3, text='Lights')
        tabControl.pack(expand=1, fill="both")
        self.tab_control = tabControl

        #desk tab
        standButton = Button(self.tab2, text="Stand", command=standingCallback)
        standButton.place(x = 40, y = 20, width = 240, height = 200)        
        sitButton = Button(self.tab2, text="Sit", command=sittingCallback)
        sitButton.place(x = 40, y = 220, width = 240, height = 200)   
        self.Desk = Desk() 

        #video tab
        self.canvas = tk.Canvas(self.tab1)
        self.canvas.place(x=0,y=0,width = 320, height = 460)   
        self.video = cameraStream(VIDEO_URL)
        self.canvas.after(500, self.updateVideo)

        #lights tab
        self.lights = lightController(LIGHTS_URL)
        self.lights.set_white()

        redButton = Button(self.tab3, bg='red', command=redCallBack)
        redButton.place(x = 5, y = 20, width = 100, height = 100)

        greenButton = Button(self.tab3, bg='green', command=greenCallBack)
        greenButton.place(x = 110, y = 20, width = 100, height = 100)

        blueButton = Button(self.tab3, bg='blue', command=blueCallBack)
        blueButton.place(x = 215, y = 20, width = 100, height = 100)

        whiteButton = Button(self.tab3, bg='white', command=whiteCallBack)
        whiteButton.place(x = 5, y = 125, width = 100, height = 100)

        blackButton = Button(self.tab3, bg='black', command=blackCallBack)
        blackButton.place(x = 110, y = 125, width = 100, height = 100)

        
    
    def updateVideo(self):
        try:
            img = self.video.getFrame()
            if (img is None):
                self.canvas.after(100, self.updateVideo)  
                return
            dim = (320, 460)
            resized = cv2.resize(img, dim, interpolation = cv2.INTER_NEAREST)  
            resized = cv2.cvtColor(resized,cv2.COLOR_BGR2RGB)
            
            photo = ImageTk.PhotoImage(image = Image.fromarray(resized))
            self.photo = photo
            self.canvas.create_image(0, 0, image = photo, anchor = tk.NW)          
            self.canvas.after(100, self.updateVideo)  
        except:
            print("error")



root = Root()
cameraButton.when_pressed = switchTabCamera
deskButton.when_pressed = switchTabDesk
lightButton.when_pressed = switchTabLights




while True:
    root.mainloop()