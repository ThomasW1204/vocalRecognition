import speech_recognition as sr
import webbrowser
import pyttsx3
import sys

from selenium import webdriver
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# options = Options()
# options.add_argument(r"user-data-dir=C:\Users\tmarv\AppData\Local\Google\Chrome\User Data")
# options.add_argument(r"profile-directory=Profile 3")

driver = None  # Initially no browser is open


#driver.get('https://www.google.com')

# Open two new tabs
#driver.execute_script("window.open('https://www.youtube.com');")
#driver.execute_script("window.open('https://www.python.org');")

#tabs = driver.window_handles
#print(tabs)  # three tabs total

# Switch to middle tab and close it
#driver.switch_to.window(tabs[1])
#time.sleep(2)
#driver.close()

# Update tabs after closing
#tabs = driver.window_handles
#print(tabs)  # two tabs left

# Switch to first tab again
#driver.switch_to.window(tabs[0])

#time.sleep(100)  # wait and keep browser open so you can see it
# driver.quit()  # Only call this if you want to close whole browser at the end


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
def getChromeDriver():
    global driver
    if driver is None:
        chrome_options = Options()
        chrome_options.add_argument(r"user-data-dir=C:\\Users\\tmarv\\AppData\\Local\\Google\\Chrome\\User Data")
        chrome_options.add_argument(r"profile-directory=Profile 3")
        try:
            driver = webdriver.Chrome(options=chrome_options)

        except Exception as e:
            print("Chrome failed to start:", e)
            speak("Chrome failed to start.")
            return None
    return driver



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

            if command_keyword == "kill" or command_keyword == "stop":
                speak("Goodbye...")
                sys.exit()  # or break this inner loop to listen for trigger again
            
            match command_keyword:
                case "open":
                    domain = argument.replace(" ", "")
                    full_url = f"https://www.{domain}.com/"
                    speak(f"Opening {domain}")
                    browser = getChromeDriver()
                    if browser:
                        browser.execute_script(f"window.open('{full_url}', '_blank');")
                        browser.switch_to.window(browser.window_handles[-1])

                case "search":
                    speak(f"Searching for {argument}")
                    browser = getChromeDriver()
                    if browser:
                        browser.execute_script(f"window.open('https://www.google.com/search?q={argument}');")
                        browser.switch_to.window(browser.window_handles[-1])

                # add more cases...

                case _:
                    print("Sorry, I didn’t understand the command.")


# while True: 
#      print("Waiting for trigger word...")
#      spoken_text = listen()                          #listen for triggerword

#      if trigger_word in spoken_text:                 #if triggerword is said 
#          speak("Hello, what can I do for you?")
#          command_text = listen() #get the command
#          print(f"Command: {command_text}")
#          command_keyword, argument  = parse_command(command_text) #fix the text to something usable

#          match command_keyword:
#             case "open":
#                 domain = argument.replace(" ", "")
#                 full_url = f"https://www.{domain}.com/"

#                 speak(f"Opening {domain}")
#                 browser = getChromeDriver()
#                 if browser:
#                         browser.switch_to.new_window('tab')
#                         browser.get(full_url)

#             case "kill":
#                 speak("Goodbye...")
#                 sys.exit()

#             case "play":
#                 speak(f"Playing {argument}")
#                 # Add play logic here

#             case "search":
#                 speak(f"Searching for {argument}")
#                 browser = getChromeDriver()
#                 if browser:
#                     browser.execute_script(f"window.open('https://www.google.com/search?q={argument}', '_blank');")
#                     browser.switch_to.window(browser.window_handles[-1])

#             case "new":
#                 browser = getChromeDriver()
#                 if browser:
#                     browser.execute_script(f"window.open('https://www.google.com/search?q={argument}', '_blank');")
#                     browser.switch_to.window(browser.window_handles[-1])           
            
#             case _:
#                  speak("Sorry, I didn’t understand the command.")





        #TO DO
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
        
        
        
        
        
       