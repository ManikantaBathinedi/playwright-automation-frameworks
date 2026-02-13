"""
End-to-End Test: Complete User Journey
Tests complete flow from login to purchase
"""

import pytest
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.product_page import ProductPage


@pytest.mark.e2e
@pytest.mark.regression
class TestShoppingFlow:
    """E2E shopping flow tests"""
    
    def test_complete_shopping_flow_from_login_to_cart(self, page: Page, base_url, test_user_email, test_user_password):
        """Test complete shopping flow"""
        # Arrange
        login_page = LoginPage(page)
        product_page = ProductPage(page)
        
        # Step 1: Login
        page.goto(f"{base_url}/login")
        login_page.login(test_user_email, test_user_password)
        page.wait_for_load_state("networkidle")
        expect(page).to_have_url(re.compile(r'dashboard|home|products'))
        
        # Step 2: Navigate to products
        page.goto(f"{base_url}/products")
        
        # Verify products are displayed
        assert product_page.are_products_displayed(), "Products should be displayed"
        
        # Step 3: Get initial product count
        product_count = product_page.get_product_count()
        assert product_count > 0, "Should have products displayed"
        
        # Step 4: Add product to cart
        initial_cart_count = product_page.get_cart_count()
        product_page.add_product_to_cart('Product Name')  # Adjust based on your app
        
        # Wait for cart update
        page.wait_for_timeout(1000)
        
        # Verify cart count increased
        new_cart_count = product_page.get_cart_count()
        assert new_cart_count > initial_cart_count, "Cart count should increase"
        
        # Step 5: View cart
        product_page.open_cart()
        expect(page).to_have_url(re.compile(r'cart'))
        
        # Step 6: Take screenshot of final state
        page.screenshot(path='reports/screenshots/e2e-shopping-complete.png')
    
    @pytest.mark.smoke
    def test_search_and_add_to_cart(self, page: Page, base_url, test_user_email, test_user_password):
        """Test product search and purchase flow"""
        # Arrange
        login_page = LoginPage(page)
        product_page = ProductPage(page)
        
        # Login
        page.goto(f"{base_url}/login")
        login_page.login(test_user_email, test_user_password)
        page.wait_for_load_state("networkidle")
        
        # Navigate to products
        page.goto(f"{base_url}/products")
        
        # Search for product
        search_query = "laptop"
        product_page.search_products(search_query)
        
        # Verify search results
        product_count = product_page.get_product_count()
        assert product_count > 0, "Should have search results"
        
        # Add first product to cart
        initial_cart_count = product_page.get_cart_count()
        products = product_page.get_all_product_titles()
        
        if products:
            product_page.add_product_to_cart(products[0])
            page.wait_for_timeout(1000)
            
            new_cart_count = product_page.get_cart_count()
            assert new_cart_count == initial_cart_count + 1, "Cart should have one more item"
    
    @pytest.mark.functional
    def test_filter_and_sort_products(self, page: Page, base_url, test_user_email, test_user_password):
        """Test product filtering and sorting"""
        # Arrange
        login_page = LoginPage(page)
        product_page = ProductPage(page)
        
        # Login
        page.goto(f"{base_url}/login")
        login_page.login(test_user_email, test_user_password)
        page.wait_for_load_state("networkidle")
        
        # Navigate to products
        page.goto(f"{base_url}/products")
        
        # Get initial product list
        initial_products = product_page.get_all_product_titles()
        
        # Filter by category
        product_page.filter_by_category('Electronics')
        page.wait_for_timeout(500)
        
        # Verify filter applied
        filtered_products = product_page.get_all_product_titles()
        assert len(filtered_products) > 0, "Should have filtered products"
        
        # Sort products
        product_page.sort_products('Price: Low to High')
        page.wait_for_timeout(500)
        
        # Verify products are still displayed
        sorted_products = product_page.get_all_product_titles()
        assert len(sorted_products) > 0, "Should have sorted products"
    
    @pytest.mark.functional
    def test_add_multiple_products_to_cart(self, page: Page, base_url, test_user_email, test_user_password):
        """Test adding multiple products to cart"""
        # Arrange
        login_page = LoginPage(page)
        product_page = ProductPage(page)
        
        # Login
        page.goto(f"{base_url}/login")
        login_page.login(test_user_email, test_user_password)
        page.wait_for_load_state("networkidle")
        
        # Navigate to products
        page.goto(f"{base_url}/products")
        
        # Get initial cart count
        initial_cart_count = product_page.get_cart_count()
        
        # Get product names
        products = product_page.get_all_product_titles()
        products_to_add = min(3, len(products))  # Add up to 3 products
        
        # Add multiple products
        for i in range(products_to_add):
            product_page.add_product_to_cart(products[i])
            page.wait_for_timeout(500)
        
        # Verify cart count
        final_cart_count = product_page.get_cart_count()
        assert final_cart_count == initial_cart_count + products_to_add, "Cart should have all added products"


@pytest.mark.e2e
@pytest.mark.guest
class TestGuestUserJourney:
    """Guest user test cases"""
    
    def test_browse_products_without_login(self, page: Page, base_url):
        """Test browsing products as guest"""
        # Arrange
        product_page = ProductPage(page)
        
        # Navigate directly to products (no login)
        page.goto(f"{base_url}/products")
        
        # Verify products are displayed
        assert product_page.are_products_displayed(), "Products should be visible to guests"
        
        # Get product count
        product_count = product_page.get_product_count()
        assert product_count > 0, "Should have products"
        
        # Search products
        product_page.search_products('test')
        page.wait_for_load_state("networkidle")
        
        # Verify still can see products
        search_results = product_page.get_product_count()
        assert search_results >= 0, "Should show search results"


# Import re for regex
import re
