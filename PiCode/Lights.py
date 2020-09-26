import requests


class lightController:   

    def __init__(self, lights_url):
        self.lights_url = lights_url        

    def set_colour(self,red,green,blue):
        url = self.lights_url + "?r" + red + "g" + green + "b" + blue + "&"
        requests.get(url = url)    

    def set_red(self):
        self.set_colour("255","0","0")

    def set_green(self):
        self.set_colour("0","255","0")
    
    def set_blue(self):
        self.set_colour("0","0","255")

    def set_white(self):
        self.set_colour("255","255","255")

    def set_black(self):
        self.set_colour("0","0","0")    
