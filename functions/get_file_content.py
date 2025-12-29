import os
from google.genai import types
def get_file_content(working_directory, file_path):
    try:
        absolute_path = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(absolute_path, file_path))
        print(target_dir)
        valid_target_dir = os.path.commonpath([absolute_path, target_dir]) == absolute_path
    except FileNotFoundError:
        print("Error handling dir")
        return "error handling dir"
    if not valid_target_dir:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_dir):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    else:
        try:
            file = open(target_dir)
        except FileNotFoundError:
            print("could not read file")
            return "Could not read file"
        data = file.read(10000)
        if file.read(1):
            data += f'[...File "{file_path}" truncated at {10000} characters]'
        
            print("Error reading file")
            return "Error reading file"
        return data
        
#print(get_file_content("calculator", "lorem.txt"))
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads and returns the content of a file, when provided with the path to the file, use this when asked to provide the content of a text file, or a .txt file, if you are unsure where the file is, just assume its in the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="When asked to read file content, put the file location here",
            ),
        },
    ),
)