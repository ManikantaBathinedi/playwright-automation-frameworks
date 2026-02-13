using Microsoft.Extensions.Configuration;

namespace PlaywrightFramework.Config;

/// <summary>
/// Application settings and configuration management
/// </summary>
public class Settings
{
    private static Settings? _instance;
    private static readonly object Lock = new();
    private readonly IConfiguration _configuration;

    private Settings()
    {
        // Get environment from TEST_ENV (default: dev)
        var environment = Environment.GetEnvironmentVariable("TEST_ENV") ?? "dev";

        _configuration = new ConfigurationBuilder()
            .SetBasePath(Directory.GetCurrentDirectory())
            .AddJsonFile("appsettings.json", optional: false, reloadOnChange: true)
            .AddJsonFile($"appsettings.{environment}.json", optional: true, reloadOnChange: true)
            .AddEnvironmentVariables()
            .Build();

        Console.WriteLine("============================================================");
        Console.WriteLine($"✅ Environment: {environment.ToUpper()}");
        Console.WriteLine($"📄 Config file: appsettings.{environment}.json");
        Console.WriteLine($"📍 BASE_URL: {BaseUrl}");
        Console.WriteLine($"🖥️  HEADLESS: {Headless}");
        Console.WriteLine($"👥 WORKERS: {MaxWorkers}");
        Console.WriteLine("============================================================\n");
    }

    public static Settings Instance
    {
        get
        {
            if (_instance == null)
            {
                lock (Lock)
                {
                    _instance ??= new Settings();
                }
            }
            return _instance;
        }
    }

    // Application Settings
    public string BaseUrl => _configuration["App:BaseUrl"] ?? "https://demo.playwright.dev/todomvc";
    public string Environment => _configuration["App:Environment"] ?? "dev";
    public string Browser => _configuration["App:Browser"] ?? "chromium";
    public bool Headless => bool.Parse(_configuration["App:Headless"] ?? "true");
    public int SlowMo => int.Parse(_configuration["App:SlowMo"] ?? "0");

    // Test User Credentials
    public string TestUserEmail => _configuration["TestUser:Email"] ?? "test@example.com";
    public string TestUserPassword => _configuration["TestUser:Password"] ?? "Test@123";

    // Admin Credentials
    public string AdminEmail => _configuration["Admin:Email"] ?? "admin@example.com";
    public string AdminPassword => _configuration["Admin:Password"] ?? "Admin@123";

    // API Settings
    public string ApiBaseUrl => _configuration["API:BaseUrl"] ?? "https://jsonplaceholder.typicode.com";
    public int ApiTimeout => int.Parse(_configuration["API:Timeout"] ?? "30000");

    // Timeouts
    public int DefaultTimeout => int.Parse(_configuration["Timeouts:Default"] ?? "30000");
    public int NavigationTimeout => int.Parse(_configuration["Timeouts:Navigation"] ?? "30000");
    public int ActionTimeout => int.Parse(_configuration["Timeouts:Action"] ?? "10000");

    // Test Settings
    public int MaxRetries => int.Parse(_configuration["TestSettings:MaxRetries"] ?? "2");
    public int MaxWorkers => int.Parse(_configuration["TestSettings:MaxWorkers"] ?? "4");
    public bool TakeScreenshotOnFailure => bool.Parse(_configuration["TestSettings:TakeScreenshotOnFailure"] ?? "true");
    public bool RecordVideo => bool.Parse(_configuration["TestSettings:RecordVideo"] ?? "false");
}
