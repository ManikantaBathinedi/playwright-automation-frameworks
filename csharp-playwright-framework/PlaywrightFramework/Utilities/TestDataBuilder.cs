using Bogus;

namespace PlaywrightFramework.Utilities
{
    /// <summary>
    /// User data class
    /// </summary>
    public class User
    {
        public string Email { get; set; } = string.Empty;
        public string Password { get; set; } = string.Empty;
        public string FirstName { get; set; } = string.Empty;
        public string LastName { get; set; } = string.Empty;
        public string Phone { get; set; } = string.Empty;
        public string Address { get; set; } = string.Empty;
        public string City { get; set; } = string.Empty;
        public string ZipCode { get; set; } = string.Empty;
        public string Country { get; set; } = string.Empty;
        public string Role { get; set; } = "user";
        public bool IsActive { get; set; } = true;

        public string FullName() => $"{FirstName} {LastName}".Trim();
    }

    /// <summary>
    /// Product data class
    /// </summary>
    public class Product
    {
        public string Name { get; set; } = string.Empty;
        public decimal Price { get; set; }
        public string Description { get; set; } = string.Empty;
        public string Category { get; set; } = string.Empty;
        public string Sku { get; set; } = string.Empty;
        public int Stock { get; set; } = 100;
        public bool IsAvailable { get; set; } = true;
        public string ImageUrl { get; set; } = string.Empty;
    }

    /// <summary>
    /// Order data class
    /// </summary>
    public class Order
    {
        public User User { get; set; } = new User();
        public List<Product> Products { get; set; } = new List<Product>();
        public string OrderId { get; set; } = string.Empty;
        public string Status { get; set; } = "pending";
        public decimal Total { get; set; }
        public string ShippingAddress { get; set; } = string.Empty;
        public string PaymentMethod { get; set; } = "credit_card";

        public decimal CalculateTotal() => Products.Sum(p => p.Price);
    }

    /// <summary>
    /// Builder for creating User test data with fluent interface
    /// </summary>
    /// <example>
    /// var user = new UserBuilder()
    ///     .WithEmail("test@example.com")
    ///     .WithPassword("Test@123")
    ///     .WithName("John", "Doe")
    ///     .WithRole("admin")
    ///     .Build();
    /// </example>
    public class UserBuilder
    {
        private readonly Faker _faker = new Faker();
        private string _email;
        private string _password;
        private string _firstName;
        private string _lastName;
        private string _phone;
        private string _address;
        private string _city;
        private string _zipCode;
        private string _country = "USA";
        private string _role = "user";
        private bool _isActive = true;

        public UserBuilder()
        {
            _email = _faker.Internet.Email();
            _password = DataGenerator.GenerateStrongPassword();
            _firstName = _faker.Name.FirstName();
            _lastName = _faker.Name.LastName();
            _phone = _faker.Phone.PhoneNumber();
            _address = _faker.Address.StreetAddress();
            _city = _faker.Address.City();
            _zipCode = _faker.Address.ZipCode();
        }

        public UserBuilder WithEmail(string email)
        {
            _email = email;
            return this;
        }

        public UserBuilder WithPassword(string password)
        {
            _password = password;
            return this;
        }

        public UserBuilder WithName(string firstName, string lastName)
        {
            _firstName = firstName;
            _lastName = lastName;
            return this;
        }

        public UserBuilder WithPhone(string phone)
        {
            _phone = phone;
            return this;
        }

        public UserBuilder WithAddress(string address, string? city = null, string? zipCode = null, string country = "USA")
        {
            _address = address;
            if (!string.IsNullOrEmpty(city))
                _city = city;
            if (!string.IsNullOrEmpty(zipCode))
                _zipCode = zipCode;
            _country = country;
            return this;
        }

        public UserBuilder WithRole(string role)
        {
            _role = role;
            return this;
        }

        public UserBuilder AsAdmin()
        {
            _role = "admin";
            return this;
        }

        public UserBuilder AsGuest()
        {
            _role = "guest";
            return this;
        }

        public UserBuilder Active(bool isActive = true)
        {
            _isActive = isActive;
            return this;
        }

        public User Build()
        {
            return new User
            {
                Email = _email,
                Password = _password,
                FirstName = _firstName,
                LastName = _lastName,
                Phone = _phone,
                Address = _address,
                City = _city,
                ZipCode = _zipCode,
                Country = _country,
                Role = _role,
                IsActive = _isActive
            };
        }
    }

