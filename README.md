# hello-agent-cli

A small Python project for experimenting with LLM-powered agents. It wraps
OpenAI-compatible chat completion APIs behind a unified `HelloAgentsLLM` client,
then builds simple conversation agents on top of that client.

The project currently focuses on:

- A common LLM client for OpenAI-compatible providers
- A base `Agent` abstraction with conversation history
- A `SimpleAgent` for single-turn and multi-turn chat
- An extensible simple agent example for custom behavior and optional tool use

Chinese documentation is available in [README-zh.md](README-zh.md).

## Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) for dependency and environment management
- An OpenAI-compatible LLM endpoint or API key

## Installation

Clone the project and install dependencies:

```powershell
uv sync
```

The project depends on:

```toml
hello-agents==0.1.1
```

## Configuration

Copy the example environment file:

```powershell
Copy-Item .env.example .env
```

Then edit `.env`:

```env
LLM_API_KEY=YOUR_API_KEY
LLM_BASE_URL=YOUR_BASE_URL
LLM_MODEL_ID=YOUR_MODEL_ID
MODELSCOPE_API_KEY=YOUR_MODELSCOPE_API_KEY
```

`HelloAgentsLLM` can also detect provider-specific variables, including:

- `OPENAI_API_KEY`
- `DEEPSEEK_API_KEY`
- `DASHSCOPE_API_KEY`
- `MODELSCOPE_API_KEY`
- `KIMI_API_KEY` or `MOONSHOT_API_KEY`
- `ZHIPU_API_KEY` or `GLM_API_KEY`
- `OLLAMA_API_KEY` or `OLLAMA_HOST`
- `VLLM_API_KEY` or `VLLM_HOST`

Common optional settings:

```env
DEBUG_TOOL=false
LOG_LEVEL=INFO
TEMPERATURE=0.7
MAX_TOKENS=1024
LLM_TIMEOUT=60
```

## Project Layout

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

Some files are placeholders for future agent and tool implementations.

## Basic Usage

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
    system_prompt="You are a helpful assistant.",
)

response = agent.run("Explain what an agent is in one paragraph.")
print(response)
```

Streaming usage:

```python
for chunk in agent.stream_run("Write a short Python learning plan."):
    print(chunk, end="", flush=True)
```

## Extending an Agent

`ExtensibleSimpleAgent` shows how to inherit from `SimpleAgent` and override the
core `run` flow. It adds a place for tool registry integration and enhanced
system prompts.

Example structure:

```python
from src.agent.simple_agent.extensible_agent import ExtensibleSimpleAgent


class MyAgent(ExtensibleSimpleAgent):
    def run(self, input_text: str, **kwargs):
        input_text = input_text.strip()
        return super().run(input_text, **kwargs)
```

Typical extension points are:

- Preprocess user input before building messages
- Add extra system prompt instructions
- Inject tool descriptions
- Customize history persistence
- Add multi-step reasoning or tool execution loops

## Running

Run the default entry point:

```powershell
uv run python main.py
```

Run a custom script:

```powershell
uv run python your_script.py
```

## Notes

- The LLM client is designed for OpenAI-compatible Chat Completions APIs.
- `SimpleAgent` stores conversation history through the base `Agent` class.
- Tool-related modules under `src/tools` are currently scaffolding and can be
  filled in as the agent framework grows.
