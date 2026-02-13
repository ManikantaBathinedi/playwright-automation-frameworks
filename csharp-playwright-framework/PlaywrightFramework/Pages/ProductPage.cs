using Microsoft.Playwright;

namespace PlaywrightFramework.Pages;

/// <summary>
/// Page Object for Product/Shopping page
/// </summary>
public class ProductPage : BasePage
{
    // Locators
    private readonly ILocator _productCards;
    private readonly ILocator _addToCartButtons;
    private readonly ILocator _cartIcon;
    private readonly ILocator _cartCount;
    private readonly ILocator _filterDropdown;
    private readonly ILocator _sortDropdown;
    private readonly ILocator _searchBox;
    private readonly ILocator _priceLabels;

    public ProductPage(IPage page) : base(page)
    {
        _productCards = page.Locator(".product-card, [data-testid='product']");
        _addToCartButtons = page.Locator("button:has-text('Add to Cart'), [data-testid='add-to-cart']");
        _cartIcon = page.Locator(".cart-icon, [data-testid='cart-icon']");
        _cartCount = page.Locator(".cart-count, [data-testid='cart-count']");
        _filterDropdown = page.Locator("#filter, [data-testid='filter-dropdown']");
        _sortDropdown = page.Locator("#sort, [data-testid='sort-dropdown']");
        _searchBox = page.Locator("input[placeholder*='Search'], [data-testid='product-search']");
        _priceLabels = page.Locator(".product-price, [data-testid='product-price']");
    }

    /// <summary>
    /// Navigate to products page
    /// </summary>
    public async Task GotoAsync(string url)
    {
        await NavigateAsync(url);
        await Page.WaitForLoadStateAsync(LoadState.NetworkIdle);
    }

    /// <summary>
    /// Check if products are displayed
    /// </summary>
    public async Task<bool> AreProductsDisplayedAsync()
    {
        return await _productCards.First.IsVisibleAsync();
    }

    /// <summary>
    /// Get count of displayed products
    /// </summary>
    public async Task<int> GetProductCountAsync()
    {
        return await _productCards.CountAsync();
    }

    /// <summary>
    /// Add first product to cart
    /// </summary>
    public async Task AddFirstProductToCartAsync()
    {
        await _addToCartButtons.First.ClickAsync();
        await WaitAsync(500); // Wait for cart update animation
    }

    /// <summary>
    /// Add product to cart by index (0-based)
    /// </summary>
    public async Task AddProductToCartByIndexAsync(int index)
    {
        await _addToCartButtons.Nth(index).ClickAsync();
        await WaitAsync(500);
    }

    /// <summary>
    /// Add product to cart by name
    /// </summary>
    public async Task AddProductToCartByNameAsync(string productName)
    {
        var product = Page.Locator($"text={productName}").First;
        var addButton = product.Locator("..").Locator("button:has-text('Add to Cart')").First;
        await addButton.ClickAsync();
        await WaitAsync(500);
    }

    /// <summary>
    /// Get cart item count
    /// </summary>
    public async Task<int> GetCartCountAsync()
    {
        try
        {
            var countText = await _cartCount.TextContentAsync();
            return int.Parse(countText ?? "0");
        }
        catch
        {
            return 0;
        }
    }

    /// <summary>
    /// Click cart icon to view cart
    /// </summary>
    public async Task ClickCartAsync()
    {
        await _cartIcon.ClickAsync();
    }

    /// <summary>
    /// Filter products by category
    /// </summary>
    public async Task FilterByCategoryAsync(string category)
    {
        await _filterDropdown.SelectOptionAsync(category);
        await Page.WaitForLoadStateAsync(LoadState.NetworkIdle);
    }

    /// <summary>
    /// Sort products
    /// </summary>
    public async Task SortProductsAsync(string sortOption)
    {
        await _sortDropdown.SelectOptionAsync(sortOption);
        await Page.WaitForLoadStateAsync(LoadState.NetworkIdle);
    }

    /// <summary>
    /// Search for products
    /// </summary>
    public async Task SearchProductsAsync(string searchTerm)
    {
        await _searchBox.FillAsync(searchTerm);
        await _searchBox.PressAsync("Enter");
        await Page.WaitForLoadStateAsync(LoadState.NetworkIdle);
    }

    /// <summary>
    /// Get list of product prices
    /// </summary>
    public async Task<List<decimal>> GetProductPricesAsync()
    {
        var prices = new List<decimal>();
        var count = await _priceLabels.CountAsync();

        for (int i = 0; i < count; i++)
        {
            var priceText = await _priceLabels.Nth(i).TextContentAsync();
            if (priceText != null)
            {
                // Remove currency symbols and parse
                var cleanPrice = priceText.Replace("$", "").Replace(",", "").Trim();
                if (decimal.TryParse(cleanPrice, out var price))
                {
                    prices.Add(price);
                }
            }
        }

        return prices;
    }

    /// <summary>
    /// Get product name by index
    /// </summary>
    public async Task<string> GetProductNameAsync(int index)
    {
        var productCard = _productCards.Nth(index);
        var nameElement = productCard.Locator(".product-name, h3, [data-testid='product-name']").First;
        return await nameElement.TextContentAsync() ?? "";
    }

    /// <summary>
    /// Verify product is in stock
    /// </summary>
    public async Task<bool> IsProductInStockAsync(int index)
    {
        var productCard = _productCards.Nth(index);
        var outOfStockLabel = productCard.Locator("text=/out of stock/i");
        return !await outOfStockLabel.IsVisibleAsync();
    }

    /// <summary>
    /// Add multiple products to cart
    /// </summary>
    public async Task AddMultipleProductsToCartAsync(int count)
    {
        var availableProducts = Math.Min(count, await _addToCartButtons.CountAsync());

        for (int i = 0; i < availableProducts; i++)
        {
            await AddProductToCartByIndexAsync(i);
            await WaitAsync(300); // Small delay between additions
        }
    }
}
