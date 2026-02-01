from langchain_groq import ChatGroq
from dotenv import load_dotenv
from tools.tools_export import available_tools
import os
from pydantic import SecretStr
load_dotenv()

api_key = os.getenv("GROQ_API_KEY_MAIN_AGENT") 

if not api_key:
    raise Exception("Groq API key not found")

llm = ChatGroq(
    api_key=SecretStr(api_key),
    model="openai/gpt-oss-120b",
    temperature=0,
    max_tokens=2000,
    timeout=None,
)

llm_with_tools = llm.bind_tools(available_tools)

