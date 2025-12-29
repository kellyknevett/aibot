import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse

load_dotenv()
from prompts import system_prompt
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file 
from functions.write_file import schema_write_file
available_functions = types.Tool(
    function_declarations=[schema_get_files_info,schema_get_file_content,schema_write_file,schema_run_python_file],
)
#get_files_info.get_files_info('/Users/kellyknevett/workspace/github.com/kellyknevett/aibot/.venv/bin/python')
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose",action="store_true",help="Enable verbose output")
args = parser.parse_args()
messages = [types.Content(role="user",parts=[types.Part(text=args.user_prompt)])]

response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=messages,
    config=types.GenerateContentConfig(system_instruction=system_prompt,tools=[available_functions])
)

if response.usage_metadata == None:
    raise RuntimeError("Gemini response failed")
if args.verbose:
    print(f"User prompt: {args.user_prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
if response.function_calls:
    for func in response.function_calls:
        print(f"Calling function: {func.name}({func.args})")
print(response.text)

def call_function(function_call, verbose=False): 
    pass
