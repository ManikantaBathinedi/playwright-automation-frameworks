using FluentAssertions;
using NUnit.Framework;
using PlaywrightFramework.Pages;
using PlaywrightFramework.Utilities;

namespace PlaywrightFramework.Tests.Auth;

[TestFixture]
[Category("Auth")]
public class LoginTests : BaseTest
{
    private LoginPage _loginPage = null!;
    private HomePage _homePage = null!;

    [SetUp]
    public new async Task SetUp()
    {
        // Base SetUp is called automatically by NUnit
        _loginPage = new LoginPage(Page);
        _homePage = new HomePage(Page);
        await Task.CompletedTask;
    }

    [Test]
    [Category("Smoke")]
    [Description("Verify user can login with valid credentials")]
    public async Task Test_SuccessfulLogin_WithValidCredentials()
    {
        // Arrange
        TestLogger.Step("Navigate to login page");
        await _loginPage.GotoAsync(Settings.BaseUrl);

        // Act
        TestLogger.Step($"Login with email: {Settings.TestUserEmail}");
        await _loginPage.LoginAsync(Settings.TestUserEmail, Settings.TestUserPassword);

        // Assert
        TestLogger.Step("Verify user is logged in");
        var isLoggedIn = await _homePage.IsLoggedInAsync();
        isLoggedIn.Should().BeTrue("User should be logged in after successful login");

        TestLogger.Success("Login successful!");
    }

    [Test]
    [Category("Negative")]
    [Description("Verify error message appears with invalid credentials")]
    public async Task Test_LoginFails_WithInvalidCredentials()
    {
        // Arrange
        await _loginPage.GotoAsync(Settings.BaseUrl);

        // Act
        TestLogger.Step("Attempt login with invalid credentials");
        await _loginPage.LoginAsync("invalid@email.com", "wrongpassword");

        // Assert
        TestLogger.Step("Verify error message is displayed");
        var errorDisplayed = await _loginPage.IsErrorDisplayedAsync();
        errorDisplayed.Should().BeTrue("Error message should be displayed for invalid credentials");

        var errorMessage = await _loginPage.GetErrorMessageAsync();
        errorMessage.Should().NotBeNullOrEmpty("Error message should not be empty");

        TestLogger.Info($"Error message: {errorMessage}");
    }

    [Test]
    [Category("Validation")]
    [Description("Verify login fails with empty email")]
    public async Task Test_LoginFails_WithEmptyEmail()
    {
        // Arrange
        await _loginPage.GotoAsync(Settings.BaseUrl);

        // Act
        await _loginPage.LoginAsync("", "password");

        // Assert
        var errorDisplayed = await _loginPage.IsErrorDisplayedAsync();
        errorDisplayed.Should().BeTrue("Error should be displayed for empty email");
    }

    [Test]
    [Category("Validation")]
    [Description("Verify login fails with empty password")]
    public async Task Test_LoginFails_WithEmptyPassword()
    {
        // Arrange
        await _loginPage.GotoAsync(Settings.BaseUrl);

        // Act
        await _loginPage.LoginAsync(Settings.TestUserEmail, "");

        // Assert
        var errorDisplayed = await _loginPage.IsErrorDisplayedAsync();
        errorDisplayed.Should().BeTrue("Error should be displayed for empty password");
    }

    [Test]
    [Category("Functional")]
    [Description("Verify remember me functionality")]
    public async Task Test_RememberMe_Functionality()
    {
        // Arrange
        await _loginPage.GotoAsync(Settings.BaseUrl);

        // Act
        TestLogger.Step("Login with 'Remember Me' checked");
        await _loginPage.LoginWithRememberMeAsync(Settings.TestUserEmail, Settings.TestUserPassword);

        // Assert
        var isLoggedIn = await _homePage.IsLoggedInAsync();
        isLoggedIn.Should().BeTrue("User should be logged in with remember me");
    }

    [Test]
    [Category("Security")]
    [Description("Verify SQL injection attempts are blocked")]
    [TestCase("' OR '1'='1", TestName = "Test_SQLInjection_IsBlocked_OR_Statement")]
    [TestCase("admin'--", TestName = "Test_SQLInjection_IsBlocked_Admin_Comment")]
    [TestCase("' OR 1=1--", TestName = "Test_SQLInjection_IsBlocked_OR_Tautology")]
    public async Task Test_SQLInjection_IsBlocked(string maliciousInput)
    {
        // Arrange
        await _loginPage.GotoAsync(Settings.BaseUrl);

        // Act
        TestLogger.Step($"Attempt SQL injection: {maliciousInput}");
        await _loginPage.LoginAsync(maliciousInput, maliciousInput);

        // Assert
        var errorDisplayed = await _loginPage.IsErrorDisplayedAsync();
        errorDisplayed.Should().BeTrue("SQL injection should be blocked and show error");
    }

    [Test]
    [Category("Security")]
    [Description("Verify XSS attempts are blocked")]
    [TestCase("<script>alert('XSS')</script>", TestName = "Test_XSS_IsBlocked_Script_Tag")]
    [TestCase("<img src=x onerror=alert('XSS')>", TestName = "Test_XSS_IsBlocked_Image_OnError")]
    public async Task Test_XSS_IsBlocked(string maliciousInput)
    {
        // Arrange
        await _loginPage.GotoAsync(Settings.BaseUrl);

        // Act
        TestLogger.Step($"Attempt XSS: {maliciousInput}");
        await _loginPage.LoginAsync(maliciousInput, "password");

        // Assert
        var errorDisplayed = await _loginPage.IsErrorDisplayedAsync();
        errorDisplayed.Should().BeTrue("XSS should be blocked and show error");
    }
}
