using Microsoft.Playwright;
using Microsoft.Playwright.NUnit;
using PlaywrightFramework.Config;
using PlaywrightFramework.Utilities;

namespace PlaywrightFramework.Tests;

/// <summary>
/// Base test class with common setup and teardown
/// Inherits from PageTest which provides Playwright context
/// </summary>
[TestFixture]
[Retry(2)]  // Retry failed tests up to 2 times
public class BaseTest : PageTest
{
    protected Settings Settings;

    [SetUp]
    public async Task SetUp()
    {
        Settings = Settings.Instance;
        TestLogger.TestStart(TestContext.CurrentContext.Test.Name);
        
        // Log browser being used
        var browserName = BrowserName ?? "chromium";
        TestLogger.Info($"🌐 Browser: {browserName}");
        
        // Configure browser options
        await Context.Tracing.StartAsync(new()
        {
            Screenshots = true,
            Snapshots = true,
            Sources = true
        });
    }

    [TearDown]
    public async Task TearDown()
    {
        var testName = TestContext.CurrentContext.Test.Name;
        var testPassed = TestContext.CurrentContext.Result.Outcome.Status == NUnit.Framework.Interfaces.TestStatus.Passed;

        // Take screenshot on failure
        if (!testPassed && Settings.TakeScreenshotOnFailure)
        {
            var screenshotPath = $"screenshots/{testName}_{DateTime.Now:yyyyMMdd_HHmmss}.png";
            Directory.CreateDirectory("screenshots");
            await Page.ScreenshotAsync(new() { Path = screenshotPath, FullPage = true });
            TestLogger.Info($"Screenshot saved: {screenshotPath}");
        }

        // Stop tracing
        await Context.Tracing.StopAsync(new()
        {
            Path = $"traces/{testName}.zip"
        });

        TestLogger.TestEnd(testName, testPassed);
    }

    /// <summary>
    /// Override to set browser type (chromium, firefox, webkit)
    /// Can be controlled via BROWSER environment variable
    /// </summary>
    public override BrowserName BrowserName
    {
        get
        {
            var browserEnv = Environment.GetEnvironmentVariable("BROWSER")?.ToLower();
            return browserEnv switch
            {
                "chrome" => Microsoft.Playwright.BrowserName.Chromium, // chrome maps to chromium
                "chromium" => Microsoft.Playwright.BrowserName.Chromium,
                "firefox" => Microsoft.Playwright.BrowserName.Firefox,
                "webkit" => Microsoft.Playwright.BrowserName.Webkit,
                _ => Microsoft.Playwright.BrowserName.Chromium // default
            };
        }
    }

    public override BrowserNewContextOptions ContextOptions()
    {
        return new BrowserNewContextOptions
        {
            BaseURL = Settings.BaseUrl,
            ViewportSize = new ViewportSize { Width = 1280, Height = 720 },
            IgnoreHTTPSErrors = true,
            RecordVideoDir = Settings.RecordVideo ? "videos/" : null,
            RecordVideoSize = Settings.RecordVideo ? new RecordVideoSize { Width = 1280, Height = 720 } : null
        };
    }
}
