# My Project

Brief description of your project.

## Features

- Feature 1
- Feature 2

## Prerequisites

- Docker & Docker Compose
- Python 3.12.1 (for local development)
- Poetry

## Quick Start with Docker

\`\`\`bash
# Clone repository
git clone https://github.com/yourusername/my-project.git
cd my-project

# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
\`\`\`

## Local Development Setup

\`\`\`bash
# Set Python version
pyenv install 3.12.1
pyenv local 3.12.1

# Install dependencies
poetry install

# Activate virtual environment
poetry shell

# Run application
task run

# Run tests
task test

# Format code
task format

# Run all checks
task all
\`\`\`

## Available Tasks

\`\`\`bash
task format      # Format code with isort and black
task lint        # Run linters (flake8, mypy, pylint)
task security    # Run security checks with bandit
task test        # Run tests with coverage
task run         # Run application
task api         # Run FastAPI with hot-reload
task doc         # Serve documentation locally
task all         # Run format, lint, security, and test
\`\`\`

## Project Structure

\`\`\`
my-project/
├── src/app/           # Application code
├── tests/             # Test files
├── docs/              # Documentation
├── .github/workflows/ # CI/CD pipelines
└── Dockerfile         # Docker configuration
\`\`\`

## Documentation

Documentation is available at [http://localhost:8000](http://localhost:8000) when running `task doc`.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run `task all` to ensure code quality
5. Submit a pull request

## License

MIT License
