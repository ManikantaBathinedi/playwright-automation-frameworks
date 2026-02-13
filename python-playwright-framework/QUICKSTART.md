# 🚀 Quick Start Guide - Playwright Framework (Python)

## Get Started in 5 Minutes!

### Step 1: Open Terminal
```powershell
# Navigate to the framework folder
cd "c:\Users\mbathinedi\source\repos\Test Interview prep\06_Playwright_Framework"
```

### Step 2: Install Dependencies
```powershell
# Install Python packages
pip install -r requirements.txt

# Install Playwright browsers
playwright install
```

### Step 3: Setup Environment
```powershell
# Copy environment template (one-time setup)
copy .env.example .env

# Edit .env file if needed (optional for demo)
```

### Step 3b: Switch Environments (Easy!)
```powershell
# DEV (default - no setup needed)
# Tests will use .env.dev automatically

# Want to test on QA? Just set one variable:
$env:TEST_ENV="qa"

# Want to test on STAGING?
$env:TEST_ENV="staging"

# That's it! Framework loads the right config automatically!
```

### Step 4: Run Your First Test!
```powershell
# Run all tests
pytest

# Or run in headed mode (see browser) - recommended for learning
pytest --headed
```

### Step 5: View Results
```powershell
# HTML report is automatically generated
# Open: reports\html-report\index.html in your browser
```

---

## What You'll See

When you run `pytest`, Playwright will:
1. ✅ Open browsers (Chromium, Firefox, WebKit)
2. ✅ Run tests in parallel (using pytest-xdist)
3. ✅ Capture screenshots on failure
4. ✅ Retry failed tests (1 retry by default)
5. ✅ Generate HTML report automatically

**Expected output:**
```
============================= test session starts =============================
platform win32 -- Python 3.11.0, pytest-7.4.3, pluggy-1.3.0
plugins: playwright-0.4.3, xdist-3.5.0, html-4.1.1
collecting ... collected 29 items

tests/auth/test_login.py::test_successful_login PASSED               [  3%]
tests/auth/test_login.py::test_invalid_credentials PASSED           [  6%]
tests/api/test_users.py::test_get_all_users PASSED                 [  9%]
...

============================== 29 passed in 15.23s ============================
```

---

## Common Commands

```powershell
# Run tests in specific browser
pytest --browser=chromium
pytest --browser=firefox
pytest --browser=webkit

# Run tests in headed mode (see browser)
pytest --headed

# Run specific test file
pytest tests/auth/test_login.py

# Run tests matching pattern
pytest -k "login"

# Run smoke tests only
pytest -m smoke

# Run with verbose output
pytest -v

# Run in parallel with 4 workers
pytest -n 4

# Rerun only failed tests
pytest --lf

# Run and stop at first failure
pytest -x
```

---

## Framework Structure

```
06_Playwright_Framework/
│
├── pages/              👉 Page Object Model
│   ├── base_page.py
│   ├── login_page.py
│   ├── home_page.py│   ├── product_page.py
│
├── tests/              👉 Your test files
│   ├── auth/test_login.py
│   ├── e2e/test_checkout.py
│   └── api/test_users.py
│
├── utils/              👉 Helper functions
│   ├── logger.py
│   ├── data_generator.py
│   └── api_helper.py
│
├── conftest.py         👉 pytest fixtures (test setup)
├── pytest.ini          👉 pytest configuration
├── requirements.txt    👉 Python dependencies
└── README.md          👉 Full documentation
```

---

## Your First Custom Test

Create `tests/my_test.py`:

```python
import pytest
from playwright.sync_api import Page, expect

@pytest.mark.smoke
def test_my_first_test(page: Page):
    """My first Playwright test"""
    # Navigate to a website
    page.goto("https://playwright.dev")
    
    # Click on "Get Started"
    page.click("text=Get started")
    
    # Assert URL changed
    expect(page).to_have_url("https://playwright.dev/python/docs/intro")
    
    # Take screenshot
    page.screenshot(path="screenshots/my_test.png")
```

Run it:
```powershell
pytest tests/my_test.py
```

---

## Learning Path

### Level 1: Beginner (Week 1)
- ✅ Run existing tests
- ✅ View HTML reports
- ✅ Understand test structure
- ✅ Modify simple test values

### Level 2: Intermediate (Week 2)  
- ✅ Create new test files
- ✅ Use Page Object Model
- ✅ Add custom locators
- ✅ Write API tests

