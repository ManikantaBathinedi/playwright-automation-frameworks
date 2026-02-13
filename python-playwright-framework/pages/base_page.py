"""
Base Page class containing common methods for all page objects
Follows Page Object Model (POM) design pattern
"""

from playwright.sync_api import Page, Locator, expect
from typing import Optional


class BasePage:
    """Base page with common methods for all page objects"""
    
    def __init__(self, page: Page):
        self.page = page
    
    def navigate(self, url: str) -> None:
        """Navigate to a specific URL"""
        self.page.goto(url, wait_until="domcontentloaded")
    
    def wait_for_page_load(self) -> None:
        """Wait for page to be fully loaded"""
        self.page.wait_for_load_state("networkidle")
    
    def click(self, locator: Locator) -> None:
        """Click on an element"""
        locator.click()
    
    def double_click(self, locator: Locator) -> None:
        """Double click on an element"""
        locator.dblclick()
    
    def right_click(self, locator: Locator) -> None:
        """Right click on an element"""
        locator.click(button="right")
    
    def fill(self, locator: Locator, text: str) -> None:
        """Fill text into an input field"""
        locator.fill(text)
    
    def type(self, locator: Locator, text: str, delay: int = 100) -> None:
        """Type text with a delay (simulates human typing)"""
        locator.type(text, delay=delay)
    
    def clear(self, locator: Locator) -> None:
        """Clear an input field"""
        locator.clear()
    
    def get_text(self, locator: Locator) -> str:
        """Get text content from an element"""
        return locator.text_content() or ""
    
    def get_inner_text(self, locator: Locator) -> str:
        """Get inner text from an element"""
        return locator.inner_text()
    
    def get_attribute(self, locator: Locator, attribute: str) -> Optional[str]:
        """Get attribute value from an element"""
        return locator.get_attribute(attribute)
    
    def is_visible(self, locator: Locator) -> bool:
        """Check if element is visible"""
        return locator.is_visible()
    
    def is_enabled(self, locator: Locator) -> bool:
        """Check if element is enabled"""
        return locator.is_enabled()
    
    def is_checked(self, locator: Locator) -> bool:
        """Check if element is checked (for checkboxes/radio buttons)"""
        return locator.is_checked()
    
    def wait_for_element(self, locator: Locator, timeout: int = 5000) -> None:
        """Wait for element to be visible"""
        locator.wait_for(state="visible", timeout=timeout)
    
    def wait_for_element_hidden(self, locator: Locator, timeout: int = 5000) -> None:
        """Wait for element to be hidden"""
        locator.wait_for(state="hidden", timeout=timeout)
    
    def select_by_value(self, locator: Locator, value: str) -> None:
        """Select option from dropdown by value"""
        locator.select_option(value=value)
    
    def select_by_label(self, locator: Locator, label: str) -> None:
        """Select option from dropdown by label"""
        locator.select_option(label=label)
    
    def get_count(self, locator: Locator) -> int:
        """Get count of elements"""
        return locator.count()
    
    def hover(self, locator: Locator) -> None:
        """Hover over an element"""
        locator.hover()
    
    def take_screenshot(self, name: str) -> None:
        """Take screenshot of the page"""
        self.page.screenshot(path=f"reports/screenshots/{name}.png", full_page=True)
    
    def take_element_screenshot(self, locator: Locator, name: str) -> None:
        """Take screenshot of a specific element"""
        locator.screenshot(path=f"reports/screenshots/{name}.png")
    
    def get_current_url(self) -> str:
        """Get current page URL"""
        return self.page.url
    
    def get_title(self) -> str:
        """Get page title"""
        return self.page.title()
    
    def go_back(self) -> None:
        """Go back to previous page"""
        self.page.go_back()
    
    def go_forward(self) -> None:
        """Go forward to next page"""
        self.page.go_forward()
    
    def reload(self) -> None:
        """Reload/refresh the page"""
        self.page.reload()
    
    def wait(self, milliseconds: int) -> None:
        """Wait for specific time (use sparingly!)"""
        self.page.wait_for_timeout(milliseconds)
    
    def execute_script(self, script: str) -> any:
        """Execute JavaScript in the page context"""
        return self.page.evaluate(script)
    
    def scroll_to_element(self, locator: Locator) -> None:
        """Scroll to element"""
        locator.scroll_into_view_if_needed()
    
    def scroll_to_top(self) -> None:
        """Scroll to top of page"""
        self.page.evaluate("window.scrollTo(0, 0)")
    
    def scroll_to_bottom(self) -> None:
        """Scroll to bottom of page"""
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    
    def press_key(self, key: str) -> None:
        """Press a keyboard key"""
        self.page.keyboard.press(key)
    
    def upload_file(self, locator: Locator, file_path: str) -> None:
        """Upload file to input element"""
        locator.set_input_files(file_path)
    
    def get_all_text(self, locator: Locator) -> list[str]:
        """Get all text from multiple elements"""
        return locator.all_text_contents()
    
    def exists(self, locator: Locator) -> bool:
        """Check if element exists in DOM (regardless of visibility)"""
        return locator.count() > 0
    
    def wait_for_url(self, url_part: str, timeout: int = 5000) -> None:
        """Wait for URL to contain specific text"""
        self.page.wait_for_url(f"**/*{url_part}*", timeout=timeout)
    
    def close_page(self) -> None:
        """Close current page/tab"""
        self.page.close()
