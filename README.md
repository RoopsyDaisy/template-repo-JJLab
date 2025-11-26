# Template for new projects that run through vscode devcontainers on the Johnson lab PC

# Project Name

Brief description of your project.

## Quick Start

1. Make sure Dev Containers in vscode is using podman rather than docker
2. **Clone and open in VS Code** with Dev Containers extension
3. VS Code will prompt to "Reopen in Container" - accept
4. Wait for container build and `uv sync` to complete
5. **Open `default.code-workspace`** to see data mounts in the explorer
6. Start coding!

> **Tip**: Opening the `.code-workspace` file gives you a multi-root workspace with 
> `/run/media` and `/run/data_raid5` visible in the file explorer alongside your code.

## Manual Setup (without devcontainer)

\`\`\`bash
# Install uv if not present
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync

# Activate environment
source .venv/bin/activate
\`\`\`

## Development

\`\`\`bash
# Run tests
uv run pytest

# Lint
uv run ruff check src/

# Format
uv run black src/ tests/
\`\`\`

## Project Structure

- `src/<package>/` - Main package code
- `tests/` - Test files
- `notebooks/` - Jupyter notebooks
- `.devcontainer/` - VS Code devcontainer config
- `.github/agents/` - Copilot agent definitions
