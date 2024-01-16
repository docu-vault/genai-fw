import dotenv as dotenv
import os
import jsonschema

dotenv.load_dotenv()
print('Loaded environment variables')
print('DEBUG: ', os.getenv('DEBUG'))
 
class Logger:
    def __init__(self, module_name):
        self._module_name = module_name
        self._debug = os.getenv('DEBUG')
        if self._debug:
            print(f'[{module_name}] Debugging enabled')
            self._debug = True
    
    def _log(self, message, isLogEnabled):
        if ( isLogEnabled ):
            print(f'[{self._module_name}] {message}')
        
    def debug(self, message):
        self._log(message, self._debug)
            
    def info(self, message):
        self._log(message, True) 
        
        
# Validate the yaml file
schema = {
    "$schema": "http://json-schema.org/draft-07/schema",
    "type": "object",
    "properties": {
        "version": {"type": "string"},
        "kind": {"type": "string"},
        "metadata": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "description": {"type": "string"},
            },
            "required": ["name"],
        },
        "spec": {
            "type": "object",
            "properties": {
                "chain": {"type": "boolean"},
                "prompts": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "text": {"type": "string"},
                            "ctx": {"type": "string"},
                        },
                        "required": ["text"],
                    },
                },
            },
            "required": ["prompts"],
        },
    },
    "required": ["version", "kind", "metadata", "spec"],
}

class schemaValidate:      
    def validate(self, data):
        jsonschema.validate(data, schema)
        



            
    