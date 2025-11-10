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
    prompt = sys.argv[1]
    messages = [types.Content(role="user", parts=[types.Part(text=prompt)]),]
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages,
        )
        print(response.text)
        if hasattr(response, "usage_metadata") and response.usage_metadata:
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