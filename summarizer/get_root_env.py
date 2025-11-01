# fmt: off
import sys
from pathlib import Path

# 必须在导入根目录的 get_env.py 之前添加路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from get_env import get_model_name as gmn
# fmt: on


def get_model_name():
    """获取模型名称的包装函数"""
    return gmn()


if __name__ == "__main__":
    print("使用模型：", get_model_name)
