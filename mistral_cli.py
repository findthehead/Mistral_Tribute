import os
import sys
from dotenv import load_dotenv
load_dotenv()

try:
    from mistralai import Mistral
except Exception as e:
    raise ImportError(
        "Failed to import `mistralai`. Make sure the package is installed: `pip install mistralai`\n"
        f"Import error: {e}"
    )


def main(content):
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise RuntimeError(
            "Environment variable MISTRAL_API_KEY is not set. "
            "Set it and retry (e.g. `export MISTRAL_API_KEY=your_key`)."
        )
    mistral = Mistral(api_key=api_key)

    messages = [
        {
            "role": "user",
            "content": content,
        }
    ]
    if content == 'exit':
        print('Mistral: Bye')
        sys.exit()
    res = mistral.chat.complete(model="mistral-small-latest", messages=messages, stream=False)
    print('Mistral: '+res.choices[0].message.content)
if __name__=='__main__':
    while True:
        main(input("User? "))
