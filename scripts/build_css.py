"""Tailwind CSS 4.1.14 standalone CLI build script.

Downloads official standalone Tailwind CLI executable for the current platform,
verifies its SHA-256 against the official published checksums from the GitHub release,
stores it in tools/ (gitignored), and compiles static/css/input.css to static/css/app.css.

No Node.js, npm, npx or pnpm required.
"""

from __future__ import annotations

import hashlib
import platform
import subprocess
import sys
import urllib.request
from pathlib import Path

TAILWIND_VERSION = "v4.1.14"
GITHUB_RELEASE_BASE = (
    f"https://github.com/tailwindlabs/tailwindcss/releases/download/{TAILWIND_VERSION}/"
)

# Official published SHA-256 checksums from:
# https://github.com/tailwindlabs/tailwindcss/releases/download/v4.1.14/sha256sums.txt
OFFICIAL_SHA256_CHECKSUMS = {
    "tailwindcss-windows-x64.exe": "ae892cdb0817fbe6b692fc67bb1339a728f21116020e620bc4b94d87d6ba1fee",
    "tailwindcss-macos-x64": "67b25b6103fa7677637e5a5de3327fec3335da316d90d3fdb1a4cd72bda41c0a",
    "tailwindcss-macos-arm64": "e722b752f51def86d42e886b4c1171f2d09a4be1a7487a0a51e4aff8e7603ce3",
    "tailwindcss-linux-x64": "bc34c301b080b6e6b98ed24118419833f966f6f347e556945d6557d36a44a56e",
    "tailwindcss-linux-arm64": "314941f5f6e143e74e740c587ad1fbaaede5462572dd330bbe0937e611e966db",
}

ROOT = Path(__file__).resolve().parents[1]
TOOLS_DIR = ROOT / "tools"
INPUT_CSS = ROOT / "static" / "css" / "input.css"
OUTPUT_CSS = ROOT / "static" / "css" / "app.css"


class BuildError(Exception):
    """Raised when Tailwind CLI download, verification, or build fails."""


def get_target_binary() -> tuple[str, str]:
    """Detect current OS and architecture, returning (display_name, binary_asset_name)."""
    os_name = platform.system()
    machine = platform.machine().lower()

    if os_name == "Windows":
        if "64" in machine or "amd64" in machine or "x86_64" in machine:
            return "Windows x64", "tailwindcss-windows-x64.exe"
        raise BuildError(f"Unsupported Windows architecture: {machine}")

    elif os_name == "Darwin":
        if "arm" in machine or "aarch64" in machine:
            return "macOS ARM64", "tailwindcss-macos-arm64"
        return "macOS x64", "tailwindcss-macos-x64"

    elif os_name == "Linux":
        if "arm" in machine or "aarch64" in machine:
            return "Linux ARM64", "tailwindcss-linux-arm64"
        return "Linux x64", "tailwindcss-linux-x64"

    raise BuildError(f"Unsupported operating system: {os_name}")


def compute_sha256(file_path: Path) -> str:
    """Compute the SHA-256 hash of a file."""
    sha = hashlib.sha256()
    with file_path.open("rb") as f:
        while chunk := f.read(65536):
            sha.update(chunk)
    return sha.hexdigest().lower()


def verify_checksum(file_path: Path, expected_hash: str) -> bool:
    """Verify file checksum against expected hash."""
    actual_hash = compute_sha256(file_path)
    if actual_hash != expected_hash.lower():
        raise BuildError(
            f"Checksum mismatch for {file_path.name}!\n"
            f"Expected: {expected_hash}\n"
            f"Actual:   {actual_hash}"
        )
    return True


def ensure_tailwind_binary() -> Path:
    """Ensure Tailwind standalone CLI binary exists and is verified in tools/."""
    platform_name, binary_name = get_target_binary()
    if binary_name not in OFFICIAL_SHA256_CHECKSUMS:
        raise BuildError(f"No pinned official checksum for asset: {binary_name}")

    expected_hash = OFFICIAL_SHA256_CHECKSUMS[binary_name]
    TOOLS_DIR.mkdir(parents=True, exist_ok=True)
    binary_path = TOOLS_DIR / binary_name

    if binary_path.exists():
        try:
            verify_checksum(binary_path, expected_hash)
            return binary_path
        except BuildError:
            binary_path.unlink()

    download_url = f"{GITHUB_RELEASE_BASE}{binary_name}"
    print(f"Downloading official Tailwind CLI {TAILWIND_VERSION} for {platform_name}...")
    print(f"URL: {download_url}")

    req = urllib.request.Request(
        download_url,
        headers={"User-Agent": "QuantAI-Build/1.0"},
    )
    with urllib.request.urlopen(req) as resp, binary_path.open("wb") as out:
        while chunk := resp.read(65536):
            out.write(chunk)

    verify_checksum(binary_path, expected_hash)
    print(f"Verified SHA-256: {expected_hash}")

    # Make executable on Unix
    if platform.system() != "Windows":
        binary_path.chmod(0o755)

    return binary_path


def build(minify: bool = True) -> Path:
    """Execute Tailwind standalone CLI to build static/css/app.css."""
    binary_path = ensure_tailwind_binary()
    OUTPUT_CSS.parent.mkdir(parents=True, exist_ok=True)

    if not INPUT_CSS.exists():
        raise BuildError(f"Input CSS not found: {INPUT_CSS}")

    cmd = [
        str(binary_path),
        "-i",
        str(INPUT_CSS),
        "-o",
        str(OUTPUT_CSS),
    ]
    if minify:
        cmd.append("--minify")

    print(f"Compiling CSS: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        raise BuildError(
            f"Tailwind CLI compilation failed with code {result.returncode}:\n"
            f"STDOUT:\n{result.stdout}\n"
            f"STDERR:\n{result.stderr}"
        )

    print(f"Successfully generated {OUTPUT_CSS} ({OUTPUT_CSS.stat().st_size} bytes)")
    return OUTPUT_CSS


if __name__ == "__main__":
    try:
        build()
    except Exception as exc:
        print(f"Build failed: {exc}", file=sys.stderr)
        sys.exit(1)
