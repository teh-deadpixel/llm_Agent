import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys

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
    description="Read file content in the specified directory, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to read from, relative to the working directory.",
            ),
        },
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
    description="Write or overwrite files in the specified file_path, constrained to the working file_path.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to Write or overwrite files, constrained to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Text content to write to the file. Existing contents will be overwritten.",
            ),
        },
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
    prompt = sys.argv[1]
    messages = [types.Content(role="user", parts=[types.Part(text=prompt)]),]
    if verbose :
        print(f"User prompt: {prompt}")
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages,
            config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
        )
        
        if response.function_calls == None:
            print(response.text)
        else:
            for function_call_part in response.function_calls:
                print(f"Calling function: {function_call_part.name}({function_call_part.args})")
            
        if verbose and hasattr(response, "usage_metadata") and response.usage_metadata:
            
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    except genai.errors.AuthenticationError as e:
        print(f"Auth error: {e}. Check GEMINI_API_KEY.")
        sys.exit(1)
    except genai.errors.InvalidArgument as e:
        print(f"Invalid request: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

        


if __name__ == "__main__":
    main()