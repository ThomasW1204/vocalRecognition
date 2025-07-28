import sys
import threading
import time
import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw
import os
import signal
import sharedObj 
class trayIcon:
    def __init__(self,uiFunction):
        self.icon = pystray.Icon("Assistant")
        self.icon.icon = self.create_image()
        self.uiFunction=uiFunction
        self.icon.menu = pystray.Menu(
            item("User Interface", self.iconUILaunch),
            item("Restart", self.restartProgram),
            item("Quit", self.quitApp)
            
    )  
        
    # Draw a simple icon
    def create_image(self):
        image = Image.new("RGB", (64, 64), color=(73, 109, 137))
        draw = ImageDraw.Draw(image)
        draw.rectangle((16, 16, 48, 48), fill="white")
        return image

    def quitApp(self,icon,item):
        icon.stop()
        print("Quitting...")
        os.kill(os.getpid(), signal.SIGTERM)  # Sends termination signal to the process
        

    def restartProgram(self,icon,item):
        print("Restarting program...")
        python = sys.executable
        os.execv(python, [python] + sys.argv)
        

    

    def iconUILaunch(self,icon,item):
        print("Simulating keybind Ctrl+Shift+;")
        time.sleep(0.1)
        threading.Thread(target=self.uiFunction, daemon=True).start()

    def run(self):
        self.icon.run()
    
 