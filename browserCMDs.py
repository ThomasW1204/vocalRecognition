from selenium import webdriver
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.edge.options import Options 
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
import subprocess
import pyautogui
import winsound

from ListenandSpeak import speak, listen




#driver = None  # Initially no browser is open


## browser itself ##
browser = None
def getEdgeDriver(url =None):

    global browser
    if browser is not None:
        return browser


    service = Service("C:/Users/tmarv/Downloads/edgedriver_win64/msedgedriver.exe")
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
####

## cmd handling ##
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



    #parse the spoken command so the computer can understand it



def parse_command(text):
    parts = text.strip().split()
    if not parts:
        return "", ""
    return parts[0], " ".join(parts[1:])