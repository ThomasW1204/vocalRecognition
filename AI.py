from mistralai import Mistral
from CMDs import executeCMDs
from ListenandSpeak import speak
from browserCMDs import parse_command

'''
    This file needs to determine if what the user said was a ? or a command

    if(?){
    ai response 2-3 senteces and leave the "call" open so i can ask more untill "end" is said
    use a flag to determine if in conversation mode ex: conversation_mode = true 
    }


    if(cmd or custom phrase){
        translate the spoken/cmd text to cmd and move it back to main for processing
    }



'''

api_key = "AzgyjA0icarZKB9DyB1aFMNXiwBWkuML"
model = "mistral-small-latest"
client = Mistral(api_key=api_key)


conversation = [ #this holds the conversation history. up to 21 lines (1 system, 10 user, 10 assistant)
    {
        "role": "system",
        "content": (
            "You are a helpful voice assistant for Thomas."
            "Always respond clearly and concisely in 1–2 sentences max. "
            "If you receive a vague command, assume it's related to controlling my computer like: web browsing, searching, or note taking and say something like 'sure thing'."
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
        determine if the folling prompt is a question or a command and respond with one word
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
    
    intent = response.choices[0].message.content.strip().lower()
    conversationMode = False
    if(intent == "question"):
        conversationMode = True
        AIresponse = askAI(spoken_text)  #fix this to speak and have a flag 
        speak(AIresponse) 
        return conversationMode
    elif(intent == "command"):
        conversationMode = False
        userInput = customCommandCheck(spoken_text)
        cmd, args = parse_command(userInput)
        executeCMDs(cmd,args)   
        return conversationMode                       
    else:
        speak("error in intent")
        return False


'''
def askAI(spoken_text):

    mapped_input = customCommandCheck(spoken_text) #check for custom phrase

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
   # print(conversation)
    return reply
'''



#need to make the program loop through custom to check if custom commadn is said
custom_commands ={   #these phases are custom. if the ai hears any of the left ones it interprets them as the right one
    "pull up": "open",
    "google": "search"
}


def customCommandCheck(spoken_text):
    input = spoken_text                     #store og input
    for phrase in custom_commands:
        if phrase in input:
           return input.replace(phrase, custom_commands[phrase]) #replace the spoken input with customcmd
    return spoken_text #<- if no customcmd was said
