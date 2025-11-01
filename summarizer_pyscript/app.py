from get_root_env import get_model_name
from flask import Flask, request, render_template, jsonify
import ollama

# 初始化 Flask 应用
app = Flask(__name__)

# 初始化 Ollama 客户端和模型
client = ollama.Client()
client_model = get_model_name()


@app.route("/", methods=["GET", "POST"])
def index():
    """根路由"""
    # 如果是 GET 请求，直接渲染模板
    return render_template("index.html")


@app.route("/api/summarize", methods=["POST"])
def api_summarize():
    """API 接口：接收文本并返回摘要"""
    # Ajax 请求发送的 JSON 数据中包含 'text' 字段
    data = request.get_json()
    text = data.get("text", "")

    if not text.strip():
        return jsonify({"error": "输入文本不能为空"}), 400

    # 调用 LLM 生成摘要
    prompt = f"请为以下内容生成简洁的摘要：\n\n{text.strip()}"
    response = client.generate(
        model=client_model,
        prompt=prompt,
        options={"temperature": 0.5},
    )
    summary = response.get("response", "").strip()

    # 返回 JSON 格式的摘要结果
    return jsonify({"result": summary})


if __name__ == "__main__":
    app.run(debug=True)
