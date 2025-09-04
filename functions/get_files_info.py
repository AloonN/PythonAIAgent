import os
from google.genai import types
# os.path.abspath(): Get an absolute path from a relative path
# os.path.join(): Join two paths together safely (handles slashes)
# .startswith(): Check if a string starts with a substring
# os.path.isdir(): Check if a path is a directory
# os.listdir(): List the contents of a directory
# os.path.getsize(): Get the size of a file
# os.path.isfile(): Check if a path is a file
# .join(): Join a list of strings together with a separator

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

def get_files_info(working_directory, directory="."):
    
    try: 
        cwd =os.path.abspath(working_directory)
        currPath = os.path.abspath(os.path.join(working_directory, directory))
     
        if not currPath.startswith(cwd):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        if not os.path.isdir(currPath):
            return f'Error: "{directory}" is not a directory'
    

        contents = os.listdir(currPath)
        res = [];
        for content in contents:
            res.append(f'{content}: file_size={os.path.getsize(os.path.join(currPath, content))} bytes, is_dir={os.path.isdir(os.path.join(currPath, content))}')
        return f'\n'.join(res)
    
    except Exception as e:
        print("Error:", e)




