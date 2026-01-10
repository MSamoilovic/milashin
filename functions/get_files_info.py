import os

def get_files_info(working_directory, directory="."):
    try: 
        working_directory_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_directory_abs, directory))

        valid_target_dir = os.path.commonpath([working_directory_abs, target_dir]) == working_directory_abs

        if valid_target_dir is False:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
        if os.path.isdir(target_dir) is False:
            return f'Error: "{directory}" is not a directory'
        
        list_directory = os.listdir(target_dir)

        result = []

        for item in list_directory:
            full_path = os.path.join(target_dir, item)
            result.append(
                f"- {item}: file_size={os.path.getsize(full_path)} bytes, "
                f"is_dir={os.path.isdir(full_path)}"
            )
        
        return "\n".join(result)
    
    except Exception as e :
        return f"Error: {e}"
