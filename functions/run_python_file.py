import os
import subprocess
from google.genai import types
def run_python_file(working_directory, file_path, args=None):
    absolute_path = os.path.abspath(working_directory)
    #abs2 = os.path.abspath(working_directory+ "/" + directory)

    target_dir = os.path.normpath(os.path.join(absolute_path, file_path))

    valid_target_dir = os.path.commonpath([absolute_path, target_dir]) == absolute_path

    if valid_target_dir == False:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_dir):
        return f'Error: "{file_path}" does not exist or is not a regular file'
    if not file_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file'
    command = ["python", target_dir]
    if args:
        command.extend(str(args).split())
    #print(command)
    try:
        result = subprocess.run(command,cwd=working_directory,capture_output=True,text=True,timeout=30)
    except Exception as e:
        return f"Error: executing Python file: {e}"
    cmd_out = ""
    if result.returncode != 0:
        cmd_out += f'Process exited with code {result.returncode}\n'
    if not result.stderr and not result.stdout:
        cmd_out += "No output produced"
    elif result.stdout:
        cmd_out += f'STDOUT: {result.stdout}'
    elif result.stderr:
        cmd_out += f'STDERR: {result.stderr}'
    return cmd_out
    

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a python file given a provided file path to a python file, and any optional arguments for the file, returns any output from the file's execution",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(type=types.Type.STRING,description="Path to the python file to execute, relative to the working directory"),
            "args": types.Schema(type=types.Type.STRING,description="Any optional arguments to provide to the python file's execution, if none are provided defaults to none."),

        },
    ),
)