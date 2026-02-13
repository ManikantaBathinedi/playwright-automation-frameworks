using Serilog;

namespace PlaywrightFramework.Utilities;

/// <summary>
/// Custom logger for test execution
/// </summary>
public static class TestLogger
{
    static TestLogger()
    {
        Log.Logger = new LoggerConfiguration()
            .MinimumLevel.Debug()
            .WriteTo.Console()
            .WriteTo.File("logs/test-.log", rollingInterval: RollingInterval.Day)
            .CreateLogger();
    }

    public static void Info(string message) => Log.Information("ℹ️  {Message}", message);
    public static void Debug(string message) => Log.Debug("🔍 {Message}", message);
    public static void Warning(string message) => Log.Warning("⚠️  {Message}", message);
    public static void Error(string message) => Log.Error("❌ {Message}", message);
    public static void Error(Exception ex, string message) => Log.Error(ex, "❌ {Message}", message);
    public static void Success(string message) => Log.Information("✅ {Message}", message);
    public static void TestStart(string testName) => Log.Information("🧪 Starting test: {TestName}", testName);
    public static void TestEnd(string testName, bool passed)
    {
        if (passed)
            Log.Information("✅ Test passed: {TestName}", testName);
        else
            Log.Error("❌ Test failed: {TestName}", testName);
    }
    public static void Step(string step) => Log.Information("📝 Step: {Step}", step);
    public static void Api(string method, string endpoint) => Log.Information("🌐 API: {Method} {Endpoint}", method, endpoint);

    public static void CloseAndFlush() => Log.CloseAndFlush();
}
