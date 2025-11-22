# from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content

cases = [
    ("Result for current directory:", ("calculator", "main.py")),
    ("Result for 'pkg' directory:", ("calculator", "pkg/calculator.py")),
    ("Result for '/bin' directory:", ("calculator", "/bin/cat")),
    ("Result for '../' directory:", ("calculator", "pkg/does_not_exist.py")),
]

if __name__ == "__main__":
    # result = get_file_content("calculator", "lorem.txt")
    # print("Lorem truncation test:")
    # print(result)
    for header, args in cases:
        print(header)
        print(get_file_content(*args))
