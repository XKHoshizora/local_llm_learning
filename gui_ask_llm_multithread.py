import ollama
import TkEasyGUI as tkgui
from get_env import get_model_name

# Initialize Ollama client and model
client = ollama.Client()
client_model = get_model_name()
default_prompt = """
给新的朋友写一封信。
思考一个很好的打招呼的开头。
既简洁又能够让人铭记在心。
"""

# Castom dialog layout
layout = [
    [tkgui.Text("将用以下提示词生成问候语，请根据需要进行修改：")],
    [tkgui.Multiline(default_prompt.strip(), size=(60, 10), key="-Prompt-")],
    [tkgui.Button("生成问候语"), tkgui.Button("退出")],
    [tkgui.Multiline("", size=(60, 15), key="-Result-")],
]
window = tkgui.Window("Ollama LLM 问候语生成器", layout)


def thread_llm(prompt):
    """在单独线程中调用 LLM 生成响应"""
    # LLM 生成响应
    response = client.generate(
        model=client_model,
        prompt=prompt,
        stream=False,
        options={"temperature": 0.7},
    )
    result = response.get("response", "")
    window.post_event("生成完毕", {"result": result})


# Event loop
while True:
    # Read events and values
    event, values = window.read()
    if event in (tkgui.WINDOW_CLOSED, "退出"):
        break
    if event == "生成问候语":
        prompt = values["-Prompt-"].strip()
        if not prompt:
            tkgui.msg("未输入提示词，无法生成问候语。", title="提示")
            continue
        # 禁用按钮以防重复点击
        window["生成问候语"].update(disabled=True)
        # 启动线程调用 LLM
        window.start_thread(thread_llm, prompt=prompt)
    elif event == "生成完毕":
        result = values["result"]
        window["-Result-"].update(result)
        window["生成问候语"].update(disabled=False)