    /// <summary>
    /// Builder for creating Product test data
    /// </summary>
    /// <example>
    /// var product = new ProductBuilder()
    ///     .WithName("Laptop")
    ///     .WithPrice(999.99m)
    ///     .InCategory("Electronics")
    ///     .WithStock(50)
    ///     .Build();
    /// </example>
    public class ProductBuilder
    {
        private readonly Faker _faker = new Faker();
        private string _name;
        private decimal _price;
        private string _description;
        private string _category = "General";
        private string _sku;
        private int _stock = 100;
        private bool _isAvailable = true;
        private string _imageUrl = "https://via.placeholder.com/300";

        public ProductBuilder()
        {
            _name = $"Product-{_faker.Random.AlphaNumeric(8)}";
            _price = _faker.Random.Decimal(10, 1000);
            _description = _faker.Lorem.Sentence(10);
            _sku = _faker.Random.String2(10, "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789");
        }

        public ProductBuilder WithName(string name)
        {
            _name = name;
            return this;
        }

        public ProductBuilder WithPrice(decimal price)
        {
            _price = price;
            return this;
        }

        public ProductBuilder WithDescription(string description)
        {
            _description = description;
            return this;
        }

        public ProductBuilder InCategory(string category)
        {
            _category = category;
            return this;
        }

        public ProductBuilder WithSku(string sku)
        {
            _sku = sku;
            return this;
        }

        public ProductBuilder WithStock(int stock)
        {
            _stock = stock;
            return this;
        }

        public ProductBuilder OutOfStock()
        {
            _stock = 0;
            _isAvailable = false;
            return this;
        }

        public ProductBuilder WithImage(string imageUrl)
        {
            _imageUrl = imageUrl;
            return this;
        }

        public Product Build()
        {
            return new Product
            {
                Name = _name,
                Price = _price,
                Description = _description,
                Category = _category,
                Sku = _sku,
                Stock = _stock,
                IsAvailable = _isAvailable,
                ImageUrl = _imageUrl
            };
        }
    }

    /// <summary>
    /// Builder for creating Order test data
    /// </summary>
    /// <example>
    /// var order = new OrderBuilder()
    ///     .ForUser(user)
    ///     .WithProducts(new List&lt;Product&gt; { product1, product2 })
    ///     .WithShippingAddress("123 Main St")
    ///     .WithPaymentMethod("paypal")
    ///     .Build();
    /// </example>
    public class OrderBuilder
    {
        private readonly Faker _faker = new Faker();
        private User _user;
        private List<Product> _products = new List<Product>();
        private string _orderId;
        private string _status = "pending";
        private string _shippingAddress = string.Empty;
        private string _paymentMethod = "credit_card";

        public OrderBuilder()
        {
            _user = new UserBuilder().Build();
            _orderId = $"ORD-{_faker.Random.Number(10000000, 99999999)}";
        }

        public OrderBuilder ForUser(User user)
        {
            _user = user;
            return this;
        }

        public OrderBuilder WithProducts(List<Product> products)
        {
            _products = products;
            return this;
        }

        public OrderBuilder AddProduct(Product product)
        {
            _products.Add(product);
            return this;
        }

        public OrderBuilder WithOrderId(string orderId)
        {
            _orderId = orderId;
            return this;
        }

        public OrderBuilder WithStatus(string status)
        {
            _status = status;
            return this;
        }

        public OrderBuilder WithShippingAddress(string address)
        {
            _shippingAddress = address;
            return this;
        }

        public OrderBuilder WithPaymentMethod(string paymentMethod)
        {
            _paymentMethod = paymentMethod;
            return this;
        }

        public Order Build()
        {
            var order = new Order
            {
                User = _user,
                Products = _products,
                OrderId = _orderId,
                Status = _status,
                ShippingAddress = string.IsNullOrEmpty(_shippingAddress) ? _user.Address : _shippingAddress,
                PaymentMethod = _paymentMethod
            };
            order.Total = order.CalculateTotal();
            return order;
        }
    }

    /// <summary>
    /// Convenience methods for common test data patterns
    /// </summary>
    public static class TestDataBuilderHelpers
    {
        public static User CreateStandardUser() => new UserBuilder().Build();

        public static User CreateAdminUser() => new UserBuilder().AsAdmin().Build();

        public static User CreateGuestUser() => new UserBuilder().AsGuest().Build();

        public static Product CreateSampleProduct(string category = "Electronics")
            => new ProductBuilder().InCategory(category).Build();

        public static Order CreateOrderWithProducts(User user, int productCount = 3)
        {
            var products = Enumerable.Range(0, productCount)
                .Select(_ => new ProductBuilder().Build())
                .ToList();
            return new OrderBuilder()
                .ForUser(user)
                .WithProducts(products)
                .Build();
        }
    }
}
