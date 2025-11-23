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
    available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
    ]
)
    system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

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