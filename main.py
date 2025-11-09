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
    client = genai.Client(api_key = api_key)
    text = sys.argv[1]
    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=[text]
    )
    print(response.text)
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()