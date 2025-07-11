
import ListenandSpeak
from AI import determineIntent



#active = True
on= True
trigger_word = "stewie"  # change this to change what the assistant listens for
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
            #ai acts wonky sometimes when it cant tell if its a question or cmd 
            #ai will say to different things sometimes 
            #convo mode is buggy 
            


        #TO DO

            #add a close window 
            



            #add join ____ discord call 
            #add shutdown
            #add open ____ steamgame 

            #add question and answer like siri ai 
            #add open spotify app / and play playlist
            #one computer startup open and run 
            #gui to get feedback taskbar icon


        
        
        
        
        
        
       