import tiktoken
def count_tokens(messages):
    encoding = tiktoken.get_encoding("cl100k_base")
    # Simple estimation: Dump messages to string and count
    text = "".join([m.content for m in messages])
    return len(encoding.encode(text))