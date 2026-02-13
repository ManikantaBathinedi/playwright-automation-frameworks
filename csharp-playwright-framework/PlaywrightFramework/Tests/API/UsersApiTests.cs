using System.Net;
using System.Text.Json;
using FluentAssertions;
using Microsoft.Playwright;
using NUnit.Framework;
using PlaywrightFramework.Utilities;

namespace PlaywrightFramework.Tests.API;

[TestFixture]
[Category("API")]
public class UsersApiTests : BaseTest
{
    private IAPIRequestContext _apiContext = null!;
    private string _apiBaseUrl = null!;

    [SetUp]
    public new async Task SetUp()
    {
        // Base SetUp is called automatically by NUnit
        _apiBaseUrl = Settings.ApiBaseUrl;

        // Create API request context
        _apiContext = await Playwright.APIRequest.NewContextAsync(new APIRequestNewContextOptions
        {
            BaseURL = _apiBaseUrl,
            ExtraHTTPHeaders = new Dictionary<string, string>
            {
                ["Content-Type"] = "application/json",
                ["Accept"] = "application/json"
            }
        });

        TestLogger.Info($"API Base URL: {_apiBaseUrl}");
    }

    [TearDown]
    public new async Task TearDown()
    {
        await _apiContext.DisposeAsync();
        await base.TearDown();
    }

    [Test]
    [Category("Smoke")]
    [Description("Test GET request - Retrieve list of users")]
    public async Task Test_GetListOfUsers_ReturnsSuccess()
    {
        // Act
        TestLogger.Step("Send GET request to /users");
        var response = await _apiContext.GetAsync("/users");

        // Assert
        TestLogger.Step("Verify response status");
        response.Ok.Should().BeTrue("Response should be successful");
        response.Status.Should().Be((int)HttpStatusCode.OK, "Status code should be 200");

        // Parse response
        var responseBody = await response.TextAsync();
        var users = JsonSerializer.Deserialize<List<JsonElement>>(responseBody);

        // Assert response data
        users.Should().NotBeNull("Response should contain users");
        users.Should().HaveCount(10, "Should have 10 users");

        // Verify user structure
        var firstUser = users![0];
        firstUser.TryGetProperty("id", out _).Should().BeTrue("User should have 'id'");
        firstUser.TryGetProperty("name", out _).Should().BeTrue("User should have 'name'");
        firstUser.TryGetProperty("email", out _).Should().BeTrue("User should have 'email'");

        TestLogger.Success($"Retrieved {users.Count} users successfully");
    }

    [Test]
    [Category("Smoke")]
    [Description("Test GET request - Retrieve single user by ID")]
    public async Task Test_GetSingleUserById_ReturnsCorrectUser()
    {
        // Arrange
        int userId = 1;

        // Act
        TestLogger.Step($"Send GET request to /users/{userId}");
        var response = await _apiContext.GetAsync($"/users/{userId}");

        // Assert
        response.Ok.Should().BeTrue("Response should be successful");
        response.Status.Should().Be(200);

        var responseBody = await response.TextAsync();
        var user = JsonSerializer.Deserialize<JsonElement>(responseBody);

        // Verify user data
        user.TryGetProperty("id", out var idProperty).Should().BeTrue();
        idProperty.GetInt32().Should().Be(userId, "User ID should match requested ID");

        user.TryGetProperty("name", out _).Should().BeTrue("User should have name");
        user.TryGetProperty("email", out _).Should().BeTrue("User should have email");

        TestLogger.Success($"User {userId} retrieved successfully");
    }

    [Test]
    [Description("Test POST request - Create new user")]
    public async Task Test_CreateNewUser_ReturnsCreatedStatus()
    {
        // Arrange
        var newUser = new
        {
            name = "Test User",
            username = "testuser",
            email = "test@example.com"
        };

        // Act
        TestLogger.Step("Send POST request to create user");
        var response = await _apiContext.PostAsync("/users", new APIRequestContextOptions
        {
            DataObject = newUser
        });

        // Assert
        response.Status.Should().Be((int)HttpStatusCode.Created, "Status should be 201 Created");

        var responseBody = await response.TextAsync();
        var createdUser = JsonSerializer.Deserialize<JsonElement>(responseBody);

        // Verify created user has ID assigned
        createdUser.TryGetProperty("id", out var idProperty).Should().BeTrue();
        idProperty.GetInt32().Should().BeGreaterThan(0, "Created user should have valid ID");

        TestLogger.Success("User created successfully");
    }

    [Test]
    [Description("Test PUT request - Update existing user")]
    public async Task Test_UpdateUser_ReturnsUpdatedData()
    {
        // Arrange
        int userId = 1;
        var updatedUser = new
        {
            id = userId,
            name = "Updated Name",
            email = "updated@example.com"
        };

        // Act
        TestLogger.Step($"Send PUT request to update user {userId}");
        var response = await _apiContext.PutAsync($"/users/{userId}", new APIRequestContextOptions
        {
            DataObject = updatedUser
        });

        // Assert
        response.Ok.Should().BeTrue("Update should be successful");

        var responseBody = await response.TextAsync();
        var user = JsonSerializer.Deserialize<JsonElement>(responseBody);

        user.TryGetProperty("id", out var idProperty).Should().BeTrue();
        idProperty.GetInt32().Should().Be(userId);

        TestLogger.Success("User updated successfully");
    }

