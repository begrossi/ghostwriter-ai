import os
import logging
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format='[%(levelname)s][%(module)s.%(funcName)s] %(message)s')
BASE_DIR=os.path.dirname(os.path.abspath(__file__))

load_dotenv(f'{BASE_DIR}/.env', verbose=True)  # take environment variables from .env.

def get_int_env(name, default):
    value = os.getenv(name)
    if value is None:
        return default
    else:
        return int(value)


OPENAI_ENGINE = os.getenv("OPENAI_ENGINE")
if OPENAI_ENGINE is None:
    raise ValueError("OPENAI_ENGINE is not set")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if OPENAI_API_KEY is None:
    raise ValueError("OPENAI_API_KEY is not set")

OPENAI_MODEL = os.getenv("OPENAI_MODEL")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE")
OPENAI_API_TYPE = os.getenv("OPENAI_API_TYPE")
OPENAI_API_VERSION = os.getenv("OPENAI_API_VERSION")

TEMPERATURE = 0.2 if os.getenv("TEMPERATURE") is None else float(os.getenv("TEMPERATURE"))
TOKEN_LIMIT = 4096 if os.getenv("TOKEN_LIMIT") is None else int(os.getenv("TOKEN_LIMIT"))
MAX_TOKENS = int(TOKEN_LIMIT/4) if os.getenv("MAX_TOKENS") is None else int(os.getenv("MAX_TOKENS"))
MAX_TOKENS_SHORT = int(MAX_TOKENS/4) if os.getenv("MAX_TOKENS_SHORT") is None else int(os.getenv("MAX_TOKENS_SHORT"))


BOOK_LANGUAGE = os.getenv("BOOK_LANGUAGE")
BOOK_TITLE = os.getenv("BOOK_TITLE")
BOOK_INSTRUCTIONS = os.getenv("BOOK_INSTRUCTIONS")

logging.info(f'''
>> Config:
TEMPERATURE: {TEMPERATURE}
TOKEN_LIMIT: {TOKEN_LIMIT}
MAX_TOKENS: {MAX_TOKENS}
MAX_TOKENS_SHORT: {MAX_TOKENS_SHORT}
'''.strip())