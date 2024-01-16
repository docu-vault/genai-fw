import google.generativeai as genai

##genai.configure(api_key="AIzaSyDluMvWjaSjBjxzPti6d1FMoR-Saftfy9Q")

# Set up the model
generation_config = {
  "temperature": 0.9,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

class gemini_ai_assistant ():
    
    def __init__(self, ctx):
        self._ctx = ctx 
        self._modelInitilized = False
        
    def _validate (self):
        if ( self._ctx == None ):
            raise Exception("Context is not set")
        
        if ( self._ctx.get('api_key') == None ):
            raise Exception("API Key is not set")
        
    def _initModel (self):
        self._validate()
        genai.configure(api_key=self._ctx.get('api_key'))
        self._model = genai.GenerativeModel(model_name="gemini-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)
        self._modelInitilized = True
  
    
    def generateContent(self, prompt_parts):
        if ( self._modelInitilized == False ):
            self._initModel()
            
        self._response = self._model.generate_content(prompt_parts)
        return self._response 
    
    def getResponse(self):
        return self._response
        
    def printResponse(self):
        print(self._response.text)


if __name__ == "__main__":
    ##genai.configure(api_key="AIzaSyDluMvWjaSjBjxzPti6d1FMoR-Saftfy9Q")
    ctx = {}
    ctx['api_key'] = "AIzaSyDluMvWjaSjBjxzPti6d1FMoR-Saftfy9Q" 
    
    ait = gemini_ai_assistant(ctx)
    
    prompt_parts = [
    "Given a typical order and products, please generate a database schema for h2 in-memory database ",
    ]   
    res = ait.generateContent(prompt_parts)
    ait.printResponse()
    