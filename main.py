import os
import json
from openai import OpenAI
from dotenv import load_dotenv
import argparse
from openai.types.chat import ChatCompletionMessageParam, ChatCompletion
from prompt import system_prompt
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file


load_dotenv()

client= OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key= os.environ["HF_TOKEN"]
)

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()



messages: list[ChatCompletionMessageParam] = [
    {"role": "system", "content": system_prompt},
    {"role":"user", "content": args.user_prompt}
]

completion: ChatCompletion = client.chat.completions.create(
    model="deepseek-ai/DeepSeek-V4-Pro:novita",
    # messages=[
    #     {
    #         "role": "user",
    #         "content": "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
    #         "content": args.user_prompt
    #     }
    # ]
    messages=messages,
    tools=[schema_get_files_info, schema_get_file_content, schema_write_file, schema_run_python_file]
)

def main():
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {completion.usage.prompt_tokens}")
        print(f"Response tokens: {completion.usage.completion_tokens}")

    message = completion.choices[0].message
    tool_calls = message.tool_calls

    if tool_calls:
        for tool_call in tool_calls:
            fn = tool_call.function
            print(f"Calling function: {fn.name}({json.loads(fn.arguments)})")
    else:
        print(f"Response: {message.content}")


if __name__ == "__main__":
    main()
