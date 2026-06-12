import os
from openai import OpenAI
from dotenv import load_dotenv
import argparse
from openai.types.chat import ChatCompletionMessageParam, ChatCompletion

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
    messages=messages
)

def main():
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {completion.usage.prompt_tokens}")
        print(f"Response tokens: {completion.usage.completion_tokens}")
        print(f"Response: {completion.choices[0].message.content}")
    else:
        print(f"Response: {completion.choices[0].message.content}")


if __name__ == "__main__":
    main()
