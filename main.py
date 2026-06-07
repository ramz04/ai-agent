import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client= OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key= os.environ["HF_TOKEN"]
)

completion = client.chat.completions.create(
    model="deepseek-ai/DeepSeek-V4-Pro:novita",
    messages=[
        {
            "role": "user",
            "content": "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
        }
    ]
)

def main():
    print("Hello from ai-agent-py!")
    print(completion.choices[0].message)


if __name__ == "__main__":
    main()
