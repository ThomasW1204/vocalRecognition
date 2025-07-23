from selenium import webdriver
import time
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.firefox import GeckoDriverManager
import subprocess
import pyautogui
import winsound


class browserCMDs:
    def __init__(self,va):
        self.va = va
        self.browser = None


    def getFirefoxDriver(self,url=None):
        if self.browser is not None:
            try:
                _ = self.browser.title
            except:
                self.browser.quit()
                self.browser = None

        options = FirefoxOptions()
        options.add_argument("--start-maximized")
        options.set_preference("toolkit.cosmeticAnimations.enabled", False)
        options.set_preference("browser.aboutConfig.showWarning", False)
        options.set_preference("browser.tabs.animate", False)
        options.profile = r"C:\Users\tmarv\AppData\Roaming\Mozilla\Firefox\Profiles\xau9cu1y.tom"

        service = FirefoxService(GeckoDriverManager().install())
        self.browser = webdriver.Firefox(service=service, options=options)

        if url:
            self.browser.get(url)

        return self.browser


    def get_channel_url(self, channel_name):
        search_url = f"https://www.youtube.com/results?search_query={channel_name}&sp=EgIQAg%253D%253D"
        self.browser.get(search_url)
        time.sleep(3)
        try:
            channel_element = self.browser.find_element(By.XPATH, "//a[@href and contains(@href, '/@')]")
            return channel_element.get_attribute("href")
        except Exception as e:
            print("Could not find a channel URL:", e)
            return None


    def play_latest_video(self, channel_url):
        self.browser.get(f"{channel_url}/videos")
        time.sleep(3)
        try:
            first_video = self.browser.find_element(By.ID, "video-title")
            first_video.click()
        except Exception as e:
            print("Failed to find video:", e)


    def open_notepad_and_type(self):
        subprocess.Popen("notepad.exe")
        time.sleep(1)
        self.va.speak("What do you want me to type?")

        while True:
            winsound.Beep(800, 20)
            text = self.va.listen()
            if text == "close":
                self.va.speak("Ending notes")
                self.save_and_close_notepad()
                break
            elif text == "new line":
                pyautogui.press("enter")
                self.va.speak("New Line")
            else:
                pyautogui.write(text, interval=0.05)
                pyautogui.press("space")


    def save_and_close_notepad(self):
        pyautogui.hotkey("ctrl", "s")
        time.sleep(1)
        while True:
            self.va.speak("What do you want to name the file?")
            name = self.va.listen()
            pyautogui.write(name)
            self.va.speak(f"Is '{name}' correct?")
            confirm = self.va.listen()
            if confirm.lower() == "yes":
                pyautogui.press("enter")
                time.sleep(1)
                pyautogui.hotkey("alt", "f4")
                break
    
    
    def skip_song(self):
        pyautogui.press("nexttrack")


    def prev_song(self):
        pyautogui.press("prevtrack")


    def playorpause(self):
        pyautogui.press("playpause")


    def spotifyplaylist(self, name):
        playlists = {
            "metal": "spotify:playlist:1hJrMsHwyS4TZYHz0j2kJ0?",
            "undertale": "spotify:playlist:2cTmuzWov9agKMHEIge9VY?",
            "delta": "spotify:playlist:2cTmuzWov9agKMHEIge9VY?",
            "jpop": "spotify:playlist:58eCqe3T6U3MWnjAJVaZJw?",
            "rap": "spotify:playlist:2hpSzh9vncqlHjpK4Gfv1T?",
            "classic": "spotify:playlist:1CnsAs7lsk0EEOQNvchbD0?",
            "rock": "spotify:playlist:0CqbH8jnHkWsuUugLlwbiI?"
        }
        uri = playlists.get(name)
        if uri:
            subprocess.Popen(["spotify", uri])
            self.va.speak(f"Opening {name} playlist")
            time.sleep(3)  # Give time for Spotify to load the playlist
            pyautogui.press('tab')
            pyautogui.press('tab')
            pyautogui.press('tab')
            pyautogui.press('tab')
            pyautogui.press('enter')
            pyautogui.hotkey('win', 'down')
            pyautogui.hotkey('win', 'down')
        else:
            self.va.speak(f"Playlist {name} not found.")        

   






#driver = None  # Initially no browser is open


##  edge browser itself ##
'''
browser = None
def getEdgeDriver(url=None):
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
    '''
####


'''
browser = None
def getFirefoxDriver(url=None):
    global browser
    
    # If browser was previously closed, reset it
    if browser is not None:
        try:
            browser.title  # Try accessing to check if it's alive
        except:
            browser.quit()
            browser = None

    options = FirefoxOptions()
    options.add_argument("--start-maximized")
    options.set_preference("toolkit.cosmeticAnimations.enabled", False)
    options.set_preference("browser.aboutConfig.showWarning", False)
    options.set_preference("browser.tabs.animate", False)

    service = FirefoxService(GeckoDriverManager().install())  # Auto installs geckodriver
    browser = webdriver.Firefox(service=service, options=options)

    if url:
        browser.get(url)

    return browser








## parse the cmd to a cmd and an argument##
def parse_command(text):
    parts = text.strip().split()
    if not parts:
        return "", ""
    return parts[0], " ".join(parts[1:])




def play_latest_video(channel_url):                                                             #STILL AN ISSUE
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
        browser = getFirefoxDriver()

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

    va.speak("What do you want me to type? on beep, say something")

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



def skipSong():
    pyautogui.press('nexttrack')


def prevSong():
    pyautogui.press('prevtrack')


def playorpause():    
    pyautogui.press('playpause')


playlists = {
        "metal":"spotify:playlist:1hJrMsHwyS4TZYHz0j2kJ0?",
        "undertale":"spotify:playlist:2cTmuzWov9agKMHEIge9VY?",
        "delta":"spotify:playlist:2cTmuzWov9agKMHEIge9VY?",
        "jpop":"spotify:playlist:58eCqe3T6U3MWnjAJVaZJw?",
        "rap":"spotify:playlist:2hpSzh9vncqlHjpK4Gfv1T?",
        "classic":"spotify:playlist:1CnsAs7lsk0EEOQNvchbD0?",
        "rock":"spotify:playlist:0CqbH8jnHkWsuUugLlwbiI?"

    }


def spotifyplaylist(name):
    uri = playlists.get(name.lower())
    if uri:
        subprocess.Popen(["start", uri], shell=True)
        speak(f"Opening {name} playlist on Spotify")

        time.sleep(3)  # Give time for Spotify to load the playlist
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.press('enter')
        pyautogui.hotkey('win', 'down')
        pyautogui.hotkey('win', 'down')

    else:
        speak("Sorry, I couldn't find that playlist.")   

'''






#for starting a steam game may have to map the specifc games to steam ids to implement. unless i can figure out how to do it dinamycally



