"""
Test Data Builders using Builder Pattern
Provides fluent interface for creating complex test objects
"""

from typing import Optional
from dataclasses import dataclass, field
from utils.data_generator import DataGenerator


@dataclass
class User:
    """User data class"""
    email: str
    password: str
    first_name: str = ""
    last_name: str = ""
    phone: str = ""
    address: str = ""
    city: str = ""
    zip_code: str = ""
    country: str = ""
    role: str = "user"
    is_active: bool = True
    
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()


@dataclass
class Product:
    """Product data class"""
    name: str
    price: float
    description: str = ""
    category: str = ""
    sku: str = ""
    stock: int = 100
    is_available:bool = True
    image_url: str = ""


@dataclass
class Order:
    """Order data class"""
    user: User
    products: list[Product] = field(default_factory=list)
    order_id: str = ""
    status: str = "pending"
    total: float = 0.0
    shipping_address: str = ""
    payment_method: str = "credit_card"
    
    def calculate_total(self) -> float:
        return sum(p.price for p in self.products)


class UserBuilder:
    """
    Builder for creating User test data with fluent interface
    
    Example:
        user = UserBuilder()\\
            .with_email("test@example.com")\\
            .with_password("Test@123")\\
            .with_name("John", "Doe")\\
            .with_role("admin")\\
            .build()
    """
    
    def __init__(self):
        self._email = DataGenerator.random_email()
        self._password = DataGenerator.random_password()
        self._first_name = DataGenerator.random_first_name()
        self._last_name = DataGenerator.random_last_name()
        self._phone = DataGenerator.random_phone()
        self._address = DataGenerator.random_address()
        self._city = DataGenerator.random_string(10)
        self._zip_code = DataGenerator.random_string(5, "0123456789")
        self._country = "USA"
        self._role = "user"
        self._is_active = True
    
    def with_email(self, email: str):
        """Set email"""
        self._email = email
        return self
    
    def with_password(self, password: str):
        """Set password"""
        self._password = password
        return self
    
    def with_name(self, first_name: str, last_name: str):
        """Set first and last name"""
        self._first_name = first_name
        self._last_name = last_name
        return self
    
    def with_phone(self, phone: str):
        """Set phone number"""
        self._phone = phone
        return self
    
    def with_address(self, address: str, city: str = "", zip_code: str = "", country: str = "USA"):
        """Set address details"""
        self._address = address
        if city:
            self._city = city
        if zip_code:
            self._zip_code = zip_code
        self._country = country
        return self
    
    def with_role(self, role: str):
        """Set user role (user, admin, guest)"""
        self._role = role
        return self
    
    def as_admin(self):
        """Make user an admin"""
        self._role = "admin"
        return self
    
    def as_guest(self):
        """Make user a guest"""
        self._role = "guest"
        return self
    
    def active(self, is_active: bool = True):
        """Set active status"""
        self._is_active = is_active
        return self
    
    def build(self) -> User:
        """Build the User object"""
        return User(
            email=self._email,
            password=self._password,
            first_name=self._first_name,
            last_name=self._last_name,
            phone=self._phone,
            address=self._address,
            city=self._city,
            zip_code=self._zip_code,
            country=self._country,
            role=self._role,
            is_active=self._is_active
        )


class ProductBuilder:
    """
    Builder for creating Product test data
    
    Example:
        product = ProductBuilder()\\
            .with_name("Laptop")\\
            .with_price(999.99)\\
            .in_category("Electronics")\\
            .with_stock(50)\\
            .build()
    """
    
    def __init__(self):
        self._name = f"Product-{DataGenerator.random_string(8)}"
        self._price = DataGenerator.random_number(10, 1000)
        self._description = DataGenerator.random_string(50)
        self._category = "General"
        self._sku = DataGenerator.random_string(10, "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
        self._stock = 100
        self._is_available = True
        self._image_url = "https://via.placeholder.com/300"
    
    def with_name(self, name: str):
        """Set product name"""
        self._name = name
        return self
    
    def with_price(self, price: float):
        """Set product price"""
        self._price = price
        return self
    
    def with_description(self, description: str):
        """Set product description"""
        self._description = description
        return self
    
    def in_category(self, category: str):
        """Set product category"""
        self._category = category
        return self
    
    def with_sku(self, sku: str):
        """Set product SKU"""
        self._sku = sku
        return self
    
    def with_stock(self, stock: int):
        """Set stock quantity"""
        self._stock = stock
        return self
    
    def out_of_stock(self):
        """Make product out of stock"""
        self._stock = 0
        self._is_available = False
        return self
    
    def with_image(self, image_url: str):
        """Set product image URL"""
        self._image_url = image_url
        return self
    
    def build(self) -> Product:
        """Build the Product object"""
        return Product(
            name=self._name,
            price=self._price,
            description=self._description,
            category=self._category,
            sku=self._sku,
            stock=self._stock,
            is_available=self._is_available,
            image_url=self._image_url
        )


class OrderBuilder:
    """
    Builder for creating Order test data
    
    Example:
        order = OrderBuilder()\\
            .for_user(user)\\
            .with_products([product1, product2])\\
            .with_shipping_address("123 Main St")\\
            .with_payment_method("paypal")\\
            .build()
    """
    
    def __init__(self):
        self._user = UserBuilder().build()
        self._products = []
        self._order_id = f"ORD-{DataGenerator.random_string(8, '0123456789')}"
        self._status = "pending"
        self._shipping_address = ""
        self._payment_method = "credit_card"
    
    def for_user(self, user: User):
        """Set the user for this order"""
        self._user = user
        return self
    
    def with_products(self, products: list[Product]):
        """Set order products"""
        self._products = products
        return self
    
    def add_product(self, product: Product):
        """Add a single product"""
        self._products.append(product)
        return self
    
    def with_order_id(self, order_id: str):
        """Set order ID"""
        self._order_id = order_id
        return self
    
    def with_status(self, status: str):
        """Set order status (pending, processing, completed, cancelled)"""
        self._status = status
        return self
    
    def with_shipping_address(self, address: str):
        """Set shipping address"""
        self._shipping_address = address
        return self
    
    def with_payment_method(self, payment_method: str):
        """Set payment method"""
        self._payment_method = payment_method
        return self
    
    def build(self) -> Order:
        """Build the Order object"""
        order = Order(
            user=self._user,
            products=self._products,
            order_id=self._order_id,
            status=self._status,
            shipping_address=self._shipping_address or self._user.address,
            payment_method=self._payment_method
        )
        order.total = order.calculate_total()
        return order


# Convenience functions for common patterns
def create_standard_user() -> User:
    """Create a standard user with default values"""
    return UserBuilder().build()


def create_admin_user() -> User:
    """Create an admin user"""
    return UserBuilder().as_admin().build()


def create_guest_user() -> User:
    """Create a guest user"""
    return UserBuilder().as_guest().build()


def create_sample_product(category: str = "Electronics") -> Product:
    """Create a sample product in given category"""
    return ProductBuilder().in_category(category).build()


def create_order_with_products(user: User, product_count: int = 3) -> Order:
    """Create an order with specified number of products"""
    products = [ProductBuilder().build() for _ in range(product_count)]
    return OrderBuilder().for_user(user).with_products(products).build()
