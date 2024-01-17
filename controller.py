from google_ai_tool import gemini_ai_assistant
import yaml 
import os 
import os.path
from utils import Logger, schemaValidate, SaveContent

logger = Logger('controller')

class controller ():
    
    def __init__(self, config_file):
        self._config_file = config_file
        self._yamls = {}
        self._prompts = {}
        self._responses = {}
        self._ctxs = {}
        
    def _loadYaml (self, config_yaml_file):
        if ( os.path.isfile(config_yaml_file) == False ):
            raise Exception("Config file {} not found", config_yaml_file)
        
        logger.info('Loading config file: {}'.format(config_yaml_file))
        
        temp_config = {}
        with open(config_yaml_file, 'r') as yaml_file:
            temp_config = yaml.safe_load(yaml_file)
            
        logger.info('Done Loading config file: {}'.format(config_yaml_file))
        return temp_config

        
    def validateConfig(self):
        if ( self._config_file == None ):
            raise Exception("Main Configuration files are not set...\n set variable CONFIG_FILE to config file path")
        
        self._api_key = os.getenv('GENAI_API_KEY')
        if ( self._api_key == None ):
            raise Exception("GenAI API Key is not set. Please set variable GENAI_API_KEY")
        
        self._config = self._loadYaml(self._config_file)
        self._printConfig()
        
    def generate(self):
        ctx = {'api_key' : self._api_key}
        sc = SaveContent(self._config)
        
        for yamlName, prompt in self._prompts.items():
            print('item: {}'.format(yamlName))
            prompts = prompt
            gemini = gemini_ai_assistant(ctx)
            if ( self._ctxs.get(yamlName) != None ):
                tempCtx = self._getPromptContext(yamlName, self._ctxs.get(yamlName))
                ##key = self._ctxs.get(yamlName)
                ##tempCtx = self._responses.get(key).text
                logger.debug('generated: tempCtx: {}'.format(tempCtx))
                prompts = prompt + tempCtx
                logger.debug('generate: value: {}'.format(prompts))
                
            self._responses[yamlName] = gemini.generateContent([prompts])
            logger.debug('response: {}'.format(self._responses[yamlName]))
            sc.save(self._responses[yamlName].text, yamlName + '.txt')
            
    def process(self):
        for config_file in self._config.get('config_files'):
            logger.debug('Proessing config file: {}'.format(config_file))
            self._loadConfigYAML(config_file)
            
    def _loadConfigYAML(self, yaml_file):
        if ( os.path.isfile(yaml_file) == False ):
            raise Exception("Config file {} not found", yaml_file)
        
        tempConfig = self._loadYaml(yaml_file)
        self._validateGenAIConfigYAML(yaml_file, tempConfig)
        
        yamlName = tempConfig.get('metadata').get('name')
        logger.debug('YAML Name (metadata.name): {}'.format(yamlName))
        prompts = tempConfig.get('spec').get('prompts')
        ##logger.info('\t prompts 0: {}'.format(prompts[0].get('text')))

        self._yamls[yamlName] = tempConfig
        self._prompts[yamlName] = self._getPrompt(yamlName, tempConfig)
        logger.debug('prompts 1: {}'.format(self._prompts[yamlName]))
        
      
    def _getPrompt(self, yamlName, config):
        prompt = config.get('spec').get('prompts')[0].get('text')
        logger.debug('\t Prompt is : {}'.format(prompt))
        ctx = config.get('spec').get('prompts')[0].get('ctx')
        ##ctx = self._getPromptContext(yamlName, config)
        logger.debug('\t Prompt ctx is : {}'.format(ctx))
        self._ctxs[yamlName] = ctx
        #if ( ctx != None ):
        #    prompt = prompt + ctx 
        #    
        return prompt
    
    def _getPromptContext(self, yamlName, ctx):
        #ctx = config.get('spec').get('prompts')[0].get('ctx')
        #logger.debug('001- Prompt ctx is : {}'.format(ctx))
        
        #ctx is an array of values 
        ctxs = self._ctxs.get(yamlName)
        logger.debug('001- Prompt ctx is : {}'.format(ctxs))
        if ( ctxs == None ):
            return None
        
        tempCtx = ''
        for ctx in ctxs:
            # see if value is specified
            value = ctx.get('value')
            logger.debug('\t 002- Prompt ctx value is : {}'.format(value))
            if ( value  ):
                tempCtx = tempCtx + value 
                continue
                
            # see if output-of is specified
            key = ctx.get('output-of')
            logger.debug('\t 003- Prompt ctx key is : {}'.format(key))
            if ( key != None ):
                if ( self._responses.get(key) == None ):
                    raise Exception("Referenced yaml metadata.name is not valid: {}".format(key))
                    
                value=self._responses.get(key).text
                tempCtx = tempCtx + value
                
        logger.debug('\t 004- Prompt ctx temp is : {}'.format(tempCtx))
        return tempCtx     
        
        # else , it is an escaped error from config file validation
        #raise Exception("Prompt context is not set or YAML file is not valid")
        

    def _validateGenAIConfigYAML(self, yaml_file, config):
        logger.debug('Validating config file: {}'.format(config))
        sv = schemaValidate()
        sv.validate(config)
        
        print('TO DO: All validations are not implemented yet')

                
    def _printConfig(self):
        print("pring config:\n", self._config)
        logger.info("output-to-dir: {}".format(self._config.get('output_to_dir')))
        logger.info('configfiles: {}'.format(self._config.get('config_files')))
        

# this is for testing purposes at module level
if __name__ == "__main__":
    ##cfile = 'config\generate-schema.yaml'
    my_controller = controller(os.getenv('CONFIG_FILE'))
    my_controller.validateConfig()  
    my_controller.process()
    my_controller.generate()