import os
from config import MAX_CHARS
from google.genai import types

schema_get_file_content = types.FunctionDeclaration( #https://googleapis.github.io/python-genai/genai.html#genai.types.FunctionDeclaration, Included in this declaration are the function name, description, parameters and response type. This FunctionDeclaration is a representation of a block of code that can be used as a Tool by the model and executed by the client.
    name="get_file_content",
    description="Read file at a specified file path relative to the working directory, truncating when the maximum amount of characters are read",
    parameters=types.Schema( #https://googleapis.github.io/python-genai/genai.html#genai.types.Schema, Schema is used to define the format of input/output data.
        #Schema is used to define the format of input/output data.
        type=types.Type.OBJECT, #https://googleapis.github.io/python-genai/genai.html#genai.types.Type, the type of the data
        properties={ #https://googleapis.github.io/python-genai/genai.html#genai.types.Schema.properties, SCHEMA FIELDS FOR TYPE OBJECT Properties of Type.OBJECT.
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to read from, relative to the working directory",
            ),
        },
        required=["file_path"] #https://googleapis.github.io/python-genai/genai.html#genai.types.Schema.required, Optional. Required properties of Type.OBJECT.
    ),
)

def get_file_content(working_directory, file_path):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if not valid_target_dir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_dir):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        with open(target_dir, "r") as f:
            file_content_string = f.read(MAX_CHARS)
        # After reading the first MAX_CHARS...
            if f.read(1):
                truncation_msg = f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                file_content_string += truncation_msg
        
        return file_content_string
    except Exception as e:
        return f"Error: {e}"