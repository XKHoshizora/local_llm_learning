import requests
from get_env import get_model_name

# Ollama API base URL
BASE_URL = "http://localhost:11434"


def generate(prompt, model=get_model_name()):
    """/api/generate endpoint"""

    # URL for the generate endpoint
    url = BASE_URL + "/api/generate"
    # Request payload
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "temperature": 0.7,
    }
    # Make the POST request
    response = requests.post(url, json=payload)
    # Check for successful response
    if response.status_code == 200:
        data = response.json()
        return data.get("response", "")
    else:
        raise Exception(f"Error: {response.status_code}, {response.text}")


if __name__ == "__main__":
    # Example usage
    print(generate("给一只猫取一个名字。"))
