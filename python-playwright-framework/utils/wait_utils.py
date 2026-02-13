"""
Custom Wait and Retry Utilities
Provides advanced waiting mechanisms beyond Playwright's built-in waits
"""

import time
from typing import Callable, Any, Optional
from functools import wraps


def wait_for_condition(
    condition: Callable[[], bool],
    timeout: int = 30,
    poll_interval: float = 0.5,
    error_message: str = "Condition not met within timeout"
) -> bool:
    """
    Wait for a condition to become true
    
    Args:
        condition: Function that returns True when condition is met
        timeout: Maximum time to wait in seconds
        poll_interval: Time between checks in seconds
        error_message: Error message if timeout occurs
        
    Returns:
        True if condition met
        
    Raises:
        TimeoutError: If condition not met within timeout
        
    Example:
        wait_for_condition(
            lambda: page.locator(".popup").is_visible(),
            timeout=10,
            error_message="Popup did not appear"
        )
    """
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        try:
            if condition():
                return True
        except Exception:
            pass  # Ignore exceptions during polling
        
        time.sleep(poll_interval)
    
    raise TimeoutError(f"{error_message} (timeout: {timeout}s)")


def retry_on_exception(
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: tuple = (Exception,)
):
    """
    Decorator to retry function on exception with exponential backoff
    
    Args:
        max_attempts: Maximum number of attempts
        delay: Initial delay between retries in seconds
        backoff: Multiplier for delay (exponential backoff)
        exceptions: Tuple of exceptions to catch
        
    Example:
        @retry_on_exception(max_attempts=3, delay=1, backoff=2)
        def flaky_operation():
            # Your code here
            pass
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 1
            current_delay = delay
            
            while attempt <= max_attempts:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_attempts:
                        raise
                    
                    print(f"⚠️  Attempt {attempt} failed: {str(e)}")
                    print(f"⏳ Retrying in {current_delay}s...")
                    time.sleep(current_delay)
                    current_delay *= backoff
                    attempt += 1
            
        return wrapper
    return decorator


def wait_until_stable(
    get_value: Callable[[], Any],
    timeout: int = 10,
    stability_time: float = 2.0,
    poll_interval: float = 0.5
) -> Any:
    """
    Wait until a value stops changing (becomes stable)
    Useful for waiting for counters, animations, or async updates to complete
    
    Args:
        get_value: Function that returns the value to monitor
        timeout: Maximum time to wait in seconds
        stability_time: How long value must remain unchanged (seconds)
        poll_interval: Time between checks in seconds
        
    Returns:
        The stable value
        
    Example:
        # Wait for cart count to stabilize
        cart_count = wait_until_stable(
            lambda: page.locator(".cart-count").text_content(),
            timeout=10,
            stability_time=1.0
        )
    """
    start_time = time.time()
    last_value = get_value()
    stable_since = time.time()
    
    while time.time() - start_time < timeout:
        time.sleep(poll_interval)
        current_value = get_value()
        
        if current_value == last_value:
            # Value hasn't changed
            if time.time() - stable_since >= stability_time:
                return current_value
        else:
            # Value changed, reset stability timer
            last_value = current_value
            stable_since = time.time()
    
    raise TimeoutError(f"Value did not stabilize within {timeout}s")


def wait_for_any(
    conditions: list[Callable[[], bool]],
    timeout: int = 30,
    poll_interval: float = 0.5
) -> int:
    """
    Wait for any one of multiple conditions to become true
    
    Args:
        conditions: List of functions that return True when condition is met
        timeout: Maximum time to wait in seconds
        poll_interval: Time between checks in seconds
        
    Returns:
        Index of the condition that became true
        
    Example:
        # Wait for either success or error message
        result = wait_for_any([
            lambda: page.locator(".success").is_visible(),
            lambda: page.locator(".error").is_visible()
        ], timeout=10)
        
        if result == 0:
            print("Success!")
        else:
            print("Error occurred")
    """
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        for index, condition in enumerate(conditions):
            try:
                if condition():
                    return index
            except Exception:
                pass
        
        time.sleep(poll_interval)
    
    raise TimeoutError("None of the conditions were met within timeout")


def wait_for_all(
    conditions: list[Callable[[], bool]],
    timeout: int = 30,
    poll_interval: float = 0.5
) -> bool:
    """
    Wait for all conditions to become true
    
    Args:
        conditions: List of functions that return True when condition is met
        timeout: Maximum time to wait in seconds
        poll_interval: Time between checks in seconds
        
    Returns:
        True if all conditions met
        
    Example:
        # Wait for multiple elements to be visible
        wait_for_all([
            lambda: page.locator(".header").is_visible(),
            lambda: page.locator(".content").is_visible(),
            lambda: page.locator(".footer").is_visible()
        ], timeout=10)
    """
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        all_met = True
        
        for condition in conditions:
            try:
                if not condition():
                    all_met = False
                    break
            except Exception:
                all_met = False
                break
        
        if all_met:
            return True
        
        time.sleep(poll_interval)
    
    raise TimeoutError("Not all conditions were met within timeout")


class SmartWait:
    """
    Smart wait utility with fluent interface
    
    Example:
        SmartWait(page).for_element(".button").to_be_visible().and_enabled()
    """
    
    def __init__(self, page):
        self.page = page
        self.locator = None
        self.timeout = 30
    
    def with_timeout(self, timeout: int):
        """Set custom timeout"""
        self.timeout = timeout
        return self
    
    def for_element(self, selector: str):
        """Select element to wait for"""
        self.locator = self.page.locator(selector)
        return self
    
    def to_be_visible(self):
        """Wait for element to be visible"""
        if self.locator:
            self.locator.wait_for(state="visible", timeout=self.timeout * 1000)
        return self
    
    def to_be_hidden(self):
        """Wait for element to be hidden"""
        if self.locator:
            self.locator.wait_for(state="hidden", timeout=self.timeout * 1000)
        return self
    
    def and_enabled(self):
        """Wait for element to be enabled"""
        if self.locator:
            wait_for_condition(
                lambda: self.locator.is_enabled(),
                timeout=self.timeout,
                error_message="Element not enabled"
            )
        return self
    
    def and_contains_text(self, text: str):
        """Wait for element to contain text"""
        if self.locator:
            wait_for_condition(
                lambda: text in (self.locator.text_content() or ""),
                timeout=self.timeout,
                error_message=f"Element does not contain text: {text}"
            )
        return self
