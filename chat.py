import tiktoken
import openai
import os
from dotenv import load_dotenv

load_dotenv('book-writer-ai/.env')  # take environment variables from .env.

OPENAI_ENGINE = os.getenv("OPENAI_ENGINE")
openai.api_base = os.getenv("OPENAI_API_BASE")
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_type = os.getenv("OPENAI_API_TYPE")
openai.api_version = os.getenv("OPENAI_API_VERSION")
#openai.debug=True
#openai.log='debug'

system_message = {"role": "system", "content": "You are a helpful assistant."}
max_response_tokens = 250
token_limit = 4096
conversation = []
conversation.append(system_message)


def num_tokens_from_messages(messages):
    encoding= tiktoken.get_encoding("cl100k_base")  #model to encoding mapping https://github.com/openai/tiktoken/blob/main/tiktoken/model.py
    num_tokens = 0
    for message in messages:
        num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":  # if there's a name, the role is omitted
                num_tokens += -1  # role is always required and always 1 token
    num_tokens += 2  # every reply is primed with <im_start>assistant
    return num_tokens

while True:
    user_input = input("")     
    conversation.append({"role": "user", "content": user_input})
    conv_history_tokens = num_tokens_from_messages(conversation)

    while conv_history_tokens + max_response_tokens >= token_limit:
        del conversation[1] 
        conv_history_tokens = num_tokens_from_messages(conversation)

    response = openai.ChatCompletion.create(
        engine=OPENAI_ENGINE, # The deployment name you chose when you deployed the GPT-35-Turbo or GPT-4 model.
        messages=conversation,
        temperature=0.7,
        max_tokens=max_response_tokens,
    )

    content = response['choices'][0]['message']['content']
    conversation.append({"role": "assistant", "content": content})
    print("\n" + content + "\n")
