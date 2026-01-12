import os
import subprocess

from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    try:
        working_directory_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_directory_abs, file_path))

        valid_target_file = os.path.commonpath([working_directory_abs, target_file]) == working_directory_abs

        if valid_target_file is False:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if os.path.isfile(target_file) == False:
            return f'Error: "{file_path}" does not exist or is not a regular file'
        
        if target_file.endswith(".py") is False:
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", target_file]

        if args is not None:
            command.extend(args)
        
        comm_output = subprocess.run(command, capture_output=True, cwd= working_directory_abs, text=True, timeout=30)
        output_string = []

        if comm_output.returncode != 0:
            output_string.append(f"Process exited with code {comm_output.returncode}")


        if len(comm_output.stdout) > 0:
            output_string.append(f"STDOUT: {comm_output.stdout}")
        if len(comm_output.stderr) > 0:
            output_string.append(f"STDERR: {comm_output.stderr}")

        if len(output_string) == 0:
            output_string.append("No output produced" )
        
        return "\n".join(output_string)
        
    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file within the working directory and returns its output (STDOUT and STDERR).",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative path to the .py file to be executed.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="A list of string arguments to pass to the Python script.",
            ),
        },
        required=["file_path"],
    ),
)