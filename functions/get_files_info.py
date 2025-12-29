import os
from google.genai import types
def get_files_info(working_directory, directory="."):
    absolute_path = os.path.abspath(working_directory)
    #abs2 = os.path.abspath(working_directory+ "/" + directory)

    target_dir = os.path.normpath(os.path.join(absolute_path, directory))

    valid_target_dir = os.path.commonpath([absolute_path, target_dir]) == absolute_path
    if not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'
    if valid_target_dir == False:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    else:
        data = ''
        for thing in os.listdir(target_dir):
           # print(thing)
           # print(os.path.getsize(abs2 +"/" + thing))
            data = data + f"- {thing}: file_size={os.path.getsize(target_dir +"/" + thing)} bytes, is_dir={os.path.isdir(target_dir +"/" + thing)} \n"
        return data

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)
