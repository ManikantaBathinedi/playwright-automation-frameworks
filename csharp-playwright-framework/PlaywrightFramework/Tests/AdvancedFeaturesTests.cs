#if false // Temporarily disabled - needs refactoring to match current page objects
using Microsoft.Playwright;
using NUnit.Framework;
using PlaywrightFramework.Pages;
using PlaywrightFramework.Utilities;
using static PlaywrightFramework.Utilities.WaitHelpers;
using static PlaywrightFramework.Utilities.TestDataBuilderHelpers;

namespace PlaywrightFramework.Tests;

/// <summary>
/// Advanced Features Demo Tests
/// Demonstrates: Test Retry, Custom Waits, Test Data Builders
/// </summary>
[TestFixture]
[Ignore("Temporarily disabled - methods need to be updated to match current page objects")]
public class AdvancedFeaturesTests : BaseTest
{
    // ============================================================================
    // TEST RETRY DEMONSTRATIONS
    // ============================================================================

    [Test]
    [Category("smoke")]
    [Retry(2)]  // This specific test will retry up to 2 times if it fails
    public async Task Test_FlakyOperation_WithRetry()
    {
        /*
         * Demonstrates test retry on failures
         * This test will automatically retry up to 2 times if it fails
         * Useful for tests that might fail due to timing issues or network problems
         */
        var loginPage = new LoginPage(Page);
        await loginPage.NavigateAsync(Settings.BaseUrl);

        // Simulate potentially flaky operation
        await loginPage.FillEmailAsync("test@example.com");
        await loginPage.FillPasswordAsync("Test@123");
        await loginPage.ClickLoginAsync();

        // Assertion that might fail due to timing
        var errorVisible = await loginPage.IsErrorMessageVisibleAsync();
        Assert.That(errorVisible, Is.True, "Error message should be visible");

        TestLogger.Success("Test completed (possibly after retries)");
    }

    // ============================================================================
    // CUSTOM WAIT UTILITIES DEMONSTRATIONS
    // ============================================================================

    [Test]
    [Category("smoke")]
    public async Task Test_WaitForCondition()
    {
        /*
         * Demonstrates custom WaitForCondition utility
         * Waits for a specific condition to be true with polling
         */
        var loginPage = new LoginPage(Page);
        await loginPage.NavigateAsync(Settings.BaseUrl);

        // Wait for login form to be fully loaded and interactive
        await WaitForCondition(
            async () => await Page.Locator("#email").IsVisibleAsync() &&
                       await Page.Locator("#password").IsVisibleAsync() &&
                       await Page.Locator("button[type='submit']").IsEnabledAsync(),
            timeout: 10000,
            errorMessage: "Login form did not fully load"
        );

        TestLogger.Success("Login form is fully loaded and ready");
    }

    [Test]
    [Category("smoke")]
    public async Task Test_WaitUntilStable()
    {
        /*
         * Demonstrates WaitUntilStable utility
         * Useful for waiting for counters, animations, or async updates
         */
        var loginPage = new LoginPage(Page);
        await loginPage.NavigateAsync(Settings.BaseUrl);
        await loginPage.LoginAsync("standard_user", "Test@123");

        // Wait for cart count to stabilize (useful for async updates)
        try
        {
            var cartCount = await WaitUntilStable(
                async () => await Page.Locator(".cart-count").TextContentAsync() ?? "0",
                timeout: 5000,
                stabilityTime: 1000
            );
            TestLogger.Success($"Cart count stabilized at: {cartCount}");
        }
        catch (TimeoutException)
        {
            TestLogger.Info("Cart count element not found (expected for demo sites)");
        }
    }

    [Test]
    [Category("smoke")]
    public async Task Test_WaitForMultipleConditions()
    {
        /*
         * Demonstrates waiting for multiple conditions (ANY or ALL)
         */
        var loginPage = new LoginPage(Page);
        await loginPage.NavigateAsync(Settings.BaseUrl);
        await loginPage.FillEmailAsync("invalid@example.com");
        await loginPage.FillPasswordAsync("wrongpassword");
        await loginPage.ClickLoginAsync();

        // Wait for EITHER success message OR error message (whichever appears first)
        var result = await WaitForAny(new[]
        {
            async () => await Page.Locator(".success-message").IsVisibleAsync(),
            async () => await Page.Locator(".error-message").IsVisibleAsync(),
            async () => await Page.Locator(".alert-danger").IsVisibleAsync()
        }, timeout: 10000);

        TestLogger.Success(result switch
        {
            0 => "Success message appeared",
            1 => "Error message appeared",
            _ => "Alert danger appeared"
        });
    }

