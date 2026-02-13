"""
Login Test Suite
Tests login functionality with various scenarios
"""

import os
import pytest
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.home_page import HomePage


@pytest.mark.smoke
class TestLogin:
    """Login test cases"""
    
    def test_login_successful_with_valid_credentials(self, page: Page, base_url, test_user_email, test_user_password):
        """Test successful login with valid credentials"""
        # Arrange
        login_page = LoginPage(page)
        home_page = HomePage(page)
        
        # Act
        page.goto(f"{base_url}/login")
        login_page.login(test_user_email, test_user_password)
        page.wait_for_load_state("networkidle")
        
        # Assert
        expect(page).to_have_url(re.compile(r'dashboard|home|products'))
        assert home_page.is_logged_in(), "User should be logged in"
    
    @pytest.mark.negative
    def test_login_with_invalid_email(self, page: Page, base_url):
        """Test login failure with invalid email"""
        # Arrange
        login_page = LoginPage(page)
        invalid_email = "invalid@example.com"
        password = "anypassword"
        
        # Act
        page.goto(f"{base_url}/login")
        login_page.login(invalid_email, password)
        
        # Assert
        assert login_page.is_error_displayed(), "Error message should be displayed"
        error_message = login_page.get_error_message()
        assert 'invalid' in error_message.lower(), "Error message should contain 'invalid'"
    
    @pytest.mark.negative
    def test_login_with_invalid_password(self, page: Page, base_url, test_user_email):
        """Test login failure with invalid password"""
        # Arrange
        login_page = LoginPage(page)
        invalid_password = "WrongPassword123!"
        
        # Act
        page.goto(f"{base_url}/login")
        login_page.login(test_user_email, invalid_password)
        
        # Assert
        assert login_page.is_error_displayed(), "Error message should be displayed"
    
    @pytest.mark.validation
    def test_login_with_empty_email(self, page: Page, base_url):
        """Test login validation with empty email"""
        # Arrange
        login_page = LoginPage(page)
        password = "Test@123"
        
        # Act
        page.goto(f"{base_url}/login")
        login_page.enter_email("")
        login_page.enter_password(password)
        login_page.click_login()
        
        # Assert
        assert login_page.is_error_displayed(), "Error message should be displayed"
    
    @pytest.mark.validation
    def test_login_with_empty_password(self, page: Page, base_url, test_user_email):
        """Test login validation with empty password"""
        # Arrange
        login_page = LoginPage(page)
        
        # Act
        page.goto(f"{base_url}/login")
        login_page.enter_email(test_user_email)
        login_page.enter_password("")
        login_page.click_login()
        
        # Assert
        assert login_page.is_error_displayed(), "Error message should be displayed"
    
    @pytest.mark.validation
    def test_login_with_empty_credentials(self, page: Page, base_url):
        """Test login validation with both fields empty"""
        # Arrange
        login_page = LoginPage(page)
        
        # Act
        page.goto(f"{base_url}/login")
        login_page.click_login()
        
        # Assert
        assert login_page.is_error_displayed(), "Error message should be displayed"
    
    @pytest.mark.functional
    def test_login_with_remember_me(self, page: Page, base_url, test_user_email, test_user_password):
        """Test login with remember me option"""
        # Arrange
        login_page = LoginPage(page)
        
        # Act
        page.goto(f"{base_url}/login")
        login_page.login_with_remember_me(test_user_email, test_user_password)
        page.wait_for_load_state("networkidle")
        
        # Assert
        expect(page).to_have_url(re.compile(r'dashboard|home|products'))
    
    @pytest.mark.functional
    def test_forgot_password_navigation(self, page: Page, base_url):
        """Test forgot password link navigation"""
        # Arrange
        login_page = LoginPage(page)
        
        # Act
        page.goto(f"{base_url}/login")
        login_page.click_forgot_password()
        
        # Assert
        expect(page).to_have_url(re.compile(r'forgot-password|reset-password'))
    
    @pytest.mark.functional
    def test_signup_navigation(self, page: Page, base_url):
        """Test signup/register link navigation"""
        # Arrange
        login_page = LoginPage(page)
        
        # Act
        page.goto(f"{base_url}/login")
        login_page.click_signup()
        
        # Assert
        expect(page).to_have_url(re.compile(r'signup|register|create-account'))
    
    @pytest.mark.ui
    def test_login_button_enabled_with_valid_input(self, page: Page, base_url):
        """Test login button state validation"""
        # Arrange
        login_page = LoginPage(page)
        
        # Act
        page.goto(f"{base_url}/login")
        login_page.enter_email("test@example.com")
        login_page.enter_password("Test@123")
        
        # Assert
        assert login_page.is_login_button_enabled(), "Login button should be enabled"
    
    @pytest.mark.functional
    def test_clear_login_form(self, page: Page, base_url):
        """Test clearing login form"""
        # Arrange
        login_page = LoginPage(page)
        
        # Act
        page.goto(f"{base_url}/login")
        login_page.enter_email("test@example.com")
        login_page.enter_password("password")
        login_page.clear_form()
        
        # Assert
        email_value = login_page.get_email_value()
        assert email_value == "", "Email field should be empty"


@pytest.mark.security
class TestLoginSecurity:
    """Login security test cases"""
    
    def test_prevent_sql_injection(self, page: Page, base_url):
        """Test SQL injection prevention"""
        # Arrange
        login_page = LoginPage(page)
        sql_injection = "' OR '1'='1"
        
        # Act
        page.goto(f"{base_url}/login")
        login_page.login(sql_injection, sql_injection)
        
        # Assert
        assert login_page.is_error_displayed(), "Should show error for SQL injection attempt"
    
    def test_prevent_xss_script_injection(self, page: Page, base_url):
        """Test XSS script injection prevention"""
        # Arrange
        login_page = LoginPage(page)
        xss_script = '<script>alert("XSS")</script>'
        
        # Act
        page.goto(f"{base_url}/login")
        login_page.login(xss_script, "password")
        
        # Assert
        assert login_page.is_error_displayed(), "Should show error for XSS attempt"


# Import re for regex
import re
