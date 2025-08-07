import os


def retrieve_input_file(filename: str) -> str | None:
    base_path = os.path.dirname(__file__)
    input_file_path = os.path.join(base_path, '..', 'input_files', filename)
    input_file_path = os.path.abspath(input_file_path)
    if not os.path.isfile(input_file_path):
        return None

    with open(input_file_path, 'r', encoding='utf-8') as f:
        return f.read()
