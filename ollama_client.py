import ollama
from get_env import get_model_name

# Make a ollama client call to generate a response
client = ollama.Client()
client_model = get_model_name()


def generate(prompt, stream=False, temperature=0.7):
    """Generate a response from the ollama model."""
    response = client.generate(
        model=client_model,
        prompt=prompt,
        stream=stream,
        options={"temperature": temperature},
    )
    return response.get("response", "")


if __name__ == "__main__":
    # Make a prompt
    prompt = """
        根据以下步骤，思考一个最独特的猫的名字：
        1. 选取10个候补
        2. 使用10层级对名字的独特性进行评分
        3. 从中选出评分最高的名字
    """

    print(generate(prompt))
