from get_root_env import get_model_name
from flask import Flask, request, render_template
import ollama

# 初始化 Flask 应用
app = Flask(__name__)

# 初始化 Ollama 客户端和模型
client = ollama.Client()
client_model = get_model_name()


@app.route("/", methods=["GET", "POST"])
def index():
    """根路由"""
    summary = None
    original_text = ""

    # 处理表单提交
    if request.method == "POST":
        # 获取用户输入的文本
        original_text = request.form.get("original_text", "").strip()
        # 如果输入文本不为空，调用 LLM 生成摘要
        if original_text:
            prompt = f"请为以下内容生成简洁的摘要：\n\n{original_text}"
            response = client.generate(
                model=client_model,
                prompt=prompt,
                options={"temperature": 0.5},
            )
            summary = response.get("response", "").strip()

    # 渲染模板并传递摘要和原始文本
    return render_template("index.html", summary=summary, original_text=original_text)


if __name__ == "__main__":
    app.run(debug=True)
