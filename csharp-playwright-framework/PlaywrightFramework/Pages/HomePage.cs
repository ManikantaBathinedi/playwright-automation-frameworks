using Microsoft.Playwright;

namespace PlaywrightFramework.Pages;

/// <summary>
/// Home Page Object Model
/// </summary>
public class HomePage : BasePage
{
    // Locators
    private readonly ILocator _welcomeMessage;
    private readonly ILocator _logoutButton;
    private readonly ILocator _userProfile;
    private readonly ILocator _userMenu;
    private readonly ILocator _searchBox;
    private readonly ILocator _searchButton;

    public HomePage(IPage page) : base(page)
    {
        // Updated for saucedemo.com - looks for inventory page elements after login
        _welcomeMessage = page.Locator(".title, .app_logo, h1:has-text('Welcome'), .greeting");
        _logoutButton = page.Locator("#logout_sidebar_link, button:has-text('Logout'), button:has-text('Sign out'), a:has-text('Logout')");
        _userProfile = page.Locator("#react-burger-menu-btn").Or(page.Locator(".user-profile, .profile-icon, [data-test='user-profile']"));
        _userMenu = page.Locator(".bm-menu, .user-menu, .dropdown-menu, [role='menu']");
        _searchBox = page.Locator("input[type='search'], input[placeholder*='Search']");
        _searchButton = page.Locator("button[type='submit']:has-text('Search')");
    }

    // Actions
    public async Task GotoAsync()
    {
        await NavigateAsync("/");
        await WaitForPageLoadAsync();
    }

    public async Task LogoutAsync()
    {
        await ClickAsync(_logoutButton);
    }

    public async Task OpenUserMenuAsync()
    {
        await ClickAsync(_userProfile);
    }

    public async Task SearchAsync(string query)
    {
        await FillAsync(_searchBox, query);
        await ClickAsync(_searchButton);
    }

    // Queries
    public async Task<string?> GetWelcomeMessageAsync()
    {
        return await GetTextAsync(_welcomeMessage);
    }

    public async Task<bool> IsWelcomeMessageDisplayedAsync()
    {
        return await IsVisibleAsync(_welcomeMessage);
    }

    public async Task<bool> IsLoggedInAsync()
    {
        return await IsVisibleAsync(_userProfile);
    }
}
