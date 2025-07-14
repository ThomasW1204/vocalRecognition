import sys


import ListenandSpeak
import browserCMDs


def executeCMDs(command_keyword,argument):
    if command_keyword == "stop":
        ListenandSpeak.speak("Goodbye...")
        sys.exit()  # or break this inner loop to listen for trigger again

    match command_keyword:
        case "open":                                #Open a specific website 
            domain = argument.replace(" ", "")
            full_url = f"https://www.{domain}.com/"
            ListenandSpeak.speak(f"Opening {domain}")
            if browserCMDs.browser is None:
                browser = browserCMDs.getEdgeDriver(full_url)
            else:
                browser = browserCMDs.getEdgeDriver()
                browser.execute_script(f"window.open('{full_url}', '_blank');")     #use this when a window is already open. (add new tab)
                browser.switch_to.window(browser.window_handles[-1])
            

        case "search":                              #search a specific thing on google
            ListenandSpeak.speak(f"Searching for {argument}")

            
            if browserCMDs.browser is None:
                browser = browserCMDs.getEdgeDriver(f'https://www.google.com/search?q={argument}')
            else:
                browser = browserCMDs.getEdgeDriver()
                browser.execute_script(f"window.open('https://www.google.com/search?q={argument}');")
                browser.switch_to.window(browser.window_handles[-1])
            

        case "close":                               #close a specific tab
            browser = browserCMDs.getEdgeDriver()  # browser always initialized
           
            tab = argument.lower()
            ListenandSpeak.speak(f"closing {tab}")
           
            for handle in browser.window_handles:   #loop through the unique tab strings from selenium
                browser.switch_to.window(handle)    #points a tab the loop looks at. doesn't switch
                if tab in browser.title.lower() or tab in browser.current_url.lower():  # check if the spoken tab is in the list
                    browser.close()
                    
                    if browser.window_handles:  # Only switch if there are tabs left
                        browser.switch_to.window(browser.window_handles[0])     #switch to first tab

                    break
            else:
                ListenandSpeak.speak(f"No tab matching {tab} found.")
            

        case "youtube":                             #open a specific channel on youtube
            domain = argument.replace(" ", "")
            full_url = f"https://www.youtube.com/{domain}"
            ListenandSpeak.speak(f"Opening {domain} on YouTube")

            if browserCMDs.browser is None:
                browser = browserCMDs.getEdgeDriver(full_url)
            else:
                browser = browserCMDs.getEdgeDriver()
                browser.execute_script(f"window.open('{full_url}', '_blank');")
                browser.switch_to.window(browser.window_handles[-1])


        case "recent":                              #open the most recent video from a specific youtube channel STILL ISSUE

            channel_url = browserCMDs.get_channel_url(argument)
            ListenandSpeak.speak(f"Opening the latest video from {argument}")

            if browserCMDs.browser is None:
                browser = browserCMDs.getEdgeDriver(channel_url)
            else:
                browser = browserCMDs.getEdgeDriver()
                browser.execute_script(f"window.open('{channel_url}', '_blank');")
                browser.switch_to.window(browser.window_handles[-1])

            browserCMDs.play_latest_video(channel_url)


        case "notepad":                             #A little wonky with opening a new notepad and saving if its already saved. need fix
            browserCMDs.open_notepad_and_type()


        case "skip":                                #skip song
            ListenandSpeak.speak("skipping")
            browserCMDs.skipSong()


        case "previous":                            #previous song
            ListenandSpeak.speak("back")
            browserCMDs.prevSong()
        

        case "pause":                               #pause song
            ListenandSpeak.speak("pausing")
            browserCMDs.playorpause()


        case "play":                                #play song
            ListenandSpeak.speak("playing")
            browserCMDs.playorpause()


        case "playlist":                            #play a specific playlist (a little wonky)
                browserCMDs.spotifyplaylist(argument)


        case _:
            ListenandSpeak.speak("Sorry try again")
            print("Sorry, I didn’t understand the command.")

