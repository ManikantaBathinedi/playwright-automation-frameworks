"""
Login Page Object Model
Contains all elements and actions for the login page
"""

from playwright.sync_api import Page, Locator
from pages.base_page import BasePage


class LoginPage(BasePage):
    """Login page object model"""
    
    # Page URL
    LOGIN_URL = "/login"
    
    def __init__(self, page: Page):
        super().__init__(page)
        
        # Initialize locators
        self._email_input = page.locator('input[name="email"], input[type="email"], input#email')
        self._password_input = page.locator('input[name="password"], input[type="password"], input#password')
        self._login_button = page.locator('button:has-text("Login"), button[type="submit"]:has-text("Sign in"), button#login-button')
        self._signup_link = page.locator('a:has-text("Sign up"), a:has-text("Register"), a:has-text("Create account")')
        self._forgot_password_link = page.locator('a:has-text("Forgot"), a:has-text("Reset password")')
        self._error_message = page.locator('.error-message, .alert-danger, [role="alert"]')
        self._success_message = page.locator('.success-message, .alert-success')
        self._remember_me_checkbox = page.locator('input[type="checkbox"][name="remember"], input#remember-me')
        self._show_password_button = page.locator('button:has-text("Show"), [aria-label="Show password"]')
        self._login_form = page.locator('form')
    
    def goto(self) -> None:
        """Navigate to login page"""
        self.navigate(self.LOGIN_URL)
        self.wait_for_page_load()
    
    def enter_email(self, email: str) -> None:
        """Enter email address"""
        self.fill(self._email_input, email)
    
    def enter_password(self, password: str) -> None:
        """Enter password"""
        self.fill(self._password_input, password)
    
    def click_login(self) -> None:
        """Click login button"""
        self.click(self._login_button)
    
    def login(self, email: str, password: str) -> None:
        """Complete login flow"""
        self.enter_email(email)
        self.enter_password(password)
        self.click_login()
    
    def login_with_remember_me(self, email: str, password: str) -> None:
        """Login with remember me option"""
        self.enter_email(email)
        self.enter_password(password)
        self.click(self._remember_me_checkbox)
        self.click_login()
    
    def get_error_message(self) -> str:
        """Get error message text"""
        self.wait_for_element(self._error_message, 3000)
        return self.get_text(self._error_message)
    
    def is_error_displayed(self) -> bool:
        """Check if error message is displayed"""
        try:
            self.wait_for_element(self._error_message, 3000)
            return self.is_visible(self._error_message)
        except:
            return False
    
    def get_success_message(self) -> str:
        """Get success message text"""
        self.wait_for_element(self._success_message, 3000)
        return self.get_text(self._success_message)
    
    def is_success_displayed(self) -> bool:
        """Check if success message is displayed"""
        try:
            self.wait_for_element(self._success_message, 3000)
            return self.is_visible(self._success_message)
        except:
            return False
    
    def click_forgot_password(self) -> None:
        """Click forgot password link"""
        self.click(self._forgot_password_link)
    
    def click_signup(self) -> None:
        """Click signup/register link"""
        self.click(self._signup_link)
    
    def is_login_button_enabled(self) -> bool:
        """Check if login button is enabled"""
        return self.is_enabled(self._login_button)
    
    def is_login_form_displayed(self) -> bool:
        """Check if login form is displayed"""
        return self.is_visible(self._login_form)
    
    def toggle_password_visibility(self) -> None:
        """Toggle show/hide password"""
        self.click(self._show_password_button)
    
    def clear_form(self) -> None:
        """Clear login form"""
        self.clear(self._email_input)
        self.clear(self._password_input)
    
    def get_email_value(self) -> str:
        """Get email input value"""
        return self.get_attribute(self._email_input, 'value') or ''
    
    def is_remember_me_checked(self) -> bool:
        """Check if remember me is checked"""
        return self.is_checked(self._remember_me_checkbox)
