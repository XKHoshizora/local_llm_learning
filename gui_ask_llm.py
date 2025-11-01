import ollama
import TkEasyGUI as tkgui
from get_env import get_model_name

# Ollama API client
client = ollama.Client()
client_model = get_model_name()

# daylog style prompt
prompt = tkgui.input("请输入你的提示词", title="Ollama LLM 提示词输入", default="你好！")

if prompt is None:
    tkgui.msg("未输入提示词，程序退出。", title="提示")
    quit()

# Generate response from Ollama
response = client.generate(
    model=client_model,
    prompt=prompt,
    stream=False,
    options={"temperature": 0.7},
)

result = response.get("response", "")

# Show the response in a message box
tkgui.popup_memo(result, title="Ollama LLM 响应")
