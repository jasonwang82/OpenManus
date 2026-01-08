#!/usr/bin/env python3
print("Testing config loading...")
from app.config import config
cfg = config.llm['default']
print(f'Backend: {cfg.backend if hasattr(cfg, "backend") else "NOT FOUND"}')
print(f'Model: {cfg.model}')
print(f'Permission Mode: {cfg.permission_mode if hasattr(cfg, "permission_mode") else "NOT FOUND"}')
print(f'API Type: {cfg.api_type}')

from app.llm import LLM
llm = LLM(config_name='default')
print(f'\nLLM Type: {type(llm).__name__}')

