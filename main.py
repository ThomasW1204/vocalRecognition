
print("initializing...")
from multiprocessing import Process
import sys
import time
from ListenandSpeak import ListenandSpeak
from browserCMDs import browserCMDs
from mistralai import Mistral
from AI_module import AI
from UI import UI
from trayIcon import trayIcon
import threading
import keyboard
import sharedObj


##obj creation##
va = ListenandSpeak(None)
commands = browserCMDs(va)

api_key = "AzgyjA0icarZKB9DyB1aFMNXiwBWkuML"
model = "mistral-small-latest"
client = Mistral(api_key=api_key)
conversation = [ #this holds the conversation history. up to 21 lines (1 system, 10 user, 10 assistant)
    {
        "role": "system",
        "content": (
            "You are a helpful voice assistant for Thomas."
            "Always respond clearly and concisely in 1–2 sentences max. "
            "If you receive a vague command, assume it's related to controlling my computer like: web browsing, searching, or note taking and only say something like 'sure thing'."
            "if the prompt is empty meaning "" or " " then do not say a word"
            "at the end of a question do not say anything like 'have anymore questions' or 'would you like to know more'"
        )
    }
]


custom_commands ={   #these phases are custom. if the ai hears any of the left ones it interprets them as the right one
        "pull up": "open",
        "google": "search",
        "show recent": "recent",
        "recent":"recent",
        "take note": "notepad",
        "previous song": "previous",
        "next song": "skip",
        "skip song": "skip",
        "play song": "play",
        "pause song": "pause",
        "play playlist": "playlist",
        "start playlist":"playlist",
        "set the mood":"mood",
        "set the":"mood",
        "d":"done",
        "finish":"done"
        }

ai = AI(va,api_key,client,model,conversation,custom_commands)
ui = UI(ai)
va.ui = ui
"""
for attempt in range(2):
    try:
        ai = AI(va,api_key,client,model,conversation,custom_commands)
        UI.ai=ai
        break
    except Exception as e:
        print(f"failed to initialize the AI: {e}")
        va.speak("there was a problem with the AI retrying...")
        time.sleep(1)
"""
if ai is None:
    va.speak("ai failed to start the program again")
    sys.exit()

######################################################################################

on= True
trigger_word = "ai"  # change this to change what the assistant listens for


def triggered():
    active = True
    command_text = va.listen_until_heard(first=True)  

    while active:       #this is when its listening for a actual command
        #command_text = ListenandSpeak.listen()

        print(f"Command: {command_text}")
        ui.log(f"Command: {command_text}")
        conversationMode = ai.determineIntent(command_text,commands)        #this will determine the intent of the user and either execute cmd or answer the user question

        if not conversationMode:   #this might error 
            active = False


def start(ui):
    while on:
        print("Waiting for trigger word...")
        ui.log("Waiting for trigger word...")
        #threading.Thread(target=hotkey, daemon=True).start()
        spoken_text = va.listen_until_heard()   #annhing you say is stored in this var 
        print(spoken_text)
        if trigger_word in spoken_text:    #if you say the trigger word
            triggered()

'''

uirunning = False
uiinstance = None
def set_ui_running_false():
    global uirunning
    uirunning = False


def handleUI():
    global uirunning, uiinstance

    if not uirunning:
        uirunning = True
        uiinstance = UI(ai)
        uiinstance.protocol("WM_DELETE_WINDOW", onclose)  # link close event
        
        uiinstance.mainloop()


def onclose():
    global uiinstance, uirunning
    uirunning = False
    if uiinstance is not None:
        uiinstance.destroy()
        uiinstance = None


def hotkey():
    print("Waiting for hotkey (Ctrl+Shift+;)...")
    while True:
        keyboard.wait("ctrl+shift+;")
        print("Hotkey pressed, launching UI...")
        threading.Thread(target=handleUI, daemon=True).start()
'''


if __name__ == "__main__":
    tray = trayIcon(uiFunction=None)
    threading.Thread(target=tray.run, daemon=True).start()

    # Create UI in main thread
   
    ListenandSpeak.ui = ui
    # Run your assistant loop in background thread
    threading.Thread(target=start, args=(ui,), daemon=True).start()

    # Start Tkinter mainloop (blocks here)
    ui.mainloop()
        #fixes needed
            #somehow make it run/listen faster 
            #"recent" isn't working right 

        #TO DO
            #add a close window 
            #make a json of history and store it somewhere. maybe sqldb

            #add join ____ discord call 
            #add shutdown
            #add open ____ steamgame maybe open desktoop folder and take a pictgure and analyze the picture to find that specific game?

            #on computer startup open and run 
            #gui to get feedback taskbar icon customtkinter/ add console to ui to debug or let the user know what state its in


        
        
        
        
        
       