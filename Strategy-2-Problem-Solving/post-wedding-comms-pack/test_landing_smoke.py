"""Smoke: Phase 0b landing files exist and contain required pitch copy."""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LANDING = ROOT / "landing"


class LandingSmokeTest(unittest.TestCase):
    def test_required_files(self) -> None:
        for name in ("index.html", "styles.css", "config.js", "landing.js"):
            path = LANDING / name
            self.assertTrue(path.is_file(), f"missing {path}")

    def test_hero_and_price_copy(self) -> None:
        html = (LANDING / "index.html").read_text(encoding="utf-8")
        self.assertIn("Post-Wedding Comms Pack", html)
        self.assertIn("Still owe thank-yous", html)
        self.assertIn("₦10,000", html)
        self.assertIn('href="styles.css"', html)
        self.assertIn("config.js", html)
        self.assertIn("landing.js", html)

    def test_config_placeholders(self) -> None:
        cfg = (LANDING / "config.js").read_text(encoding="utf-8")
        self.assertIn("CONTACT_URL", cfg)
        self.assertIn("WHATSAPP_E164", cfg)
        self.assertIn("APP_URL", cfg)
        self.assertRegex(cfg, re.compile(r"PWCP_LANDING\s*="))
        # Public config must not look like a committed Nigerian mobile.
        self.assertNotRegex(cfg, re.compile(r'WHATSAPP_E164:\s*"234\d{7,}"'))

    def test_local_example_exists(self) -> None:
        example = LANDING / "config.local.js.example"
        self.assertTrue(example.is_file())
        self.assertIn("PWCP_LANDING_LOCAL", example.read_text(encoding="utf-8"))

    def test_deploy_doc(self) -> None:
        deploy = ROOT / "DEPLOY.md"
        self.assertTrue(deploy.is_file())
        text = deploy.read_text(encoding="utf-8")
        self.assertIn("Streamlit Cloud", text)
        self.assertIn("CONTACT_URL", text)
        self.assertIn("config.local.js", text)
        setup = LANDING / "SET_CONTACT_URL.md"
        self.assertTrue(setup.is_file())
        self.assertIn("Google Form", setup.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
