#!/usr/bin/env bash
set -euo pipefail

# Build wheel and sdist
python -m build

# Upload artifacts to repository (defaults to TestPyPI)
REPOSITORY_URL="${REPOSITORY_URL:-https://test.pypi.org/legacy/}"

twine upload --repository-url "$REPOSITORY_URL" dist/*

# Verify installation from TestPyPI
pip install -i https://test.pypi.org/simple --no-deps --force-reinstall web2pdfbook

echo "\nPackage uploaded to $REPOSITORY_URL"
echo "Install with: pip install -i https://test.pypi.org/simple web2pdfbook"
