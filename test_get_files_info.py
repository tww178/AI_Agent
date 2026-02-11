from functions.get_files_info import get_files_info


def log_execution(func):
    def wrapper(*args, **kwargs):
        print(f"Result for {args[1]} directory:\n")
        return func(*args, **kwargs)
    return wrapper



test = log_execution(get_files_info)
print(test("calculator", "."))
print(test("calculator", "pkg"))
print(test("calculator", "/bin"))
print(test("calculator", "../"))