from pathlib import Path
from loguru import logger

def retrieve_input_file(filename: str = 'Business_ZenithPoint.txt'):
    script_dir = Path(__file__).parent
    input_dir = script_dir.parent / 'input_files'
    file_path = input_dir / filename
    try:
        with open(file_path, 'r') as file:
            logger.info(f"Business example retrieved from {file_path}")
            return file.read()
    except FileNotFoundError:
        logger.error(f'ERROR! File not found: {file_path}')
        return None