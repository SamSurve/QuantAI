"""Tests for QuantAI static image assets.

Verifies all four original image assets exist in static/assets/ and are non-empty.
"""

from __future__ import annotations

from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]
ASSETS_DIR = ROOT / "static" / "assets"

EXPECTED_ASSETS = [
    "analysts-ledger-briefing.jpg",
    "analysts-ledger-hero.jpg",
    "analysts-ledger-logo.png",
    "analysts-ledger-market.jpg",
]


@pytest.mark.parametrize("filename", EXPECTED_ASSETS)
def test_static_asset_exists_and_non_empty(filename: str):
    asset_path = ASSETS_DIR / filename
    assert asset_path.exists(), f"Static asset missing: {filename}"
    assert asset_path.is_file(), f"Static asset is not a file: {filename}"
    assert asset_path.stat().st_size > 1000, f"Static asset is unexpectedly small: {filename}"
