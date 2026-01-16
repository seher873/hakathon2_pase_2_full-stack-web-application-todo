#!/usr/bin/env python3
"""
Test script to debug the settings loading issue.
"""

import tempfile
import os
from pydantic import field_validator
from pydantic_settings import BaseSettings
from typing import List, Union


class TestSettings(BaseSettings):
    allowed_origins: List[str] = ["http://localhost:3000"]

    @field_validator("allowed_origins", mode="before")
    @classmethod
    def parse_allowed_origins(cls, v: Union[str, List[str]]) -> List[str]:
        """Parse allowed_origins from comma-separated string or list."""
        print(f"Validator received: {repr(v)} (type: {type(v)})")
        if isinstance(v, str):
            result = [origin.strip() for origin in v.split(",") if origin.strip()]
            print(f"Validator returning: {result}")
            return result
        return v

    model_config = {
        "env_file": ".env.test",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
        "extra": "ignore"
    }


# Create a temporary .env file for testing
with tempfile.NamedTemporaryFile(mode='w', suffix='.env', delete=False) as f:
    f.write("DATABASE_URL=sqlite:///./test.db\n")
    f.write("JWT_SECRET=testsecretkey123456789012345678\n")
    f.write("ALLOWED_ORIGINS=http://localhost:3000,https://localhost:3000\n")
    temp_env_path = f.name

# Set the env file for the model
TestSettings.model_config["env_file"] = temp_env_path

try:
    print("Attempting to create settings...")
    settings = TestSettings()
    print(f"Success! allowed_origins: {settings.allowed_origins}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    # Clean up
    os.unlink(temp_env_path)