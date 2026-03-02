import yaml
import logging
import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field



config_path = "config.yaml"
logger = logging.getLogger(__name__)

class SecretSettings(BaseSettings):
    '''
    Use to set secret settings: Passwords, API keys and the like
    Non-sensitive settings go into the YAML file
    Declare one property per secret setting to get from the .env file
    '''
    api_key: str = '' #Field(alias='my_api_key')

    class Config:
        env_file = ".env"

secret_settings = SecretSettings()
API_KEY = secret_settings.api_key

try:
    with open(config_path, "r") as f:
        
        _cfgGeneral = yaml.safe_load(f)
        EXPERIMENT_NAME = _cfgGeneral.get("EXPERIMENT_NAME")
        SEEDS = _cfgGeneral.get("SEEDS")
        GAIN_CORRECT_PREDICTION = _cfgGeneral.get("GAIN_CORRECT_PREDICTION")
        COST_MARKETING_ACTION = _cfgGeneral.get("COST_MARKETING_ACTION")
        
        # Change this for different competencia
        _cfgCompetencia = _cfgGeneral.get("competencia01")
        DATA_PATHS = _cfgCompetencia.get("DATA_PATHS")
        TRAIN_MONTHS = _cfgCompetencia.get("TRAIN_MONTHS")
        TEST_MONTHS = _cfgCompetencia.get("TEST_MONTHS")
        VALIDATION_MONTHS = _cfgCompetencia.get("VALIDATION_MONTHS")

except Exception as e:
    logger.error(f"Exception while loading the yaml config file: {e}")
