from mistralai import Mistral
from CMDs import executeCMDs
from sharedObj import va
from browserCMDs import parse_command


api_key = "AzgyjA0icarZKB9DyB1aFMNXiwBWkuML"
model = "mistral-small-latest"
client = Mistral(api_key=api_key)

conversation = [ #this holds the conversation history. up to 21 lines (1 system, 10 user, 10 assistant)
    {
        "role": "system",
        "content": (
            "You are a helpful voice assistant for Thomas."
            "Always respond clearly and concisely in 1–2 sentences max. "
            "If you receive a vague command, assume it's related to controlling my computer like: web browsing, searching, or note taking and only say something like 'sure thing'."
            "if the prompt is empty meaning "" or " " then do not say a word"
            "at the end of a question do not say anything like 'have anymore questions' or 'would you like to know more'"
        )
    }
]
def askAI(spoken_text):

    conversation.append({"role": "user", "content":spoken_text})  #add the prompt to the conversation history
    
    if len(conversation) > 21: # if the conversation history is bigger than 21 (1 system, 10 assistant, 10 user)
        del conversation[1:3] # Remove oldest user+assistant pair (keep system message at index 0)


    response = client.chat.complete(
        model= model,
        messages = conversation, #pull the conversation
        temperature=0.5
    )
    reply = response.choices[0].message.content.strip() #generate the reponse
    conversation.append({"role": "assistant", "content": reply})
    print(conversation)
    return reply


def determineIntent(spoken_text):
    classifyPrompt = f""" 
        determine if the following prompt is a question or a command and respond with strictly one word
        either: "command" or "question"

        Input: "{spoken_text}"
    """
    response = client.chat.complete(
        model= model,
        messages =[
            {"role": "system", "content": "Classify user input as either a command or a question."},
            {"role": "user", "content": classifyPrompt}
        ]
    )

    if((spoken_text == "") or (spoken_text == " ")):
        va.speak("try again")
        return False
    
    intent = response.choices[0].message.content.strip().lower()
    if(intent == "question"):
        convomode = True
        AIresponse = askAI(spoken_text)  #response to users question
        va.speak(AIresponse)
        while convomode:                            
            va.speak("anything else?") 
            followup =va.listen_until_heard().lower()
            if followup in ["no", "na", "nah", "nope"]: 
                va.speak("ok exiting convo mode")
                return False
            
            AIresponse = askAI(followup)
            va.speak(AIresponse)
    elif(intent == "command"):
        userInput = customCommandCheck(spoken_text)
        cmd, args = parse_command(userInput)
        executeCMDs(cmd,args)  
        return False 
    else:
        va.speak("error in intent")
        return False


#need to make the program loop through custom to check if custom commadn is said
custom_commands ={   #these phases are custom. if the ai hears any of the left ones it interprets them as the right one
    "pull up": "open",
    "google": "search",
    "show recent": "recent",
    "recent":"recent",
    "take note": "notepad",
    "previous song": "previous",
    "next song": "skip",
    "skip song": "skip",
    "play song": "play",
    "pause song": "pause",
    "play playlist": "playlist",
    "start playlist":"playlist"
    }


def customCommandCheck(spoken_text):
    input = spoken_text                     #store og input
    for phrase in custom_commands:
        if phrase in input:
           return input.replace(phrase, custom_commands[phrase]) #replace the spoken input with customcmd
    return spoken_text #<- if no customcmd was said
