import ollama
from get_env import get_model_name

# Initialize Ollama client and model
client = ollama.Client()
client_model = get_model_name()
default_prompt = """
给新的朋友写一封信。
思考一个很好的打招呼的开头。
既简洁又能够让人铭记在心。
"""

stream = client.generate(
    model=client_model,
    prompt=default_prompt,
    stream=True,
    options={"temperature": 0.7},
)

for chunk in stream:
    subtext = chunk.get("response", "")
    print(subtext, end="", flush=True)

print("\n---\n")
