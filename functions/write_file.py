import os
from google.genai import types
def write_file(working_directory, file_path, content):

    absolute_path = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(absolute_path, file_path))
    valid_target_dir = os.path.commonpath([absolute_path, target_dir]) == absolute_path
    print(target_dir)
    print(valid_target_dir)
    if not valid_target_dir:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if os.path.isdir(target_dir):
        return f'Error: Cannot write to "{file_path}" as it is a directory'
    try:
        print("/".join(target_dir.split("/")[0:-1]))
        os.makedirs("/".join(target_dir.split("/")[0:-1]), exist_ok=True)
        with open(target_dir,mode="w") as f:
            f.write(content)
    except Exception as e:
        return e
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes the provided content to the file located at the provided file path, the file's content is overwritten if already exists, file location is relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(type=types.Type.STRING,description="Path to the file to write to, relative to the working directory"),
            "content": types.Schema(type=types.Type.STRING,description="The desired text content to write into the file"),
        },
    ),
)