import os
from config import MAX_CHARACTER_LIMIT

def get_file_content(working_directory, file_path):
    try:
        working_directory_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_directory_abs, file_path))

        valid_target_file = os.path.commonpath([working_directory_abs, target_file]) == working_directory_abs

        if valid_target_file is False:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        if os.path.isfile(target_file) == False:
            return f'Error: File not found or is not a regular file: "{file_path}"'
      
        with open(target_file, "r") as f:
            content = f.read(MAX_CHARACTER_LIMIT)

            if f.read(1):
                content += f'[...File "{target_file}" truncated at {MAX_CHARACTER_LIMIT} characters]'

        return content
        
    except Exception as e:
        return f'Error: Reading file {file_path}: {e}'