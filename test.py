import speech_recognition as sr
import webbrowser
import pyttsx3
import sys

from selenium import webdriver
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium import webdriver
from selenium.webdriver.edge.options import Options 
from selenium.webdriver.edge.service import Service
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import subprocess
import pyautogui
import winsound

import requests
import os
from mistralai import Mistral

api_key = "AzgyjA0icarZKB9DyB1aFMNXiwBWkuML"
model = "mistral-small-latest"
client = Mistral(api_key=api_key)


conversation = [ #this holds the conversation history. up to 21 lines (1 system, 10 user, 10 assistant)
    {
        "role": "system",
        "content": (
            "You are a helpful voice assistant for Thomas."
            "Always respond clearly and concisely in 1–2 sentences max. "
            "If you receive a vague command, assume it's related to web browsing, searching, or note taking."
        )
    }
]


#need to make the program loop through custom to check if custom commadn is said
custom_commands ={   #these phases are custom. if the ai hears any of the left ones it interprets them as the right one
    "pull up": "open",
    "google": "search"
}

def customCommandCheck(user_input):
    for phrase in custom_commands:
        if phrase in spoken_text:
            return spoken_text.replace(phrase, custom_commands[phrase])
    return user_input

def askAI(spoken_text):

    mapped_input = customCommandCheck(spoken_text) #check for custom phrase

    conversation.append({"role": "user", "content":spoken_text})  #add the prompt to the conversation history
    
    if len(conversation) > 21: # if the conversation history is bigger than 21 (1 system, 10 assistant, 10 user)
        del conversation[1:3] # Remove oldest user+assistant pair (keep system message at index 0)


    response = client.chat.complete(
        model= model,
        messages = conversation, #pull the conversation
        temperature=0.5
    )
    reply = response.choices[0].message.content.strip() #generate the reponse
    conversation.append({"role": "assistant", "content": reply})
    print(conversation)
    return reply





#driver = None  # Initially no browser is open

browser = None



def getEdgeDriver(url =None):

    global browser
    if browser is not None:
        return browser


    service = Service("C:\\WebDrivers\\msedgedriver.exe")
    options = Options()
    options.add_argument(r"--user-data-dir=C:\\Users\\tmarv\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("start-maximized")

    browser = webdriver.Edge(service=service, options=options)
    
    # Hide webdriver flag
    browser.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    if(url):
        browser.get(url)
    
    return browser



r = sr.Recognizer()         #microphone

#initialize text to speech
engine = pyttsx3.init()   
rate = engine.getProperty('rate')  
engine.setProperty('rate', 150)
volume = engine.getProperty('volume')
engine.setProperty('volume', 1.0)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id) #1 is female 0 is male 



trigger_word = "ai"  # change this to change what the assistant listens for



#text to speech
def speak(text):
    engine.say(text)
    engine.runAndWait()


#listen to all audio will stop running when trigger word is said
def listen():
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
    try:
        return r.recognize_google(audio).lower()  #return the spoken word
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        speak("Sorry, I'm having trouble connecting.")
        return ""
    

#parse the spoken command so the computer can understand it
def parse_command(text):
    parts = text.strip().split()
    if not parts:
        return "", ""
    return parts[0], " ".join(parts[1:])




def play_latest_video(channel_url):
    browser.get(f"{channel_url}/videos")  # go directly to the Videos tab
    time.sleep(3)  # let it load

    try:
        # Find and click the first video
        first_video = browser.find_element(By.ID, "video-title")
        first_video.click()
        print("Playing newest video.")
    except Exception as e:
        print("Failed to find or click the video:", e)

def get_channel_url(channel_name):
    global browser

    search_url = f"https://www.youtube.com/results?search_query={channel_name}&sp=EgIQAg%253D%253D"  
    # `sp=EgIQAg%253D%253D` filters for Channels only

    if browser is None:
        browser = getEdgeDriver()

    browser.get(search_url)
    time.sleep(3)  # wait for page to load

    try:
        # Look for a channel link under the search result
        channel_element = browser.find_element(By.XPATH, "//a[@href and contains(@href, '/@')]")
        href = channel_element.get_attribute("href")
        return href
    except Exception as e:
        print("Could not find a channel URL:", e)
        return None

def open_notepad_and_type():
    r=True
    subprocess.Popen("notepad.exe")
    time.sleep(1)  

    speak("What do you want me to type? on beep, say something")

    while r:
        winsound.Beep(800, 20)
        spoken_text = listen()
    # Open Notepad
       
        print(f"Typing: {spoken_text}")
        
        if spoken_text == "close":
            speak("ending notes")
            r = False
            save_and_close_notepad()
        elif spoken_text == "new line":
            pyautogui.press('enter')
            speak("New Line")
        else:
            pyautogui.write(spoken_text, interval=0.05)  # types with small delay between keys
            pyautogui.press("space")

       


