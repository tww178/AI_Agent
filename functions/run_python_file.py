import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration( #https://googleapis.github.io/python-genai/genai.html#genai.types.FunctionDeclaration, Included in this declaration are the function name, description, parameters and response type. This FunctionDeclaration is a representation of a block of code that can be used as a Tool by the model and executed by the client.
    name="run_python_file",
    description="Run Python file at a specified file path relative to the working directory",
    parameters=types.Schema( #https://googleapis.github.io/python-genai/genai.html#genai.types.Schema, Schema is used to define the format of input/output data.
        #Schema is used to define the format of input/output data.
        type=types.Type.OBJECT, #https://googleapis.github.io/python-genai/genai.html#genai.types.Type, the type of the data
        properties={ #https://googleapis.github.io/python-genai/genai.html#genai.types.Schema.properties, SCHEMA FIELDS FOR TYPE OBJECT Properties of Type.OBJECT.
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to run, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Array of arguments supplied to run the Python file",
                items=types.Schema(
                    type=types.Type.STRING,
                ) #https://googleapis.github.io/python-genai/genai.html#genai.types.Schema.items
            ),
        },
        required=["file_path"] #https://googleapis.github.io/python-genai/genai.html#genai.types.Schema.required, Optional. Required properties of Type.OBJECT.
    ),
)

def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if not valid_target_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_dir):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not target_dir.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", target_dir]
        if args:
            command.extend(args)
        completed_process_object = subprocess.run(command, cwd=working_dir_abs, capture_output=True, text=True, timeout=30)
        output_string_list = []
        if completed_process_object.returncode != 0:
            output_string_list.append(f"Process exited with code {completed_process_object.returncode}")
        if not completed_process_object.stdout and not completed_process_object.stderr:
            output_string_list.append(f"No output produced")
        if completed_process_object.stdout:
            output_string_list.append(f"STDOUT:\n{completed_process_object.stdout}")
        if completed_process_object.stderr:
            output_string_list.append(f"STDERR:\n{completed_process_object.stderr}")
        output_string = "\n".join(output_string_list)
        return output_string
    except Exception as e:
        return f"Error: executing Python file: {e}"