import os
def write_file(working_directory, file_path, content):
    abs_working = os.path.abspath(working_directory)
    abs_target = os.path.abspath(os.path.join(working_directory, file_path))
    inside = abs_target == abs_working or abs_target.startswith(abs_working+os.sep)
    if not inside:
        return f'Error: Cannot write "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(abs_target):
        dir_path = os.path.dirname(abs_target)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
    
    try:
        with open(abs_target, "w") as w:
            w.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f'Error: {e}'

