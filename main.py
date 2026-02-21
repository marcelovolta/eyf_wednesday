# Core Python
import logging
import os
import datetime as dt 

# External libraries
import pandas as pd
import polars as pl
import duckdb

# Modular code
from src import * 
from src.config import *

#load_data_pandas, load_data_duckdb, select_amount_cols, select_count_cols, \
#    generate_lags

# Log setup
os.makedirs('logs', exist_ok=True)
fecha = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
nombre_log = f'logs/log_{fecha}.log'
logging.basicConfig(level=logging.DEBUG, 
    format='%(asctime)s - %(levelname)s - %(name)s - %(lineno)d - %(message)s', \
        datefmt='%Y-%m-%d %H:%M:%S', 
    handlers = [logging.FileHandler(nombre_log, mode='w', encoding='utf-8'), \
                logging.StreamHandler()
                ]
            )
logger = logging.getLogger(__name__)

def main():
    # Setup logging
    
    logger.info("Start run")

    print(API_KEY)
    print(EXPERIMENT_NAME)
    print(DATA_PATHS)
    return

    # Load the data from the CSV file
    archivo_de_datos_02 = 'data/competencia_02_crudo.csv.gz'
    archivo_de_datos_03 = 'data/competencia_03_crudo.csv.gz'
    data = load_data_pandas([archivo_de_datos_02, archivo_de_datos_03])
    # data = load_data_pandas([archivo_de_datos_03])


    if data is None: return
    print(data.head())
    print(data.tail())
    
    logging.info(f"Rows: {data.shape[0]}")
    logging.info(f"Columns: {data.shape[1]}")
    
    amount_cols = select_amount_cols(data)
    count_cols = select_count_cols(data)

    if amount_cols is None or count_cols is None:
        logging.error("No amount columns, or no count cols have been found")
        return
    
    logging.info(f"Length of amount column list: {len(amount_cols)}")
    logging.info(f"Length of count column list: {len(count_cols)}")
    cols_for_lag = amount_cols + count_cols
    
    data = generate_lags(data, cols_for_lag, [1, 2, 3, 6, 12], True)

    
    
    logging.info("End run")

    


'''
This is the main function that will be called when the script is run.
Do not allow it to be called from outside this file.
'''
if __name__ == "__main__":
    main()