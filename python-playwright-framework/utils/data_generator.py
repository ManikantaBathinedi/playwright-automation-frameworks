"""
Data Generator utility
Generates random test data for automation tests
"""

import random
import string
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()


class DataGenerator:
    """Test data generator"""
    
    @staticmethod
    def random_email(domain: str = "example.com") -> str:
        """Generate random email address"""
        timestamp = datetime.now().timestamp()
        random_num = random.randint(1000, 9999)
        return f"test.user.{int(timestamp)}.{random_num}@{domain}"
    
    @staticmethod
    def random_string(length: int = 10, include_special: bool = False) -> str:
        """Generate random string"""
        characters = string.ascii_letters + string.digits
        
        if include_special:
            characters += "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        return ''.join(random.choice(characters) for _ in range(length))
    
    @staticmethod
    def random_number(min_val: int = 1, max_val: int = 100) -> int:
        """Generate random number"""
        return random.randint(min_val, max_val)
    
    @staticmethod
    def random_phone(format_type: str = "US") -> str:
        """Generate random phone number"""
        if format_type == "US":
            area_code = random.randint(200, 999)
            first_part = random.randint(200, 999)
            second_part = random.randint(1000, 9999)
            return f"{area_code}-{first_part}-{second_part}"
        else:
            country_code = random.randint(1, 99)
            number = random.randint(1000000000, 9999999999)
            return f"+{country_code}{number}"
    
    @staticmethod
    def random_date(start_date: datetime = None, end_date: datetime = None) -> datetime:
        """Generate random date"""
        if start_date is None:
            start_date = datetime(2020, 1, 1)
        if end_date is None:
            end_date = datetime.now()
        
        time_between = end_date - start_date
        days_between = time_between.days
        random_days = random.randrange(days_between)
        
        return start_date + timedelta(days=random_days)
    
    @staticmethod
    def random_date_string(date_format: str = "%Y-%m-%d") -> str:
        """Generate random date string"""
        random_date = DataGenerator.random_date()
        return random_date.strftime(date_format)
    
    @staticmethod
    def random_boolean() -> bool:
        """Generate random boolean"""
        return random.choice([True, False])
    
    @staticmethod
    def random_password(length: int = 12) -> str:
        """Generate random password"""
        # Ensure at least one of each type
        password = [
            random.choice(string.ascii_uppercase),
            random.choice(string.ascii_lowercase),
random.choice(string.digits),
            random.choice("!@#$%^&*")
        ]
        
        # Fill the rest
        all_chars = string.ascii_letters + string.digits + "!@#$%^&*"
        password += [random.choice(all_chars) for _ in range(length - 4)]
        
        # Shuffle to randomize positions
        random.shuffle(password)
        
        return ''.join(password)
    
    @staticmethod
    def random_first_name() -> str:
        """Generate random first name"""
        return fake.first_name()
    
    @staticmethod
    def random_last_name() -> str:
        """Generate random last name"""
        return fake.last_name()
    
    @staticmethod
    def random_full_name() -> str:
        """Generate random full name"""
        return fake.name()
    
    @staticmethod
    def random_address() -> dict:
        """Generate random address"""
        return {
            "street": fake.street_address(),
            "city": fake.city(),
            "state": fake.state_abbr(),
            "zip_code": fake.zipcode(),
            "country": fake.country()
        }
    
    @staticmethod
    def random_credit_card() -> str:
        """Generate random credit card number (for testing only!)"""
        # Generate 16 random digits
        card_parts = []
        for i in range(4):
            part = ''.join([str(random.randint(0, 9)) for _ in range(4)])
            card_parts.append(part)
        
        return '-'.join(card_parts)
    
    @staticmethod
    def random_cvv() -> str:
        """Generate random CVV (3 digits)"""
        return str(random.randint(100, 999))
    
    @staticmethod
    def generate_user() -> dict:
        """Generate test user data"""
        return {
            "first_name": DataGenerator.random_first_name(),
            "last_name": DataGenerator.random_last_name(),
            "full_name": DataGenerator.random_full_name(),
            "email": DataGenerator.random_email(),
            "password": DataGenerator.random_password(12),
            "phone": DataGenerator.random_phone(),
            "address": DataGenerator.random_address()
        }
    
    @staticmethod
    def random_from_list(items: list) -> any:
        """Generate random item from array"""
        return random.choice(items)
    
    @staticmethod
    def random_url() -> str:
        """Generate random URL"""
        domains = ["example.com", "test.com", "demo.com", "sample.org", "website.net"]
        protocols = ["http", "https"]
        protocol = random.choice(protocols)
        domain = random.choice(domains)
        return f"{protocol}://{domain}"
    
    @staticmethod
    def generate_uuid() -> str:
        """Generate UUID"""
        import uuid
        return str(uuid.uuid4())