def save_and_close_notepad():
    # Save (Ctrl + S)
    pyautogui.hotkey('ctrl', 's')
    time.sleep(1)  # wait for the save dialog to open
    j = True
    while j:
        speak("what do you want to name the file")
        spoken_text = listen()
        pyautogui.write(spoken_text, interval=0.05)
        speak("is" + spoken_text + "correct?")
        ans = listen()
       
        if ans == "yes":
            j=False
            pyautogui.press('enter')
            time.sleep(1)
            pyautogui.hotkey('alt', 'f4')
        else:
            continue




    time.sleep(0.5)
    
    # Press Enter to confirm save
   




#active = True
on= True

while on:
    print("Waiting for trigger word...")
    spoken_text = listen()   #anything you say is stored in this var 
    
    if trigger_word in spoken_text:    #if you say the trigger word
        active = True
        speak("Hello")

    
        while active:       #this is when its listening for a actual command

            command_text = listen()
            print(f"Command: {command_text}")
            
            command_keyword = askAI(command_text)                                                               # this is an issue as of now, the ai responds with a reply not a word FIX THIS
            #command_keyword, argument = parse_command(command_text)            #keep incase

            if command_keyword == "stop":
                speak("Goodbye...")
                sys.exit()  # or break this inner loop to listen for trigger again

            match command_keyword:
                
                case "open":                                #Open a specific website 
                    domain = argument.replace(" ", "")
                    full_url = f"https://www.{domain}.com/"
                    speak(f"Opening {domain}")
                    
                    if browser is None:
                        browser = getEdgeDriver(full_url)   #opens the window the first time straight to the spoken url
                
                    else:
                        browser.execute_script(f"window.open('{full_url}', '_blank');")     #use this when a window is already open. (add new tab)
                        browser.switch_to.window(browser.window_handles[-1])
                    
                    active = False  #stops listening for commands goes back to listening for trigger word

                case "search":                              #search a specific thing on google
                    speak(f"Searching for {argument}")
                    
                    if browser is None:
                        browser = getEdgeDriver(f'https://www.google.com/search?q={argument}')

                    else:
                        browser.execute_script(f"window.open('https://www.google.com/search?q={argument}');")
                        browser.switch_to.window(browser.window_handles[-1])
                    
                    active = False  #stops listening for commands goes back to listening for trigger word


                case "close":                               #close a specific tab
                    
                    tab = argument.lower()
                    
                    for handle in browser.window_handles:   #loop through the unique tab strings from selenium
                        browser.switch_to.window(handle)    #points a tab the loop looks at. doesn't switch
                        if tab in browser.title.lower() or tab in browser.current_url.lower():  # check if the spoken tab is in the list
                            browser.close()
                            browser.switch_to.window(browser.window_handles[0])     #switch to first tab
                            break
                    else:
                        speak(f"No tab matching {tab} found.")

                case "youtube":                             #open a specific channel on youtube
                    speak(f"opening {argument} on youtube")
                    
                    if browser is None:
                        browser = getEdgeDriver(f'https://www.youtube.com/{argument}')

                    else:
                        browser.execute_script(f"window.open('https://www.youtube.com/{argument}');")
                        browser.switch_to.window(browser.window_handles[-1])
                    
                    active = False  #stops listening for commands goes back to listening for trigger word

                case "recent":                              #open the most recent video from a specific youtube channel

                    if browser is None:
                        channel_url = get_channel_url(argument)

                        browser = getEdgeDriver(channel_url)
                        play_latest_video(channel_url)

                    else:
                        channel_url = get_channel_url(argument)
                        browser.execute_script(f"window.open('{channel_url}');")
                        browser.switch_to.window(browser.window_handles[-1])
                        play_latest_video(channel_url)


                    active = False  #stops listening for commands goes back to listening for trigger word

                case "notepad":
                    open_notepad_and_type()
                    active=False
                # add more cases...

                case "test":
                    speak("What would you like to ask me?")
                    spoken_text = listen()  # from your voice input
                    if spoken_text:
                        answer = askAI(spoken_text)
                        speak(answer)  # TTS it back
                    active = False


                case _:
                    print("Sorry, I didn’t understand the command.")




        #TO DO

            #add a close window 
            #add open new window



            #add join ____ discord call 
            #add shutdown
            #add open ____ steamgame 

            #add question and answer like siri ai 
            #add open spotify app / and play playlist
            #one computer startup open and run 
            #gui to get feedback taskbar icon


        
        
        
        
        
        
       