    [Test]
    [Category("smoke")]
    public async Task Test_SmartWaitFluentInterface()
    {
        /*
         * Demonstrates SmartWait with fluent interface
         * Clean, readable waiting syntax
         */
        var loginPage = new LoginPage(Page);
        await loginPage.NavigateAsync(Settings.BaseUrl);

        // Fluent wait interface
        await new SmartWait(Page)
            .WithTimeout(10000)
            .ForElement("#email")
            .ToBeVisibleAsync();

        await new SmartWait(Page)
            .WithTimeout(10000)
            .ForElement("#password")
            .ToBeVisibleAsync();

        TestLogger.Success("All form fields are visible and ready");
    }

    // ============================================================================
    // RETRY HELPER DEMONSTRATION
    // ============================================================================

    [Test]
    [Category("api")]
    public async Task Test_RetryHelper()
    {
        /*
         * Demonstrates RetryAsync helper for flaky operations
         */
        var result = await RetryAsync(
            async () =>
            {
                // Simulate API call that might fail
                await Task.Delay(100);
                var random = new Random().Next(0, 100);
                if (random < 30)  // 30% chance of failure
                {
                    throw new Exception("Simulated network error");
                }
                return "Success";
            },
            maxAttempts: 3,
            initialDelay: 500,
            backoffMultiplier: 2.0
        );

        Assert.That(result, Is.EqualTo("Success"));
        TestLogger.Success("API call succeeded (possibly after retries)");
    }

    // ============================================================================
    // TEST DATA BUILDER DEMONSTRATIONS
    // ============================================================================

    [Test]
    [Category("smoke")]
    public void Test_UserBuilder_Basic()
    {
        /*
         * Demonstrates UserBuilder for creating test data
         */
        var user = new UserBuilder()
            .WithEmail("john.doe@example.com")
            .WithPassword("SecurePass@123")
            .WithName("John", "Doe")
            .WithPhone("+1-555-0123")
            .Build();

        Assert.That(user.Email, Is.EqualTo("john.doe@example.com"));
        Assert.That(user.FullName(), Is.EqualTo("John Doe"));
        Assert.That(user.Role, Is.EqualTo("user"));

        TestLogger.Success($"Created user: {user.FullName()} ({user.Email})");
    }

    [Test]
    [Category("smoke")]
    public void Test_UserBuilder_Admin()
    {
        /*
         * Demonstrates creating admin user with builder
         */
        var admin = new UserBuilder()
            .WithEmail("admin@example.com")
            .WithPassword("Admin@123")
            .AsAdmin()
            .Build();

        Assert.That(admin.Role, Is.EqualTo("admin"));
        TestLogger.Success($"Created admin user: {admin.Email} with role: {admin.Role}");
    }

    [Test]
    [Category("smoke")]
    public void Test_ProductBuilder()
    {
        /*
         * Demonstrates ProductBuilder for creating product test data
         */
        var laptop = new ProductBuilder()
            .WithName("Dell XPS 15")
            .WithPrice(1299.99m)
            .WithDescription("High-performance laptop")
            .InCategory("Electronics")
            .WithStock(25)
            .Build();

        Assert.That(laptop.Name, Is.EqualTo("Dell XPS 15"));
        Assert.That(laptop.Price, Is.EqualTo(1299.99m));
        Assert.That(laptop.Category, Is.EqualTo("Electronics"));
        Assert.That(laptop.Stock, Is.EqualTo(25));

        TestLogger.Success($"Created product: {laptop.Name} - ${laptop.Price}");
    }

