import os
import subprocess

def run_python_file(working_directory, file_path, args=[]):
    abs_working = os.path.abspath(working_directory)
    abs_target = os.path.abspath(os.path.join(working_directory, file_path))
    inside = abs_target == abs_working or abs_target.startswith(abs_working+os.sep)
    if not inside:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(abs_target):
        return f'Error: File "{file_path}" not found.'
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        running = subprocess.run(["python", abs_target, *args], cwd =abs_working, capture_output=True, text=True, timeout=30)
        stdout_text = running.stdout or ""
        error_text = running.stderr or ""
        combined = ""
        if stdout_text:
            combined += stdout_text
        if error_text:
            combined += error_text

        output = []
        if combined:
            output.append(f"STDOUT:\n{combined}".rstrip())

        if running.returncode != 0:
            output.append(f"Process exited with code {running.returncode}")

        result = "\n".join(output).strip()

        if not combined and running.returncode == 0:
            return "No output produced."

        return result
    except Exception as e:
        return f"Error: executing Python file: {e}"
