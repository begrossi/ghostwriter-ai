import time
import logging
import openai
import tiktoken
import config

encoding = tiktoken.encoding_for_model(config.OPENAI_MODEL or config.OPENAI_ENGINE)

openai.api_base = config.OPENAI_API_BASE
openai.api_key = config.OPENAI_API_KEY
openai.api_type = config.OPENAI_API_TYPE
openai.api_version = config.OPENAI_API_VERSION
# openai.debug=True
# openai.log='debug'

# from https://learn.microsoft.com/en-us/answers/questions/1193969/how-to-integrate-tiktoken-library-with-azure-opena?orderby=oldest
def num_tokens_from_messages(messages):
    num_tokens = 0
    for message in messages:
        num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":  # if there's a name, the role is omitted
                num_tokens += -1  # role is always required and always 1 token
    num_tokens += 2  # every reply is primed with <im_start>assistant
    return num_tokens

def _check_num_tokens(messages, max_tokens=config.MAX_TOKENS):
    # remove messages until the number of tokens is below the limit
    # the first one is always an important system message, so we don't remove it
    # this is a very naive approach, but it works for now
    # TODO: improve this

    deleted = 0
    num_tokens = num_tokens_from_messages(messages)
    while (len(messages)>2 and num_tokens + max_tokens >= config.TOKEN_LIMIT):
        del messages[1] # index 0 is always an important system message, so we don't remove it
        deleted += 1
        num_tokens = num_tokens_from_messages(messages)
    
    if deleted > 0:
        logging.info(f">> Removed {deleted} messages. Number of tokens: {num_tokens}. Max tokens: {max_tokens}. Total Tokens: {num_tokens+max_tokens}. Limit: {config.TOKEN_LIMIT}. Num. of Messages: {len(messages)}")
    
    if num_tokens + max_tokens >= config.TOKEN_LIMIT:
        raise Exception(f"Number of tokens ({num_tokens}) still exceeds limit ({config.TOKEN_LIMIT})")

    return num_tokens

def get_retry_after(e, default=30):
    # get retru time from header
    if e.headers.get('Retry-After') is not None:
        return int(e.headers['Retry-After'])
    
    # try get retry time from error message
    try:
        return int(e.message.split('retry after ')[1].split(' seconds')[0])
    except:
        return default

# from https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/chatgpt?pivots=programming-language-chat-completions
def callOpenAI(prompt, history, waitingShortAnwser=False, forceMaximum=False, appendResponse=True):
    max_tokens = config.MAX_TOKENS_SHORT if waitingShortAnwser else config.MAX_TOKENS
    maxtokensstr = f' Try to use the maximum {max_tokens} tokens available.' if forceMaximum else ''
    history.append({"role": "user", "content": f'{prompt}\nLimit the output to {max_tokens} tokens.{maxtokensstr}'})
    _check_num_tokens(history, max_tokens)

    try:
        response = openai.ChatCompletion.create(
            engine=config.OPENAI_ENGINE,
            model=config.OPENAI_MODEL,
            temperature=config.TEMPERATURE,
            max_tokens=max_tokens,
            frequency_penalty=0.0,
            messages=history,
        )
        if response['choices'][0]['finish_reason'] == 'length':
            raise Exception("Number of tokens still exceeds limit")

        content = response['choices'][0]['message']['content']
    except openai.error.RateLimitError as e:
        retry_after = get_retry_after(e)+5
        logging.info(f">> Rate limit exceeded. Retrying in {retry_after} seconds.")
        time.sleep(retry_after)
        logging.info(">> Retrying...")
        history.pop() # remove prompt from history because it will be added again
        content = callOpenAI(prompt, history, appendResponse=False)

    if appendResponse:
        history.append({"role": "assistant", "content": content})

    time.sleep(5)
    return content
