import json
import logging
import os
from ollama import chat
from ollama import ChatResponse
import ollama

class Harness():
    #https://docs.ollama.com/api#generate-a-completion
    def __init__(self, model):
        self.model = self.updateModel(model) # (required) the model name
        self.role = 'user' # the role of the message, either system, user, assistant, or tool
        self.prompt = None #the prompt to generate a response for
        self.suffix = None # the text after the model response
        self.images = None # (optional) a list of base64-encoded images (for multimodal models such as llava)
        self.tool_calls = None # (optional): a list of tools in JSON that the model wants to use
        
        #self.tools = None
        self.format = None # the format to return a response in. Format can be json or a JSON schema
        self.options = None # additional model parameters listed in the documentation for the Modelfile such as temperature
        self.system = None # system message to (overrides what is defined in the Modelfile)
        self.template = None # the prompt template to use (overrides what is defined in the Modelfile)
        self.stream = False # if false the response will be returned as a single response object, rather than a stream of objects
        self.raw = False #  if true no formatting will be applied to the prompt. You may choose to use the raw parameter if you are specifying a full templated prompt in your request to the API
        self.keepAlive = '5m' # controls how long the model will stay loaded into memory following the request (default: 5m)
        self.context = [] #  (deprecated): the context parameter returned from a previous request to /generate, this can be used to keep a short conversational memory
                
        self.response = None

    def generateResponse(self):
        #Generates a response if a valid model is loaded
        if self.model != None:
            response: ChatResponse = chat(model=self.model, messages=[
                {
                    'role': self.role,
                    'content': self.prompt,
                    'images': self.images,
                    'tool_calls': self.tool_calls,
                    #'tools': self.tools, # ollama._types.ResponseError: registry.ollama.ai/library/gemma3:latest does not support tools (status code: 400)
                    'format': self.format,
                    'options': self.options,
                    'system': self.system,
                    'template': self.template,
                    'stream': self.stream, 
                    'raw': self.raw,
                    'keep_alive': self.keepAlive,       
                    'context': self.context 
                },
            ],)
            self.response = response
            
    def updateModel(self, model='None'):
        #Attempts to establish a connection with models
        try:
            ollama.chat(model)
            return model
        except ollama.ResponseError as e:
            print('Error:', e.error)
            if e.status_code == 404:
                try:
                    ollama.pull(model)
                    return model
                except ollama.ResponseError as e:
                    print('Error:', e.error)
        return None
    
    def updateContent(self, prompt):
        #If prompt is a str update Prompt
        if type(prompt) == str:
            self.prompt = prompt
            return prompt
        return None
    
    def updateImages(self, Images):
        #Checks if Images is in a list and all elements area string, then updates object
        if type(Images) == list:
            for image in Images:
                if type(image) != str:
                    return None
        self.images = Images
            
    """def updateTools(self, file_path):
        return self.loadJsonFile(file_path)"""
        
    def updateFormat(self, file_path):
        #Updates Format
        if self.loadJsonFile(file_path):
            self.format = file_path
            return file_path
        return None
    
    def updateOptions(self, file_path):
        #Updates Options
        if self.loadJsonFile(file_path):
            self.options = file_path
            return file_path
        return None
        
    def updateSystem(self, Instruction):
        #Checks if System is in a valid format and updates object
        if type(Instruction) == str:
            self.system = Instruction
            return Instruction
        return None
            
    def updateTemplate(self, file_path):
        #Updates template
        if self.loadJsonFile(file_path):
            self.template = file_path
            return file_path
        return None
    
    def updateRole(self, role):
        #Checks if role is in a valid choice and updates object 
        #Models can support specialised roles in agent creation (This is not currently Supported)
        if role in ['system', 'user', 'assistant', 'tool']:
            self.role = role
            return role
        return None

    def updateStream(self, state):
        #Checks if state is in a valid format and updates object
        if type(state) == bool:
            self.stream =  state
            return state
        return None
        
    def updateRaw(self, state):
        #Checks if state is in a valid format and updates object
        if type(state) == bool:
            self.raw =  state
            return state
        return None
            
    def updatekeepAlive(self, time):
        #Checks if time is in a valid format and updates object
        try:
            if time == 0:
                self.keepAlive = time
                return time
            if (type(int(time[:-1])) == int and time[-1:] == 'm'):
                self.keepAlive = time
                return time
        except:
            return None
            
            
    def updateContext(self, context):
        if type(context) == list:
            self.context = context
            return context
        return None
            
    def loadJsonFile(self, file_path):
        # Checks if File exists and is a JSON
        try:
            with open(file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            logging.error(f"File not found: {file_path}")
        except json.JSONDecodeError:
            logging.error(f"Invalid JSON format in {file_path}")
        except PermissionError:
            logging.error(f"Permission denied: {file_path}")
        return None

    def getModel(self):
        return self.model
    
    def getPrompt(self):
        return self.prompt
    
    def getSuffix(self):
        return self.suffix
    
    def getImages(self):
        return self.images
    
    def getFormat(self):
        return self.format
    
    def getOptions(self):
        return self.options
    
    def getSystem(self):
        return self.system
    
    def getTemplate(self):
        return self.template
    
    def getStream(self):
        return self.stream
    
    def getRaw(self):
        return self.raw
    
    def getKeepAlive(self):
        return self.keepAlive
    
    def getContext(self):
        #an encoding of the conversation used in this response, this can be sent in the next request to keep a conversational memory
        return self.context
    
    def getReseponse(self):
        #empty if the response was streamed, if not streamed, this will contain the full response
        return self.response
    
    def getResponseMessage(self):
        #contains response data
        return self.response['message']
    
    def getTotalDuration(self):
        #time spent generating the response
        return self.response.total_duration
    
    def getLoadDuration(self):
        #time spent in nanoseconds loading the model
        return self.response.load_duration
    
    def getPromptEvalCount(self):
        #number of tokens in the prompt
        return self.response.prompt_eval_count
    
    def getEvalCount(self):
        #number of tokens in the response
        return self.response.eval_count
    
    def getPromptEvalDuration(self):
        #time in nanoseconds spent generating the response
        return self.response.eval_duration
    
    def getCreatedAt(self):
        #time agent was created
        return self.response.created_at
    
    def getDone(self):
        #returns boolean if response is returned
        return self.response.done
    
    def getList():
        #List models that are available locally.
        ollama.list()
    
    def getModelInfo(self):
        #Show information about a model including details, modelfile, template, parameters, license, system prompt.
        ollama.show(self.model)
    

m = Harness('gemma3:1b')
m.updateContent("What day is it?")
m.generateResponse()