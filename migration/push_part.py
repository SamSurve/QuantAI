
"""
QuantAI controlled commit and push script.

Python 3.12 standard library only.

Usage:
    python migration/push_part.py 1 "part 01: establish Python-only foundation"

Works from Windows PowerShell.

Supports an unborn main branch (zero existing commits).

Safety:
- Exact origin URL.
- main branch.
- Configured Git author email.
- Part number and message validation.
- PROGRESS.md verification.
- Sequential prior part commit verification.
- No pre-staged files.
- Full pytest before commit.
- Explicit safe-file staging.
- Exactly one commit.
- One push attempt.
- No automatic push retry.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath


# ------------------------------------------------------------
# CONFIGURATION
# ------------------------------------------------------------

EXPECTED_REMOTE = "https://github.com/SamSurve/QuantAI.git"
EXPECTED_BRANCH = "main"

TOTAL_PARTS = 30
PROGRESS_FILE = "migration/PROGRESS.md"

BATCH_ENDS = {5, 10, 15, 20, 25, 30}
DAY_ENDS = {10, 20, 30}

IGNORED_DIRECTORIES = {
    ".git",
    ".venv",
    "venv",
    "env",
    "ENV",
    "node_modules",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".tox",
    ".nox",
    ".vercel",
    "tools",
}

PROTECTED_DIRECTORIES = {
    ".ssh",
    ".aws",
    ".azure",
    "secrets",
    "credentials",
}

PROTECTED_FILENAMES = {
    ".env",
    "id_rsa",
    "id_dsa",
    "id_ecdsa",
    "id_ed25519",
    "authorized_keys",
    "credentials.json",
    "secrets.json",
    ".netrc",
    ".npmrc",
    ".pypirc",
}

SENSITIVE_SUFFIXES = {
    ".pem",
    ".key",
    ".p12",
    ".pfx",
    ".p8",
    ".p7b",
    ".p7c",
    ".jks",
    ".ppk",
}

UNMERGED_STATUSES = {
    "DD", "AU", "UD", "UA", "DU", "AA", "UU"
}

PART_COMMIT_PATTERN = re.compile(
    r"^part\s+(\d{2}):\s+\S.*$",
    re.IGNORECASE,
)


# ------------------------------------------------------------
# ERRORS
# ------------------------------------------------------------

class PushError(Exception):
    """Expected validation or Git failure."""


class PushAfterCommitError(PushError):
    """A local commit exists, but pushing failed."""


# ------------------------------------------------------------
# SUBPROCESS EXECUTION
# ------------------------------------------------------------

def execute(
    command: list[str],
    cwd: Path,
) -> subprocess.CompletedProcess[str]:
    """Execute commands without invoking a shell."""

    try:
        return subprocess.run(
            command,
            cwd=str(cwd),
            shell=False,
            text=True,
            encoding="utf-8",
            errors="surrogateescape",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
    except FileNotFoundError as exc:
        raise PushError(
            f"Required executable unavailable: {command[0]}"
        ) from exc


def git(
    arguments: list[str],
    root: Path,
) -> subprocess.CompletedProcess[str]:
    """Run Git and convert failures into safe errors."""

    result = execute(["git", *arguments], root)

    if result.returncode != 0:
        raise PushError(
            f"Git operation failed: {arguments[0]}"
        )

    return result


# ------------------------------------------------------------
# PYTHON VERSION
# ------------------------------------------------------------

def validate_python() -> None:
    if sys.version_info[:2] != (3, 12):
        raise PushError(
            "Python 3.12 is required to run push_part.py."
        )


# ------------------------------------------------------------
# ARGUMENT VALIDATION
# ------------------------------------------------------------

def validate_arguments(
    part_no: int,
    message: str,
) -> None:

    if not 1 <= part_no <= TOTAL_PARTS:
        raise PushError("part_no must be between 1 and 30.")

    if "\n" in message or "\r" in message:
        raise PushError("Commit message must be a single line.")

    expected = f"part {part_no:02d}:"

    if not message.startswith(expected):
        raise PushError(
            f'Commit message must start with "{expected}"'
        )

    description = message[len(expected):].strip()

    if not description:
        raise PushError("Commit message needs a description.")


# ------------------------------------------------------------
# REPOSITORY DISCOVERY
# ------------------------------------------------------------

def find_repository_root() -> Path:

    script_directory = Path(__file__).resolve().parent

    result = execute(
        ["git", "rev-parse", "--show-toplevel"],
        script_directory,
    )

    if result.returncode != 0:
        raise PushError(
            "This script must be inside the new Git repository."
        )

    return Path(result.stdout.strip()).resolve()


def has_head(root: Path) -> bool:
    """Return False for a newly initialized, unborn branch."""

    result = execute(
        ["git", "rev-parse", "--verify", "HEAD"],
        root,
    )

    return result.returncode == 0


# ------------------------------------------------------------
# REPOSITORY VALIDATION
# ------------------------------------------------------------

def validate_repository(root: Path) -> None:

    remote = git(
        ["remote", "get-url", "origin"],
        root,
    ).stdout.strip()

    if remote != EXPECTED_REMOTE:
        raise PushError(
            "origin does not match the approved GitHub repository."
        )

    branch = git(
        ["branch", "--show-current"],
        root,
    ).stdout.strip()

    if branch != EXPECTED_BRANCH:
        raise PushError("Active branch must be main.")

    email = execute(
        ["git", "config", "--get", "user.email"],
        root,
    )

    if email.returncode != 0 or not email.stdout.strip():
        raise PushError(
            "Git user.email is missing. Configure it before pushing."
        )


def validate_clean_index(root: Path) -> None:

    result = execute(
        ["git", "diff", "--cached", "--quiet"],
        root,
    )

    if result.returncode == 1:
        raise PushError(
            "Pre-staged changes detected. Unstage them first."
        )

    if result.returncode != 0:
        raise PushError("Could not inspect Git staging area.")


# ------------------------------------------------------------
# PROGRESS VALIDATION
# ------------------------------------------------------------

def checked_pattern(part_no: int) -> re.Pattern[str]:

    return re.compile(
        rf"(?im)^\s*-\s+\[x\]\s+PART\s+{part_no:02d}\b"
    )


def part_is_checked(
    content: str,
    part_no: int,
) -> bool:

    return bool(
        checked_pattern(part_no).search(content)
    )


def read_committed_progress(root: Path) -> str:
    """
    Read progress from HEAD.

    An unborn branch has no committed files, so return an empty
    string instead of treating this as a fatal error.
    """

    if not has_head(root):
        return ""

    result = execute(
        ["git", "show", f"HEAD:{PROGRESS_FILE}"],
        root,
    )

    if result.returncode != 0:
        return ""

    return result.stdout


def validate_progress(
    root: Path,
    part_no: int,
) -> None:

    progress_path = root / PROGRESS_FILE

    if not progress_path.is_file():
        raise PushError(
            "migration/PROGRESS.md is missing."
        )

    working = progress_path.read_text(
        encoding="utf-8"
    )

    if not part_is_checked(working, part_no):
        raise PushError(
            f"PART {part_no:02d} is not checked in PROGRESS.md."
        )

    for previous in range(1, part_no):

        if not part_is_checked(working, previous):
            raise PushError(
                f"PART {previous:02d} is not checked. "
                "Parts cannot be skipped."
            )

    committed = read_committed_progress(root)

    if part_is_checked(committed, part_no):
        raise PushError(
            f"PART {part_no:02d} is already checked in HEAD. "
            "Duplicate part commits are forbidden."
        )


# ------------------------------------------------------------
# PRIOR PART COMMIT VALIDATION
# ------------------------------------------------------------

def validate_prior_commits(
    root: Path,
    part_no: int,
) -> None:
    """
    Require exactly part_no - 1 prior migration commits.

    For an unborn main branch, the prior part count is zero.
    Unrelated commits are not counted as migration part commits.
    """

    if not has_head(root):
        subjects: list[str] = []
    else:
        subjects = git(
            ["log", "--format=%s", "HEAD"],
            root,
        ).stdout.splitlines()

    found: list[int] = []

    for subject in subjects:

        match = PART_COMMIT_PATTERN.match(subject.strip())

        if match:
            found.append(int(match.group(1)))

    expected = list(range(1, part_no))

    if len(found) != part_no - 1:
        raise PushError(
            f"Expected {part_no - 1} previous part commits; "
            f"found {len(found)}."
        )

    if sorted(found) != expected:
        raise PushError(
            "Previous part commits are not consecutive. "
            "Skipping or duplicating parts is forbidden."
        )


# ------------------------------------------------------------
# FULL PYTEST
# ------------------------------------------------------------

def run_full_pytest(root: Path) -> None:

    print()
    print("=== Running mandatory full pytest suite ===")

    result = execute(
        [sys.executable, "-m", "pytest", "-q"],
        root,
    )

    if result.returncode != 0:
        # Keep arbitrary test output hidden to avoid accidentally
        # printing environment secrets.
        raise PushError(
            "FULL PYTEST FAILED. No commit was created. "
            "Inspect and fix the tests before retrying."
        )

    print("Full pytest suite: PASSED.")


# ------------------------------------------------------------
# SAFE FILE FILTERING
# ------------------------------------------------------------

def is_safe_to_stage(relative_path: str) -> bool:

    normalized = relative_path.replace("\\", "/")
    path = PurePosixPath(normalized)

    if not normalized or path.is_absolute():
        return False

    if ".." in path.parts:
        return False

    if any(
        item in IGNORED_DIRECTORIES
        for item in path.parts
    ):
        return False

    if any(
        item.lower() in PROTECTED_DIRECTORIES
        for item in path.parts
    ):
        return False

    filename = path.name.lower()

    # Permit only the names-only environment template.
    if filename.startswith(".env") and filename != ".env.example":
        return False

    if filename in PROTECTED_FILENAMES:
        return False

    if Path(filename).suffix.lower() in SENSITIVE_SUFFIXES:
        return False

    if filename.startswith(
        ("private_key", "secret_", "credentials.")
    ):
        return False

    if filename.endswith(".pyc"):
        return False

    return True


# ------------------------------------------------------------
# GIT STATUS PARSING
# ------------------------------------------------------------

def collect_changed_paths(root: Path) -> list[str]:
    """
    Collect changed paths from NUL-delimited Git status.

    Supports:
    - Modified files.
    - Added files.
    - Deleted files.
    - Renamed files.
    - Copied files.
    - Type changes.
    - Untracked, non-ignored files.

    Supports filenames containing spaces.
    """

    result = git(
        [
            "status",
            "--porcelain=v1",
            "-z",
            "--untracked-files=all",
        ],
        root,
    )

    tokens = result.stdout.split("\0")
    index = 0

    safe_paths: set[str] = set()

    while index < len(tokens):

        record = tokens[index]
        index += 1

        if not record:
            continue

        if len(record) < 4 or record[2] != " ":
            raise PushError(
                "Unexpected Git status format. Refusing to stage."
            )

        status = record[:2]
        current_path = record[3:]

        if status in UNMERGED_STATUSES:
            raise PushError(
                "Git merge conflict detected. Resolve it first."
            )

        paths = [current_path]

        # With porcelain -z, rename/copy records contain
        # destination first and original path second.
        if "R" in status or "C" in status:

            if index >= len(tokens) or not tokens[index]:
                raise PushError(
                    "Incomplete rename/copy status record."
                )

            paths.append(tokens[index])
            index += 1

        # Exclude the complete operation if any path is protected.
        if not all(is_safe_to_stage(item) for item in paths):
            continue

        safe_paths.update(paths)

    return sorted(safe_paths)


# ------------------------------------------------------------
# EXPLICIT STAGING
# ------------------------------------------------------------

def stage_safe_files(
    root: Path,
    paths: list[str],
) -> None:

    if not paths:
        raise PushError("No safe changed files found.")

    if PROGRESS_FILE not in paths:
        raise PushError(
            "migration/PROGRESS.md must be included "
            "in the current part commit."
        )

    # Explicit literal pathspecs only.
    # Never use git add -A.
    pathspecs = [
        f":(literal){item}"
        for item in paths
    ]

    git(
        ["add", "--", *pathspecs],
        root,
    )

    staged_output = git(
        ["diff", "--cached", "--name-only", "-z"],
        root,
    ).stdout

    staged_paths = [
        item
        for item in staged_output.split("\0")
        if item
    ]

    if not staged_paths:
        raise PushError("No files were staged.")

    if any(
        not is_safe_to_stage(item)
        for item in staged_paths
    ):
        raise PushError(
            "A protected file entered the staging area."
        )

    if PROGRESS_FILE not in staged_paths:
        raise PushError(
            "PROGRESS.md was not successfully staged."
        )

    print(f"Explicit safe files staged: {len(staged_paths)}")


# ------------------------------------------------------------
# EXACTLY ONE COMMIT
# ------------------------------------------------------------

def create_one_commit(
    root: Path,
    message: str,
) -> str:

    staged = execute(
        ["git", "diff", "--cached", "--quiet"],
        root,
    )

    if staged.returncode == 0:
        raise PushError("No staged changes available.")

    if staged.returncode != 1:
        raise PushError("Could not validate the Git index.")

    old_head = None

    if has_head(root):
        old_head = git(
            ["rev-parse", "HEAD"],
            root,
        ).stdout.strip()

    result = execute(
        ["git", "commit", "-m", message],
        root,
    )

    if result.returncode != 0:
        raise PushError(
            "Git commit failed. Inspect repository state. "
            "Do not create an additional commit blindly."
        )

    new_head = git(
        ["rev-parse", "HEAD"],
        root,
    ).stdout.strip()

    if new_head == old_head:
        raise PushError("HEAD did not change after committing.")

    if old_head is None:
        # First commit in an empty repository.
        count = git(
            ["rev-list", "--count", "HEAD"],
            root,
        ).stdout.strip()
    else:
        count = git(
            ["rev-list", "--count", f"{old_head}..{new_head}"],
            root,
        ).stdout.strip()

    if count != "1":
        raise PushError(
            "Expected exactly one new commit. "
            "Stop and inspect Git history."
        )

    subject = git(
        ["log", "-1", "--format=%s"],
        root,
    ).stdout.strip()

    if subject != message:
        raise PushError(
            "Committed message does not match the requested message."
        )

    return new_head


# ------------------------------------------------------------
# PUSH
# ------------------------------------------------------------

def push_one_commit(root: Path) -> None:

    print()
    print("=== Pushing exactly once to origin main ===")

    result = execute(
        ["git", "push", "origin", "main"],
        root,
    )

    if result.returncode != 0:
        raise PushAfterCommitError(
            "PUSH FAILED AFTER COMMIT. "
            "The local commit exists, but the push was unsuccessful. "
            "Do not retry this script and do not create another commit. "
            "Inspect Git status and history, resolve the issue, "
            "and report the result."
        )

    print("Push successful.")


# ------------------------------------------------------------
# COMPLETION MESSAGES
# ------------------------------------------------------------

def print_completion(part_no: int) -> None:

    if part_no in BATCH_ENDS:
        print()
        print("BATCH COMPLETE, STOP")

    if part_no in DAY_ENDS:
        print("DAY COMPLETE")


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------

def main() -> int:

    parser = argparse.ArgumentParser(
        description="Commit and push exactly one QuantAI migration part."
    )

    parser.add_argument(
        "part_no",
        type=int,
        help="Part number, 1 through 30.",
    )

    parser.add_argument(
        "message",
        type=str,
        help='Example: "part 01: establish Python-only foundation".',
    )

    args = parser.parse_args()

    commit_created = False

    try:
        validate_python()
        validate_arguments(args.part_no, args.message)

        root = find_repository_root()

        print("=== QuantAI part push ===")
        print(f"Repository: {root}")
        print(f"Part: {args.part_no:02d}")

        validate_repository(root)
        validate_clean_index(root)
        validate_prior_commits(root, args.part_no)
        validate_progress(root, args.part_no)

        # Tests run before staging or committing.
        run_full_pytest(root)

        paths = collect_changed_paths(root)
        stage_safe_files(root, paths)

        commit_sha = create_one_commit(root, args.message)
        commit_created = True

        print(f"Commit created: {commit_sha}")

        # A failed push must never trigger a second commit.
        push_one_commit(root)

        print()
        print(f"PART {args.part_no:02d} PUSHED SUCCESSFULLY.")

        print_completion(args.part_no)

        return 0

    except PushAfterCommitError as exc:
        print()
        print(f"STOP: {exc}")
        return 2

    except PushError as exc:
        print()
        print(f"ABORTED: {exc}")

        if commit_created:
            print(
                "A local commit exists. Do not create another commit."
            )
        else:
            print("No commit was created by this run.")

        return 1

    except KeyboardInterrupt:
        print()
        print(
            "INTERRUPTED. Inspect Git status and history "
            "before continuing."
        )
        return 130

    except Exception:
        print()
        print(
            "UNEXPECTED FAILURE. Inspect repository state securely. "
            "Do not create a duplicate commit."
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
