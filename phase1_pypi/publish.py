"""
Automated PyPI / TestPyPI publishing helper script.
Usage:
    python phase1_pypi/publish.py --target testpypi
    python phase1_pypi/publish.py --target pypi
"""

import os
import sys
import argparse
import subprocess


def run_command(cmd, desc):
    print(f"\n--> {desc}...")
    print(f"Command: {cmd}")
    res = subprocess.run(cmd, shell=True)
    if res.returncode != 0:
        print(f"[ERROR] Failed during: {desc}", file=sys.stderr)
        sys.exit(res.returncode)


def main():
    parser = argparse.ArgumentParser(description="Publish MCP package to PyPI or TestPyPI")
    parser.add_argument(
        "--target",
        choices=["testpypi", "pypi"],
        default="testpypi",
        help="Repository target: 'testpypi' (default) or 'pypi'"
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Remove existing dist/ directory before building"
    )
    args = parser.parse_args()

    # 1. Clean old builds if requested
    if args.clean and os.path.exists("dist"):
        import shutil
        print("Cleaning existing dist/ folder...")
        shutil.rmtree("dist")

    # 2. Build distributions
    run_command("uv build", "Building source distribution and wheel")

    # 3. Publish
    if args.target == "testpypi":
        print("\n=======================================================")
        print("Publishing to TestPyPI (Recommended for validation)")
        print("=======================================================")
        print("When prompted:")
        print("  Username: __token__")
        print("  Password: <your-testpypi-api-token (starts with pypi-)>")
        print("=======================================================\n")
        run_command("uv publish --publish-url https://test.pypi.org/legacy/", "Publishing to TestPyPI via uv")
    else:
        print("\n=======================================================")
        print("Publishing to Production PyPI")
        print("=======================================================")
        print("When prompted:")
        print("  Username: __token__")
        print("  Password: <your-pypi-api-token (starts with pypi-)>")
        print("=======================================================\n")
        run_command("uv publish", "Publishing to Production PyPI via uv")

    print("\n[SUCCESS] Package published successfully!")


if __name__ == "__main__":
    main()
