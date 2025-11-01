import os
from pathlib import Path
from dotenv import load_dotenv

# 使用 pathlib 构建路径
env_path = Path(__file__).parent / '.env'

# 加载环境变量
load_dotenv(dotenv_path=env_path)


def get_model_name():
    """获取模型名称的环境变量"""
    return os.getenv('MODEL_NAME', 'gpt-oss')  # 默认值为 'gpt-oss'
