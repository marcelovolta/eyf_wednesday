import pandas as pd
import logging
import os
import datetime 

def main():
    # Setup logging
    logging.basicConfig(filename='logs/log.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("Inicio de Ejecución")

    # Load the data from the CSV file
    logging.info("Cargando datos...")
    data = pd.read_csv('data/competencia_01_crudo.csv')

    print(data.head())
    print("Filas: ", data.shape[0])
    print("Columnas: ", data.shape[1])


    # Logs by hand
    # with open('logs/log.txt', 'w') as f:
    #     f.write(logging.info("Fin de Ejecución"))
    #     f.write("Filas: ", data.shape[0])
    #     f.write("Columnas: ", data.shape[1])
    #     f.write("Datos: ", data.head())
    #     f.write("Fin de Ejecución")
    #     f.write("Fin de Ejecución")

    logging.info(f"Filas: {data.shape[0]}")
    logging.info(f"Columnas: {data.shape[1]}")
    logging.info("Fin de Ejecución")

'''
This is the main function that will be called when the script is run.
Do not allow it to be called from outside this file.
'''
if __name__ == "__main__":
    main()