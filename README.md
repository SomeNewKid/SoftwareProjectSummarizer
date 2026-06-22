# Software Project Summarizer

Software Project Summarizer is a small Python command-line sample for exploring
LangChain's Deep Agents framework. It accepts the path to a local software
project, lets a DeepAgent inspect selected files through read-only local tools,
and prints a high-level summary of what the project does and how it works.

> [!WARNING]
> This is an experimental project and should not be considered production-ready.

The project was created to learn the basics of DeepAgent, including custom
tools, model-driven file selection, and controlled local filesystem access. It
is intentionally small and is not intended to be a robust general-purpose code
analysis system.

## What It Does

The CLI accepts a local project directory such as:

```powershell
.\.venv\Scripts\python.exe -m software_project_summarizer C:\Git\ExampleProject
```

The agent then:

- calls a local tool to inspect the accessible project tree
- chooses useful source, configuration, test, and metadata files to inspect
- reads selected files through a controlled local file-reading tool
- avoids README files so the summary is based on code and project metadata
- prints a Markdown summary of the project's purpose, language, frameworks, and
  high-level execution flow

The local tools restrict what the agent can see. Hidden directories, generated
directories, dependency folders, virtual environments, README files, and large
files are excluded from inspection.

## Requirements

- Python 3.11.
- PowerShell on Windows.
- An `OPENAI_API_KEY` environment variable for OpenAI model calls.

## Setup

Create the virtual environment and install the project with development
dependencies:

```powershell
.\scripts\setup-dev.ps1
```

The setup script expects Python 3.11 at the path configured in
`scripts\setup-dev.ps1`.

## Running

Run the summarizer from the repository root and pass the project directory to
inspect:

```powershell
.\.venv\Scripts\python.exe -m software_project_summarizer C:\Git\ExampleProject
```

The command prints the final agent-generated summary. Tool calls may also be
printed when verbose debugging is enabled in `src/software_project_summarizer/tools.py`.

## Development Checks

Run formatting, linting, type checking, and tests:

```powershell
.\scripts\check.ps1
```

This runs:

- `ruff format .`
- `ruff check .`
- `pyright`
- `pytest`

## Project Structure

```text
src/software_project_summarizer/
  __main__.py   Package entry point for python -m software_project_summarizer
  cli.py        Command-line argument handling and console output
  agent.py      DeepAgent setup, prompt, model configuration, and agent run
  tools.py      Read-only project tree and file-reading tools
  utilities.py  File and directory inspection rules

tests/
  test_smoke.py
  test_utlities.py

scripts/
  setup-dev.ps1
  check.ps1
```

## Notes

This project is a DeepAgent learning exercise. It deliberately gives the model
only two project-inspection tools: one for the directory tree and one for
reading permitted files. The Python code controls filesystem access, while the
agent decides which visible files are worth reading.

README files are intentionally excluded so the agent must infer the project
purpose from source code, tests, and metadata instead of relying on a human
summary.

Agent behavior and final wording can vary between runs because file selection
and summarization are model-driven. OpenAI API calls may incur usage costs.

## Third-Party Notices

This project has direct runtime dependencies on third-party Python packages,
including `deepagents`, `langchain-openai`, and `pathspec`. See each package's
PyPI license metadata for full license and notice terms.

## License

GNU General Public License v3.0. See the `LICENSE` file for details.
