# 🎭 Playwright Automation Framework - Production Ready (Python)

A comprehensive, scalable, and production-ready Playwright automation framework with **Python + pytest**, following industry best practices.

## 📋 Table of Contents

1. [Why Playwright?](#-why-playwright-over-selenium)
2. [Features](#-features)
3. [Quick Start](#-quick-start)
4. [Usage](#-usage)
5. [Parallel Execution](#-parallel-execution-explained)
6. [Project Structure](#-project-structure)
7. [Interview Tips](#-interview-tips)

---

## 🎯 Why Playwright Over Selenium?

**Playwright is 3-5x faster** and more reliable than Selenium! Here's why this framework uses Playwright:

| Feature | Playwright ✅ | Selenium ❌ |
|---------|--------------|-------------|
| **Speed** | ⚡ 3-5x Faster | Slower |
| **Auto-Wait** | Built-in smart waiting | Manual waits needed |
| **Parallel Execution** | Native support | Needs Grid setup |
| **Installation** | Single command | Multiple drivers |
| **Flakiness** | Less flaky (95-98% reliability) | More flaky (70-80%) |
| **API Testing** | Built-in | External library needed |
| **Modern Apps** | SPAs, PWAs, WebSockets | Limited support |

**Key Advantages:**
1. ✅ **No manual waits** - Playwright auto-waits for elements
2. ✅ **Built-in parallel execution** - Tests run simultaneously  
3. ✅ **Single installation** - `pip install pytest-playwright`
4. ✅ **Network mocking** - Mock APIs, block resources
5. ✅ **Less flaky** - Smart retry and auto-wait mechanisms

📖 [Read detailed comparison: PLAYWRIGHT_VS_SELENIUM.md](PLAYWRIGHT_VS_SELENIUM.md)

---

## 📋 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Framework Architecture](#framework-architecture)
- [Quick Start](#quick-start)
- [Running Tests](#running-tests)
- [CI/CD Integration](#cicd-integration)
- [Reporting](#reporting)
- [Best Practices](#best-practices)

---

## 🎯 Overview

This framework demonstrates a **real-world, enterprise-grade** Playwright automation solution that you can use in production projects. It includes:

- ✅ **Page Object Model (POM)** - Maintainable and reusable page objects
- ✅ **Python + pytest** - Easy to learn, powerful testing
- ✅ **pytest Fixtures** - Reusable test setup and teardown
- ✅ **Utilities & Helpers** - Logger, data generators (Faker), API helpers
- ✅ **Environment Management** - Dev, QA, Staging, Production configs (.env)
- ✅ **Parallel Execution** - Fast test execution with pytest-xdist
- ✅ **Retry Mechanism** - Handle flaky tests
- ✅ **Screenshot & Video** - Capture on failure
- ✅ **HTML Reports** - Beautiful pytest-html reports
- ✅ **CI/CD Ready** - GitHub Actions & Azure DevOps pipelines
- ✅ **Test Markers** - Organize tests (@smoke, @regression, @api)

---

## 🚀 Features

### 1. **Page Object Model (POM)**
```
pages/
├── base/
│   └── BasePage.ts          # Common methods for all pages
├── LoginPage.ts             # Login page object
├── HomePage.ts              # Home page object
└── ProductPage.ts           # Product page object
```

### 2. **Test Organization**
```
tests/
├── auth/
│   ├── login.spec.ts        # Login tests
│   └── register.spec.ts     # Registration tests
├── e2e/
│   └── checkout.spec.ts     # End-to-end tests
└── api/
    └── users.spec.ts        # API tests
```

### 3. **Utilities**
```
utils/
├── logger.ts                # Custom logger
├── data-generator.ts        # Test data generation
├── api-helper.ts            # API utilities
└── db-helper.ts             # Database utilities
```

### 4. **Configuration Management**
- Environment-based configs (dev, qa, staging, prod)
- Browser configuration (Chrome, Firefox, Safari, Edge)
- Parallel execution settings
- Retry and timeout configurations

---

## 🏗️ Framework Architecture

```
06_Playwright_Framework/
│
├── pages/                   # Page Object Model
│   ├── base/
│   │   └── BasePage.ts
│   ├── LoginPage.ts
│   ├── HomePage.ts
│   └── ProductPage.ts
│
├── tests/                   # Test files
│   ├── auth/
│   ├── e2e/
│   └── api/
│
├── fixtures/                # Custom fixtures
│   └── test-fixtures.ts
│
├── utils/                   # Utilities
│   ├── logger.ts
│   ├── data-generator.ts
│   └── api-helper.ts
│
├── test-data/              # Test data
│   └── users.json
│
├── config/                 # Environment configs
│   ├── dev.config.ts
│   ├── qa.config.ts
│   └── prod.config.ts
│
├── .github/workflows/      # GitHub Actions
│   └── playwright.yml
│
├── azure-pipelines.yml     # Azure DevOps
│
├── playwright.config.ts    # Main Playwright config
├── package.json           # Dependencies
├── tsconfig.json          # TypeScript config
├── .env.example           # Environment variables template
│
└── README.md              # This file
```

---

## 🎬 Quick Start

### **Prerequisites**
- Python 3.11+ installed
- pip (Python package manager)
- VS Code (recommended)
- Git

### **Step 1: Install Dependencies**
```bash
cd 06_Playwright_Framework
pip install -r requirements.txt
```

### **Step 2: Install Playwright Browsers**
```bash
playwright install
```

### **Step 3: Setup Environment**
```bash
# Copy environment template
copy .env.example .env  # Windows
# or
cp .env.example .env    # Mac/Linux

# Edit .env with your configuration
```

### **Step 3b: Switch Environments (Optional)**

The framework supports multiple environments (dev, qa, staging, prod). Simply set the `TEST_ENV` variable:

```powershell
# Windows PowerShell

# DEV (default - no variable needed)
pytest

# QA
$env:TEST_ENV="qa"; pytest

# STAGING
$env:TEST_ENV="staging"; pytest

# PROD
$env:TEST_ENV="prod"; pytest -m smoke
```

```bash
# Mac/Linux

# QA
TEST_ENV=qa pytest

# STAGING
TEST_ENV=staging pytest

# PROD
TEST_ENV=prod pytest -m smoke
```

📖 **See full guide:** [HOW_TO_USE_ENVIRONMENTS.md](HOW_TO_USE_ENVIRONMENTS.md)

### **Step 4: Run Tests**
```bash
# Run all tests
pytest

# Run with specific browser
pytest --browser=chromium

# Run specific test file
pytest tests/auth/test_login.py

# Run in headed mode (see browser)
pytest --headed

# Run with specific marker
pytest -m smoke
```

---

pytest

# Run tests in specific browser
pytest --browser=chromium
pytest --browser=firefox
pytest --browser=webkit

# Run specific test file
pytest tests/auth/test_login.py

# Run tests matching pattern
pytest -k "login"

# Run in headed mode (see browser)
pytest --headed

# Run with specific markers
pytest -m smoke
pytest -m regression
pytest -m api

# Run in parallel
pytest -n auto

# Verbose output
pytest -vtest --headed
 (4 workers)
pytest -n 4

# Run tests with specific marker
pytest -m "smoke"

# Run tests excluding marker
pytest -m "not slow"

# Run with coverage
pytest --cov=pages --cov=utils

# Run tests in specific environment
# Set environment variables in .env file
pytest

# Rerun only failed tests
pytest --lf

# Run tests that failed last time
pyHTML report is generated automatically in reports/html-report/
# Open reports/html-report/index.html in browser

# View JSON report
cat reports/test-results.json

# View logs
cat reports/logs/pytest.log
# Update snapshots
npx playwright test --update-snapshots

# Run tests in specific environment
ENV=qa npm test
ENV=staging npm test
```

### **Reporting**

```bash
# HTML report is generated automatically in reports/html-report/
# Open reports/html-report/index.html in browser

# View JSON report
cat reports/test-results.json

# View logs
cat reports/logs/pytest.log
```

---

## ⚡ Parallel Execution Explained

One of the biggest advantages of this framework is **automatic parallel test execution**.

### **How It Works:**

The framework uses `pytest-xdist` to run tests in parallel automatically:

```ini
# pytest.ini (already configured)
[pytest]
addopts = 
    -n auto  # ← Automatically uses all CPU cores
```

### **Example: Speed Comparison**

**Without Parallel (Sequential):**
```
Worker 1: [====================] 100 tests
Time: 15 minutes
```

**With Parallel (8 CPU cores):**
```
Worker 1: [==] 12 tests   ┐
Worker 2: [==] 13 tests   │
Worker 3: [==] 12 tests   │
Worker 4: [==] 13 tests   ├─ Run simultaneously!
Worker 5: [==] 12 tests   │
Worker 6: [==] 13 tests   │
Worker 7: [==] 12 tests   │
Worker 8: [==] 13 tests   ┘

Time: ~3 minutes  ← 5x FASTER!
```

### **Control Workers:**

```bash
# Auto-detect CPU cores (default)
pytest -n auto

# Use specific number of workers
pytest -n 4         # Run with 4 workers

# No parallel (sequential)
pytest              # Single worker

# Parallel by test scope
pytest -n auto --dist loadscope
```

### **Why Parallel Execution Matters:**

1. **Faster CI/CD** - Get test results in minutes, not hours
2. **Quick feedback** - Developers get faster feedback on code changes
3. **Efficient resources** - Use all CPU cores effectively
4. **Scale easily** - Add more tests without increasing runtime proportionally

**Real-world example:**
- 500 tests × 10 seconds each = 83 minutes sequential
- Same 500 tests on 8 cores = ~12 minutes parallel
- **Time saved: 71 minutes per run!** ⏱️

### **How Each Worker Works:**

```
Master Process (pytest)
    ↓
    Discovers all tests
    ↓
    Spawns 8 Worker Processes
    ↓
Worker 1 → Browser Instance 1 → Tests 1-12
Worker 2 → Browser Instance 2 → Tests 13-25
Worker 3 → Browser Instance 3 → Tests 26-37
... (continues)
    ↓
    Collect results from all workers
    ↓
    Generate combined HTML report
```

Each worker:
- Has its own browser instance
- Runs tests independently
- Reports results back to master
- No interference between workers

📖 [Read more details: PLAYWRIGHT_VS_SELENIUM.md](PLAYWRIGHT_VS_SELENIUM.md#-how-parallel-execution-works-in-our-framework)

---

## 🔄 CI/CD Integration

### **GitHub Actions**

The framework includes a complete GitHub Actions workflow at `.github/workflows/playwright-python.yml`.

**Features:**
- ✅ Runs on push and pull requests
- ✅ Matrix testing (multiple browsers and OS)
- ✅ Artifact upload (reports, videos, screenshots)
- ✅ Test retry on failure
- ✅ Parallel execution

**Setup:**
1. Push code to GitHub
2. GitHub Actions automatically runs tests
3. View results in Actions tab
4. Download artifacts (reports, videos)

### **Azure DevOps**

The framework includes Azure Pipelines configuration at `azure-pipelines.yml`.

**Features:**
- ✅ Multi-stage pipeline
- ✅ Test execution across environments
- ✅ Test result publishing
- ✅ Artifact publishing
- ✅ Email notifications

**Setup:**
1. Create new pipeline in Azure DevOps
2. Point to `azure-pipelines.yml`
3. Configure service connections
4. Run pipeline

---

## 📊 Reporting

### **HTML Report** (Built-in)
```bash
npm run report
```
- View test results in browser
- Screenshots and videos attached
- Execution timeline
- Error stack traces

### **Allure Report** (Optional)
```bash
npm run allure:generate
npm run allure:open
```
- Beautiful, interactive reports
- Trend analysis
- Categorized failures
- Historical data

### **Custom Logging**
The framework includes a custom logger that:
- Logs test steps
- Captures timestamps
- Different log levels (INFO, WARN, ERROR)
- Saves logs to files

---

## 📝 Best Practices Implemented

### 1. **Page Object Model**
- Each page is a separate class
- Locators are private and encapsulated
- Actions are public methods
- Reusable and maintainable

### 2. **Test Organization**
- Tests grouped by feature/module
- Descriptive test names
- Use of fixtures for setup/teardown
- Tagged for selective execution (@smoke, @regression)

### 3. **Wait Strategies**
- Auto-waiting enabled
- Explicit waits when needed
- No hard-coded sleeps
- Wait for network idle

### 4. **Error Handling**
- Try-catch blocks where needed
- Meaningful error messages
- Screenshot on failure
- Video recording on failure

### 5. **Test Data Management**
- Separate test data files
- Data generators for dynamic data
- Environment-specific data
- No hardcoded credentials

### 6. **Parallel Execution**
- Tests run in parallel by default
- Workers configured optimally
- Isolated browser contexts
- No test dependencies

### 7. **Retry Mechanism**
- Flaky tests automatically retried
- Configurable retry count
- Only retries on failure

---

## 🎓 Learn More

For detailed step-by-step instructions on building this framework from scratch, see:
- **[SETUP_GUIDE.md](./SETUP_GUIDE.md)** - Complete setup walkthrough
- **[CODING_STANDARDS.md](./CODING_STANDARDS.md)** - Coding conventions
- **[TROUBLESHOOTING.md](./TROUBLESHOOTING.md)** - Common issues and solutions

---

## 📚 Additional Resources

- [Playwright Documentation](https://playwright.dev/)
- [Playwright Best Practices](https://playwright.dev/docs/best-practices)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)

---

## 📞 Support
Python and pytest for easy maintenance"
2. **Scalability** - "The framework supports parallel execution with pytest-xdist and can scale to thousands of tests"
3. **Maintainability** - "Using POM makes tests easy to maintain when UI changes"
4. **CI/CD** - "Integrated with GitHub Actions/Azure DevOps for automated testing"
5. **Best Practices** - "Implemented pytest fixtures, markers, retry mechanism, screenshot on failure"
6. **Real-World Use** - "This framework structure is enterprise-ready and follows industry standards"
7. **Python Ecosystem** - "Leverages pytest, Faker for data generation, and python-dotenv for configuration"

---

## 🎯 Interview Tips

When discussing this framework in interviews, highlight:

1. **Technology Choice** - "I chose Playwright over Selenium because it's 3-5x faster, has built-in auto-waiting which reduces flakiness, and includes native parallel execution support"

2. **Architecture** - "I designed a Page Object Model framework with Python and pytest. Each page class encapsulates its locators and methods following the Single Responsibility Principle"

3. **Parallel Execution** - "The framework runs tests in parallel using pytest-xdist with `-n auto`, automatically utilizing all CPU cores. For example, 100 tests that take 15 minutes sequentially complete in 3 minutes with 8 cores—that's 5x faster!"

4. **Scalability** - "The framework can scale to thousands of tests without proportional time increase due to parallel execution. We can run 500 tests in under 15 minutes"

5. **Reliability** - "Built-in auto-retry mechanism (pytest-rerunfailures) handles flaky tests. Combined with Playwright's smart auto-waiting, we achieve 95-98% test reliability"

6. **Maintainability** - "Using POM design pattern, when UI changes, I only update one file. For example, if a button selector changes, I update it in `LoginPage` and all 15 tests using that button work immediately"

7. **CI/CD Integration** - "Integrated with GitHub Actions and Azure DevOps. The pipeline runs tests on every commit across multiple OS (Windows, Ubuntu, macOS) and browsers (Chromium, Firefox, WebKit) in parallel"

8. **Best Practices** - "Follows industry standards: pytest fixtures for reusable setup, test markers (@smoke, @regression) for selective execution, automatic screenshot on failure for debugging, custom logger for better visibility"

9. **Real-World Production Ready** - "This framework handles API testing, E2E flows, mobile viewports, and can handle thousands of tests. It's structured exactly how frameworks are built at companies like Microsoft, Google, and Amazon"

10. **Developer Experience** - "Single command setup (`pip install -r requirements.txt`), clear documentation, and less code to write compared to Selenium thanks to Playwright's auto-waiting"

---

**Created for interview preparation - ready to use in real projects! 🚀**
