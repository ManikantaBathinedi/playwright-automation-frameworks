# 🚀 Getting Started with Python Playwright Framework

## Step-by-Step Setup Guide

### 📋 Prerequisites

Before you begin, make sure you have:
- ✅ Python 3.11 or higher - [Download here](https://www.python.org/downloads/)
- ✅ Git - [Download here](https://git-scm.com/)
- ✅ VS Code (recommended) - [Download here](https://code.visualstudio.com/)

**Verify Python installation:**
```bash
python --version
# Should show: Python 3.11.x or higher
```

---

## 🎯 Installation Steps

### Step 1: Clone the Repository

Open Terminal/PowerShell and run:

```bash
# Clone the repository
git clone https://github.com/ManikantaBathinedi/playwright-automation-frameworks.git

# Navigate to Python framework
cd playwright-automation-frameworks/python-playwright-framework
```

---

### Step 2: Install Python Dependencies

```bash
# Install all required packages
pip install -r requirements.txt
```

This installs:
- `pytest` - Testing framework
- `playwright` - Browser automation
- `pytest-playwright` - Playwright pytest plugin
- `pytest-xdist` - Parallel execution
- `python-dotenv` - Environment variables
- `faker` - Test data generation
- And more...

---

### Step 3: Install Playwright Browsers

```bash
# Install Chromium browser (fastest for testing)
python -m playwright install chromium

# Optional: Install all browsers
python -m playwright install
```

---

### Step 4: Setup Environment Configuration

The framework is pre-configured for QA environment with demo site URLs.

**To view current config:**
```bash
# Open .env.qa file and verify:
cat .env.qa
```

You should see:
```
BASE_URL=https://www.saucedemo.com
TEST_USER_EMAIL=standard_user
TEST_USER_PASSWORD=secret_sauce
```

---

### Step 5: Run Your First Test

#### Quick Test - Single Test

```bash
# Run one login test to verify everything works
pytest tests/auth/test_login.py::TestLogin::test_login_successful_with_valid_credentials -v
```

#### Run All Tests

```bash
# Run all tests
pytest

# Run with visible browser (headed mode)
pytest --headed

# Run specific test file
pytest tests/auth/test_login.py

# Run tests with specific marker
pytest -m smoke
```

---

## ✅ Verify Installation

You should see output like:

```
====== test session starts ======
tests/auth/test_login.py::TestLogin::test_login_successful... PASSED [100%]

====== 1 passed in 5.23s ======
```

**Congratulations! 🎉 Your framework is ready!**

---

## 🎮 Running Tests

### Basic Commands

```bash
# Run all tests
pytest

# Run with HTML report
pytest --html=reports/report.html

# Run in parallel (4 workers)
pytest -n 4

# Run specific browser
pytest --browser chromium
pytest --browser firefox
pytest --browser webkit
```

### Run Different Test Categories

| Category | What it tests | Command |
|----------|---------------|---------|
| **Smoke** | Critical functionality | `pytest -m smoke` |
| **Auth** | Login/logout tests | `pytest tests/auth/` |
| **API** | API endpoint tests | `pytest -m api` |
| **E2E** | End-to-end flows | `pytest -m e2e` |
| **Negative** | Error scenarios | `pytest -m negative` |

### Advanced Options

```bash
# Verbose output
pytest -v

# Show print statements
pytest -s

# Stop after first failure
pytest -x

# Run last failed tests only
pytest --lf

# Run with specific number of retries
pytest --reruns 2

# Run in headed mode with slowmo
pytest --headed --slowmo 500
```

---

## 🌍 Switch Environments

### Windows (PowerShell)

```powershell
# QA Environment (default - uses saucedemo.com)
$env:TEST_ENV="qa"
pytest

# Dev Environment
$env:TEST_ENV="dev"
pytest

# Staging Environment
$env:TEST_ENV="staging"
pytest
```

### Mac/Linux (Bash)

```bash
# QA Environment
TEST_ENV=qa pytest

# Dev Environment
TEST_ENV=dev pytest

# Staging Environment
TEST_ENV=staging pytest
```

**Configuration files:**
- `.env.qa` - QA settings (pre-configured for demo)
- `.env.dev` - Dev settings
- `.env.staging` - Staging settings
- `.env.prod` - Production settings

---

## 📊 View Test Results

### Console Output

Tests show detailed output:
```
✅ Environment: QA
📄 Config file: .env.qa
📍 BASE_URL: https://www.saucedemo.com
🖥️  HEADLESS: true
👥 WORKERS: 4

tests/auth/test_login.py::TestLogin::test_login_successful... PASSED
```

### HTML Reports

```bash
# Generate HTML report
pytest --html=reports/html-report/index.html

# Open the report
# Windows:
start reports/html-report/index.html

# Mac:
open reports/html-report/index.html

# Linux:
xdg-open reports/html-report/index.html
```

### Screenshots & Videos

On test failure, framework automatically captures:
- 📸 Screenshots → `reports/screenshots/`
- 🎥 Videos → `reports/videos/`
- 📋 Logs → `reports/logs/`

---

## 📁 Project Structure Overview

```
python-playwright-framework/
├── pages/                  # Page Object Model
│   ├── base_page.py       # Base class with common methods
│   ├── login_page.py      # Login page interactions
│   ├── home_page.py       # Home page interactions
│   └── product_page.py    # Product page interactions
│
├── tests/                  # Test files
│   ├── auth/              # Login/Auth tests
│   │   └── test_login.py
│   ├── api/               # API tests
│   └── e2e/               # End-to-end tests
│
├── utils/                  # Helper utilities
│   ├── logger.py          # Custom logging
│   ├── data_generator.py  # Test data with Faker
│   └── api_helper.py      # API utilities
│
├── config/                 # Configuration
│   └── env_switcher.py    # Environment manager
│
├── .env.*                  # Environment configs
├── conftest.py            # Pytest configuration
├── pytest.ini             # Pytest settings
└── requirements.txt       # Python dependencies
```

---

## 🔧 VS Code Setup (Recommended)

### Install Python Extension

1. Open VS Code
2. Go to Extensions (Ctrl+Shift+X)
3. Search for "Python"
4. Install "Python" by Microsoft

### Configure Python

1. Press `Ctrl+Shift+P`
2. Type: "Python: Select Interpreter"
3. Choose Python 3.11 or higher

### Run Tests in VS Code

1. Open Testing sidebar (flask icon)
2. Click "Configure Python Tests"
3. Select "pytest"
4. Select root directory
5. Tests will appear in sidebar
6. Click play button to run!

---

## 🆘 Troubleshooting

### Problem: `pytest: command not found`

**Solution:**
```bash
# Ensure pip packages are in PATH
# OR use:
python -m pytest

# Reinstall if needed:
pip install --upgrade pytest
```

### Problem: Browser not found

**Solution:**
```bash
# Reinstall browsers
python -m playwright install chromium

# Check installation
python -m playwright --version
```

### Problem: Import errors

**Solution:**
```bash
# Upgrade pip
python -m pip install --upgrade pip

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Problem: Tests timing out

**Solution:**
```bash
# Increase timeout in pytest.ini
# Already set to: timeout = 300 (5 minutes)

# Or run with custom timeout:
pytest --timeout=600
```

### Problem: Permission denied on Windows

**Solution:**
```bash
# Run as administrator
# OR
# Add Python to PATH during installation
```

---

## 🎯 Quick Command Reference

```bash
# Most used commands
pytest                          # Run all tests
pytest -v                       # Verbose output  
pytest -m smoke                 # Smoke tests only
pytest -n 4                     # 4 parallel workers
pytest --headed                 # See browser
pytest --html=report.html       # Generate HTML report
pytest -k "login"               # Run tests matching "login"
pytest tests/auth/              # Run auth folder only

# Environment
$env:TEST_ENV="qa"; pytest      # Windows
TEST_ENV=qa pytest              # Mac/Linux

# Debugging
pytest -s                       # Show print()
pytest --pdb                    # Drop to debugger on failure
pytest --trace                  # Start debugger immediately
```

---

## 🎓 What's Next?

1. ✅ **Explore the tests** - Open `tests/auth/test_login.py` and read through
2. ✅ **Run different markers** - Try `pytest -m smoke`, `pytest -m regression`
3. ✅ **Check reports** - Generate HTML report and view in browser
4. ✅ **Modify a test** - Change assertions and see what happens
5. ✅ **Create new test** - Copy existing test structure
6. ✅ **Run in parallel** - Try `pytest -n 4` for faster execution

---

## 📚 Additional Resources

- 📖 [Full README](README.md) - Complete framework documentation
- 🎯 [Pytest Documentation](https://docs.pytest.org/) - Pytest official docs
- 🎭 [Playwright Python Docs](https://playwright.dev/python/) - Playwright for Python
- 🔧 [Configuration Guide](docs/CONFIGURATION.md) - Advanced config options

---

## ✨ Success Criteria

You're ready to start developing when:

- ✅ `pytest --version` shows pytest installed
- ✅ `python -m playwright --version` shows playwright installed
- ✅ At least one test passes when you run `pytest -m smoke`
- ✅ HTML report generates successfully
- ✅ You can see tests in VS Code Testing sidebar

**Happy Testing! 🎉**
