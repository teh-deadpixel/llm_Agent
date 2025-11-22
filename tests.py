# from functions.get_files_info import get_files_info
#from functions.get_file_content import get_file_content
#from functions.write_file import write_file
from functions.run_python_file import run_python_file

cases = [
    # ("Result for current directory:", ("calculator", "main.py")),
    # ("Result for 'pkg' directory:", ("calculator", "pkg/calculator.py")),
    # ("Result for '/bin' directory:", ("calculator", "/bin/cat")),
    # ("Result for '../' directory:", ("calculator", "pkg/does_not_exist.py")),
    ("Result for case_1:",("calculator", "main.py")),
    ("Result for case_2:",("calculator", "main.py", ["3 + 5"])),
    ("Result for case_3:",("calculator", "tests.py")),
    ("Result for case_4:",("calculator", "../main.py")),
    ("Result for case_5:",("calculator", "nonexistent.py")),
    ("Result for case_6:",("calculator", "lorem.txt")),

]

if __name__ == "__main__":
    # result = get_file_content("calculator", "lorem.txt")
    # print("Lorem truncation test:")
    # print(result)
    for header, args in cases:
        print(header)
        print(run_python_file(*args))
