import sys

#my imports
import ListenandSpeak
import browserCMDs
import AI


#active = True
on= True
trigger_word = "ai"  # change this to change what the assistant listens for

while on:
    print("Waiting for trigger word...")
    spoken_text = ListenandSpeak.listen()   #anything you say is stored in this var 
    
    if trigger_word in spoken_text:    #if you say the trigger word
        active = True
        ListenandSpeak.speak("Hello")

    
        while active:       #this is when its listening for a actual command

            command_text = ListenandSpeak.listen()
            print(f"Command: {command_text}")
            
            #command_keyword = askAI(command_text)                                                               # this is an issue as of now, the ai responds with a reply not a word FIX THIS
            command_keyword, argument = ListenandSpeak.parse_command(command_text)            #keep incase

            if command_keyword == "stop":
                ListenandSpeak.speak("Goodbye...")
                sys.exit()  # or break this inner loop to listen for trigger again

            match command_keyword:
                
                case "open":                                #Open a specific website 
                    domain = argument.replace(" ", "")
                    full_url = f"https://www.{domain}.com/"
                    ListenandSpeak.speak(f"Opening {domain}")
                    
                    if browser is None:
                        browser = browserCMDs.getEdgeDriver(full_url)   #opens the window the first time straight to the spoken url
                
                    else:
                        browser.execute_script(f"window.open('{full_url}', '_blank');")     #use this when a window is already open. (add new tab)
                        browser.switch_to.window(browser.window_handles[-1])
                    
                    active = False  #stops listening for commands goes back to listening for trigger word

                case "search":                              #search a specific thing on google
                    ListenandSpeak.speak(f"Searching for {argument}")
                    
                    if browser is None:
                        browser = browserCMDs.getEdgeDriver(f'https://www.google.com/search?q={argument}')

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
                        ListenandSpeak.speak(f"No tab matching {tab} found.")

                case "youtube":                             #open a specific channel on youtube
                    ListenandSpeak.speak(f"opening {argument} on youtube")
                    
                    if browser is None:
                        browser = browserCMDs.getEdgeDriver(f'https://www.youtube.com/{argument}')

                    else:
                        browser.execute_script(f"window.open('https://www.youtube.com/{argument}');")
                        browser.switch_to.window(browser.window_handles[-1])
                    
                    active = False  #stops listening for commands goes back to listening for trigger word

                case "recent":                              #open the most recent video from a specific youtube channel

                    if browser is None:
                        channel_url = browserCMDs.get_channel_url(argument)

                        browser = browserCMDs.getEdgeDriver(channel_url)
                        browserCMDs.play_latest_video(channel_url)

                    else:
                        channel_url = browserCMDs.get_channel_url(argument)
                        browser.execute_script(f"window.open('{channel_url}');")
                        browser.switch_to.window(browser.window_handles[-1])
                        browserCMDs.play_latest_video(channel_url)


                    active = False  #stops listening for commands goes back to listening for trigger word

                case "notepad":
                    browserCMDs.open_notepad_and_type()
                    active=False
                # add more cases...

                case "test":
                    ListenandSpeak.speak("What would you like to ask me?")
                    spoken_text = ListenandSpeak.listen()  # from your voice input
                    if spoken_text:
                        answer = AI.askAI(spoken_text)
                        ListenandSpeak.speak(answer)  # TTS it back
                    active = False


                case _:
                    print("Sorry, I didn’t understand the command.")




        #TO DO6

            #add a close window 
            #add open new window



            #add join ____ discord call 
            #add shutdown
            #add open ____ steamgame 

            #add question and answer like siri ai 
            #add open spotify app / and play playlist
            #one computer startup open and run 
            #gui to get feedback taskbar icon


        
        
        
        
        
        
       