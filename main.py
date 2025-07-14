


import ListenandSpeak
from AI import determineIntent



#active = True
on= True
trigger_word = "ai"  # change this to change what the assistant listens for
def start():
    while on:
        print("Waiting for trigger word...")
        spoken_text = ListenandSpeak.listen()   #anything you say is stored in this var 
    
        if trigger_word in spoken_text:    #if you say the trigger word
            active = True
            ListenandSpeak.speak("Whats up?")

    
            while active:       #this is when its listening for a actual command
                command_text = ListenandSpeak.listen()
                print(f"Command: {command_text}")

                conversationMode = determineIntent(command_text)        #this will determine the intent of the user and either execute cmd or answer the user question

                if not conversationMode:   #this might error 
                    active = False


start()

        #fixes needed
             
            #somehow make it run/listen faster 
            #"recent" isn't working right 
            #"notepad" not working right  (saving and new tab)

        #TO DO
            #add a close window 
            #make a json of history and store it somewhere. maybe sqldb
            #have a ui overlay that i can pop out and type to the ai (maybe make it a keybind to pop out) customtkinter

            #add join ____ discord call 
            #add shutdown
            #add open ____ steamgame 

            #on computer startup open and run 
            #gui to get feedback taskbar icon customtkinter


        
        
        
        
        
       