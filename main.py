import os
import json
import sys
from openai import OpenAI
from dotenv import load_dotenv
import argparse
from openai.types.chat import ChatCompletionMessageParam
from prompt import system_prompt
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file
from call_function import call_function


load_dotenv()

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.environ["HF_TOKEN"],
)

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

tools = [schema_get_files_info, schema_get_file_content, schema_write_file, schema_run_python_file]

messages: list[ChatCompletionMessageParam] = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": args.user_prompt},
]


def main():
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")

    for _ in range(20):
        completion = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-V4-Pro:novita",
            messages=messages,
            tools=tools,
        )

        if args.verbose:
            print(f"Prompt tokens: {completion.usage.prompt_tokens}")
            print(f"Response tokens: {completion.usage.completion_tokens}")

        message = completion.choices[0].message
        messages.append(message)  # type: ignore

        tool_calls = message.tool_calls

        if not tool_calls:
            print(f"Final response:\n{message.content}")
            return

        for tool_call in tool_calls:
            result = call_function(tool_call, verbose=args.verbose)
            content = json.loads(result["content"])
            if not content:
                raise Exception("Empty response from function call")
            if "result" not in content and "error" not in content:
                raise Exception("No result in function response")
            if args.verbose:
                print(f"-> {content.get('result', content.get('error'))}")
            messages.append(result)  # type: ignore

    print("Error: maximum iterations reached without a final response")
    sys.exit(1)


if __name__ == "__main__":
    main()
