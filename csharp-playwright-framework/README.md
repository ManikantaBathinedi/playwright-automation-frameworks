# 🎭 Playwright C# Framework - Visual Studio Edition

A production-ready Playwright automation framework using **C# + NUnit**, designed for **Visual Studio Test Explorer**!

---

## ✨ Features

- ✅ **Visual Studio Test Explorer Integration** - Run, debug, and analyze tests from VS
- ✅ **NUnit Framework** - Industry-standard testing framework for .NET
- ✅ **Page Object Model (POM)** - Clean, maintainable test code
- ✅ **Multi-Environment Support** - Dev, QA, Staging, Prod configurations
- ✅ **Fluent Assertions** - Readable and expressive test assertions
- ✅ **Serilog Logging** - Beautiful console and file logging
- ✅ **Bogus Data Generator** - Realistic test data generation
- ✅ **Parallel Execution** - Fast test execution with NUnit workers
- ✅ **Screenshot on Failure** - Automatic debugging aid
- ✅ **Trace Files** - Playwright trace for test debugging
- ✅ **CI/CD Ready** - GitHub Actions + Azure DevOps pipelines included
- ✅ **Matrix Testing** - 3 OS × 3 Browsers = 9 test combinations

---

## 🚀 Quick Start

### **Step 0: Clone the Repository**

```bash
# Clone the repository
git clone https://github.com/ManikantaBathinedi/playwright-automation-frameworks.git

# Navigate to C# framework folder
cd playwright-automation-frameworks/csharp-playwright-framework
```

---

### **Step 1: Open in Visual Studio**

1. Open Visual Studio 2022 (or later)
2. File → Open → Project/Solution
3. Navigate to: `06_Playwright_Framework_CSharp\PlaywrightFramework.sln`
4. Click "Open"

---

### **Step 2: Restore NuGet Packages**

Visual Studio will automatically restore packages, or:

```
Right-click Solution → Restore NuGet Packages
```

Or use Package Manager Console:
```powershell
dotnet restore
```

---

### **Step 3: Install Playwright Browsers**

Open **Package Manager Console** (Tools → NuGet Package Manager → Package Manager Console):

```powershell
pwsh bin/Debug/net8.0/playwright.ps1 install
```

Or use Terminal:
```powershell
cd PlaywrightFramework
dotnet build
powershell bin/Debug/net8.0/playwright.ps1 install
```

---

### **Step 4: Run Tests from Test Explorer**

1. **Open Test Explorer**: View → Test Explorer (or Ctrl+E, T)
2. Click **"Run All"** to run all tests
3. Or right-click individual tests to run specific ones

---

## 🎮 Using Test Explorer

### **Run Tests:**
- **Run All**: Green play button at top
- **Run Specific Test**: Right-click test → Run
- **Run Category**: Right-click category → Run
- **Debug Test**: Right-click test → Debug

### **View Results:**
- ✅ **Green checkmark** = Passed
- ❌ **Red X** = Failed
- ⚠️ **Yellow warning** = Skipped

### **Group Tests:**
- By **Class**
- By **Namespace**
- By **Category** (Smoke, Regression, Auth, etc.)
- By **Status** (Passed, Failed)

---

## 🌍 Switch Environments

Set environment variable **before** opening Visual Studio:

```powershell
# Windows PowerShell

# Set to DEV (default)
$env:TEST_ENV="dev"

# Set to QA
$env:TEST_ENV="qa"

# Set to STAGING
$env:TEST_ENV="staging"

# Set to PROD
$env:TEST_ENV="prod"

# Then start Visual Studio
code # or just open Visual Studio
```

**Or configure in Visual Studio:**
1. Right-click project → Properties
2. Debug → General → Open debug launch profiles UI
3. Add environment variable: `TEST_ENV` = `qa`

---

## 📁 Project Structure

```
PlaywrightFramework/
│
├── Pages/                      # Page Object Model
│   ├── BasePage.cs            # Base class with common methods
│   ├── LoginPage.cs           # Login page object
│   ├── HomePage.cs            # Home page object
│   └── ProductPage.cs         # Product/shopping page object
│
├── Tests/                      # Test files
│   ├── BaseTest.cs            # Base test class
│   ├── Auth/
│   │   └── LoginTests.cs      # Login test cases (8 tests)
│   ├── E2E/
│   │   └── CheckoutTests.cs   # End-to-end tests (6 tests)
│   └── API/
│       └── UsersApiTests.cs   # API tests (12 tests)
│
├── Config/                     # Configuration
│   └── Settings.cs            # Settings singleton
│
├── Utilities/                  # Helper classes
│   ├── Logger.cs              # Serilog logger
│   └── DataGenerator.cs       # Bogus data generator
│
├── appsettings.json           # Default configuration
├── appsettings.dev.json       # Dev environment
├── appsettings.qa.json        # QA environment
├── appsettings.staging.json   # Staging environment
└── appsettings.prod.json      # Prod environment
```

