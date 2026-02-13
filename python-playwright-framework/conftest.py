"""
Pytest configuration and fixtures for Playwright tests
This file contains shared fixtures and hooks for all tests
"""

import os
import pytest
from pathlib import Path
from playwright.sync_api import Browser, BrowserContext, Page
from dotenv import load_dotenv

# ============================================
# ENVIRONMENT CONFIGURATION
# ============================================
# Get environment from TEST_ENV variable (default: dev)
env = os.getenv("TEST_ENV", "dev").lower()
env_file = f".env.{env}"

# Load the environment file
if os.path.exists(env_file):
    load_dotenv(env_file, override=True)
    print(f"\n{'='*60}")
    print(f"✅ Environment: {env.upper()}")
    print(f"📄 Config file: {env_file}")
    print(f"📍 BASE_URL: {os.getenv('BASE_URL', 'Not set')}")
    print(f"🖥️  HEADLESS: {os.getenv('HEADLESS', 'Not set')}")
    print(f"👥 WORKERS: {os.getenv('WORKERS', 'Not set')}")
    print(f"{'='*60}\n")
else:
    print(f"\n{'='*60}")
    print(f"⚠️  Environment file not found: {env_file}")
    print(f"📄 Using default: .env.example")
    print(f"💡 Set TEST_ENV variable: dev, qa, staging, prod")
    print(f"{'='*60}\n")
    load_dotenv(".env.example")

# Get project root directory
PROJECT_ROOT = Path(__file__).parent


# ============================================
# PYTEST CONFIGURATION HOOKS
# ============================================
def pytest_addoption(parser):
    """Add custom command line options"""
    parser.addoption(
        "--workers",
        action="store",
        default=None,
        help="Number of parallel workers (default: from WORKERS env var or 'auto')"
    )
    parser.addoption(
        "--browser",
        action="store",
        default=None,
        help="Browser to use: chrome, firefox, or webkit (default: from BROWSER env var or 'chrome')"
    )


def pytest_configure(config):
    """
    Configure pytest with dynamic worker count and browser type
    Reads from: 1) CLI argument, 2) Environment variables, 3) defaults
    """
    # ===== Configure Workers =====
    # Check if -n is already specified in command line
    if hasattr(config.option, 'numprocesses') and config.option.numprocesses:
        # User explicitly set -n on command line, don't override
        workers = config.option.numprocesses
        print(f"👥 Using command-line workers: {workers}")
    else:
        # Get workers from CLI --workers option first
        cli_workers = config.getoption("--workers")
        
        if cli_workers:
            workers = cli_workers
            source = "CLI argument"
        else:
            # Get from WORKERS environment variable
            workers = os.getenv("WORKERS", "auto")
            source = "environment variable" if os.getenv("WORKERS") else "default (auto)"
        
        # Set the numprocesses for pytest-xdist
        try:
            if workers == "auto":
                config.option.numprocesses = "auto"
            else:
                config.option.numprocesses = int(workers)
            
            print(f"👥 Parallel execution: {workers} workers (from {source})")
        except ValueError:
            print(f"⚠️  Invalid WORKERS value: {workers}, defaulting to 'auto'")
            config.option.numprocesses = "auto"
    
    # ===== Configure Browser Type =====
    cli_browser = config.getoption("--browser")
    if cli_browser:
        browser_name = cli_browser
        browser_source = "CLI argument"
    else:
        browser_name = os.getenv("BROWSER", "chrome")
        browser_source = "environment variable" if os.getenv("BROWSER") else "default"
    
    # Validate browser name and map 'chrome' to 'chromium'
    browser_name = browser_name.lower()
    if browser_name == "chrome":
        browser_name = "chromium"
        print(f"💡 Mapping 'chrome' to 'chromium' (Playwright's Chrome engine)")
    
    valid_browsers = ["chromium", "firefox", "webkit"]
    if browser_name not in valid_browsers:
        print(f"⚠️  Invalid browser: {browser_name}, using 'chromium'")
        browser_name = "chromium"
    
    print(f"🌐 Browser configured: {browser_name} (from {browser_source})")


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """
    Configure browser context settings
    """
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 720},
        "ignore_https_errors": True,
        "record_video_dir": "reports/videos/",
        "record_video_size": {"width": 1280, "height": 720}
    }


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    """
    Configure browser launch settings
    """
    return {
        **browser_type_launch_args,
        "headless": os.getenv("HEADLESS", "true").lower() == "true",
        "slow_mo": 0,  # Add delay between actions (ms) for debugging
    }


