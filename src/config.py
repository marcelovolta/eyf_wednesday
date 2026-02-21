from dataclasses import asdict
import yaml
import logging
import os
from dotenv import load_dotenv



config_path = "config.yaml"
logger = logging.getLogger(__name__)


# 2. Función que reemplaza ${VAR}
def replace_env_vars(obj):
    if isinstance(obj, dict):
        return {k: replace_env_vars(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [replace_env_vars(i) for i in obj]
    elif isinstance(obj, str):
        return os.path.expandvars(obj)   # <- aquí ocurre la magia
    else:
        return obj

load_dotenv()    
try:
    with open(config_path, "r") as f:
        _cfgGeneral = yaml.safe_load(f)
        _cfgGeneral = replace_env_vars(_cfgGeneral)
        
        EXPERIMENT_NAME = _cfgGeneral.get("EXPERIMENT_NAME")
        GAIN_CORRECT_PREDICTION = _cfgGeneral.get("GAIN_CORRECT_PREDICTION")
        COST_MARKETING_ACTION = _cfgGeneral.get("COST_MARKETING_ACTION")
        API_KEY = _cfgGeneral.get("API_KEY")
        _cfgCompetencia01 = _cfgGeneral.get("competencia03")
        DATA_PATHS = _cfgCompetencia01.get("DATA_PATHS")
    
except Exception as e:
    logger.error(f"Exception while loading the yaml config file: {e}")
