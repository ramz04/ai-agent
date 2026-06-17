import json
from collections.abc import Callable

from openai.types.chat import ChatCompletionMessageToolCall

from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

function_map: dict[str, Callable[..., str]] = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "write_file": write_file,
    "run_python_file": run_python_file,
}


def call_function(tool_call: ChatCompletionMessageToolCall, verbose: bool = False) -> dict:
    function_name = tool_call.function.name or ""

    if verbose:
        print(f"Calling function: {function_name}({json.loads(tool_call.function.arguments)})")
    else:
        print(f" - Calling function: {function_name}")

    if function_name not in function_map:
        return {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps({"error": f"Unknown function: {function_name}"}),
        }

    args = json.loads(tool_call.function.arguments) if tool_call.function.arguments else {}
    args["working_directory"] = "./calculator"

    try:
        function_result = function_map[function_name](**args)
    except Exception as e:
        function_result = f"Error: {e}"

    return {
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": json.dumps({"result": function_result}),
    }
