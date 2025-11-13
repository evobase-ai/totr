import os
import json
from openai import OpenAI
from pathlib import Path


def load_categories(data_dir: str = "data") -> list:
    """加载 data/ 目录下所有 .txt 文件的文件名（不含扩展名）作为类别"""
    categories = []
    data_path = Path(data_dir)
    if not data_path.exists():
        raise FileNotFoundError(f"目录 {data_dir} 不存在")
    
    for file in data_path.glob("*.txt"):
        category = file.stem  # 去掉 .txt 后缀
        categories.append(category)
    
    if not categories:
        raise ValueError(f"目录 {data_dir} 中没有找到 .txt 文件")
    
    return sorted(categories)


def classify_customer_query(query: str, categories: list, config_path: str = "config/openai.json") -> str:
    """使用 OpenAI 兼容 API（如 Ollama）对客户问题进行分类"""
    # 加载配置
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)
    
    base_url = config.get("base_url", "http://localhost:11434/v1")  # 默认 Ollama 地址
    api_key = config.get("api_key", "ollama")  # Ollama 通常使用 "ollama" 作为占位 key
    model = config.get("model", "qwen:7b")     # 示例模型，请根据实际调整
    temperature = config.get("temperature", 0.0)
    max_tokens = config.get("max_tokens", 100)

    # 初始化 OpenAI 客户端（兼容 Ollama）
    client = OpenAI(
        base_url=base_url,
        api_key=api_key
    )

    # 构造 prompt
    categories_str = "\n".join(categories)
    prompt = f"""你是一个法律问题分类专家。请根据以下客户问题，从给定的类别列表中选择最匹配的一个类别。

类别列表：
{categories_str}

客户问题：
{query}

要求：
- 只输出类别名称，不要任何解释、标点或额外文字。
- 必须严格从上述类别列表中选择，不能自行编造。
"""

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        result = response.choices[0].message.content.strip()
        return result
    except Exception as e:
        raise RuntimeError(f"调用大模型 API 失败: {e}")


if __name__ == "__main__":
    # 示例用法
    query = "我在小区被狗咬了，狗主人要负责吗？"
    try:
        cats = load_categories()
        result = classify_customer_query(query, cats)
        print(f"客户问题: {query}")
        print(f"分类结果: {result}")
    except Exception as e:
        print(f"错误: {e}")