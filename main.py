import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info,get_files_info
from functions.get_file_content import schema_get_file_content,get_file_content
from functions.write_file import schema_write_file,write_file
from functions.run_python_file import schema_run_python_file,run_python_file

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
system_prompt =  """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

When the user aks about the code project - they are referring to the working directory. 
you should generally start by looking at the project's files, and figuring out how to run the project and its tests.
you'll always want to test the tests and the actual project to verify that behavior is working.
All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

def call_function(func, verbose=False):
    """
    how does an LLM actually call a function?
        We tell the LLM which functions are available to it
        We give it a prompt
        It describes which function it wants to call, and what arguments to pass to it
        We call that function with the arguments it provided
        We return the result to the LLM
    """
    if verbose:
        print(f"Calling function: {func.name}({func.args})")
    else:
        print(f"Calling function: {func.name}")

    result = ''

    if func.name == "get_files_info":
        result = get_files_info("./calculator",**func.args)
    if func.name == "get_file_content":
        result = get_file_content("./calculator",**func.args)
    if func.name == "write_file":
        result = write_file("./calculator",**func.args)
    if func.name == "run_python_file":
        result = run_python_file("./calculator",**func.args)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=func.name,
                response={"result": result},
            )
        ],
    )

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file
    ]
)
def main():

    verbose = "--verbose" in sys.argv
    args =[]
    
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here"')
        print('Example: python main.py "How do I build a calculator app?"')
        sys.exit(1)    

    try:
        user_prompt = ' '.join(args)
        if verbose:
            print('User prompt:',user_prompt)
            
        messages = [
            types.Content(role="user", parts=[types.Part(text=user_prompt)]),
        ]
      
        response = generate_content(client,messages,verbose)

  


    except Exception as e:
        print("Error:", e)
        
def generate_content(client,prompt,verbose):
    
    for _ in range(0,20):
        response = client.models.generate_content(
            model='gemini-2.0-flash-001',
            contents=prompt,
            config=types.GenerateContentConfig(tools=[available_functions],system_instruction=system_prompt)
        )
        if verbose:
            print("Prompt tokens:", response.usage_metadata.prompt_token_count)
            print("Response tokens:", response.usage_metadata.candidates_token_count)
            print("Response:")

        for cand in response.candidates:
            if cand is None or cand.content is None:
                continue
            prompt.append(cand.content)

        if not response.function_calls:
            print(response.text)
            return response.text

        function_responses = []
        for function_call_part in response.function_calls:
            function_call_result = call_function(function_call_part, verbose)
            prompt.append(function_call_result)
            if (
                not function_call_result.parts
                or not function_call_result.parts[0].function_response
            ):
                raise Exception("empty function call result")
            if verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
            function_responses.append(function_call_result.parts[0])

        if not function_responses:
            raise Exception("no function responses generated, exiting.")
    
if __name__ == "__main__":
    main()

