import speech_recognition as sr
import pyttsx3


class ListenandSpeak:
    def __init__(self, rate=150, volume=1.0, voice_index=1):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        
        # Configure TTS engine
        self.engine.setProperty('rate', rate)
        self.engine.setProperty('volume', volume)
        voices = self.engine.getProperty('voices')
        if voice_index < len(voices):
            self.engine.setProperty('voice', voices[voice_index].id)

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self, prompt=None, return_empty=True):
        with sr.Microphone() as source:
            self.recognizer.pause_threshold = 2
            self.recognizer.energy_threshold = 1
            if prompt:
                self.speak(prompt)
            print("Listening...")
            audio = self.recognizer.listen(source)

        try:
            text = self.recognizer.recognize_google(audio).lower()
            return text
        except sr.UnknownValueError:
            return "" if return_empty else None
        except sr.RequestError:
            self.speak("Sorry, I'm having trouble connecting.")
            return None

    def listen_until_heard(self, first=None):
        with sr.Microphone() as source:
            if first:
                self.speak("whats up")

            print("Listening continuously...")
            while True:
                try:
                    audio = self.recognizer.listen(source)
                    text = self.recognizer.recognize_google(audio).lower()
                    if text.strip():
                        print(f"Heard: {text}")
                        return text
                except sr.UnknownValueError:
                    print("Didn't catch that. Still listening...")
                except sr.RequestError as e:
                    print(f"API error: {e}")
                    break
        return None   































'''
r = sr.Recognizer()         #microphone

#initialize text to speech
engine = pyttsx3.init()   
rate = engine.getProperty('rate')  
engine.setProperty('rate', 150)
volume = engine.getProperty('volume')
engine.setProperty('volume', 1.0)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id) #1 is female 0 is male 




#text to speech
def speak(text):
    engine.say(text)
    engine.runAndWait()


#listen to all audio will stop running when trigger word is said
def listen(first=False):
    with sr.Microphone() as source:
        r.pause_threshold = 2  # Wait for 1 seconds of silence before ending
        r.energy_threshold = 1 
        if (first):
            speak("whats up")
        print("listening...")
        audio = r.listen(source)
    try:
        return r.recognize_google(audio).lower()  #return the spoken word
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        speak("Sorry, I'm having trouble connecting.")
        return ""
    


def listen_until_heard(first=False):
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        
        while True:
            if(first):
                speak("whats up")
            try:
                audio = recognizer.listen(source, timeout=None, phrase_time_limit=None)
                text = recognizer.recognize_google(audio)
                
                if text.strip():  # Only break if we actually got something
                    print(f"Heard: {text}")
                    return text.lower()

            except sr.UnknownValueError:
                # Didn't understand, keep listening
                print("Didn't catch that. Still listening...")

            except sr.RequestError as e:
                print(f"API error: {e}")
                break
    

def SpeakandListen(text):
    spoken = listen()
    print("Waiting for cmd")
    engine.say(text)
    engine.runAndWait()
    return spoken


'''