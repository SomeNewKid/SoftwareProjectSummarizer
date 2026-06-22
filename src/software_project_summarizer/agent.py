"""The Software Project Summarizer agent."""

from __future__ import annotations

from pathlib import Path

from deepagents import HarnessProfile, create_deep_agent, register_harness_profile

from software_project_summarizer.tools import create_project_tools

_SYSTEM_PROMPT = """
You are a software project summarizer.

You inspect source code repositories using only the provided tools.

Before writing the final answer, you must read at least one source code 
file using read_project_file.

If the project tree contains dependency or project metadata files such as 
pyproject.toml, package.json, *.csproj, Cargo.toml, go.mod, or pom.xml, 
you should read the most relevant one unless it is inaccessible.

Do not summarize the project from the directory tree alone. 
The project tree is only a starting point for choosing files to inspect.

The summary should use Markdown formatting.

Important rules:
- Start by requesting and inspecting the project tree.
- Decide which source, configuration, test, and metadata files are useful.
- Prefer direct evidence from code and project metadata.
- Do not try to read every file unless the project is very small.
- Summarize what the software does and how it works at a high level.
- Mention uncertainty where the available files do not prove something.

Your final answer should include:
- Purpose
- Primary language
- Main frameworks or libraries
- Important files inspected
- High-level execution flow
- Notable architecture
- Unknowns or assumptions
"""

MODEL_NAME = "openai:gpt-4o"


def summarize_project(project_directory: Path) -> str:
    """Summarize a software project repository."""
    tools = create_project_tools(project_directory)

    register_harness_profile(
        MODEL_NAME,
        HarnessProfile(
            excluded_tools=frozenset(
                {"ls", "read_file", "write_file", "edit_file", "glob", "grep"}
            ),
        ),
    )

    agent = create_deep_agent(
        model=MODEL_NAME, tools=tools, system_prompt=_SYSTEM_PROMPT
    )

    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": (
                        "Inspect the accessible project directory and summarize "
                        "what the software does and how it works."
                    ),
                }
            ]
        }
    )

    final_message = result["messages"][-1]
    content = final_message.content

    if isinstance(content, str):
        return content

    return "\n".join(block["text"] for block in content if block.get("type") == "text")
