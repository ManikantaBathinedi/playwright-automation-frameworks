using Microsoft.Playwright;
using Microsoft.Playwright.NUnit;
using NUnit.Framework;
using PlaywrightFramework.Config;
using PlaywrightFramework.Utilities;

namespace PlaywrightFramework.Tests;

/// <summary>
/// Base test class with common setup and teardown
/// Inherits from PageTest which provides Playwright context
/// </summary>
[TestFixture]
public class BaseTest : PageTest
{
    protected Settings Settings;

    [SetUp]
    public async Task SetUp()
    {
        Settings = Config.Settings.Instance;
        TestLogger.TestStart(TestContext.CurrentContext.Test.Name);
        
        // Log browser being used
        var browserName = BrowserName ?? "chromium";
        TestLogger.Info($"🌐 Browser: {browserName}");
        
        // Configure browser options (only for UI tests that use Context)
        try
        {
            if (Context != null)
            {
                await Context.Tracing.StartAsync(new()
                {
                    Screenshots = true,
                    Snapshots = true,
                    Sources = true
                });
            }
        }
        catch
        {
            // Context not available for API-only tests, skip tracing
        }
    }

    [TearDown]
    public async Task TearDown()
    {
        var testName = TestContext.CurrentContext.Test.Name;
        var testPassed = TestContext.CurrentContext.Result.Outcome.Status == NUnit.Framework.Interfaces.TestStatus.Passed;

        try
        {
            // Take screenshot on failure (only for UI tests)
            if (!testPassed && Settings.TakeScreenshotOnFailure && Page != null)
            {
                var screenshotPath = $"screenshots/{testName}_{DateTime.Now:yyyyMMdd_HHmmss}.png";
                Directory.CreateDirectory("screenshots");
                await Page.ScreenshotAsync(new() { Path = screenshotPath, FullPage = true });
                TestLogger.Info($"Screenshot saved: {screenshotPath}");
            }

            // Stop tracing (only if it was started)
            if (Context != null)
            {
                await Context.Tracing.StopAsync(new()
                {
                    Path = $"traces/{testName}.zip"
                });
            }
        }
        catch
        {
            // Ignore teardown errors for API tests
        }

        TestLogger.TestEnd(testName, testPassed);
    }

    public override BrowserNewContextOptions ContextOptions()
    {
        return new BrowserNewContextOptions
        {
            BaseURL = Config.Settings.Instance.BaseUrl,
            ViewportSize = new ViewportSize { Width = 1280, Height = 720 },
            IgnoreHTTPSErrors = true,
            RecordVideoDir = Config.Settings.Instance.RecordVideo ? "videos/" : null,
            RecordVideoSize = Config.Settings.Instance.RecordVideo ? new RecordVideoSize { Width = 1280, Height = 720 } : null
        };
    }
}
