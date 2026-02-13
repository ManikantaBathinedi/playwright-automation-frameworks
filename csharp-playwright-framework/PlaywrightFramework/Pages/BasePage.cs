using Microsoft.Playwright;

namespace PlaywrightFramework.Pages;

/// <summary>
/// Base page class with common methods for all page objects
/// Follows Page Object Model (POM) design pattern
/// </summary>
public class BasePage
{
    protected readonly IPage Page;

    public BasePage(IPage page)
    {
        Page = page;
    }

    // Navigation Methods
    public async Task NavigateAsync(string url)
    {
        await Page.GotoAsync(url, new PageGotoOptions { WaitUntil = WaitUntilState.DOMContentLoaded });
    }

    public async Task WaitForPageLoadAsync()
    {
        await Page.WaitForLoadStateAsync(LoadState.NetworkIdle);
    }

    public string GetCurrentUrl() => Page.Url;

    public async Task<string> GetTitleAsync() => await Page.TitleAsync();

    public async Task GoBackAsync() => await Page.GoBackAsync();

    public async Task GoForwardAsync() => await Page.GoForwardAsync();

    public async Task ReloadAsync() => await Page.ReloadAsync();

    // Element Interaction Methods
    public async Task ClickAsync(ILocator locator)
    {
        await locator.ClickAsync();
    }

    public async Task DoubleClickAsync(ILocator locator)
    {
        await locator.DblClickAsync();
    }

    public async Task RightClickAsync(ILocator locator)
    {
        await locator.ClickAsync(new LocatorClickOptions { Button = MouseButton.Right });
    }

    public async Task FillAsync(ILocator locator, string text)
    {
        await locator.FillAsync(text);
    }

    public async Task TypeAsync(ILocator locator, string text, int delay = 100)
    {
        await locator.TypeAsync(text, new LocatorTypeOptions { Delay = delay });
    }

    public async Task ClearAsync(ILocator locator)
    {
        await locator.ClearAsync();
    }

    public async Task CheckAsync(ILocator locator)
    {
        await locator.CheckAsync();
    }

    public async Task UncheckAsync(ILocator locator)
    {
        await locator.UncheckAsync();
    }

    public async Task SelectOptionAsync(ILocator locator, string value)
    {
        await locator.SelectOptionAsync(value);
    }

    public async Task HoverAsync(ILocator locator)
    {
        await locator.HoverAsync();
    }

    // Element Query Methods
    public async Task<string?> GetTextAsync(ILocator locator)
    {
        return await locator.TextContentAsync();
    }

    public async Task<string> GetInnerTextAsync(ILocator locator)
    {
        return await locator.InnerTextAsync();
    }

    public async Task<string?> GetAttributeAsync(ILocator locator, string attribute)
    {
        return await locator.GetAttributeAsync(attribute);
    }

    public async Task<bool> IsVisibleAsync(ILocator locator)
    {
        return await locator.IsVisibleAsync();
    }

    public async Task<bool> IsEnabledAsync(ILocator locator)
    {
        return await locator.IsEnabledAsync();
    }

    public async Task<bool> IsCheckedAsync(ILocator locator)
    {
        return await locator.IsCheckedAsync();
    }

    public async Task<int> GetCountAsync(ILocator locator)
    {
        return await locator.CountAsync();
    }

    // Wait Methods
    public async Task WaitForElementAsync(ILocator locator, int timeout = 5000)
    {
        await locator.WaitForAsync(new LocatorWaitForOptions
        {
            State = WaitForSelectorState.Visible,
            Timeout = timeout
        });
    }

    public async Task WaitForElementHiddenAsync(ILocator locator, int timeout = 5000)
    {
        await locator.WaitForAsync(new LocatorWaitForOptions
        {
            State = WaitForSelectorState.Hidden,
            Timeout = timeout
        });
    }

    public async Task WaitForUrlAsync(string urlPart, int timeout = 5000)
    {
        await Page.WaitForURLAsync($"**/*{urlPart}*", new PageWaitForURLOptions { Timeout = timeout });
    }

    // Screenshot Methods
    public async Task TakeScreenshotAsync(string name)
    {
        await Page.ScreenshotAsync(new PageScreenshotOptions
        {
            Path = $"screenshots/{name}.png",
            FullPage = true
        });
    }

    public async Task TakeElementScreenshotAsync(ILocator locator, string name)
    {
        await locator.ScreenshotAsync(new LocatorScreenshotOptions
        {
            Path = $"screenshots/{name}.png"
        });
    }

    // Scroll Methods
    public async Task ScrollToElementAsync(ILocator locator)
    {
        await locator.ScrollIntoViewIfNeededAsync();
    }

    public async Task ScrollToTopAsync()
    {
        await Page.EvaluateAsync("window.scrollTo(0, 0)");
    }

    public async Task ScrollToBottomAsync()
    {
        await Page.EvaluateAsync("window.scrollTo(0, document.body.scrollHeight)");
    }

    // Keyboard Methods
    public async Task PressKeyAsync(string key)
    {
        await Page.Keyboard.PressAsync(key);
    }

    // File Upload
    public async Task UploadFileAsync(ILocator locator, string filePath)
    {
        await locator.SetInputFilesAsync(filePath);
    }

    // JavaScript Execution
    public async Task<T> ExecuteScriptAsync<T>(string script)
    {
        return await Page.EvaluateAsync<T>(script);
    }

    // Wait for specific time (use sparingly!)
    public async Task WaitAsync(int milliseconds)
    {
        await Page.WaitForTimeoutAsync(milliseconds);
    }
}
