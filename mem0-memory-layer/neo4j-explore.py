# adding neo4j to config, helps in building knowledge graph in neo4j db instance.
# mem0 provides vector store + neo4j db instance connection/configuration.
# vector db stores the semantic meaning.
# graph db stores the relationships and exact textual content.
# mem_client queries both the grap and vector db and it updates both of them at same time.
from dotenv import load_dotenv
load_dotenv()
from os import getenv
from mem0 import Memory
from openai import OpenAI
import json
from qdrant_client import QdrantClient

api_key = getenv("GROQ_API_KEY")
neo4jURI = getenv("neo4j_URI")
neo4jUsername =getenv("neo4j_username")
neo4jPass = getenv("neo4j_pass")
qdrant_client_instance = QdrantClient(
    host="localhost", 
    port=6333, 
    timeout=60  # This sets the timeout at the client level
)

config = {
    "version": "v1.1",
    "embedder": {
        "provider": "ollama", # running locally with docker ollama
        "config": {
            "model": "nomic-embed-text",
            # "url": "http://localhost:11434" # already hardcodes to default url so this is not needed.
        }
    }, 
    "llm": {
        "provider": "groq",
        "config": {"api_key": api_key, "model": "qwen/qwen3-32b"}
    },
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "client": qdrant_client_instance,
            "embedding_model_dims": 768,
        }
    },
    # adding graph db for relationships#
    "graph_store": {
        "provider": "neo4j", 
        "config" : {
            "url": neo4jURI,
            "username": neo4jUsername,
            "password": neo4jPass
        }
    }
}

userQuery = "hey, my name is aditya and i am not a student anymore, i am working professional for acme.mc and i like to explore different technologies."
userID = "mem0_explore"

mem_client = Memory.from_config(config)

memory_dict = mem_client.search(query=userQuery, user_id=userID)
search_memory = memory_dict.get("results")
memories = [
    f"id:{mem.get('id')}\nMemory: {mem.get('memory')}" for mem in search_memory
]


SYSTEM_PROMPT= f"""
    Some context about the user: 
    {json.dumps(memories)}
"""
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=api_key
)

response = client.chat.completions.create(
    model = "qwen/qwen3-32b",
    messages = [
        {"role":"system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": userQuery}
    ]
)
llm_res = response.choices[0].message.content
print(llm_res)

mem_client.add(
    
    user_id=userID,
    messages=[
        {"role": "user", "content": userQuery},
        {"role": "assistant", "content": llm_res}

    ]
)

print("stored memory in qdrant")