### Level 3: Advanced (Week 3-4)
- ✅ Create custom fixtures
- ✅ Add utilities
- ✅ Setup CI/CD
- ✅ Configure parallel execution

---

## Interview Demo Strategy

When showing this framework in interviews:

### 1. **Opening** (30 seconds)
> "I've built a production-ready Playwright framework using Python and pytest with Page Object Model design pattern."

### 2. **Architecture** (1 minute)
Show the folder structure and explain:
- Page objects for maintainability
- pytest fixtures for reusable setup
- Utilities for common operations
- CI/CD integration

### 3. **Demo** (2 minutes)
### 3. **Live Demo** (2 minutes)
```powershell
# Run in headed mode to show browser
pytest --headed -v
```
- Show tests running in browser
- Demonstrate parallel execution
- Display HTML report

### 4. **Code Walkthrough** (2 minutes)
Open `pages/login_page.py`:
- Show clean, maintainable code
- Explain BasePage inheritance
- Demonstrate reusability

### 5. **CI/CD** (1 minute)
Show `.github/workflows/playwright-python.yml`:
- Automated testing on push
- Multi-browser testing (Chromium, Firefox, WebKit)
- Multi-OS testing (Windows, Ubuntu, macOS)
- Report artifact upload

### 6. **Closing**
> "This framework is scalable, follows Python and pytest best practices, and can handle thousands of tests in production."

---

## Troubleshooting

### ❌ "python: command not found"
**Solution:** Install Python from https://www.python.org/downloads/

### ❌ "playwright: command not found"  
**Solution:** Install playwright after pip install:
```powershell
pip install pytest-playwright
playwright install
```

### ❌ Tests fail with timeout
**Solution:** Increase timeout in conftest.py or test:
```python
@pytest.fixture
def timeout():
    return 60000  # 60 seconds
```

### ❌ Browser not found
**Solution:**
```powershell
playwright install --with-deps
```

### ❌ "ModuleNotFoundError: No module named 'faker'"
**Solution:**
```powershell
pip install -r requirements.txt
```

---

## Next Steps

1. ✅ **Read SETUP_GUIDE.md** - Detailed walkthrough
2. ✅ **Read README.md** - Complete documentation
3. ✅ **Practice writing tests** - Modify existing tests
4. ✅ **Setup CI/CD** - Push to GitHub and see it run
5. ✅ **Read TROUBLESHOOTING.md** - Common issues

---

## Quick Reference Card

```
╔══════════════════════════════════════════════════════════╗
║       PLAYWRIGHT FRAMEWORK COMMANDS (PYTHON)             ║
╠══════════════════════════════════════════════════════════╣
║  BASIC COMMANDS:                                         ║
║  pytest                → Run all tests                   ║
║  pytest --headed       → Show browser                    ║
║  pytest -m smoke       → Smoke tests only                ║
║  pytest -v             → Verbose output                  ║
║  pytest -n 4           → Run with 4 workers              ║
║  pytest --browser=firefox → Specific browser            ║
║  playwright codegen    → Record actions                  ║
║                                                          ║
║  ENVIRONMENT SWITCHING (EASY!):                          ║
║  pytest                → DEV (default)                   ║
║  $env:TEST_ENV="qa"; pytest → QA environment            ║
║  $env:TEST_ENV="staging"; pytest → Staging              ║
║  $env:TEST_ENV="prod"; pytest -m smoke → Production     ║
╚══════════════════════════════════════════════════════════╝
```

---

## 🌍 Working with Environments

The framework automatically loads the right configuration based on `TEST_ENV` variable:

```powershell
# Windows PowerShell
$env:TEST_ENV="qa"; pytest        # Test on QA
$env:TEST_ENV="staging"; pytest   # Test on Staging

# Clear variable
$env:TEST_ENV=$null
```

📖 **Full guide:** [HOW_TO_USE_ENVIRONMENTS.md](HOW_TO_USE_ENVIRONMENTS.md)

---

## Support

- 📖 **Documentation:** See README.md and SETUP_GUIDE.md
- 🐛 **Issues:** Check TROUBLESHOOTING.md
- 🌐 **Playwright Docs:** https://playwright.dev/python/
- 🐍 **pytest Docs:** https://docs.pytest.org/
- 💬 **Questions:** Create an issue or ask in team chat

---

**You're ready to go! Start with `pytest --headed` to see the magic! ✨**
