1. Local Setup Instructions
To bootstrap the local development environment for Web2PDFBook, execute the following steps:

🔧 Shell Commands (Linux/macOS)
# 1. Create project directory
mkdir web2pdfbook && cd web2pdfbook

# 2. Initialize Git repository (local-first rule)
git init

# 3. Set up Python virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 4. Create requirements.txt
cat <<EOF > requirements.txt
requests
beautifulsoup4
PyPDF2
playwright
pytest
tox
rich
EOF

# 5. Install dependencies
pip install -r requirements.txt
python -m playwright install

# 6. Create project file structure
mkdir -p tests tests/fixtures
touch cli.py crawler.py renderer.py merger.py logger.py config.py utils.py main.py

2. Directory Structure
web2pdfbook/
├── cli.py
├── crawler.py
├── renderer.py
├── merger.py
├── logger.py
├── config.py
├── utils.py
├── main.py
├── requirements.txt
├── .gitignore
├── pytest.ini
├── tox.ini
└── tests/
    ├── test_crawler.py
    ├── test_renderer.py
    ├── test_merger.py
    └── fixtures/

3. Configuration Files
.gitignore
.venv/
__pycache__/
*.log
*.pdf
tests/__pycache__/

pytest.ini
[pytest]
addopts = -ra -q
testpaths = tests

tox.ini
[tox]
envlist = py311

[testenv]
deps = pytest
commands = pytest

4. Installed Toolchain
| Tool       | Version Requirement |
| ---------- | ------------------- |
| Python     | 3.11+               |
| Playwright | latest              |
| PyPDF2     | latest              |
| requests   | latest              |
| pytest     | latest              |
| tox        | latest              |
