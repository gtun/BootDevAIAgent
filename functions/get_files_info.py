import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

        print("Result for current directory:")

        if not os.path.isdir(target_dir):
            raise Exception(f'{directory} is not a directory')
        if not valid_target_dir:
            raise Exception(f'Cannot list "{directory}" as it is outside the permitted working directory')
        
        file_list = [f for f in os.listdir(target_dir) if not f.startswith("__") and not f.endswith("__") and not f.startswith(".")]
        for file in file_list:
            print(f"  - {file}: file_size={os.path.getsize(os.path.join(target_dir, file))} bytes, is_dir={os.path.isdir(os.path.join(target_dir, file))}")
        return f'Success: "{directory}" is within the working directory'
    except Exception as e:
        return f'Error: {e}'