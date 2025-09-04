import os
import subprocess

from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file within the working directory and returns the output from the interpreter.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Optional arguments to pass to the Python file.",
                ),
                description="Optional arguments to pass to the Python file.",
            ),
        },
        required=["file_path"],
    ),
)
def run_python_file(working_directory, file_path, args=[]):
        cwd =os.path.abspath(working_directory)
        currPath = os.path.abspath(os.path.join(working_directory, file_path))
        if not currPath.startswith(cwd):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
                
        if not os.path.isfile(currPath):
            return f'Error: File "{file_path}" not found.'
        
        if not currPath.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.' 
        
        try:
            res = subprocess.run(["python",currPath],capture_output=True,timeout=30,text=True)

            result = [f"STDOUT:{res.stdout}",f"STDERR:{res.stderr}"]
            return '\n'.join(result)

        except Exception as e:
             print(f"Error: executing Python file: {e}")