from CMDs import executeCMDs



class AI:
    def __init__(self,va,key,client,model,conversation,custom_commands):
        self.va= va
        self.key=key
        self.client=client
        self.model=model
        self.conversation = conversation
        self.custom_commands = custom_commands

    def askAI(self,spoken_text):

        self.conversation.append({"role": "user", "content":spoken_text})  #add the prompt to the conversation history
        
        if len(self.conversation) > 21: # if the conversation history is bigger than 21 (1 system, 10 assistant, 10 user)
            del self.conversation[1:3] # Remove oldest user+assistant pair (keep system message at index 0)


        response = self.client.chat.complete(
            model= self.model,
            messages = self.conversation, #pull the conversation
            temperature=0.5
        )
        reply = response.choices[0].message.content.strip() #generate the reponse
        self.conversation.append({"role": "assistant", "content": reply})
        print(self.conversation)
        return reply


    #this determines if the user is asking a question or giving a command and handles accordingly 
    def determineIntent(self,spoken_text,commands):
        classifyPrompt = f""" 
            determine if the following prompt is a question or a command and respond with strictly one word
            either: "command" or "question"

            Input: "{spoken_text}"
        """
        response = self.client.chat.complete(
            model= self.model,
            messages =[
                {"role": "system", "content": "Classify user input as either a command or a question."},
                {"role": "user", "content": classifyPrompt}
            ]
        )

        if((spoken_text == "") or (spoken_text == " ")):
            self.va.speak("try again")
            return False
        
        intent = response.choices[0].message.content.strip().lower()
        if(intent == "question"):
            convomode = True
            AIresponse = self.askAI(spoken_text)  #response to users question
            self.va.speak(AIresponse)
            while convomode:                            
                self.va.speak("anything else?") 
                followup =self.va.listen_until_heard().lower()
                if followup in ["no", "na", "nah", "nope"]: 
                    self.va.speak("ok exiting convo mode")
                    return False
                
                AIresponse = self.askAI(followup)
                self.va.speak(AIresponse)
        elif(intent == "command"):
            userInput = self.customCommandCheck(spoken_text)
            cmd, args = self.parse_command(userInput)
            executeCMDs(cmd,args,self.va,commands)  
            return False 
        else:
            self.va.speak("error in intent")
            return False


    #checks if any mapped pharases were said and handles them
    def customCommandCheck(self, spoken_text):
        input = spoken_text                     #store og input
        for phrase in self.custom_commands:
            if phrase in input:
                return input.replace(phrase, self.custom_commands[phrase]) #replace the spoken input with customcmd
        return spoken_text #<- if no customcmd was said


    #parses the command for the computer to understand 
    def parse_command(self,text):
        parts = text.strip().split()
        if not parts:
            return "", ""
        return parts[0], " ".join(parts[1:])





























