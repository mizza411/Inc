"""Unit tests for LLM provider resolution (no live API calls)."""

from __future__ import annotations

import os
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from generation import (  # noqa: E402
    get_client,
    missing_key_message,
    resolve_config,
    resolve_provider,
)


class ResolveProviderTests(unittest.TestCase):
    def test_default_is_deepseek(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            self.assertEqual(resolve_provider(), "deepseek")

    def test_explicit_openai(self) -> None:
        with patch.dict(os.environ, {"LLM_PROVIDER": "openai"}, clear=True):
            self.assertEqual(resolve_provider(), "openai")

    def test_unknown_raises(self) -> None:
        with self.assertRaises(ValueError):
            resolve_provider("claude")


class ResolveConfigTests(unittest.TestCase):
    def test_deepseek_uses_deepseek_key_and_base(self) -> None:
        env = {
            "LLM_PROVIDER": "deepseek",
            "DEEPSEEK_API_KEY": "sk-ds-test",
        }
        with patch.dict(os.environ, env, clear=True):
            cfg = resolve_config()
        assert cfg is not None
        self.assertEqual(cfg.provider, "deepseek")
        self.assertEqual(cfg.api_key, "sk-ds-test")
        self.assertEqual(cfg.base_url, "https://api.deepseek.com")
        self.assertEqual(cfg.model, "deepseek-chat")

    def test_llm_api_key_fallback(self) -> None:
        env = {"LLM_PROVIDER": "deepseek", "LLM_API_KEY": "sk-generic"}
        with patch.dict(os.environ, env, clear=True):
            cfg = resolve_config()
        assert cfg is not None
        self.assertEqual(cfg.api_key, "sk-generic")

    def test_openai_legacy_model_env(self) -> None:
        env = {
            "LLM_PROVIDER": "openai",
            "OPENAI_API_KEY": "sk-oa",
            "OPENAI_MODEL": "gpt-4o",
        }
        with patch.dict(os.environ, env, clear=True):
            cfg = resolve_config()
        assert cfg is not None
        self.assertIsNone(cfg.base_url)
        self.assertEqual(cfg.model, "gpt-4o")

    def test_missing_key_returns_none(self) -> None:
        with patch.dict(os.environ, {"LLM_PROVIDER": "deepseek"}, clear=True):
            self.assertIsNone(resolve_config())
        self.assertIn("DEEPSEEK_API_KEY", missing_key_message("deepseek"))

    def test_ngpt_base_override(self) -> None:
        env = {
            "LLM_PROVIDER": "ngpt",
            "NGPT_API_KEY": "sk-ngpt",
            "LLM_BASE_URL": "https://example.ngpt.local/v1",
        }
        with patch.dict(os.environ, env, clear=True):
            cfg = resolve_config()
        assert cfg is not None
        self.assertEqual(cfg.base_url, "https://example.ngpt.local/v1")


class GetClientTests(unittest.TestCase):
    @patch("generation.OpenAI")
    def test_passes_base_url_for_deepseek(self, mock_openai: MagicMock) -> None:
        env = {"LLM_PROVIDER": "deepseek", "DEEPSEEK_API_KEY": "sk-ds"}
        with patch.dict(os.environ, env, clear=True):
            get_client()
        mock_openai.assert_called_once_with(
            api_key="sk-ds",
            base_url="https://api.deepseek.com",
        )


if __name__ == "__main__":
    raise SystemExit(unittest.main())
