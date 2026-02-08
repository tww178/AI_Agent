import os
import subprocess

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