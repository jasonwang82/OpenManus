# Quick Start: Using OpenManus with CodeBuddy Backend

This is a quick reference for switching OpenManus to use CodeBuddy Agent SDK.

## 1. Install CodeBuddy SDK

```bash
pip install codebuddy-agent-sdk
```

## 2. Configure Backend

Edit `config/config.toml`:

```toml
[llm]
backend = "codebuddy"              # Switch to CodeBuddy
model = "gpt-4o"
base_url = "https://api.openai.com/v1"
api_key = "your-api-key-here"
permission_mode = "bypassPermissions"  # Let OpenManus handle tools
```

## 3. Run OpenManus

```bash
python main.py --prompt "Create a Python script to analyze sales data"
```

That's it! OpenManus will now use CodeBuddy Agent SDK as the LLM backend.

## Need More Details?

See [CODEBUDDY_INTEGRATION.md](CODEBUDDY_INTEGRATION.md) for complete documentation.

## Switching Back to OpenAI

Change in `config/config.toml`:

```toml
[llm]
backend = "openai"  # Back to OpenAI
```

