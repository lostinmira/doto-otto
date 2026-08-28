#!/usr/bin/env python3
"""
otto thought generator. openai/gpt

usage:
    python generate.py                                    # random thought
    python generate.py --reply "some text" --author "user" # reply to something
"""

import argparse
import os
import sys

import openai

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SYSTEM_PROMPT = open(os.path.join(SCRIPT_DIR, "system_prompt.txt")).read().strip()


def generate_thought(reply_to: str = None, author: str = None) -> str:
    client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    if reply_to and author:
        user_msg = f"@{author} said: \"{reply_to}\"\n\nwrite a reply. include ascii art if the moment calls for it."
    else:
        user_msg = "write a post for x. say something. include ascii art if you feel like it."

    response = client.chat.completions.create(
        model="gpt-4o",
        max_tokens=512,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_msg},
        ],
    )

    return response.choices[0].message.content.strip()


def main():
    parser = argparse.ArgumentParser(description="generate an otto thought")
    parser.add_argument("--reply", help="text to reply to")
    parser.add_argument("--author", help="author of the text being replied to")
    args = parser.parse_args()

    thought = generate_thought(reply_to=args.reply, author=args.author)
    print(thought)


if __name__ == "__main__":
    main()
