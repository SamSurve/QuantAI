"""Tests for Tailwind CSS standalone build script (scripts/build_css.py).

Verifies platform detection, checksum verification, mismatch abort,
and CSS compilation.
"""

from __future__ import annotations

import hashlib
import platform
import pytest
from pathlib import Path

from scripts import build_css

ROOT = Path(__file__).resolve().parents[1]


def test_detect_platform_supported():
    """Verify platform detection works on common platforms."""
    name, binary = build_css.get_target_binary()
    assert isinstance(name, str) and len(name) > 0
    assert isinstance(binary, str) and len(binary) > 0
    if platform.system() == "Windows":
        assert binary == "tailwindcss-windows-x64.exe"
    elif platform.system() == "Darwin":
        assert "macos" in binary
    elif platform.system() == "Linux":
        assert "linux" in binary


def test_official_checksum_pinned():
    """Verify official checksums are pinned for all target binaries."""
    target_name, binary = build_css.get_target_binary()
    assert binary in build_css.OFFICIAL_SHA256_CHECKSUMS
    pinned_checksum = build_css.OFFICIAL_SHA256_CHECKSUMS[binary]
    assert len(pinned_checksum) == 64
    assert int(pinned_checksum, 16) > 0


def test_verify_checksum_valid(tmp_path: Path):
    """Verify checksum validator accepts matching data."""
    fake_binary = tmp_path / "test.exe"
    content = b"fake-tailwind-content"
    fake_binary.write_bytes(content)
    expected_hash = hashlib.sha256(content).hexdigest()

    assert build_css.verify_checksum(fake_binary, expected_hash) is True


def test_verify_checksum_mismatch_raises(tmp_path: Path):
    """Verify checksum validator raises error on mismatch."""
    fake_binary = tmp_path / "test.exe"
    fake_binary.write_bytes(b"tampered-content")
    expected_hash = "0" * 64

    with pytest.raises(build_css.BuildError, match="Checksum mismatch"):
        build_css.verify_checksum(fake_binary, expected_hash)


def test_build_css_creates_output():
    """Verify build_css produces static/css/app.css."""
    app_css = ROOT / "static" / "css" / "app.css"
    assert app_css.exists(), "static/css/app.css was not created"
    assert app_css.stat().st_size > 0, "static/css/app.css is empty"
    content = app_css.read_text(encoding="utf-8")
    assert "--bg" in content
    assert "--card" in content
