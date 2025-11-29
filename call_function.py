from google import genai
from google.genai import types
from functions.write_file import write_file
from functions.run_python_file import run_python_file
from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from config import WORKING_DIR

def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    
    func_map ={"get_files_info": get_files_info, "get_file_content": get_file_content, "run_python_file": run_python_file, "write_file": write_file} 
    func_name = function_call_part.name
    if not func_name in func_map:
        return types.Content(role="tool", parts=[types.Part.from_function_response(name=func_name, response={"error": f"Unknown function: {func_name}"},)],)
    else:
        args = dict(function_call_part.args)
        args["working_directory"] = WORKING_DIR
        func_results = func_map[func_name](**args)
        return types.Content(role="tool", parts=[types.Part.from_function_response(name=func_name, response={"result": func_results},)],)