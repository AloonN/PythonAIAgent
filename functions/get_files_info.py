import os
from google.genai import types

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




