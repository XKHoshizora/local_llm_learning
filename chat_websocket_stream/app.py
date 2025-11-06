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
    # 获取完整的历史消息列表
    messages = data.get('message', [])
    print(f"用户消息: {messages[-1]['content']}")

    # 如果消息列表为空，则返回
    if not messages:
        return
    
    # 发送开始信号
    emit('bot_stream_start', {'model': client_model})
    
    # 使用流式 API 调用 LLM
    stream = client.chat(
        model=client_model,
        messages=messages,
        options={"temperature": 0.7},
        stream=True,
    )

    bot_reply = ''
    for chunk in stream:
        # 获取响应内容
        if 'message' in chunk and 'content' in chunk['message']:
            subtext = chunk['message']['content'].strip()
        else:
            bot_reply = 'Sorry, I cannot answer that question.'
        
        # 发送响应给客户端
        emit('bot_stream_chunk', {'model': client_model, 'chunk': subtext})
        bot_reply += subtext

    # 流式生成完毕，发送结束信号
    emit('bot_stream_end', {'model': client_model, 'message': bot_reply})

    # 打印响应
    print(f"{client_model} 回复: {bot_reply}")
    print(f"---------------共有历史消息{len(messages)}条(不包含系统提示词)---------------")

if __name__ == "__main__":
    socketio.run(app, debug=True)
