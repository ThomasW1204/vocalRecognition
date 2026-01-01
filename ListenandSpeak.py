import speech_recognition as sr
import pyttsx3


class ListenandSpeak:
    def __init__(self,ui, rate=150, volume=1.0, voice_index=1):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.ui = ui
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
            self.ui.log("Listening")
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
                        self.ui.log(f"Heard: {text}")
                        return text
                except sr.UnknownValueError:
                    print("Didn't catch that. Still listening...")
                    self.ui.log("Didn't catch that. Still listening...")
                except sr.RequestError as e:
                    print(f"API error: {e}")
                    break
        return None   























