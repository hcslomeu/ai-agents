# Architecture Decision: Monorepo with Dual Docker Environments

## Context

This project demonstrates two popular AI agent frameworks: **LangChain/LangGraph** and **CrewAI**. These frameworks have **incompatible dependencies**:

- LangChain requires `openai >= 2.0`
- CrewAI requires `openai >= 1.83, < 1.84`

## Decision

We chose a **single repository with separate Docker environments** instead of two separate repositories.

## Alternatives Considered

### Option A: Separate Repositories (Not chosen)

```
ai-agents-langchain/   # Separate repo
ai-agents-crewai/      # Separate repo
```

**Pros:**

- Simpler CI/CD configuration
- Standard linting setup (no exclusions needed)
- Each repo is self-contained

**Cons:**

- Two repositories to maintain
- Duplicate infrastructure (CI/CD, docs, Docker configs)
- Harder to compare approaches side-by-side
- Less cohesive portfolio presentation

### Option B: Single Repository with Dual Docker (Chosen)

```
ai-agents/
├── src/langchain_examples/
├── src/crewai_examples/
├── Dockerfile.langchain
└── Dockerfile.crewai
```

**Pros:**

- Single portfolio project to showcase
- Shared documentation and infrastructure
- Easy to compare and contrast frameworks
- Demonstrates Docker multi-environment skills

**Cons:**

- Linters must exclude Docker-only directories
- CI/CD requires special configuration
- Packages not available for local type-checking

## Consequences

### CI/CD Configuration

Since the AI packages are only installed inside Docker containers (not in the CI environment), we must exclude the example directories from linting tools:

```yaml
# .github/workflows/ci.yml
poetry run flake8 src/ --exclude=src/langchain_examples,src/crewai_examples
poetry run pylint src/ --ignore=langchain_examples,crewai_examples
```

### Pre-commit Hooks

Same exclusions apply to pre-commit hooks:

```yaml
# .pre-commit-config.yaml
- id: flake8
  exclude: ^src/(langchain_examples|crewai_examples)/
```

### Type Checking

Mypy cannot validate imports from packages not installed locally:

```toml
# pyproject.toml
[tool.mypy]
exclude = [
    "src/langchain_examples/",
    "src/crewai_examples/",
]
```

### Running Code

Code must be executed inside Docker containers:

```bash
# LangChain examples
docker compose run --rm langchain python src/langchain_examples/script.py

# CrewAI examples
docker compose run --rm crewai python src/crewai_examples/script.py
```

## Conclusion

The added CI/CD complexity is a worthwhile trade-off for having a unified portfolio project that demonstrates:

1. Knowledge of multiple AI agent frameworks
2. Docker multi-environment architecture
3. Understanding of dependency management challenges
4. Ability to make and document architectural decisions

This decision showcases real-world engineering skills where trade-offs must be evaluated and documented.
