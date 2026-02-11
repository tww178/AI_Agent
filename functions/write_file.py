import os
from google.genai import types

schema_write_file = types.FunctionDeclaration( #https://googleapis.github.io/python-genai/genai.html#genai.types.FunctionDeclaration, Included in this declaration are the function name, description, parameters and response type. This FunctionDeclaration is a representation of a block of code that can be used as a Tool by the model and executed by the client.
    name="write_file",
    description="Write file at a specified file path relative to the working directory, creating necessary parent directories when needed",
    parameters=types.Schema( #https://googleapis.github.io/python-genai/genai.html#genai.types.Schema, Schema is used to define the format of input/output data.
        #Schema is used to define the format of input/output data.
        type=types.Type.OBJECT, #https://googleapis.github.io/python-genai/genai.html#genai.types.Type, the type of the data
        properties={ #https://googleapis.github.io/python-genai/genai.html#genai.types.Schema.properties, SCHEMA FIELDS FOR TYPE OBJECT Properties of Type.OBJECT.
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to write to, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="content to be written to the file at file_path"
            )
        },
        required=["file_path", "content"] #https://googleapis.github.io/python-genai/genai.html#genai.types.Schema.required, Optional. Required properties of Type.OBJECT.
    ),
)

def write_file(working_directory, file_path, content):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))

        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if not valid_target_dir:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_dir):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        parent_dir = os.path.dirname(target_dir)
        os.makedirs(parent_dir, exist_ok=True)
        #new_target_dir = os.path.normpath(os.path.join(target_dir, file_path))
        with open(target_dir, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"