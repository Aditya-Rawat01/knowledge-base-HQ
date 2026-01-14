from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

load_dotenv()


def getllm(llm:str):
    match llm:
        case "openai":
            return init_chat_model(model="gpt-4o", model_provider=llm)
        case "anthropic":
            return init_chat_model(model="claude-3-5-sonnet-latest", model_provider=llm)
        case "google_genai":
            return init_chat_model(model="gemini-2.5-flash", model_provider=llm)
        case "huggingface":
            return init_chat_model(model="meta-llama/Meta-Llama-3.1-70B-Instruct", model_provider=llm)
        case "groq":
            return init_chat_model(model="llama-3.3-70b-versatile", model_provider=llm)
        case "ollama":
            return init_chat_model(model="gemma:2b", model_provider=llm)
        case _:
            raise ValueError("sorry this provider is not configured!")

try:
    llm = getllm("groq")
except ValueError as e:
    print(e)
