# 🚀 Getting Started with C# Playwright Framework

## Step-by-Step Setup Guide

### 📋 Prerequisites

Before you begin, make sure you have:
- ✅ Visual Studio 2022 (or later) - [Download here](https://visualstudio.microsoft.com/)
- ✅ .NET 8.0 SDK - [Download here](https://dotnet.microsoft.com/download)
- ✅ Git - [Download here](https://git-scm.com/)

---

## 🎯 Installation Steps

### Step 1: Clone the Repository

Open PowerShell or Command Prompt and run:

```bash
# Clone the repository
git clone https://github.com/ManikantaBathinedi/playwright-automation-frameworks.git

# Navigate to C# framework
cd playwright-automation-frameworks/csharp-playwright-framework
```

---

### Step 2: Open the Solution

1. Double-click on `PlaywrightFramework.sln` file
   - OR -
2. Open Visual Studio → File → Open → Project/Solution
3. Navigate to `PlaywrightFramework.sln` and click **Open**

Visual Studio will automatically restore NuGet packages.

---

### Step 3: Install Playwright Browsers

In Visual Studio, open **Package Manager Console**:
- Go to: **Tools → NuGet Package Manager → Package Manager Console**

Run this command:

```powershell
pwsh bin/Debug/net8.0/playwright.ps1 install chromium
```

**Alternative method** - using Terminal:

```powershell
cd PlaywrightFramework
dotnet build
pwsh bin/Debug/net8.0/playwright.ps1 install chromium
```

---

### Step 4: Run Your First Test

#### Option A: Using Test Explorer (Recommended)

1. Open **Test Explorer**: 
   - Menu: **Test → Test Explorer**
   - Or press: **Ctrl + E, T**

2. You'll see all tests organized by categories:
   - ✅ **Auth** - Login tests
   - ✅ **API** - API endpoint tests  
   - ✅ **Smoke** - Quick critical tests

3. Click the green **▶ Run All** button at the top

#### Option B: Using Command Line

```powershell
# Run all tests
dotnet test

# Run only smoke tests
dotnet test --filter "Category=Smoke"

# Run specific test
dotnet test --filter "FullyQualifiedName~LoginTests"
```

---

## ✅ Verify Installation

You should see output like this:

```
Passed!  - Failed:     0, Passed:     3, Skipped:     0, Total:     3
```

**Congratulations! 🎉 Your framework is ready!**

---

## 🎮 Running Tests

### Run Different Test Categories

In Test Explorer, you can filter by:

| Category | What it tests | Command Line |
|----------|---------------|--------------|
| **Smoke** | Critical functionality (3 tests) | `dotnet test --filter "Category=Smoke"` |
| **Auth** | Login/logout tests (8 tests) | `dotnet test --filter "Category=Auth"` |
| **API** | API endpoint tests (12 tests) | `dotnet test --filter "Category=API"` |
| **E2E** | End-to-end flows (6 tests) | `dotnet test --filter "Category=E2E"` |

### Debug a Test

1. Set a breakpoint in your test code (click left margin)
2. Right-click the test in Test Explorer
3. Click **Debug**
4. Test will pause at your breakpoint

---

## 🌍 Switch Environments

The framework supports multiple environments:

```powershell
# QA Environment (default for demo)
$env:TEST_ENV="qa"
dotnet test

# Dev Environment
$env:TEST_ENV="dev"
dotnet test

# Staging Environment
$env:TEST_ENV="staging"
dotnet test
```

**Configuration files:**
- `appsettings.qa.json` - QA settings (uses saucedemo.com)
- `appsettings.dev.json` - Dev settings
- `appsettings.staging.json` - Staging settings
- `appsettings.prod.json` - Production settings

---

## 📊 View Test Results

### In Test Explorer:
1. Click on any test after it runs
2. View the **Test Detail Summary** panel below
3. See:
   - ✅ Pass/Fail status
   - 📝 Console output
   - ⏱️ Duration
   - 🖼️ Screenshots (on failure)

### In Console:
- All test output appears in **Output** window
- View detailed logs with timestamps
- See which steps passed/failed

---

## 📁 Project Structure Overview

```
csharp-playwright-framework/
├── PlaywrightFramework/
│   ├── Pages/              # Page Object Model files
│   │   ├── LoginPage.cs    # Login page interactions
│   │   ├── HomePage.cs     # Home page interactions
│   │   └── ProductPage.cs  # Product page interactions
│   │
│   ├── Tests/              # Test files
│   │   ├── Auth/           # Login/Auth tests
│   │   ├── API/            # API tests
│   │   └── E2E/            # End-to-end tests
│   │
│   ├── Config/             # Configuration
│   │   └── Settings.cs     # Environment settings
│   │
│   └── Utilities/          # Helper classes
│       ├── Logger.cs       # Logging
│       └── DataGenerator.cs # Test data
│
├── appsettings.*.json      # Environment configs
└── GETTING_STARTED.md      # This file
```

---

## 🆘 Troubleshooting

### Problem: Tests fail with browser not found

**Solution:**
```powershell
# Reinstall browsers
pwsh bin/Debug/net8.0/playwright.ps1 install
```

### Problem: NuGet packages not restored

**Solution:**
```powershell
# In Visual Studio
Right-click Solution → Restore NuGet Packages

# OR in terminal
dotnet restore
```

### Problem: Can't see tests in Test Explorer

**Solution:**
1. Build the solution: **Ctrl + Shift + B**
2. Close and reopen Test Explorer
3. Click refresh button in Test Explorer

### Problem: Tests fail with connection errors

**Solution:**
- Check your internet connection
- The framework uses `https://www.saucedemo.com` and `https://jsonplaceholder.typicode.com`
- Make sure these URLs are accessible

---

## 🎓 What's Next?

1. ✅ **Explore the tests** - Open test files and see how they work
2. ✅ **Modify a test** - Change assertions and see results
3. ✅ **Create new tests** - Copy existing test structure
4. ✅ **Run in parallel** - Edit `.runsettings` to increase workers
5. ✅ **Check CI/CD** - View GitHub Actions workflow in `.github/workflows/`

---

## 📚 Additional Resources

- 📖 [Full README](README.md) - Complete framework documentation
- 🎯 [Quick Reference](QUICK_REFERENCE.md) - Command cheatsheet
- 🔧 [Playwright Docs](https://playwright.dev/dotnet) - Official Playwright for .NET docs
- 🧪 [NUnit Docs](https://docs.nunit.org/) - NUnit testing framework

---

## ✨ Success Criteria

You're ready to start developing when:

- ✅ All 3 smoke tests pass
- ✅ You can see tests in Test Explorer
- ✅ You can run and debug individual tests
- ✅ Screenshots appear in `/screenshots` folder on failures

**Happy Testing! 🎉**
