"""
Home Page Object Model
Contains all elements and actions for the home/dashboard page
"""

from playwright.sync_api import Page, Locator
from pages.base_page import BasePage


class HomePage(BasePage):
    """Home page object model"""
    
    # Page URL
    HOME_URL = "/"
    
    def __init__(self, page: Page):
        super().__init__(page)
        
        # Initialize locators
        self._welcome_message = page.locator('.welcome-message, h1:has-text("Welcome"), .greeting')
        self._logout_button = page.locator('button:has-text("Logout"), button:has-text("Sign out"), a:has-text("Logout")')
        self._user_profile = page.locator('.user-profile, .profile-icon, [data-test="user-profile"]')
        self._user_menu = page.locator('.user-menu, .dropdown-menu, [role="menu"]')
        self._search_box = page.locator('input[type="search"], input[placeholder*="Search"], input[name="search"]')
        self._search_button = page.locator('button[type="submit"]:has-text("Search"), button:has([aria-label="Search"])')
        self._navigation_menu = page.locator('nav, .navigation, .navbar')
        self._notification_bell = page.locator('.notification-icon, [aria-label="Notifications"]')
        self._settings_icon = page.locator('.settings-icon, [aria-label="Settings"]')
        self._page_title = page.locator('h1, .page-title')
    
    def goto(self) -> None:
        """Navigate to home page"""
        self.navigate(self.HOME_URL)
        self.wait_for_page_load()
    
    def get_welcome_message(self) -> str:
        """Get welcome message text"""
        return self.get_text(self._welcome_message)
    
    def is_welcome_message_displayed(self) -> bool:
        """Check if welcome message is displayed"""
        return self.is_visible(self._welcome_message)
    
    def logout(self) -> None:
        """Logout from the application"""
        self.click(self._logout_button)
    
    def open_user_menu(self) -> None:
        """Open user menu"""
        self.click(self._user_profile)
        self.wait_for_element(self._user_menu, 2000)
    
    def is_logged_in(self) -> bool:
        """Check if user is logged in"""
        return self.is_visible(self._user_profile)
    
    def search(self, query: str) -> None:
        """Search for a query"""
        self.fill(self._search_box, query)
        self.press_key('Enter')
    
    def search_with_button(self, query: str) -> None:
        """Search using search button"""
        self.fill(self._search_box, query)
        self.click(self._search_button)
    
    def click_navigation_item(self, menu_item: str) -> None:
        """Click on navigation menu item"""
        menu_locator = self.page.locator(f'a:has-text("{menu_item}"), button:has-text("{menu_item}")')
        self.click(menu_locator)
    
    def is_navigation_displayed(self) -> bool:
        """Check if navigation menu is displayed"""
        return self.is_visible(self._navigation_menu)
    
    def click_notifications(self) -> None:
        """Click notifications bell"""
        self.click(self._notification_bell)
    
    def open_settings(self) -> None:
        """Open settings"""
        self.click(self._settings_icon)
    
    def get_page_title(self) -> str:
        """Get page title"""
        return self.get_text(self._page_title)
    
    def is_home_page_loaded(self) -> bool:
        """Verify home page is loaded"""
        return self.is_visible(self._navigation_menu)
