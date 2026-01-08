#!/usr/bin/env python3
"""Test script to verify all imports work correctly."""

print('Testing OpenManus imports...')
print('=' * 50)

try:
    from app.llm import LLM
    print('✅ LLM import successful')

    from app.llm_codebuddy import CodeBuddyLLM
    print('✅ CodeBuddyLLM import successful')

    from app.adapters.codebuddy_response import CodeBuddyResponseTranslator
    print('✅ CodeBuddyResponseTranslator import successful')

    from app.adapters.codebuddy_tool_mapper import CodeBuddyToolMapper
    print('✅ CodeBuddyToolMapper import successful')

    from app.agent.manus import Manus
    print('✅ Manus agent import successful')

    from app.config import config
    print('✅ Config loaded successfully')

    # Check backend configuration
    default_config = config.llm.get("default", config.llm["default"])
    backend = default_config.backend if hasattr(default_config, "backend") else "openai"
    print(f'\n📋 Configuration:')
    print(f'   Backend: {backend}')
    print(f'   Model: {default_config.model}')
    print(f'   API Type: {default_config.api_type if hasattr(default_config, "api_type") else "N/A"}')

    # Test LLM factory
    print(f'\n🏭 Testing LLM Factory...')
    llm = LLM(config_name="default")
    print(f'   Created LLM type: {type(llm).__name__}')
    print(f'   Expected: {"CodeBuddyLLM" if backend == "codebuddy" else "LLM"}')

    if backend == "codebuddy" and type(llm).__name__ == "CodeBuddyLLM":
        print('   ✅ Correct backend loaded (CodeBuddy)')
    elif backend == "openai" and type(llm).__name__ == "LLM":
        print('   ✅ Correct backend loaded (OpenAI)')
    else:
        print(f'   ⚠️  Backend mismatch')

    print('\n' + '=' * 50)
    print('🎉 All imports successful! Code compiles correctly.')
    print('=' * 50)

except Exception as e:
    print(f'\n❌ Error: {e}')
    import traceback
    traceback.print_exc()
    exit(1)

