# CodeBuddy Agent SDK Integration Guide

This guide explains how to use CodeBuddy Agent SDK as the LLM backend for OpenManus, replacing or supplementing the default OpenAI-based implementation.

## Overview

OpenManus now supports two LLM backends:
- **OpenAI Backend** (default): Direct OpenAI API calls
- **CodeBuddy Backend** (new): CodeBuddy Agent SDK integration

The CodeBuddy integration provides:
- ✅ Full tool calling capability with OpenManus tools
- ✅ Multi-step reasoning and planning
- ✅ Memory and conversation history
- ✅ MCP server integration
- ✅ Browser automation
- ✅ Same "Manus effect" user experience

## Installation

### 1. Install CodeBuddy SDK

```bash
pip install codebuddy-agent-sdk
```

Or add to `requirements.txt`:
```
codebuddy-agent-sdk>=0.1.0
```

### 2. Install CodeBuddy CLI (Optional)

The SDK includes a bundled CLI, but you can optionally specify a custom path:

```bash
# Download and install CodeBuddy CLI
# Follow instructions from https://www.codebuddy.ai/docs/cli/installation
```

## Configuration

### Method 1: Modify Existing Config

Edit your `config/config.toml`:

```toml
[llm]
# Switch to CodeBuddy backend
backend = "codebuddy"

model = "gpt-4o"
base_url = "https://api.openai.com/v1"  # Used by CodeBuddy for model access
api_key = "your-api-key-here"           # Your OpenAI/Claude/etc API key
max_tokens = 4096
temperature = 0.0
api_type = "openai"
api_version = ""

# CodeBuddy-specific settings
permission_mode = "bypassPermissions"    # Recommended: let OpenManus handle tool permissions
# codebuddy_code_path = "/custom/path/to/codebuddy"  # Optional: custom CLI path
```

### Method 2: Use Example Config

Copy the CodeBuddy example configuration:

```bash
cp config/config.example-codebuddy.toml config/config.toml
```

Then edit `config/config.toml` to add your API keys.

### Configuration Options

#### `backend`
- **Type**: `string`
- **Default**: `"openai"`
- **Options**: `"openai"` or `"codebuddy"`
- **Description**: Selects which LLM backend to use

#### `permission_mode`
- **Type**: `string`
- **Default**: `"bypassPermissions"`
- **Options**:
  - `"default"`: All operations require confirmation
  - `"acceptEdits"`: Auto-approve file edits
  - `"plan"`: Planning mode, only allow reads
  - `"bypassPermissions"`: Skip all permission checks (recommended for OpenManus)
- **Description**: Controls CodeBuddy's permission system. Use `"bypassPermissions"` to let OpenManus handle tool execution.

#### `codebuddy_code_path`
- **Type**: `string` (optional)
- **Default**: `None` (uses bundled CLI)
- **Description**: Path to custom CodeBuddy CLI executable

## Usage

Once configured, use OpenManus normally. The CodeBuddy backend is transparent:

```bash
# Run with default prompt
python main.py

# Run with specific prompt
python main.py --prompt "Analyze the sales data in data.csv"

# Run MCP version
python run_mcp.py

# Run multi-agent flow
python run_flow.py
```

## Architecture

### High-Level Flow

```
User Prompt
    ↓
Manus Agent
    ↓
ToolCallAgent.think()
    ↓
LLM Factory (checks config.backend)
    ├── "openai" → OpenAI LLM (original)
    └── "codebuddy" → CodeBuddy LLM (new)
         ↓
    CodeBuddy SDK Client
         ↓
    Tool Execution Callback
         ↓
    OpenManus ToolCollection
```

### Key Components

#### 1. **CodeBuddyLLM** (`app/llm_codebuddy.py`)
Main adapter class that implements the LLM interface using CodeBuddy SDK.

**Key Methods:**
- `ask()`: Simple text generation
- `ask_tool()`: Tool-calling interface (main integration point)
- `ask_with_images()`: Multimodal requests
- `set_tool_collection()`: Registers OpenManus tools

#### 2. **CodeBuddyResponseTranslator** (`app/adapters/codebuddy_response.py`)
Translates CodeBuddy message types to OpenAI format:
- `AssistantMessage` → `ChatCompletionMessage`
- `ToolUseBlock` → `tool_calls`
- `TextBlock` → content string

#### 3. **CodeBuddyToolMapper** (`app/adapters/codebuddy_tool_mapper.py`)
Converts OpenManus tool definitions to CodeBuddy format.

### Tool Execution Flow

1. **Tool Registration**: OpenManus tools are registered with CodeBuddyLLM via `set_tool_collection()`

