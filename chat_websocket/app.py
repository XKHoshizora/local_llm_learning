from get_root_env import get_model_name
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import ollama

# 初始化 Flask 应用
app = Flask(__name__)
app.config['SECRET_KEY'] = 'hoshizora'

# 初始化 SocketIO
socketio = SocketIO(app)

# 初始化 Ollama 客户端和模型
client = ollama.Client()
client_model = get_model_name()


@app.route("/", methods=["GET", "POST"])
def index():
    """根路由"""
    # 如果是 GET 请求，直接渲染模板
    return render_template("index.html")

@socketio.on('user_message')
def handle_message(data):
    """处理用户消息"""
    user_message = data.get('message', '')
    print(f"用户消息: {user_message}")

    # 如果用户消息为空，则返回
    if not user_message.strip():
        return
    
    # 调用 LLM
    response = client.generate(
        model=client_model,
        prompt=user_message,
        options={"temperature": 0.7},
    )

    if 'response' in response:  
        # 如果 response 在 response 中，则获取响应
        response = response.get('response', '').strip()
    else:  
        # 如果 response 不在 response 中，则返回错误
        response = 'Sorry, I cannot answer that question.'

    # 发送响应给客户端
    emit('bot_response', {'model': client_model, 'response': response})
    # 打印响应
    print(f"{client_model} 回复: {response}")


if __name__ == "__main__":
    socketio.run(app, debug=True)
