from google_ai_tool import gemini_ai_assistant
import yaml 
import os 
import os.path
from utils import Logger, schemaValidate

logger = Logger('controller')

class controller ():
    
    def __init__(self, config_file):
        self._config_file = config_file
        self._yamls = {}
        self._prompts = {}
        
    def _loadYaml (self, config_yaml_file):
        if ( os.path.isfile(config_yaml_file) == False ):
            raise Exception("Config file {} not found", config_yaml_file)
        
        logger.info('loading config file: {}'.format(config_yaml_file))
        
        temp_config = {}
        with open(config_yaml_file, 'r') as yaml_file:
            temp_config = yaml.safe_load(yaml_file)
            
        logger.info('loaded config file: {}'.format(config_yaml_file))
        return temp_config

        
    def validateConfig(self):
        if ( self._config_file == None ):
            raise Exception("Main Configuration files are not set...")
        
        self._api_key = os.getenv('GENAI_API_KEY')
        if ( self._api_key == None ):
            raise Exception("GenAI API Key is not set. Please set variable GENAI_API_KEY")
        
        self._config = self._loadYaml(self._config_file)
        self._printConfig()
        
    def generate(self):
        ctx = {'api_key' : self._api_key}
        for key, value in self._prompts.items():
            print('item: {}'.format(key))
            gemini = gemini_ai_assistant(ctx)
            gemini.generateContent(value)
            gemini.printResponse()
        
        
    def load(self):
        for config_file in self._config.get('config_files'):
            logger.debug('Proessing config file: {}'.format(config_file))
            self._loadConfigYAML(config_file)
            
    def _loadConfigYAML(self, yaml_file):
        if ( os.path.isfile(yaml_file) == False ):
            raise Exception("Config file {} not found", yaml_file)
        
        tempConfig = self._loadYaml(yaml_file)
        self._validateGenAIConfigYAML(yaml_file, tempConfig)
        prompts = tempConfig.get('spec').get('prompts')
        logger.info('prompts 0: {}'.format(prompts[0].get('text')))
        yamlKey = tempConfig.get('metadata').get('name')
        logger.debug('yamlKey: {}'.format(yamlKey))
        self._yamls[yamlKey] = tempConfig
        self._prompts[yamlKey] = self._getPtompt(tempConfig)
        logger.debug('prompts 1: {}'.format(self._prompts))
        
      
    def _getPtompt(self, config):
        prompt = config.get('spec').get('prompts')[0].get('text')
        return [prompt]
        
    def _validateGenAIConfigYAML(self, yaml_file, config):
        logger.debug('Validating config file: {}'.format(config))
        sv = schemaValidate()
        sv.validate(config)
        
        print('TO DO: All validations are not implemented yet')

                
    def _printConfig(self):
        print("pring config:\n", self._config)
        logger.info("output-to-dir: {}".format(self._config.get('output_to_dir')))
        logger.info('configfiles: {}'.format(self._config.get('config_files')))
        

## This is for testing purpoes only
if __name__ == "__main__":
    ##cfile = 'config\generate-schema.yaml'
    my_controller = controller(os.getenv('CONFIG_FILE'))
    my_controller.validateConfig()  
    my_controller.load()
    my_controller.generate()