@pytest.fixture
def base_url():
    """
    Base URL for the application
    """
    return os.getenv("BASE_URL", "https://demo.playwright.dev/todomvc")


@pytest.fixture
def api_base_url():
    """
    Base URL for API testing
    """
    return os.getenv("API_BASE_URL", "https://jsonplaceholder.typicode.com")


@pytest.fixture
def test_user_email():
    """
    Test user email
    """
    return os.getenv("TEST_USER_EMAIL", "test@example.com")


@pytest.fixture
def test_user_password():
    """
    Test user password
    """
    return os.getenv("TEST_USER_PASSWORD", "Test@123")


@pytest.fixture
def authenticated_context(context: BrowserContext, base_url, test_user_email, test_user_password):
    """
    Fixture that provides an authenticated browser context
    Use this when tests need a logged-in user
    """
    from pages.login_page import LoginPage
    
    page = context.new_page()
    login_page = LoginPage(page)
    
    # Perform login
    page.goto(f"{base_url}/login")
    login_page.login(test_user_email, test_user_password)
    page.wait_for_load_state("networkidle")
    
    yield context
    
    # Cleanup
    page.close()


@pytest.fixture
def screenshots_dir():
    """
    Directory for screenshots
    """
    screenshots_path = PROJECT_ROOT / "reports" / "screenshots"
    screenshots_path.mkdir(parents=True, exist_ok=True)
    return screenshots_path


@pytest.fixture
def logs_dir():
    """
    Directory for logs
    """
    logs_path = PROJECT_ROOT / "reports" / "logs"
    logs_path.mkdir(parents=True, exist_ok=True)
    return logs_path


def pytest_configure(config):
    """
    Pytest configuration hook - runs before test collection
    """
    # Create reports directory
    reports_dir = PROJECT_ROOT / "reports"
    reports_dir.mkdir(exist_ok=True)
    
    (reports_dir / "screenshots").mkdir(exist_ok=True)
    (reports_dir / "videos").mkdir(exist_ok=True)
    (reports_dir / "logs").mkdir(exist_ok=True)
    (reports_dir / "html-report").mkdir(exist_ok=True)


def pytest_runtest_makereport(item, call):
    """
    Hook to capture test failure and take screenshot
    """
    if call.when == "call":
        if call.excinfo is not None:
            # Test failed - try to capture screenshot
            try:
                page = item.funcargs.get("page")
                if page:
                    screenshot_path = PROJECT_ROOT / "reports" / "screenshots" / f"{item.name}_failure.png"
                    page.screenshot(path=str(screenshot_path))
            except Exception as e:
                print(f"Could not capture screenshot: {e}")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_protocol(item, nextitem):
    """
    Hook to log test start/end
    """
    print(f"\n{'='*80}")
    print(f"Starting test: {item.nodeid}")
    print(f"{'='*80}\n")
    
    yield
    
    print(f"\n{'='*80}")
    print(f"Finished test: {item.nodeid}")
    print(f"{'='*80}\n")


# Pytest-playwright configuration
@pytest.fixture(scope="session")
def playwright_browser_args():
    """
    Arguments passed to browser.new_context()
    """
    return {
        "args": [
            "--start-maximized",
            "--disable-blink-features=AutomationControlled"
        ]
    }
