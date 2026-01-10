from functions.get_files_info import get_files_info

result_current = get_files_info("calculator", ".")
indented_current = "  " + result_current.replace("\n", "\n  ")
print("Result for current directory:")
print(indented_current)

result_pkg = get_files_info("calculator", "pkg")
indented_pkg = "  " + result_pkg.replace("\n", "\n  ")
print("Result for 'pkg' directory:")
print(indented_pkg)

result_bin = get_files_info("calculator", "/bin")
indented_bin = "  " + result_bin.replace("\n", "\n  ")
print("Result for '/bin' directory:")
print(indented_bin)

result_directory = get_files_info("calculator", "../")
indented_directory = "  " + result_directory.replace("\n", "\n  ")
print("Result for '../' directory:")
print(indented_directory)