---

## 🏷️ Test Categories

Tests are organized by categories (visible in Test Explorer):

| Category | Description | Test Count | File Location |
|----------|-------------|------------|---------------|
| **Auth** | Authentication tests | 8 | Tests/Auth/LoginTests.cs |
| **E2E** | End-to-end user journeys | 6 | Tests/E2E/CheckoutTests.cs |
| **API** | API endpoint validation | 12 | Tests/API/UsersApiTests.cs |
| **Smoke** | Critical path (quick) | 3 | Across all categories |
| **Regression** | Full test suite | 26 | All test files |
| **Negative** | Error handling | 4 | Login + API tests |
| **Security** | Security validation | 5 | SQL injection, XSS |
| **Performance** | Response time checks | 1 | API tests |

**Total: 26 tests** across 3 test files

**Filter by category in Test Explorer:**
```
Right-click category → Run Selected Tests
Or search: Category:Smoke
```

---

## ⚙️ Configuration

### **Environment-Specific Settings:**

| Setting | DEV | QA | STAGING | PROD |
|---------|-----|----|---------| -----|
| **Headless** | false (visible) | true | true | true |
| **MaxWorkers** | 2 | 4 | 6 | 2 |
| **MaxRetries** | 1 | 2 | 2 | 0 |
| **SlowMo** | 100ms | 0ms | 0ms | 0ms |

Edit `appsettings.<env>.json` to customize!

---

## 🔧 Common Tasks

### **Run Specific Category:**

**In Test Explorer:**
1. Group by: Category
2. Right-click "Smoke"
3. Click "Run"

**In Code:**
```csharp
[Test]
[Category("Smoke")]
[Category("Auth")]
public async Task MyTest()
{
    // Test code
}
```

---

### **Debug a Test:**

1. Set breakpoint in test code
2. Right-click test in Test Explorer
3. Click "Debug"
4. Test will pause at breakpoint!

---

### **View Test Output:**

1. Click test in Test Explorer
2. Look at bottom pane "Test Detail Summary"
3. View logs, assertions, and errors

---

### **Run Tests in Parallel:**

Configured in `.runsettings`:
```xml
<NumberOfTestWorkers>4</NumberOfTestWorkers>
```

Or set in Test Explorer:
1. Test → Configure Run Settings
2. Select .runsettings file

---
## 🚀 CI/CD Pipelines

This framework includes **production-ready CI/CD pipelines** for both GitHub Actions and Azure DevOps.

### **GitHub Actions**
- File: [.github/workflows/playwright-csharp.yml](.github/workflows/playwright-csharp.yml)
- **5 Jobs**: Test Matrix (9 combinations), Smoke Tests, Security Tests, Full Regression, Test Summary
- **Matrix Strategy**: 3 OS (Ubuntu/Windows/macOS) × 3 Browsers (Chromium/Firefox/WebKit)
- **Triggers**: Push, Pull Request, Manual

### **Azure DevOps**
- File: [azure-pipelines-csharp.yml](azure-pipelines-csharp.yml)
- **3 Stages**: Build, Test, Report
- **Test Jobs**: Smoke Tests, Security Tests, Full Regression Suite
- **Artifacts**: Test results, screenshots, traces, HTML reports

### **What Pipelines Do:**
✅ Build project in Release mode  
✅ Install Playwright browsers  
✅ Run tests with environment switching  
✅ Execute category-specific test suites (Smoke, Security, Regression)  
✅ Upload test results (TRX, HTML)  
✅ Save debug artifacts (screenshots, traces, videos)  
✅ Publish test reports  
✅ Generate execution summary

📖 **Full Guide:** See [CI_CD_GUIDE.md](CI_CD_GUIDE.md) for detailed setup and usage

---
## 📝 Writing New Tests

### **1. Create Test Class:**

