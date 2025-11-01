import ollama
import TkEasyGUI as tkgui
from get_env import get_model_name

# Default greeting prompt
default_prompt = """
给新的朋友写一封信。
思考一个很好的打招呼的开头。
既简洁又能够让人铭记在心。
"""

client = ollama.Client()
client_model = get_model_name()

# Show prompt in dialog for user to edit
prompt = tkgui.popup_memo(
    default_prompt.strip(),
    header="将用以下提示词生成问候语，请根据需要进行修改：",
    title="Ollama LLM 问候语生成器",
)

if prompt is None:
    tkgui.msg("未输入提示词，程序退出。", title="提示")
    quit()

# Loop to allow regeneration until user is satisfied
while True:
    # Generate response from Ollama
    response = client.generate(
        model=client_model,
        prompt=prompt,
        stream=False,
        options={"temperature": 0.7},
    )
    result = response.get("response", "")

    # Show the response in a dialog for user to accept or regenerate
    user_choice = tkgui.popup_memo(
        result,
        header="生成的问候语如下：\n\n如果满意，请点击“OK”按钮；如果需要重新生成，请点击“Cancel”按钮。",
        title="Ollama LLM 问候语生成器",
    )
    if user_choice is not None:
        break  # User accepted the result
