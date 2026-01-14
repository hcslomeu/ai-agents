# AI Agents Portfolio

A portfolio project demonstrating AI agent development using **LangChain/LangGraph** and **CrewAI** frameworks. Each framework runs in its own Docker environment to avoid dependency conflicts.

## Why Two Environments?

LangChain and CrewAI have incompatible dependencies:
- **LangChain/LangGraph** requires `openai >= 2.0`
- **CrewAI** requires `openai >= 1.83, < 1.84`

This project uses separate Docker containers to run both frameworks seamlessly.

## Project Structure

```
ai-agents/
├── src/
│   ├── langchain_examples/    # LangChain/LangGraph code
│   └── crewai_examples/       # CrewAI code
├── requirements/
│   ├── langchain.txt          # LangChain dependencies
│   └── crewai.txt             # CrewAI dependencies
├── Dockerfile.langchain
├── Dockerfile.crewai
├── docker-compose.yml
└── pyproject.toml             # Local dev tools (linting, testing)
```

## Prerequisites

- Docker & Docker Compose
- Python 3.12+ (for local development tools)
- Poetry (optional, for local linting/testing)

## Quick Start

### 1. Clone and configure

```bash
git clone https://github.com/yourusername/ai-agents.git
cd ai-agents

# Copy and configure environment variables
cp .env.example .env
# Edit .env with your API keys (OPENAI_API_KEY, etc.)
```

### 2. Build the Docker images

```bash
docker compose build
```

### 3. Run your code

```bash
# Run a LangChain script
docker compose run --rm langchain python src/langchain_examples/your_script.py

# Run a CrewAI script
docker compose run --rm crewai python src/crewai_examples/your_script.py

# Interactive shell (explore, test imports)
docker compose run --rm langchain
docker compose run --rm crewai
```

### 4. Run web apps (Streamlit/Gradio)

```bash
# Streamlit with hot reload (LangChain env)
docker compose run --rm --service-ports langchain streamlit run src/langchain_examples/app.py

# Gradio (LangChain env)
docker compose run --rm --service-ports langchain python src/langchain_examples/gradio_app.py

# Streamlit (CrewAI env) - uses port 8502
docker compose run --rm --service-ports crewai streamlit run src/crewai_examples/app.py
```

## Environment Details

### LangChain Environment

Includes the modern LangChain stack with OpenAI 2.x:

| Package | Description |
|---------|-------------|
| `langchain` | Core LangChain framework |
| `langgraph` | Multi-agent workflows and state machines |
| `langsmith` | Observability and tracing |
| `langchain-openai` | OpenAI integration |
| `langchain-ollama` | Local LLM support via Ollama |
| `langchain-chroma` | Vector store |
| `langchain-tavily` | Web search tool |
| `litellm` | Unified LLM API (100+ providers) |
| `mcp`, `fastmcp` | Model Context Protocol |
| `streamlit`, `gradio` | UI frameworks |

### CrewAI Environment

Focused CrewAI setup with OpenAI 1.x:

| Package | Description |
|---------|-------------|
| `crewai` | Multi-agent orchestration |
| `crewai-tools` | Built-in tools for agents |
| `ollama` | Local LLM support |
| `streamlit` | UI framework |

## Ports

| Service | Port | Description |
|---------|------|-------------|
| LangChain Streamlit | 8501 | `localhost:8501` |
| LangChain Gradio | 7860 | `localhost:7860` |
| LangChain FastAPI | 8000 | `localhost:8000` |
| CrewAI Streamlit | 8502 | `localhost:8502` |
| CrewAI FastAPI | 8001 | `localhost:8001` |
| PostgreSQL | 5432 | `localhost:5432` |

## Local Development (Optional)

For linting, testing, and code quality tools:

```bash
# Install Poetry dependencies
poetry install

# Available tasks
task format      # Format code (isort + black)
task lint        # Run linters (flake8, mypy, pylint)
task test        # Run tests with coverage
task security    # Security audit (bandit + pip-audit)
task all         # Run all checks
```

## Environment Variables

Create a `.env` file with your API keys:

```env
# Required
OPENAI_API_KEY=sk-...

# Optional (for specific features)
TAVILY_API_KEY=tvly-...
LANGSMITH_API_KEY=lsv2_...

# Database (if using PostgreSQL)
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=ai_agents
```

## License

MIT License
