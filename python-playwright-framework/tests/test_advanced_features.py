"""
Advanced Features Demo Tests
Demonstrates: Test Retry, Custom Waits, Test Data Builders
"""

import pytest
from pages.login_page import LoginPage
from pages.home_page import HomePage
from utils.wait_utils import (
    wait_for_condition,
    retry_on_exception,
    wait_until_stable,
    wait_for_any,
    wait_for_all,
    SmartWait
)
from utils.test_data_builder import (
    UserBuilder,
    ProductBuilder,
    OrderBuilder,
    create_admin_user,
    create_sample_product,
    create_order_with_products
)


# ============================================================================
# TEST RETRY DEMONSTRATIONS
# ============================================================================

@pytest.mark.smoke
@pytest.mark.flaky(reruns=2, reruns_delay=1)  # Will retry up to 2 times if it fails
def test_flaky_operation_with_retry(page, base_url):
    """
    Demonstrates test retry on failures
    This test will automatically retry up to 2 times if it fails
    """
    login_page = LoginPage(page)
    login_page.navigate(base_url)
    
    # Simulate potentially flaky operation
    # In real scenarios, this could be:
    # - Network timeouts
    # - Element not ready
    # - Race conditions
    login_page.fill_email("test@example.com")
    login_page.fill_password("Test@123")
    login_page.click_login()
    
    # Assertion that might fail due to timing
    assert login_page.is_error_message_visible(), "Error message should be visible"


# ============================================================================
# CUSTOM WAIT UTILITIES DEMONSTRATIONS
# ============================================================================

@pytest.mark.smoke
def test_wait_for_condition(page, base_url):
    """
    Demonstrates custom wait_for_condition utility
    Waits for a specific condition to be true
    """
    login_page = LoginPage(page)
    login_page.navigate(base_url)
    
    # Wait for login form to be fully loaded and interactive
    wait_for_condition(
        condition=lambda: page.locator("#email").is_visible() and 
                         page.locator("#password").is_visible() and
                         page.locator("button[type='submit']").is_enabled(),
        timeout=10,
        error_message="Login form did not fully load"
    )
    
    print("✅ Login form is fully loaded and ready")


@pytest.mark.smoke
def test_wait_until_stable(page, base_url):
    """
    Demonstrates wait_until_stable utility
    Useful for waiting for counters, animations, or async updates
    """
    login_page = LoginPage(page)
    home_page = HomePage(page)
    
    login_page.navigate(base_url)
    login_page.login("standard_user", "Test@123")
    
    # Wait for cart count to stabilize (useful for async updates)
    if page.locator(".cart-count").is_visible():
        cart_count = wait_until_stable(
            get_value=lambda: page.locator(".cart-count").text_content(),
            timeout=5,
            stability_time=1.0
        )
        print(f"✅ Cart count stabilized at: {cart_count}")


@pytest.mark.smoke
def test_wait_for_multiple_conditions(page, base_url):
    """
    Demonstrates waiting for multiple conditions (ANY or ALL)
    """
    login_page = LoginPage(page)
    login_page.navigate(base_url)
    login_page.fill_email("invalid@example.com")
    login_page.fill_password("wrongpassword")
    login_page.click_login()
    
    # Wait for EITHER success message OR error message (whichever appears first)
    result = wait_for_any([
        lambda: page.locator(".success-message").is_visible(),
        lambda: page.locator(".error-message").is_visible(),
        lambda: page.locator(".alert-danger").is_visible()
    ], timeout=10)
    
    if result == 0:
        print("✅ Success message appeared")
    elif result == 1:
        print("✅ Error message appeared")
    else:
        print("✅ Alert danger appeared")


@pytest.mark.smoke
def test_smart_wait_fluent_interface(page, base_url):
    """
    Demonstrates SmartWait with fluent interface
    Clean, readable waiting syntax
    """
    login_page = LoginPage(page)
    login_page.navigate(base_url)
    
    # Fluent wait interface
    SmartWait(page)        .with_timeout(10)        .for_element("#email")        .to_be_visible()        .and_enabled()
    
    SmartWait(page)        .with_timeout(10)        .for_element("#password")        .to_be_visible()        .and_enabled()
    
    print("✅ All form fields are visible and enabled")


# ============================================================================
# RETRY DECORATOR DEMONSTRATION
# ============================================================================

@retry_on_exception(max_attempts=3, delay=1.0, backoff=2.0)
def flaky_api_call():
    """
    Example function that might fail but will auto-retry
    """
    import random
    if random.random() < 0.5:  # 50% chance of failure
        raise ConnectionError("Network timeout")
    return "Success"


@pytest.mark.api
def test_retry_decorator():
    """
    Demonstrates retry decorator for functions
    """
    result = flaky_api_call()
    assert result == "Success"
    print("✅ API call succeeded (possibly after retries)")


# ============================================================================
# TEST DATA BUILDER DEMONSTRATIONS
# ============================================================================

