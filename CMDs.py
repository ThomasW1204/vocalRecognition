import sys

import ListenandSpeak
import browserCMDs





def executeCMDs(command_keyword,argument):
    browser = browserCMDs.getEdgeDriver()
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
            

        case "search":                              #search a specific thing on google
            ListenandSpeak.speak(f"Searching for {argument}")

            if browser is None:
                browser = browserCMDs.getEdgeDriver(f'https://www.google.com/search?q={argument}')

            else:
                browser.execute_script(f"window.open('https://www.google.com/search?q={argument}');")
                browser.switch_to.window(browser.window_handles[-1])
            



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



        case "notepad":
            browserCMDs.open_notepad_and_type()

       # case "test":
       #     ListenandSpeak.speak("What would you like to ask me?")
       #     spoken_text = ListenandSpeak.listen()  # from your voice input
       #     if spoken_text:
        #        answer = AI.askAI(spoken_text)
        #        ListenandSpeak.speak(answer)  # TTS it back

        #    main.start() # go back to listening for trigger

        case _:
            print("Sorry, I didn’t understand the command.")