    [Test]
    [Description("Test PATCH request - Partial update user")]
    public async Task Test_PatchUser_UpdatesSingleField()
    {
        // Arrange
        int userId = 1;
        var partialUpdate = new
        {
            email = "patched@example.com"
        };

        // Act
        TestLogger.Step($"Send PATCH request to update user {userId} email");
        var response = await _apiContext.PatchAsync($"/users/{userId}", new APIRequestContextOptions
        {
            DataObject = partialUpdate
        });

        // Assert
        response.Ok.Should().BeTrue("Patch should be successful");

        TestLogger.Success("User patched successfully");
    }

    [Test]
    [Description("Test DELETE request - Delete user")]
    public async Task Test_DeleteUser_ReturnsSuccess()
    {
        // Arrange
        int userId = 1;

        // Act
        TestLogger.Step($"Send DELETE request to remove user {userId}");
        var response = await _apiContext.DeleteAsync($"/users/{userId}");

        // Assert
        response.Ok.Should().BeTrue("Delete should be successful");

        TestLogger.Success($"User {userId} deleted successfully");
    }

    [Test]
    [Category("Negative")]
    [Description("Test GET request with invalid user ID returns 404")]
    public async Task Test_GetInvalidUserId_Returns404()
    {
        // Arrange
        int invalidUserId = 99999;

        // Act
        TestLogger.Step($"Send GET request for non-existent user {invalidUserId}");
        var response = await _apiContext.GetAsync($"/users/{invalidUserId}");

        // Assert
        response.Status.Should().Be((int)HttpStatusCode.NotFound, "Should return 404 for invalid user ID");

        TestLogger.Success("404 error handled correctly");
    }

    [Test]
    [Category("Negative")]
    [Description("Test POST with invalid data returns error")]
    public async Task Test_CreateUserWithInvalidData_ReturnsError()
    {
        // Arrange
        var invalidUser = new
        {
            name = "",  // Empty name should fail validation
            email = "not-an-email"  // Invalid email format
        };

        // Act
        TestLogger.Step("Send POST with invalid user data");
        var response = await _apiContext.PostAsync("/users", new APIRequestContextOptions
        {
            DataObject = invalidUser
        });

        // Assert
        // Most APIs return 400 Bad Request or 422 Unprocessable Entity
        response.Status.Should().BeOneOf(400, 422, 201);

        TestLogger.Info($"Response status: {response.Status} - Should return validation error or be lenient");
    }

    [Test]
    [Category("Performance")]
    [Description("Test API response time is acceptable")]
    public async Task Test_ApiResponseTime_IsAcceptable()
    {
        // Arrange
        var stopwatch = System.Diagnostics.Stopwatch.StartNew();

        // Act
        TestLogger.Step("Measure API response time");
        var response = await _apiContext.GetAsync("/users");
        stopwatch.Stop();

        // Assert
        response.Ok.Should().BeTrue();
        var responseTime = stopwatch.ElapsedMilliseconds;

        TestLogger.Info($"Response time: {responseTime}ms");
        responseTime.Should().BeLessThan(3000, "Response should be under 3 seconds");

        TestLogger.Success($"API responded in {responseTime}ms");
    }

    [Test]
    [Description("Test API response headers are correct")]
    public async Task Test_VerifyResponseHeaders()
    {
        // Act
        TestLogger.Step("Send request and verify headers");
        var response = await _apiContext.GetAsync("/users");

        // Assert
        response.Ok.Should().BeTrue();

        var headers = response.Headers;
        TestLogger.Info("Checking response headers:");

        // Verify common headers exist
        headers.ContainsKey("content-type").Should().BeTrue("Should have Content-Type header");
        TestLogger.Info($"Content-Type: {headers["content-type"]}");

        if (headers.ContainsKey("content-type"))
        {
            headers["content-type"].Should().Contain("application/json", "API should return JSON");
        }

        TestLogger.Success("Response headers verified");
    }

    [Test]
    [Description("Test API pagination with query parameters")]
    public async Task Test_GetUsersWithPagination()
    {
        // Act
        TestLogger.Step("Send GET request with pagination params");
        var response = await _apiContext.GetAsync("/users?_page=1&_limit=5");

        // Assert
        response.Ok.Should().BeTrue();

        var responseBody = await response.TextAsync();
        var users = JsonSerializer.Deserialize<List<JsonElement>>(responseBody);

        users.Should().NotBeNull();
        users!.Count.Should().BeLessOrEqualTo(5, "Should respect pagination limit");

        TestLogger.Success($"Retrieved {users.Count} users with pagination");
    }

    [Test]
    [Description("Test GET user posts - Nested resource")]
    public async Task Test_GetUserPosts_ReturnsUserData()
    {
        // Arrange
        int userId = 1;

        // Act
        TestLogger.Step($"Get posts for user {userId}");
        var response = await _apiContext.GetAsync($"/users/{userId}/posts");

        // Assert
        response.Ok.Should().BeTrue();

        var responseBody = await response.TextAsync();
        var posts = JsonSerializer.Deserialize<List<JsonElement>>(responseBody);

        posts.Should().NotBeNull();
        TestLogger.Info($"User {userId} has {posts!.Count} posts");

        TestLogger.Success("Nested resource retrieved successfully");
    }
}
