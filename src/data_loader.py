import pandas as pd
import duckdb
import polars as pl
import logging

logger = logging.getLogger(__name__)

def load_data_pandas(path: list[str]) -> pd.DataFrame | None:
    '''
    Loads data from several CSV files and concatenates them assuming
    matching column names, types and position. Discards the existing index
    and creates a new one
    Args
    ----
        path: List of strings that includes all the paths where the CSV files are located

    Returns
    -------
        A pandas dataframe if the load process was successful, None otherwise
    '''
    if path is None or len(path) == 0:
        logger.error("Error when trying to load. An empty path was provided")
        return None
    
    logger.info(f"Loading data with Pandas from {path}...")
    df = pd.DataFrame()
    try:
        for filepath in path:
            newdf = pd.read_csv(filepath)
            df = pd.concat(
            [
                df,
                newdf,
            ],
                ignore_index = True
            )
    except Exception as e:
        logger.error(f"Error when trying to load data: {e}")
        raise e
    logger.info(f"Data loaded successfully from {path}")
    return df

def load_data_polars(path: str) -> pl.DataFrame | None:
    logger.info(f"Loading data with Polars from {path}...")
    try:
        df = pl.read_csv(path)
    except Exception as e:
        logger.error(f"Error when trying to load data: {e}")
        raise e
    logger.info(f"Data loaded successfully from {path}")
    return df

def load_data_duckdb(path: list[str]) -> pd.DataFrame | None:
    '''
    Loads data from several CSV files and concatenates them assuming
    matching column names, types and position. Discards the existing index
    and creates a new one. Uses DuckDB to load and then export the data to
    a Pandas DataFrame 
    Args
    ----
        path: List of strings that includes all the paths where the CSV files are located

    Returns
    -------
        A pandas dataframe if the load process was successful, None otherwise
    '''
    if path is None or len(path) == 0:
        logger.error("Error when trying to load. An empty path was provided")
        return None

    df = pd.DataFrame()
    logger.info(f"Loading data with DuckDB from {path}...")
    conn = duckdb.connect()
    try:
        for filepath in path:
            sql = f"SELECT * FROM read_csv_auto('{filepath}')"
            logger.info(f"SQL expression to load {sql}")
            newdf = conn.execute(sql).df()
            df = pd.concat(
                [
                    df,
                    newdf,
                ],
                    ignore_index = True
                )    
    except Exception as e:
        logger.error(f"Error when trying to load data: {e}")
        raise e
    logger.info(f"Data loaded successfully from {path}")
    return df
