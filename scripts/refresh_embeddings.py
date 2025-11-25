"""Utility script to refresh LanceDB embeddings from the Prisma API."""

import os
import subprocess
import sys
from pathlib import Path


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    prisma_url = os.environ.get("PRISMA_API_URL")

    if not prisma_url:
        raise SystemExit("PRISMA_API_URL environment variable is required")

    python_exe = sys.executable

    commands = [
        [python_exe, "main.py", "reset"],
        [python_exe, "main.py", "add", "-p", prisma_url],
    ]

    for cmd in commands:
        print(f"Running: {' '.join(cmd)}")
        result = subprocess.run(cmd, cwd=project_root, check=False)
        if result.returncode != 0:
            raise SystemExit(f"Command {' '.join(cmd)} failed with code {result.returncode}")

    print("✅ Embeddings refreshed successfully.")


if __name__ == "__main__":
    main()
