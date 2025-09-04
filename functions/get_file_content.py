import os
from constants import MAX_CHARS
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Reads and returns the first {MAX_CHARS} characters of the content from a specified file within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file whose content should be read, relative to the working directory.",
            ),
        },
        required=["file_path"],
    ),
)

def get_file_content(working_directory, file_path):
        cwd =os.path.abspath(working_directory)
        currPath = os.path.abspath(os.path.join(working_directory, file_path))

        if not currPath.startswith(cwd):
            return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(currPath):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        try:
            with open(currPath, "r") as f:                
                file_content_string = f.read(MAX_CHARS)
                if os.path.getsize(currPath) > MAX_CHARS:
                    file_content_string += (
                        f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                    )
            return file_content_string
        except Exception as e:
            print("Error:", e)