@pytest.mark.smoke
def test_user_builder_basic():
    """
    Demonstrates UserBuilder for creating test data
    """
    # Build user with fluent interface
    user = UserBuilder()        .with_email("john.doe@example.com")        .with_password("SecurePass@123")        .with_name("John", "Doe")        .with_phone("+1-555-0123")        .build()
    
    assert user.email == "john.doe@example.com"
    assert user.full_name() == "John Doe"
    assert user.role == "user"
    print(f"✅ Created user: {user.full_name()} ({user.email})")


@pytest.mark.smoke
def test_user_builder_admin():
    """
    Demonstrates creating admin user with builder
    """
    admin = UserBuilder()        .with_email("admin@example.com")        .with_password("Admin@123")        .as_admin()        .build()
    
    assert admin.role == "admin"
    print(f"✅ Created admin user: {admin.email} with role: {admin.role}")


@pytest.mark.smoke
def test_product_builder():
    """
    Demonstrates ProductBuilder for creating product test data
    """
    laptop = ProductBuilder()        .with_name("Dell XPS 15")        .with_price(1299.99)        .with_description("High-performance laptop")        .in_category("Electronics")        .with_stock(25)        .build()
    
    assert laptop.name == "Dell XPS 15"
    assert laptop.price == 1299.99
    assert laptop.category == "Electronics"
    assert laptop.stock == 25
    print(f"✅ Created product: {laptop.name} - ${laptop.price}")


@pytest.mark.smoke
def test_order_builder():
    """
    Demonstrates OrderBuilder for creating complex order scenarios
    """
    # Create user, products, and order
    user = UserBuilder()        .with_email("customer@example.com")        .with_name("Jane", "Smith")        .build()
    
    product1 = ProductBuilder()        .with_name("Laptop")        .with_price(999.99)        .build()
    
    product2 = ProductBuilder()        .with_name("Mouse")        .with_price(29.99)        .build()
    
    order = OrderBuilder()        .for_user(user)        .with_products([product1, product2])        .with_payment_method("paypal")        .with_status("completed")        .build()
    
    assert order.user.email == "customer@example.com"
    assert len(order.products) == 2
    assert order.total == 1029.98  # Sum of product prices
    assert order.payment_method == "paypal"
    print(f"✅ Created order {order.order_id} for {order.user.full_name()}: ${order.total}")


@pytest.mark.smoke
def test_convenience_builder_functions():
    """
    Demonstrates convenience functions for common patterns
    """
    # Quick user creation
    standard_user = create_admin_user()
    assert standard_user.role == "admin"
    
    # Quick product creation
    product = create_sample_product("Electronics")
    assert product.category == "Electronics"
    
    # Create order with multiple products
    user = UserBuilder().with_name("Test", "User").build()
    order = create_order_with_products(user, product_count=5)
    assert len(order.products) == 5
    assert order.total > 0
    
    print(f"✅ Created user, product, and order with 5 items (Total: ${order.total:.2f})")


@pytest.mark.e2e
def test_complete_user_journey_with_builders(page, base_url):
    """
    Demonstrates using builders in E2E test scenario
    """
    # Build test data
    user = UserBuilder()        .with_email("test.user@example.com")        .with_password("Test@123")        .with_name("Test", "User")        .build()
    
    product = ProductBuilder()        .with_name("Test Product")        .with_price(49.99)        .build()
    
    # Use in test
    login_page = LoginPage(page)
    login_page.navigate(base_url)
    
    # Attempt login with builder-created user
    login_page.fill_email(user.email)
    login_page.fill_password(user.password)
    login_page.click_login()
    
    print(f"✅ Tested login flow for {user.full_name()}")
    print(f"✅ Test data: User={user.email}, Product={product.name}")


# ============================================================================
# COMBINED FEATURES DEMONSTRATION
# ============================================================================

@pytest.mark.e2e
@pytest.mark.flaky(reruns=1)
def test_combined_advanced_features(page, base_url):
    """
    Demonstrates multiple advanced features together:
    - Test retry (via @flaky decorator)
    - Custom waits
    - Test data builders
    """
    # Create test data with builder
    user = UserBuilder()        .with_email("combined.test@example.com")        .with_password("Test@123")        .build()
    
    login_page = LoginPage(page)
    login_page.navigate(base_url)
    
    # Use SmartWait for better control
    SmartWait(page)        .with_timeout(10)        .for_element("#email")        .to_be_visible()        .and_enabled()
    
    # Perform login
    login_page.fill_email(user.email)
    login_page.fill_password(user.password)
    login_page.click_login()
    
    # Wait for either success or error (custom wait)
    result = wait_for_any([
        lambda: page.locator(".dashboard").is_visible(),
        lambda: page.locator(".error-message").is_visible()
    ], timeout=10)
    
    print(f"✅ Test completed with user: {user.email}")
    print(f"✅ Result: {'Dashboard visible' if result == 0 else 'Error message shown'}")
