"""
Product Page Object Model
Contains all elements and actions for product/catalog pages
"""

from playwright.sync_api import Page, Locator
from pages.base_page import BasePage


class ProductPage(BasePage):
    """Product page object model"""
    
    # Page URL
    PRODUCTS_URL = "/products"
    
    def __init__(self, page: Page):
        super().__init__(page)
        
        # Initialize locators
        self._product_list = page.locator('.products-list, .product-grid, [data-test="products"]')
        self._product_cards = page.locator('.product-card, .product-item, [data-test="product"]')
        self._add_to_cart_button = page.locator('button:has-text("Add to Cart"), [data-test="add-to-cart"]')
        self._cart_icon = page.locator('.cart-icon, [data-test="shopping-cart"], a:has-text("Cart")')
        self._cart_count = page.locator('.cart-count, .cart-badge, [data-test="cart-count"]')
        self._product_title = page.locator('.product-title, .product-name, h2')
        self._product_price = page.locator('.product-price, .price, [data-test="price"]')
        self._product_image = page.locator('.product-image, img[alt*="product"]')
        self._filter_dropdown = page.locator('select[name="filter"], [data-test="filter"]')
        self._sort_dropdown = page.locator('select[name="sort"], [data-test="sort"]')
        self._search_input = page.locator('input[placeholder*="Search products"]')
    
    def goto(self) -> None:
        """Navigate to products page"""
        self.navigate(self.PRODUCTS_URL)
        self.wait_for_page_load()
    
    def get_product_count(self) -> int:
        """Get total number of products"""
        return self.get_count(self._product_cards)
    
    def click_product(self, product_name: str) -> None:
        """Click on a specific product by name"""
        product = self.page.locator(f'.product-card:has-text("{product_name}")')
        self.click(product)
    
    def add_product_to_cart(self, product_name: str) -> None:
        """Add product to cart by name"""
        add_to_cart_btn = self.page.locator(
            f'.product-card:has-text("{product_name}") button:has-text("Add to Cart")'
        )
        self.click(add_to_cart_btn)
    
    def get_cart_count(self) -> int:
        """Get cart item count"""
        try:
            count_text = self.get_text(self._cart_count)
            return int(count_text) if count_text else 0
        except:
            return 0
    
    def open_cart(self) -> None:
        """Open shopping cart"""
        self.click(self._cart_icon)
    
    def get_all_product_titles(self) -> list[str]:
        """Get all product titles"""
        return self.get_all_text(self._product_title)
    
    def get_all_product_prices(self) -> list[str]:
        """Get all product prices"""
        return self.get_all_text(self._product_price)
    
    def filter_by_category(self, category: str) -> None:
        """Filter products by category"""
        self.select_by_label(self._filter_dropdown, category)
        self.wait_for_page_load()
    
    def sort_products(self, sort_option: str) -> None:
        """Sort products"""
        self.select_by_label(self._sort_dropdown, sort_option)
        self.wait_for_page_load()
    
    def search_products(self, query: str) -> None:
        """Search for products"""
        self.fill(self._search_input, query)
        self.press_key('Enter')
        self.wait_for_page_load()
    
    def are_products_displayed(self) -> bool:
        """Check if products are displayed"""
        return self.is_visible(self._product_list)
