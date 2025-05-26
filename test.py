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


driver = None  # Initially no browser is open


def getEdgeDriver():
    service = Service("C:\\WebDrivers\\msedgedriver.exe")
    options = Options()
    options.add_argument(r"--user-data-dir=C:\\Users\\tmarv\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Edge(service=service, options=options)
    
    # Hide webdriver flag
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    return driver

#driver = getEdgeDriver()
#
# driver.get("https://accounts.google.com/signin")

#driver.execute_script("window.open('https://example.com', '_blank', 'toolbar=yes,scrollbars=yes,resizable=yes,width=800,height=600');")
#driver.switch_to.window(driver.window_handles[-1])

#driver.get("edge://newtab")  # truly blank tab
#driver.switch_to.window(driver.window_handles[-1])

#driver.execute_script("window.open('https://example.com', '_blank');")

# print(driver.title)
# time.sleep(5)
# driver.quit()


r = sr.Recognizer()         #microphone

#initialize text to speech
engine = pyttsx3.init()   
rate = engine.getProperty('rate')  
engine.setProperty('rate', 150)
volume = engine.getProperty('volume')
engine.setProperty('volume', 1.0)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id) #1 is female 0 is male 



trigger_word = "ai"  # You can change this to anything you want



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


#get the specific chrome profile to launch
# def getChromeDriver():
#     global driver
#     if driver is None:
#         chrome_options = Options()
#         chrome_options.add_argument(r"user-data-dir=C:\\Users\\tmarv\\AppData\\Local\\Google\\Chrome\\User Data")
#         chrome_options.add_argument(r"profile-directory=Profile 3")
#         try:
#             driver = webdriver.Chrome(options=chrome_options)

#         except Exception as e:
#             print("Chrome failed to start:", e)
#             speak("Chrome failed to start.")
#             return None
#     return driver



while True:
    print("Waiting for trigger word...")
    spoken_text = listen()
    
    if trigger_word in spoken_text:
        speak("Hello, what can I do for you?")

        # Keep listening commands until user says 'stop' or 'kill'
        while True:
            command_text = listen()
            print(f"Command: {command_text}")
            command_keyword, argument = parse_command(command_text)

            if command_keyword == "kill yourself" or command_keyword == "stop":
                speak("Goodbye...")
                sys.exit()  # or break this inner loop to listen for trigger again
            
            match command_keyword:
                case "open":
                    domain = argument.replace(" ", "")
                    full_url = f"https://www.{domain}.com/"
                    speak(f"Opening {domain}")
                    browser = getEdgeDriver()
                    if browser:
                        browser.execute_script(f"window.open('{full_url}', '_blank');")
                        browser.switch_to.window(browser.window_handles[-1])

                case "search":
                    speak(f"Searching for {argument}")
                    browser = getEdgeDriver()
                    if browser:
                        browser.execute_script(f"window.open('https://www.google.com/search?q={argument}');")
                        browser.switch_to.window(browser.window_handles[-1])

                # add more cases...

                case _:
                    print("Sorry, I didn’t understand the command.")




        #TO DO
            #make it open new tab if a window is already open (right now it opens a new window everytime)
            #make it keep listening when one comand is completed

            #add a close ___ tab 

            #add a close window 
            #add open new window
            #add open ___ on youtube 
            #add join ____ discord call 
            #add shutdown
            #add open ____ steamgame 
            #add take note (opens a notpad and writes what you say)
            #add question and answer like siri ai 
            #add open spotify app / and play playlist


        #COMPLETED
            #add a someone talking back 
            #add a trigger word
            #add google search
        
        
        
        
        
       