2. **Tool Call Interception**: When CodeBuddy wants to use a tool, the `can_use_tool` callback is invoked

3. **Local Execution**: The callback executes the tool using OpenManus's `ToolCollection.execute()`

4. **Result Return**: Tool results are returned to CodeBuddy in the expected format

This approach ensures OpenManus maintains control over tool execution while leveraging CodeBuddy's agent capabilities.

## Switching Between Backends

You can have multiple LLM configurations with different backends:

```toml
[llm]
backend = "codebuddy"
model = "gpt-4o"
# ... CodeBuddy settings ...

[llm.vision]
backend = "openai"  # Use OpenAI for vision tasks
model = "gpt-4o"
# ... OpenAI settings ...

[llm.planning]
backend = "codebuddy"  # Use CodeBuddy for planning
model = "claude-3-opus"
# ... CodeBuddy settings ...
```

The agent will automatically use the appropriate backend for each configuration.

## Comparison: OpenAI vs CodeBuddy Backend

| Feature | OpenAI Backend | CodeBuddy Backend |
|---------|---------------|-------------------|
| Tool Calling | Direct API | Via SDK callback |
| Streaming | Yes | Yes |
| Token Counting | Exact | Estimated |
| Multi-turn | Manual | SDK-managed |
| Permission Control | N/A | SDK-based |
| Model Support | OpenAI compatible | OpenAI, Claude, etc. |
| Setup Complexity | Simple | Requires SDK |

## Troubleshooting

### "CodeBuddy Agent SDK not installed"

**Solution**: Install the SDK:
```bash
pip install codebuddy-agent-sdk
```

### "Invalid Anthropic API Key" or "OpenAI authentication error"

**Solution**: Check your API key in `config/config.toml`:
```toml
api_key = "your-actual-api-key-here"
```

### Tools not executing

**Solution**: Verify `permission_mode` is set correctly:
```toml
permission_mode = "bypassPermissions"
```

### CodeBuddy CLI not found

**Solution**: Either:
1. Let the SDK use the bundled CLI (default)
2. Specify a custom path:
   ```toml
   codebuddy_code_path = "/path/to/codebuddy"
   ```

### Backend not switching

**Solution**: Check the `backend` field in your config:
```toml
[llm]
backend = "codebuddy"  # Make sure this is set
```

## Testing

Run the integration test suite:

```bash
python3 test_codebuddy_integration.py
```

This will:
1. ✅ Verify correct backend loading
2. ✅ Test basic queries
3. ✅ Test tool calling integration

## Examples

### Example 1: Simple Query

```python
from app.llm import LLM
from app.schema import Message

llm = LLM(config_name="default")  # Uses backend from config
messages = [Message.user_message("What is 2 + 2?")]
response = await llm.ask(messages)
print(response)
```

### Example 2: With Tools

```python
from app.llm import LLM
from app.tool import PythonExecute, ToolCollection
from app.schema import Message

llm = LLM(config_name="default")
tools = ToolCollection(PythonExecute())

# Set tools on CodeBuddy LLM (no-op for OpenAI)
if hasattr(llm, "set_tool_collection"):
    llm.set_tool_collection(tools)

messages = [Message.user_message("Calculate factorial of 5 using Python")]
response = await llm.ask_tool(
    messages=messages,
    tools=tools.to_params()
)
print(response.content)
```

### Example 3: Manus Agent (Automatic)

```python
from app.agent.manus import Manus

# Manus automatically uses the configured backend
agent = await Manus.create()
await agent.run("Analyze the data in data.csv and create a report")
```

## Performance Considerations

1. **Token Counting**: CodeBuddy backend uses estimation (~4 chars/token) instead of exact counting
2. **Streaming**: Both backends support streaming, but CodeBuddy processes messages iteratively
3. **Tool Execution**: CodeBuddy adds a small callback overhead but maintains full compatibility

## Future Enhancements

Potential future improvements:
- [ ] Better token counting for CodeBuddy backend
- [ ] Support for CodeBuddy-specific features (hooks, agents)
- [ ] Enhanced error handling and retry logic
- [ ] Performance metrics and comparison tools

## Contributing

To contribute to the CodeBuddy integration:

1. Make changes in `app/llm_codebuddy.py` or `app/adapters/`
2. Run tests: `python3 test_codebuddy_integration.py`
3. Check linting: `pre-commit run --all-files`
4. Submit a pull request

## Support

For issues related to:
- **OpenManus**: https://github.com/FoundationAgents/OpenManus
- **CodeBuddy SDK**: https://www.codebuddy.ai/docs/cli/sdk-python

## License

This integration follows the same MIT license as OpenManus.

