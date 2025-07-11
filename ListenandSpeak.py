import speech_recognition as sr
import pyttsx3









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
    
