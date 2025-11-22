# from functions.get_files_info import get_files_info
#from functions.get_file_content import get_file_content
from functions.write_file import write_file

cases = [
    # ("Result for current directory:", ("calculator", "main.py")),
    # ("Result for 'pkg' directory:", ("calculator", "pkg/calculator.py")),
    # ("Result for '/bin' directory:", ("calculator", "/bin/cat")),
    # ("Result for '../' directory:", ("calculator", "pkg/does_not_exist.py")),
    ("Result for case_1:",("calculator", "lorem.txt", "wait, this isn't lorem ipsum")),
    ("Result for case_2:",("calculator",  "pkg/morelorem.txt", "lorem ipsum dolor sit amet")),
    ("Result for case_3:",("calculator", "/tmp/temp.txt", "this should not be allowed"))

]

if __name__ == "__main__":
    # result = get_file_content("calculator", "lorem.txt")
    # print("Lorem truncation test:")
    # print(result)
    for header, args in cases:
        print(header)
        print(write_file(*args))
