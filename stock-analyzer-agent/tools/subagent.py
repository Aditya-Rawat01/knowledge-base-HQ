from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
from pydantic import BaseModel, Field
from typing import Literal
from pydantic import SecretStr

load_dotenv()

api_key = os.getenv("GROQ_API_KEY_SUB_AGENT") 

if not api_key:
    raise Exception("Groq API key not found")

llm = ChatGroq(
    api_key=SecretStr(api_key),
    model="qwen/qwen3-32b",
    temperature=0,
    max_tokens=2000,
    timeout=None,
)

class SentimentResponse(BaseModel):
    sentiment_score: float = Field(description="A score between -1.0 and 1.0")
    label: Literal["Bullish", "Bearish", "Neutral"] = Field(description="One word: Bullish, Bearish or Neutral")
    summary: str = Field(description="A 2-sentence summary for the overall news sentiment.")


structuredllm = llm.with_structured_output(schema=SentimentResponse)

