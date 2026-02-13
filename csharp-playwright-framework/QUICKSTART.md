# 🚀 QUICKSTART - Visual Studio

## Open and Run in 5 Steps!

### **Step 1: Open Solution**
```
1. Open Visual Studio 2022
2. File → Open → Project/Solution
3. Select: 06_Playwright_Framework_CSharp\PlaywrightFramework.sln
4. Click "Open"
```

---

### **Step 2: Restore Packages**
```
Visual Studio will auto-restore packages
Or: Right-click solution → Restore NuGet Packages
```

---

### **Step 3: Install Playwright Browsers**

**Option A - Package Manager Console (Recommended):**
```powershell
# Open: Tools → NuGet Package Manager → Package Manager Console
pwsh bin/Debug/net8.0/playwright.ps1 install
```

**Option B - Terminal:**
```powershell
cd PlaywrightFramework
dotnet build
powershell bin/Debug/net8.0/playwright.ps1 install
```

---

### **Step 4: Open Test Explorer**
```
View → Test Explorer
Or press: Ctrl+E, T
```

---

### **Step 5: Run Tests!**
```
Click the green "Run All" button at top of Test Explorer
Or: Right-click any test → Run
```

---

## ✅ What You'll See

**Test Explorer shows:**
- ✅ 8 tests (7 pass, maybe 1 fails on demo site)
- Tests grouped by class/category
- Green checkmarks for passed tests
- Detailed output for each test

---

## 🎯 Quick Actions

```
Run all tests:          Click ▶ button
Run specific test:      Right-click test → Run
Debug test:             Right-click test → Debug
Run by category:        Group by Category → Right-click → Run
View test output:       Click test → See bottom pane
```

---

## 🌍 Switch Environments

**Before opening Visual Studio:**
```powershell
# Windows PowerShell
$env:TEST_ENV="qa"

# Then open Visual Studio
```

**Or in Visual Studio:**
```
Project → Properties → Debug → Environment Variables
Add: TEST_ENV = qa
```

---

## 🎬 What's Next?

1. ✅ Explore tests in Test Explorer
2. ✅ Set breakpoint in a test (click left margin)
3. ✅ Debug test (right-click → Debug)
4. ✅ Write your own test in `Tests/` folder
5. ✅ Add more page objects in `Pages/` folder

---

**You're all set! Happy testing! 🚀**

📖 **Full guide:** See [README.md](README.md)
