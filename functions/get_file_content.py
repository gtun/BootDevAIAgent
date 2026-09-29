import os
import config

def get_file_content(working_directory: str, file_path: str) -> str:
    working_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
    file_in_working_directory = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
    
    try:
        if not file_in_working_directory:
            raise Exception(f'Cannot read "{file_path}" as it is outside the permitted working directory')
        if not os.path.isfile(target_file):
            raise Exception(f'File not found or is not a regular file: "{file_path}"')
        
        with open(target_file, "r") as f:
            file_contents = f.read(config.FILE_CONTENT_LIMIT)
            # After reading the first MAX_CHARS...
            if f.read(1):
                file_contents += f'[...File "{target_file}" truncated at {config.FILE_CONTENT_LIMIT} characters]'
        
        return(file_contents)
    except Exception as e:
        return f'Error: {e}'
    
schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": f"Returns the content of the specified file at the file path, truncated to {config.FILE_CONTENT_LIMIT} characters",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to file to get the content from",
                },
            },
            "required": ["file_path"],
        },
    },
}