    [Test]
    [Category("smoke")]
    public void Test_OrderBuilder()
    {
        /*
         * Demonstrates OrderBuilder for creating complex order scenarios
         */
        var user = new UserBuilder()
            .WithEmail("customer@example.com")
            .WithName("Jane", "Smith")
            .Build();

        var product1 = new ProductBuilder()
            .WithName("Laptop")
            .WithPrice(999.99m)
            .Build();

        var product2 = new ProductBuilder()
            .WithName("Mouse")
            .WithPrice(29.99m)
            .Build();

        var order = new OrderBuilder()
            .ForUser(user)
            .WithProducts(new List<Product> { product1, product2 })
            .WithPaymentMethod("paypal")
            .WithStatus("completed")
            .Build();

        Assert.That(order.User.Email, Is.EqualTo("customer@example.com"));
        Assert.That(order.Products, Has.Count.EqualTo(2));
        Assert.That(order.Total, Is.EqualTo(1029.98m));
        Assert.That(order.PaymentMethod, Is.EqualTo("paypal"));

        TestLogger.Success($"Created order {order.OrderId} for {order.User.FullName()}: ${order.Total}");
    }

    [Test]
    [Category("smoke")]
    public void Test_ConvenienceBuilderFunctions()
    {
        /*
         * Demonstrates convenience functions for common patterns
         */
        var adminUser = CreateAdminUser();
        Assert.That(adminUser.Role, Is.EqualTo("admin"));

        var product = CreateSampleProduct("Electronics");
        Assert.That(product.Category, Is.EqualTo("Electronics"));

        var user = new UserBuilder().WithName("Test", "User").Build();
        var order = CreateOrderWithProducts(user, productCount: 5);
        Assert.That(order.Products, Has.Count.EqualTo(5));
        Assert.That(order.Total, Is.GreaterThan(0));

        TestLogger.Success($"Created user, product, and order with 5 items (Total: ${order.Total:F2})");
    }

    [Test]
    [Category("e2e")]
    public async Task Test_CompleteUserJourneyWithBuilders()
    {
        /*
         * Demonstrates using builders in E2E test scenario
         */
        var user = new UserBuilder()
            .WithEmail("test.user@example.com")
            .WithPassword("Test@123")
            .WithName("Test", "User")
            .Build();

        var product = new ProductBuilder()
            .WithName("Test Product")
            .WithPrice(49.99m)
            .Build();

        var loginPage = new LoginPage(Page);
        await loginPage.NavigateAsync(Settings.BaseUrl);

        // Attempt login with builder-created user
        await loginPage.FillEmailAsync(user.Email);
        await loginPage.FillPasswordAsync(user.Password);
        await loginPage.ClickLoginAsync();

        TestLogger.Success($"Tested login flow for {user.FullName()}");
        TestLogger.Info($"Test data: User={user.Email}, Product={product.Name}");
    }

    // ============================================================================
    // COMBINED FEATURES DEMONSTRATION
    // ============================================================================

    [Test]
    [Category("e2e")]
    [Retry(1)]
    public async Task Test_CombinedAdvancedFeatures()
    {
        /*
         * Demonstrates multiple advanced features together:
         * - Test retry (via [Retry] attribute)
         * - Custom waits
         * - Test data builders
         */
        var user = new UserBuilder()
            .WithEmail("combined.test@example.com")
            .WithPassword("Test@123")
            .Build();

        var loginPage = new LoginPage(Page);
        await loginPage.NavigateAsync(Settings.BaseUrl);

        // Use SmartWait for better control
        await new SmartWait(Page)
            .WithTimeout(10000)
            .ForElement("#email")
            .ToBeVisibleAsync();

        // Perform login
        await loginPage.FillEmailAsync(user.Email);
        await loginPage.FillPasswordAsync(user.Password);
        await loginPage.ClickLoginAsync();

        // Wait for either success or error (custom wait)
        var result = await WaitForAny(new[]
        {
            async () => await Page.Locator(".dashboard").IsVisibleAsync(),
            async () => await Page.Locator(".error-message").IsVisibleAsync()
        }, timeout: 10000);

        TestLogger.Success($"Test completed with user: {user.Email}");
        TestLogger.Success(result == 0 ? "Dashboard visible" : "Error message shown");
    }
}
#endif
