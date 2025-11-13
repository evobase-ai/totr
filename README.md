# ToTR 演示。

> 基于本地大模型（Ollama）的法律领域客户问题自动分类工具  
> Inspired by **ToTR V2: Vector-Aided Classification for Hierarchical Retrieval**

---

## 📌 项目简介

本项目实现了一个轻量级、高精度的**法律问题分类系统**，能够根据用户输入的自然语言问题，自动将其归类到预定义的法律条文类别中。

- **类别来源**：`data/` 目录下的所有 `.txt` 文件名（如 `侵权责任_饲养动物损害责任`）
- **推理引擎**：调用本地 **Ollama** 服务（兼容 OpenAI API）
- **核心模型**：支持 `qwen3` 等开源大模型
- **架构理念**：借鉴 [ToTR V2](pdf.html) 提出的 **向量辅助分类（VAC）** 思想，通过结构化类别标签 + 精准提示工程，实现高效、低幻觉的分类决策

> 💡 虽未实现完整 ToTR 层次检索，但本系统体现了其“**结构化知识 + 精确路由**”的核心思想。

---

## 🚀 快速开始

### 1. 环境准备

```bash
# 安装依赖（仅需 openai SDK）
pip install -r requirements.txt

# 安装并启动 Ollama
# 下载模型（以 qwen3 为例）
ollama pull qwen3
```

确保 Ollama 服务正在运行（默认监听 `http://localhost:11434`）。

### 2. 配置模型

编辑 `config/openai.json`：

```json
{
  "base_url": "http://localhost:11434/v1",
  "api_key": "ollama",
  "model": "qwen3:latest",
  "temperature": 0.0,
  "max_tokens": 100
}
```

> ✅ 支持任意 Ollama 模型（如 `llama3`, `phi3`, `mistral`），只需修改 `model` 字段。

### 3. 运行分类器

```bash
python run.py
```

交互式输入客户问题，系统将返回最匹配的法律类别：

```
请输入客户问题: 我在网上买的东西有质量问题，商家不给退怎么办？
【分类结果】合同_典型合同_买卖合同
```

---

## 📁 项目结构

```
.
├── config/
│   └── openai.json          # Ollama / OpenAI 配置
├── data/                    # 法律类别定义（文件名即类别）
├── src/
│   └── classifier.py        # 核心分类逻辑
├── run.py                   # 主程序入口
├── requirements.txt         # 依赖（仅 openai>=1.0.0）
└── pdf.html                 # ToTR V2 架构论文（含 VAC 设计思想）
```

---

## 🔍 技术亮点

| 特性 | 说明 |
|------|------|
| **本地运行** | 无需联网，数据不出内网，保障隐私安全 |
| **零训练成本** | 利用 LLM 的 zero-shot 能力，直接基于文件名分类 |
| **精准约束** | Prompt 强制模型从给定类别中选择，杜绝幻觉 |
| **低延迟** | `temperature=0.0` + 小模型 = 快速稳定响应 |
| **ToTR 启发** | 采用结构化类别标签，模拟 SCK（结构化压缩键）思想 |

---

## 📄 关于 ToTR V2

本项目受 `pdf.html` 中提出的 **ToTR V2 架构**启发：
- 使用**结构化类别名称**（如 `合同_典型合同_买卖合同`）作为知识树节点
- 通过**精确提示词**引导模型进行层次化路由决策
- 虽未实现向量主路由（VAC Mode 1），但为未来集成 FAISS / Milvus 留下扩展空间

> 📖 详细架构请查阅 [`pdf.html`](pdf.html)

---

## 🛠️ 扩展建议

- ✅ **集成向量检索**：对类别名嵌入，实现“向量初筛 + LLM 精排”的 VAC 双模式
- ✅ **支持多级分类**：递归调用分类器，实现真正的 ToTR 层次导航
- ✅ **Web 界面**：结合 Gradio 快速部署演示界面

---

