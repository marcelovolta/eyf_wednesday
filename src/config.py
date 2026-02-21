import yaml
import logging
import os
from pydantic_settings import BaseSettings



config_path = "config.yaml"
logger = logging.getLogger(__name__)

class SecretSettings(BaseSettings):
    '''
    Use to set secret settings: Passwords, API keys and the like
    Non-sensitive settings go into the YAML file
    Declare one property per secret setting to get from the .env file
    '''
    api_key: str

    class Config:
        env_file = ".env"

secret_settings = SecretSettings()
API_KEY = secret_settings.api_key

try:
    with open(config_path, "r") as f:
        
        _cfgGeneral = yaml.safe_load(f)
        EXPERIMENT_NAME = _cfgGeneral.get("EXPERIMENT_NAME")
        LOGGING_CONFIG = _cfgGeneral.get("LOGGING_CONFIG")
        GAIN_CORRECT_PREDICTION = _cfgGeneral.get("GAIN_CORRECT_PREDICTION")
        COST_MARKETING_ACTION = _cfgGeneral.get("COST_MARKETING_ACTION")
        
        _cfgCompetencia01 = _cfgGeneral.get("competencia03")
        DATA_PATHS = _cfgCompetencia01.get("DATA_PATHS")
    
except Exception as e:
    logger.error(f"Exception while loading the yaml config file: {e}")
