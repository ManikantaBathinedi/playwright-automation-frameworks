"""
Pages package - Contains all Page Object Models
"""

from .base_page import BasePage
from .login_page import LoginPage
from .home_page import HomePage
from .product_page import ProductPage

__all__ = [
    'BasePage',
    'LoginPage',
    'HomePage',
    'ProductPage'
]
