import os
import subprocess
import sys
import time

import pyautogui

#executes given command from keyword and argument (ex: open youtube)
def executeCMDs(command_keyword,argument,va,commands):
    if ((command_keyword == "stop") | (command_keyword == "exit")):
        va.speak("Goodbye...")
        sys.exit()  # or break this inner loop to listen for trigger again
    try:
        match command_keyword:
            case "open":                                #Open a specific website 
                domain = argument.replace(" ", "")
                full_url = f"https://www.{domain}.com/"
                va.speak(f"Opening {domain}")
                
                start = time.time()
                if commands.browser is None:
                    browser = commands.getFirefoxDriver(full_url)
                    browser.maximize_window()
                else:
                    browser = commands.getFirefoxDriver()
                    browser.execute_script(f"window.open('{full_url}', '_blank');")     #use this when a window is already open. (add new tab)
                    browser.maximize_window()

                    browser.switch_to.window(browser.window_handles[-1])
                end = time.time()
                print(f"Elapsed time: {end - start:.6f} seconds")

            case "search":                              #search a specific thing on google
                va.speak(f"Searching for {argument}")

                
                if commands.browser is None:
                    browser = commands.getFirefoxDriver(f'https://www.duckduckgo.com/search?q={argument}')
                else:
                    browser = commands.getFirefoxDriver()
                    browser.execute_script(f"window.open('https://www.duckduckgo.com/search?q={argument}');")
                    browser.switch_to.window(browser.window_handles[-1])
                

            case "close":                               #close a specific tab
                browser = commands.getFirefoxDriver()  # browser always initialized
            
                tab = argument.lower()
                va.speak(f"closing {tab}")
            
                for handle in browser.window_handles:   #loop through the unique tab strings from selenium
                    browser.switch_to.window(handle)    #points a tab the loop looks at. doesn't switch
                    if tab in browser.title.lower() or tab in browser.current_url.lower():  # check if the spoken tab is in the list
                        browser.close()
                        
                        if browser.window_handles:  # Only switch if there are tabs left
                            browser.switch_to.window(browser.window_handles[0])     #switch to first tab

                        break
                else:
                    va.speak(f"No tab matching {tab} found.")
                

            case "youtube":                             #open a specific channel on youtube
                domain = argument.replace(" ", "")
                full_url = f"https://www.youtube.com/{domain}"
                va.speak(f"Opening {domain} on YouTube")

                if commands.browser is None:
                    browser = commands.getFirefoxDriver(full_url)
                else:
                    browser = commands.getFirefoxDriver()
                    browser.execute_script(f"window.open('{full_url}', '_blank');")
                    browser.switch_to.window(browser.window_handles[-1])


            case "recent":                              #open the most recent video from a specific youtube channel                                   BROKEN

                channel_url = commands.get_channel_url(argument)
                va.speak(f"Opening the latest video from {argument}")

                if commands.browser is None:
                    browser = commands.getFirefoxDriver(channel_url)
                else:
                    browser = commands.getFirefoxDriver()
                    browser.execute_script(f"window.open('{channel_url}', '_blank');")
                    browser.switch_to.window(browser.window_handles[-1])

                commands.play_latest_video(channel_url)


            case "notepad":                             #A little wonky with opening a new notepad and saving if its already saved. need fix
                commands.open_notepad_and_type()


            case "skip":                                #skip song
                va.speak("skipping")
                commands.skipSong()


            case "previous":                            #previous song
                va.speak("back")
                commands.prevSong()
            

            case "pause":                               #pause song
                va.speak("pausing")
                commands.playorpause()


            case "play":                                #play song
                va.speak("playing")
                commands.playorpause()


            case "playlist":                            #play a specific playlist (a little wonky)
                    commands.spotifyplaylist(argument)


            case _:
                from main import triggered  # Local import avoids circular issue
                va.speak("Sorry try again")
                triggered()
                print("Sorry, I didn’t understand the command.")
    except Exception as e:
        from main import start
        print("something went wrong with the command:", e) 
        start()
