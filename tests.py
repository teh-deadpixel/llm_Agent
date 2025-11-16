from functions.get_files_info import get_files_info

cases = [
    ("Result for current directory:", ("calculator", ".")),
    ("Result for 'pkg' directory:", ("calculator", "pkg")),
    ("Result for '/bin' directory:", ("calculator", "/bin")),
    ("Result for '../' directory:", ("calculator", "../")),
]

if __name__ == "__main__":
    for header, args in cases:
        print(header)
        print(get_files_info(*args))
