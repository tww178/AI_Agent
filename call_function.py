from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.run_python_file import schema_run_python_file, run_python_file
from functions.write_file import schema_write_file, write_file

available_functions = types.Tool( #https://googleapis.github.io/python-genai/genai.html#genai.types.Tool, Tool details of a tool that the model may use to generate a response.
    function_declarations=[schema_get_files_info, schema_get_file_content, schema_run_python_file, schema_write_file],
)


#https://googleapis.github.io/python-genai/genai.html#genai.types.GenerateContentResponse
#https://googleapis.github.io/python-genai/genai.html#genai.types.FunctionCall
def call_function(function_call, verbose=False):
    if verbose:
        print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(f" - Calling function: {function_call.name}")
    function_map = {
    "get_file_content": get_file_content,
    "get_files_info": get_files_info,
    "run_python_file": run_python_file,
    "write_file": write_file
    }
    function_name = function_call.name or ""
    if function_name not in function_map:
        return types.Content( #https://googleapis.github.io/python-genai/genai.html#genai.types.Content
            role="tool",
            parts=[
                types.Part.from_function_response( #https://googleapis.github.io/python-genai/genai.html#genai.types.Part
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    else:
        args = dict(function_call.args) if function_call.args else {}
        args["working_directory"] = "./calculator"
        function_result = function_map[function_name](**args)
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": function_result},
                )
            ],
        )