import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys
from call_function import call_function
from config import MAX_CHARS

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
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute Python files with optional arguments, constrained to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "working_directory": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory. The file may receive optional arguments.",
            ),
        },
    ),
)   
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file within the working directory. Creates the file if it doesn't exist.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to write, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to the file",
            ),
        },
        required=["file_path", "content"],
    ),
)
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
    ]
)
system_prompt = """
You are a helpful AI coding agent.
When a user asks a question or makes a request, you must decide whether any of the available operations are needed. 
If the user asks you to list, read, run, or write files, you must respond by selecting and calling the appropriate function instead of answering directly in text.
When a user asks a question or makes a request, make a function call plan. You will perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

def gen_content(client, messages, verbose):
    response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages,
            config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt))
    if response.candidates:
        for candidate in response.candidates:
            messages.append(candidate.content)
    if not response.function_calls and response.text:
        return response.text
    func_responses = []
    for function_call_part in response.function_calls:
        func_call_result = call_function(function_call_part, verbose)
        if (
        not hasattr(func_call_result, "parts") or
        not func_call_result.parts or
        not hasattr(func_call_result.parts[0], "function_response") or
        not hasattr(func_call_result.parts[0].function_response, "response")
    ):
            raise Exception("ERROR: empty call")
        func_responses.append(func_call_result.parts[0])
        if verbose:
            print(f"-> {func_call_result.parts[0].function_response.response}")
    if verbose and hasattr(response, "usage_metadata") and response.usage_metadata:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    messages.append(types.Content(role="user", parts=func_responses))

    return None

def main():


    load_dotenv()
    if len(sys.argv)< 2:
        print('Usage: uv run main.py "your prompt here"')
        # raise Exception("invalid prompt")
        sys.exit(1)
    
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Missing api key")
        sys.exit(1)
    client = genai.Client(api_key = api_key)
    verbose = "--verbose" in sys.argv
    
    prompt = sys.argv[1]
    messages = [types.Content(role="user", parts=[types.Part(text=prompt)]),]
    if verbose :
        print(f"User prompt: {prompt}")
    max_iter = 20
    iters = 0

    while True:
        iters += 1
        if iters > max_iter:
            print("Maximum iterations reached.")
            sys.exit(1)

        try:
            final_response = gen_content(client, messages, verbose)
            if final_response:
                print("Final response:")
                print(final_response)
                break
        except Exception as e:
            print(f"Unexpected error: {e}")
            sys.exit(1)
        
        
       
       
                
        
    
        


if __name__ == "__main__":
    main()