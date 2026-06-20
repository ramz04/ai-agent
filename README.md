# AI Agent in Python

A terminal-based AI coding agent that can read, write, and execute files in a sandboxed working directory using LLM-driven tool calls.

## Prerequisites

- Python 3.14+
- [`uv`](https://docs.astral.sh/uv/getting-started/installation/) — install with:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

- A [Hugging Face](https://huggingface.co) account with an API token that has Inference access

## Installation

```bash
git clone https://github.com/Ramz04/ai-agent-py.git
cd ai-agent-py
uv sync
```

## Configuration

Create a `.env` file in the project root:

```env
HF_TOKEN=your_huggingface_token_here
```

The agent uses the Hugging Face Inference Router (`https://router.huggingface.co/v1`) with the `deepseek-ai/DeepSeek-V4-Pro:novita` model by default. To switch models or providers, update `base_url` and `model` in [`main.py`](main.py).

## Usage

```bash
uv run main.py "<your prompt>" [--verbose]
```

| Argument | Description |
|---|---|
| `<your prompt>` | Natural language instruction for the agent (required) |
| `--verbose` | Print token counts and full function call arguments |

### Examples

```bash
# List the files in the working directory
uv run main.py "what files are in the root?"

# Find and fix a bug, then re-run tests
uv run main.py "there's a bug in the calculator — find and fix it" --verbose

# Add a new feature
uv run main.py "add support for the ** exponentiation operator to the calculator"
```

The agent operates on the `./calculator` directory by default. To point it at a different codebase, change `working_directory` in [`call_function.py`](call_function.py).

## Available Tools

The agent can call four functions during a session:

| Function | Description |
|---|---|
| `get_files_info` | List files and directories with size and type info |
| `get_file_content` | Read a file's contents (truncated at 10,000 characters) |
| `write_file` | Create or overwrite a file |
| `run_python_file` | Execute a `.py` file and capture stdout/stderr |

All file paths are resolved relative to the working directory; paths outside it are rejected.

## Output

The agent prints each tool call as it runs, then prints a `Final response:` block when the model stops issuing tool calls. With `--verbose`, it also prints token usage per iteration and the full arguments passed to each function.

Example output:

```
 - Calling function: get_files_info
 - Calling function: get_file_content
 - Calling function: run_python_file
Final response:
All 9 tests pass. The bug was an off-by-one error in the tokeniser...
```

## Limitations

- **Working directory is hardcoded** — `./calculator` is set in [`call_function.py`](call_function.py) and must be changed manually to point the agent at a different project.
- **No undo** — `write_file` overwrites files immediately with no confirmation or backup; commit your work before running the agent on a real codebase.
- **Tool-calling reliability varies by model** — weaker models may omit required arguments (e.g. `file_path` for `run_python_file`), causing the call to fail gracefully but the task to stall.
- **Loop limit** — the agent stops after 20 LLM iterations regardless of whether the task is complete; increase `range(20)` in [`main.py`](main.py) for complex tasks.