```csharp
using FluentAssertions;
using PlaywrightFramework.Pages;

namespace PlaywrightFramework.Tests.MyFeature;

[TestFixture]
[Category("Smoke")]
public class MyFeatureTests : BaseTest
{
    [Test]
    [Description("Test description here")]
    public async Task Test_MyFeature_WorksCorrectly()
    {
        // Arrange
        var loginPage = new LoginPage(Page);
        await loginPage.GotoAsync(Settings.BaseUrl);

        // Act
        await loginPage.LoginAsync("test@example.com", "password");

        // Assert
        var homePage = new HomePage(Page);
        var isLoggedIn = await homePage.IsLoggedInAsync();
        isLoggedIn.Should().BeTrue();
    }
}
```

### **2. Test Appears in Test Explorer Automatically!**

Build solution → Test Explorer refreshes → New test appears!

---

## 🎓 Interview Talking Points

> **Q: Tell me about your C# Playwright framework**
>
> "I built a production-ready Playwright framework using C# and NUnit, designed for Visual Studio Test Explorer integration. Key features include:
>
> **Architecture:** Page Object Model with a BasePage containing 40+ reusable methods. Tests inherit from BaseTest which handles setup, teardown, screenshots on failure, and Playwright trace generation.
>
> **Test Organization:** NUnit categories (Smoke, Regression, Auth, Security) allow flexible test filtering in Test Explorer. I can run all smoke tests with one click, or debug individual tests with breakpoints.
>
> **Configuration:** Environment-specific settings using appsettings.json with automatic selection based on TEST_ENV variable. Dev uses visible browser for debugging, QA runs headless with 4 parallel workers.
>
> **Tools:** FluentAssertions for readable assertions, Serilog for structured logging with emojis, Bogus for realistic test data generation.
>
> **Visual Studio Integration:** Full Test Explorer support - run, debug, group by category, view test output, parallel execution. This makes it developer-friendly unlike command-line-only frameworks."

---

## 🎯 Tips & Tricks

### **Tip 1: Use Live Unit Testing**

Visual Studio Enterprise:
- Test → Live Unit Testing → Start
- Tests run automatically as you code!

---

### **Tip 2: Test Playlists**

Create custom test playlists:
1. Select multiple tests
2. Right-click → Add to Playlist → New Playlist
3. Name it "My Smoke Tests"
4. Run playlist anytime!

---

### **Tip 3: Code Coverage**

```
Test → Analyze Code Coverage for All Tests
```
See which code is tested!

---

### **Tip 4: Keyboard Shortcuts**

- **Ctrl+R, T** = Run all tests
- **Ctrl+R, Ctrl+T** = Debug all tests
- **Ctrl+E, T** = Open Test Explorer

---

## � CI/CD Pipelines

This framework includes **production-ready CI/CD pipelines** for both GitHub Actions and Azure DevOps!

### **GitHub Actions**
- **File**: `.github/workflows/playwright-csharp.yml`
- **Jobs**: Test Matrix (3 OS × 3 Browsers), Smoke Tests, Security Tests, Full Regression, Test Summary
- **Triggers**: Push, Pull Requests, Manual Dispatch

### **Azure DevOps**
- **File**: `azure-pipelines-csharp.yml`
- **Stages**: Build → Test → Report
- **Jobs**: Smoke Tests, Security Tests, Full Regression Suite

### **What Pipelines Do:**
✅ Build project in Release mode  
✅ Install Playwright browsers  
✅ Run tests across multiple OS/browsers  
✅ Execute category-specific tests (Smoke, Security, Regression)  
✅ Upload test results (TRX, HTML reports)  
✅ Save debug artifacts (screenshots, traces, videos)  
✅ Generate execution summary  

📖 **Full CI/CD Guide**: See [CI_CD_GUIDE.md](CI_CD_GUIDE.md) for complete setup instructions

---

## �📦 NuGet Packages Used

- **Microsoft.Playwright.NUnit** - Playwright + NUnit integration
- **NUnit** - Testing framework
- **FluentAssertions** - Readable assertions
- **Serilog** - Logging
- **Bogus** - Test data generation
- **Microsoft.Extensions.Configuration** - Configuration management

---

## 🎬 Next Steps

1. ✅ Open solution in Visual Studio
2. ✅ Build project (Ctrl+Shift+B)
3. ✅ Install Playwright browsers
4. ✅ Open Test Explorer (Ctrl+E, T)
5. ✅ Run all tests
6. ✅ View results and logs
7. ✅ Debug a test with breakpoints
8. ✅ Write your own test

---

**🚀 Ready to test! Open in Visual Studio and explore!**
