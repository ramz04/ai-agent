import os
import subprocess


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(working_dir_abs, file_path))

        if os.path.commonpath([working_dir_abs, target_path]) != working_dir_abs:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not target_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_path]
        if args:
            command.extend(args)
            result = subprocess.run(command, capture_output=True, text=True, timeout=30)
            if result.returncode != 0:
                return result.stdout + f"Process exited with code {result.returncode}"
            if len(result.stdout) == 0 and len(result.stderr) == 0:
                return "No output produced"
            return f"STDOUT: {result.stdout}\nSTDERR: {result.stderr}"
    except Exception as e:
        return f"Error: executing Python file: {e}"
