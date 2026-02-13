using FluentAssertions;
using PlaywrightFramework.Pages;
using PlaywrightFramework.Utilities;

namespace PlaywrightFramework.Tests.E2E;

[TestFixture]
[Category("E2E")]
[Category("Regression")]
public class CheckoutTests : BaseTest
{
    private LoginPage _loginPage = null!;
    private HomePage _homePage = null!;
    private ProductPage _productPage = null!;

    [SetUp]
    public new async Task SetUp()
    {
        await base.SetUp();
        _loginPage = new LoginPage(Page);
        _homePage = new HomePage(Page);
        _productPage = new ProductPage(Page);
    }

    [Test]
    [Category("Critical")]
    [Description("Test complete shopping flow from login to cart")]
    public async Task Test_CompleteShoppingFlow_FromLoginToCart()
    {
        // Arrange
        TestLogger.Step("Step 1: Navigate to login page");
        await _loginPage.GotoAsync(Settings.BaseUrl + "/login");

        // Act & Assert - Step 1: Login
        TestLogger.Step($"Step 2: Login with credentials: {Settings.TestUserEmail}");
        await _loginPage.LoginAsync(Settings.TestUserEmail, Settings.TestUserPassword);

        await Page.WaitForLoadStateAsync(Microsoft.Playwright.LoadState.NetworkIdle);

        // Verify login successful
        var isLoggedIn = await _homePage.IsLoggedInAsync();
        isLoggedIn.Should().BeTrue("User should be logged in");
        TestLogger.Success("Login successful");

        // Step 2: Navigate to products
        TestLogger.Step("Step 3: Navigate to products page");
        await _productPage.GotoAsync(Settings.BaseUrl + "/products");

        // Step 3: Verify products are displayed
        TestLogger.Step("Step 4: Verify products are displayed");
        var productsDisplayed = await _productPage.AreProductsDisplayedAsync();
        productsDisplayed.Should().BeTrue("Products should be visible on page");

        var productCount = await _productPage.GetProductCountAsync();
        productCount.Should().BeGreaterThan(0, "Should have at least one product");
        TestLogger.Info($"Found {productCount} products");

        // Step 4: Add product to cart
        TestLogger.Step("Step 5: Add first product to cart");
        var initialCartCount = await _productPage.GetCartCountAsync();
        TestLogger.Info($"Initial cart count: {initialCartCount}");

        await _productPage.AddFirstProductToCartAsync();

        // Step 5: Verify cart count increased
        TestLogger.Step("Step 6: Verify cart count increased");
        var newCartCount = await _productPage.GetCartCountAsync();
        TestLogger.Info($"New cart count: {newCartCount}");

        newCartCount.Should().BeGreaterThan(initialCartCount, "Cart count should increase after adding product");

        TestLogger.Success("Complete shopping flow test passed!");
    }

    [Test]
    [Description("Test searching for products and adding to cart")]
    public async Task Test_SearchAndAddToCart()
    {
        // Arrange
        await _loginPage.GotoAsync(Settings.BaseUrl + "/login");
        await _loginPage.LoginAsync(Settings.TestUserEmail, Settings.TestUserPassword);
        await _productPage.GotoAsync(Settings.BaseUrl + "/products");

        // Act
        TestLogger.Step("Search for products");
        await _productPage.SearchProductsAsync("laptop");

        var productsDisplayed = await _productPage.AreProductsDisplayedAsync();
        productsDisplayed.Should().BeTrue("Search results should be displayed");

        TestLogger.Step("Add searched product to cart");
        await _productPage.AddFirstProductToCartAsync();

        // Assert
        var cartCount = await _productPage.GetCartCountAsync();
        cartCount.Should().BeGreaterThan(0, "Cart should contain items");

        TestLogger.Success("Search and add to cart successful");
    }

    [Test]
    [Description("Test filtering and sorting products")]
    public async Task Test_FilterAndSortProducts()
    {
        // Arrange
        await _loginPage.GotoAsync(Settings.BaseUrl + "/login");
        await _loginPage.LoginAsync(Settings.TestUserEmail, Settings.TestUserPassword);
        await _productPage.GotoAsync(Settings.BaseUrl + "/products");

        // Act - Filter
        TestLogger.Step("Filter products by category");
        await _productPage.FilterByCategoryAsync("Electronics");

        var filteredProducts = await _productPage.GetProductCountAsync();
        filteredProducts.Should().BeGreaterThan(0, "Filtered products should be displayed");
        TestLogger.Info($"Filtered products count: {filteredProducts}");

        // Act - Sort
        TestLogger.Step("Sort products by price");
        await _productPage.SortProductsAsync("price-low-to-high");

        // Assert - Verify sorting
        var prices = await _productPage.GetProductPricesAsync();
        if (prices.Count > 1)
        {
            for (int i = 0; i < prices.Count - 1; i++)
            {
                prices[i].Should().BeLessOrEqualTo(prices[i + 1], "Prices should be sorted in ascending order");
            }
            TestLogger.Success("Products are sorted correctly");
        }
    }

    [Test]
    [Description("Test adding multiple products to cart")]
    public async Task Test_AddMultipleProductsToCart()
    {
        // Arrange
        await _loginPage.GotoAsync(Settings.BaseUrl + "/login");
        await _loginPage.LoginAsync(Settings.TestUserEmail, Settings.TestUserPassword);
        await _productPage.GotoAsync(Settings.BaseUrl + "/products");

        // Act
        TestLogger.Step("Add 3 products to cart");
        var initialCartCount = await _productPage.GetCartCountAsync();

        await _productPage.AddMultipleProductsToCartAsync(3);

        // Assert
        var finalCartCount = await _productPage.GetCartCountAsync();
        TestLogger.Info($"Initial: {initialCartCount}, Final: {finalCartCount}");

        finalCartCount.Should().Be(initialCartCount + 3, "Should have 3 more items in cart");

        TestLogger.Success("Successfully added multiple products to cart");
    }

    [Test]
    [Category("Guest")]
    [Description("Test browsing products as guest user without login")]
    public async Task Test_BrowseProducts_AsGuest()
    {
        // Arrange & Act
        TestLogger.Step("Navigate to products page as guest");
        await _productPage.GotoAsync(Settings.BaseUrl + "/products");

        // Assert
        TestLogger.Step("Verify products are visible to guest users");
        var productsDisplayed = await _productPage.AreProductsDisplayedAsync();
        productsDisplayed.Should().BeTrue("Guest users should be able to view products");

        var productCount = await _productPage.GetProductCountAsync();
        productCount.Should().BeGreaterThan(0, "Products should be available for guests");

        TestLogger.Info($"Guest can view {productCount} products");
        TestLogger.Success("Guest browsing test passed");
    }

    [Test]
    [Description("Test product stock availability")]
    public async Task Test_VerifyProductStockStatus()
    {
        // Arrange
        await _productPage.GotoAsync(Settings.BaseUrl + "/products");

        // Act
        TestLogger.Step("Check product stock status");
        var productCount = await _productPage.GetProductCountAsync();

        int inStockCount = 0;
        for (int i = 0; i < Math.Min(5, productCount); i++)
        {
            var inStock = await _productPage.IsProductInStockAsync(i);
            if (inStock)
            {
                inStockCount++;
                var productName = await _productPage.GetProductNameAsync(i);
                TestLogger.Info($"Product '{productName}' is in stock");
            }
        }

        // Assert
        inStockCount.Should().BeGreaterThan(0, "At least some products should be in stock");

        TestLogger.Success($"Found {inStockCount} products in stock");
    }
}
