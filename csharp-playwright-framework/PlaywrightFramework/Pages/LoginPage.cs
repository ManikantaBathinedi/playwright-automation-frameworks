using Microsoft.Playwright;

namespace PlaywrightFramework.Pages;

/// <summary>
/// Login Page Object Model
/// </summary>
public class LoginPage : BasePage
{
    // Locators
    private readonly ILocator _emailInput;
    private readonly ILocator _passwordInput;
    private readonly ILocator _loginButton;
    private readonly ILocator _errorMessage;
    private readonly ILocator _rememberMeCheckbox;
    private readonly ILocator _forgotPasswordLink;

    public LoginPage(IPage page) : base(page)
    {
        // Updated for saucedemo.com compatibility
        _emailInput = page.Locator("#user-name, #email, input[type='email'], input[name='email'], input[name='user-name']");
        _passwordInput = page.Locator("#password, input[type='password'], input[name='password']");
        _loginButton = page.Locator("#login-button, button[type='submit'], button:has-text('Login'), button:has-text('Sign in')");
        _errorMessage = page.Locator("[data-test='error'], .error-message, .alert-danger, [role='alert']");
        _rememberMeCheckbox = page.Locator("#remember-me, input[type='checkbox'][name='remember']");
        _forgotPasswordLink = page.Locator("a:has-text('Forgot'), a[href*='forgot']");
    }

    // Actions
    public async Task GotoAsync(string baseUrl)
    {
        // saucedemo.com login is on homepage, not /login
        await NavigateAsync(baseUrl);
        await WaitForPageLoadAsync();
    }

    public async Task LoginAsync(string email, string password)
    {
        await FillAsync(_emailInput, email);
        await FillAsync(_passwordInput, password);
        await ClickAsync(_loginButton);
    }

    public async Task LoginWithRememberMeAsync(string email, string password)
    {
        await FillAsync(_emailInput, email);
        await FillAsync(_passwordInput, password);
        await CheckAsync(_rememberMeCheckbox);
        await ClickAsync(_loginButton);
    }

    public async Task ClickForgotPasswordAsync()
    {
        await ClickAsync(_forgotPasswordLink);
    }

    // Assertions/Queries
    public async Task<string?> GetErrorMessageAsync()
    {
        return await GetTextAsync(_errorMessage);
    }

    public async Task<bool> IsErrorDisplayedAsync()
    {
        return await IsVisibleAsync(_errorMessage);
    }

    public async Task<bool> IsLoginButtonEnabledAsync()
    {
        return await IsEnabledAsync(_loginButton);
    }
}
