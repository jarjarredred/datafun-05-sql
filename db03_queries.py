import sqlite3
import os
import pathlib
import pandas as pd
from utils_logger import logger

def execute_and_save_query(connection, file_path, output_folder) -> None:
    """
    Executes a SQL file and saves results to CSV.
    Args:
        connection (sqlite3.Connection): SQLite connection object.
        file_path (pathlib.Path): Path to the SQL file to be executed.
        output_folder (pathlib.Path): Folder to save query results.
    """
    try:
        with open(file_path, 'r') as file:
            sql_script: str = file.read()
        
        # Execute query and save results
        df = pd.read_sql_query(sql_script, connection)
        output_file = output_folder.joinpath(f"{file_path.stem}.csv")
        df.to_csv(output_file, index=False)
        
        logger.info(f"Executed and saved: {file_path} → {output_file}")
        
    except Exception as e:
        logger.error(f"Failed to execute/save {file_path}: {e}")
        raise

def execute_all_sql_files(connection, queries_folder, output_folder) -> None:
    """
    Executes all SQL files in folder and saves outputs.
    Args:
        connection: SQLite connection
        queries_folder: Folder containing SQL files
        output_folder: Folder to save CSV results
    """
    # Create output folder if it doesn't exist
    output_folder.mkdir(parents=True, exist_ok=True)
    
    # Get all .sql files in the folder and sort them alphabetically
    sql_files = sorted(queries_folder.glob('*.sql'))
    
    if not sql_files:
        logger.warning(f"No SQL files found in {queries_folder}")
        return
    
    for sql_file in sql_files:
        execute_and_save_query(connection, sql_file, output_folder)

def main() -> None:
    logger.info("Starting query execution...")
    
    # Define path variables
    ROOT_DIR = pathlib.Path(__file__).parent.resolve()
    SQL_QUERIES_FOLDER = ROOT_DIR.joinpath("sql_queries")
    DATA_FOLDER = ROOT_DIR.joinpath("data")
    SQL_OUTPUT_FOLDER = ROOT_DIR.joinpath("sql_output")  # New output folder
    DB_PATH = DATA_FOLDER.joinpath('project.sqlite3')

    # Ensure folders exist
    DATA_FOLDER.mkdir(exist_ok=True)
    SQL_QUERIES_FOLDER.mkdir(exist_ok=True)

    # Connect to SQLite database
    try:
        connection = sqlite3.connect(DB_PATH)
        logger.info(f"Connected to database: {DB_PATH}")

        # Execute all SQL files and save results
        execute_all_sql_files(connection, SQL_QUERIES_FOLDER, SQL_OUTPUT_FOLDER)

        logger.info("Query execution and saving completed successfully.")
    except Exception as e:
        logger.error(f"Error during execution: {e}")
    finally:
        connection.close()
        logger.info("Database connection closed.")

if __name__ == '__main__':
    main()