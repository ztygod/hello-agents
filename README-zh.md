# hello-agent-cli

一个用于实验 LLM Agent 的 Python 项目。项目用 `HelloAgentsLLM` 封装兼容
OpenAI Chat Completions 的模型服务，并在此基础上实现对话 Agent。

当前项目重点包括：

- 统一的 OpenAI 兼容 LLM 客户端
- 带对话历史的 `Agent` 基类
- 支持普通调用和流式调用的 `SimpleAgent`
- 基于 `SimpleAgent` 继承改造的可扩展 Agent 示例

英文文档见 [README.md](README.md)。

## 环境要求

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) 用于依赖和虚拟环境管理
- 一个兼容 OpenAI API 的模型服务或 API Key

## 安装

在项目根目录安装依赖：

```powershell
uv sync
```

当前项目依赖：

```toml
hello-agents==0.1.1
```

## 配置

复制环境变量模板：

```powershell
Copy-Item .env.example .env
```

然后编辑 `.env`：

```env
LLM_API_KEY=YOUR_API_KEY
LLM_BASE_URL=YOUR_BASE_URL
LLM_MODEL_ID=YOUR_MODEL_ID
MODELSCOPE_API_KEY=YOUR_MODELSCOPE_API_KEY
```

`HelloAgentsLLM` 支持通过环境变量自动识别不同 Provider，例如：

- `OPENAI_API_KEY`
- `DEEPSEEK_API_KEY`
- `DASHSCOPE_API_KEY`
- `MODELSCOPE_API_KEY`
- `KIMI_API_KEY` 或 `MOONSHOT_API_KEY`
- `ZHIPU_API_KEY` 或 `GLM_API_KEY`
- `OLLAMA_API_KEY` 或 `OLLAMA_HOST`
- `VLLM_API_KEY` 或 `VLLM_HOST`

常用可选配置：

```env
DEBUG_TOOL=false
LOG_LEVEL=INFO
TEMPERATURE=0.7
MAX_TOKENS=1024
LLM_TIMEOUT=60
```

## 项目结构

```text
.
├── main.py
├── pyproject.toml
├── src
│   ├── agent
│   │   ├── simple_agent
│   │   │   ├── simple_agent.py
│   │   │   └── extensible_agent.py
│   │   ├── plan_solve_agent.py
│   │   ├── react_agent.py
│   │   └── reflection_agent.py
│   ├── core
│   │   ├── agent.py
│   │   ├── config.py
│   │   ├── exceptions.py
│   │   ├── llm.py
│   │   └── message.py
│   └── tools
│       ├── base.py
│       ├── registry.py
│       └── builtin
│           ├── calculator.py
│           └── search.py
```

其中 `plan_solve_agent.py`、`react_agent.py`、`reflection_agent.py` 和部分
`tools` 文件目前还是脚手架，后续可以继续补全。

## 基础用法

```python
from src.core.llm import HelloAgentsLLM
from src.agent.simple_agent.simple_agent import SimpleAgent


llm = HelloAgentsLLM(
    provider="deepseek",
    model="deepseek-chat",
)

agent = SimpleAgent(
    name="assistant",
    llm=llm,
    system_prompt="你是一个有帮助的 AI 助手。",
)

response = agent.run("用一段话解释什么是 Agent。")
print(response)
```

流式调用：

```python
for chunk in agent.stream_run("写一个简短的 Python 学习计划。"):
    print(chunk, end="", flush=True)
```

## 扩展 Agent

`ExtensibleSimpleAgent` 演示了如何继承 `SimpleAgent` 并重写核心运行逻辑。它预留了
工具注册表、增强系统提示词和多轮工具调用等扩展位置。

示例：

```python
from src.agent.simple_agent.extensible_agent import ExtensibleSimpleAgent


class MyAgent(ExtensibleSimpleAgent):
    def run(self, input_text: str, **kwargs):
        input_text = input_text.strip()
        return super().run(input_text, **kwargs)
```

常见扩展方向：

- 在构建消息前预处理用户输入
- 动态追加系统提示词
- 注入工具说明
- 自定义历史记录保存逻辑
- 增加多步推理或工具执行循环

## 运行

运行默认入口：

```powershell
uv run python main.py
```

运行自定义脚本：

```powershell
uv run python your_script.py
```

## 说明

- `HelloAgentsLLM` 面向兼容 OpenAI Chat Completions 的接口。
- `SimpleAgent` 通过 `Agent` 基类维护对话历史。
- `src/tools` 下的工具系统目前主要是框架占位，适合继续扩展工具注册和调用能力。
