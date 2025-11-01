import ollama
from get_env import get_model_name

# Call ollama to get a response from the model
response = ollama.generate(
    model=get_model_name(),
    prompt="给一只猫取一个名字。",
    stream=False,
    options={"temperature": 0.7},
)

# Print the response
print(response.get("response", ""))
