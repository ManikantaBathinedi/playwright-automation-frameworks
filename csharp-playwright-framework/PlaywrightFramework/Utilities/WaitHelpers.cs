using Microsoft.Playwright;

namespace PlaywrightFramework.Utilities
{
    /// <summary>
    /// Custom wait and retry utilities for Playwright tests
    /// Provides advanced waiting mechanisms beyond Playwright's built-in waits
    /// </summary>
    public static class WaitHelpers
    {
        /// <summary>
        /// Wait for a condition to become true with polling
        /// </summary>
        /// <param name="condition">Function that returns true when condition is met</param>
        /// <param name="timeout">Maximum time to wait in milliseconds (default: 30000)</param>
        /// <param name="pollInterval">Time between checks in milliseconds (default: 500)</param>
        /// <param name="errorMessage">Error message if timeout occurs</param>
        /// <returns>True if condition met</returns>
        /// <exception cref="TimeoutException">If condition not met within timeout</exception>
        /// <example>
        /// await WaitHelpers.WaitForCondition(
        ///     async () => await page.Locator(".popup").IsVisibleAsync(),
        ///     timeout: 10000,
        ///     errorMessage: "Popup did not appear"
        /// );
        /// </example>
        public static async Task<bool> WaitForCondition(
            Func<Task<bool>> condition,
            int timeout = 30000,
            int pollInterval = 500,
            string errorMessage = "Condition not met within timeout")
        {
            var stopwatch = System.Diagnostics.Stopwatch.StartNew();

            while (stopwatch.ElapsedMilliseconds < timeout)
            {
                try
                {
                    if (await condition())
                    {
                        return true;
                    }
                }
                catch
                {
                    // Ignore exceptions during polling
                }

                await Task.Delay(pollInterval);
            }

            throw new TimeoutException($"{errorMessage} (timeout: {timeout}ms)");
        }

        /// <summary>
        /// Wait until a value stops changing (becomes stable)
        /// Useful for waiting for counters, animations, or async updates to complete
        /// </summary>
        /// <typeparam name="T">Type of value being monitored</typeparam>
        /// <param name="getValue">Function that returns the value to monitor</param>
        /// <param name="timeout">Maximum time to wait in milliseconds (default: 10000)</param>
        /// <param name="stabilityTime">How long value must remain unchanged in milliseconds (default: 2000)</param>
        /// <param name="pollInterval">Time between checks in milliseconds (default: 500)</param>
        /// <returns>The stable value</returns>
        /// <exception cref="TimeoutException">If value does not stabilize within timeout</exception>
        /// <example>
        /// var cartCount = await WaitHelpers.WaitUntilStable(
        ///     async () => await page.Locator(".cart-count").TextContentAsync(),
        ///     timeout: 10000,
        ///     stabilityTime: 1000
        /// );
        /// </example>
        public static async Task<T> WaitUntilStable<T>(
            Func<Task<T>> getValue,
            int timeout = 10000,
            int stabilityTime = 2000,
            int pollInterval = 500)
        {
            var stopwatch = System.Diagnostics.Stopwatch.StartNew();
            var lastValue = await getValue();
            var stableStopwatch = System.Diagnostics.Stopwatch.StartNew();

            while (stopwatch.ElapsedMilliseconds < timeout)
            {
                await Task.Delay(pollInterval);
                var currentValue = await getValue();

                if (EqualityComparer<T>.Default.Equals(currentValue, lastValue))
                {
                    // Value hasn't changed
                    if (stableStopwatch.ElapsedMilliseconds >= stabilityTime)
                    {
                        return currentValue;
                    }
                }
                else
                {
                    // Value changed, reset stability timer
                    lastValue = currentValue;
                    stableStopwatch.Restart();
                }
            }

            throw new TimeoutException($"Value did not stabilize within {timeout}ms");
        }

        /// <summary>
        /// Wait for any one of multiple conditions to become true
        /// </summary>
        /// <param name="conditions">List of condition functions</param>
        /// <param name="timeout">Maximum time to wait in milliseconds (default: 30000)</param>
        /// <param name="pollInterval">Time between checks in milliseconds (default: 500)</param>
        /// <returns>Index of the condition that became true</returns>
        /// <exception cref="TimeoutException">If none of the conditions are met within timeout</exception>
        /// <example>
        /// var result = await WaitHelpers.WaitForAny(new[]
        /// {
        ///     async () => await page.Locator(".success").IsVisibleAsync(),
        ///     async () => await page.Locator(".error").IsVisibleAsync()
        /// }, timeout: 10000);
        /// 
        /// if (result == 0)
        ///     Console.WriteLine("Success!");
        /// else
        ///     Console.WriteLine("Error occurred");
        /// </example>
        public static async Task<int> WaitForAny(
            Func<Task<bool>>[] conditions,
            int timeout = 30000,
            int pollInterval = 500)
        {
            var stopwatch = System.Diagnostics.Stopwatch.StartNew();

            while (stopwatch.ElapsedMilliseconds < timeout)
            {
                for (int i = 0; i < conditions.Length; i++)
                {
                    try
                    {
                        if (await conditions[i]())
                        {
                            return i;
                        }
                    }
                    catch
                    {
                        // Ignore exceptions during polling
                    }
                }

                await Task.Delay(pollInterval);
            }

            throw new TimeoutException("None of the conditions were met within timeout");
        }

        /// <summary>
        /// Wait for all conditions to become true
        /// </summary>
        /// <param name="conditions">List of condition functions</param>
        /// <param name="timeout">Maximum time to wait in milliseconds (default: 30000)</param>
        /// <param name="pollInterval">Time between checks in milliseconds (default: 500)</param>
        /// <returns>True if all conditions met</returns>
        /// <exception cref="TimeoutException">If all conditions are not met within timeout</exception>
        /// <example>
        /// await WaitHelpers.WaitForAll(new[]
        /// {
        ///     async () => await page.Locator(".header").IsVisibleAsync(),
        ///     async () => await page.Locator(".content").IsVisibleAsync(),
        ///     async () => await page.Locator(".footer").IsVisibleAsync()
        /// }, timeout: 10000);
        /// </example>
        public static async Task<bool> WaitForAll(
            Func<Task<bool>>[] conditions,
            int timeout = 30000,
            int pollInterval = 500)
        {
            var stopwatch = System.Diagnostics.Stopwatch.StartNew();

            while (stopwatch.ElapsedMilliseconds < timeout)
            {
                bool allMet = true;

                foreach (var condition in conditions)
                {
                    try
                    {
                        if (!await condition())
                        {
                            allMet = false;
                            break;
                        }
                    }
                    catch
                    {
                        allMet = false;
                        break;
                    }
                }

                if (allMet)
                {
                    return true;
                }

                await Task.Delay(pollInterval);
            }

            throw new TimeoutException("Not all conditions were met within timeout");
        }

        /// <summary>
        /// Retry an action with exponential backoff
        /// </summary>
        /// <typeparam name="T">Return type of the action</typeparam>
        /// <param name="action">Action to retry</param>
        /// <param name="maxAttempts">Maximum number of attempts (default: 3)</param>
        /// <param name="initialDelay">Initial delay in milliseconds (default: 1000)</param>
        /// <param name="backoffMultiplier">Multiplier for exponential backoff (default: 2.0)</param>
        /// <returns>Result of the action</returns>
        /// <exception cref="Exception">Throws the last exception if all attempts fail</exception>
        /// <example>
        /// var response = await WaitHelpers.RetryAsync(
        ///     async () => await apiClient.GetDataAsync(),
        ///     maxAttempts: 3,
        ///     initialDelay: 1000
        /// );
        /// </example>
        public static async Task<T> RetryAsync<T>(
            Func<Task<T>> action,
            int maxAttempts = 3,
            int initialDelay = 1000,
            double backoffMultiplier = 2.0)
        {
            Exception lastException = null;
            int currentDelay = initialDelay;

            for (int attempt = 1; attempt <= maxAttempts; attempt++)
            {
                try
                {
                    return await action();
                }
                catch (Exception ex)
                {
                    lastException = ex;

                    if (attempt == maxAttempts)
                    {
                        throw;
                    }

                    Console.WriteLine($"⚠️  Attempt {attempt} failed: {ex.Message}");
                    Console.WriteLine($"⏳ Retrying in {currentDelay}ms...");

                    await Task.Delay(currentDelay);
                    currentDelay = (int)(currentDelay * backoffMultiplier);
                }
            }

            throw lastException;  // This should never be reached, but satisfies compiler
        }

        /// <summary>
        /// Fluent wait helper for chaining wait conditions
        /// </summary>
        public class SmartWait
        {
            private readonly IPage _page;
            private ILocator _locator;
            private int _timeout = 30000;

            public SmartWait(IPage page)
            {
                _page = page;
            }

            public SmartWait WithTimeout(int timeout)
            {
                _timeout = timeout;
                return this;
            }

            public SmartWait ForElement(string selector)
            {
                _locator = _page.Locator(selector);
                return this;
            }

            public async Task<SmartWait> ToBeVisibleAsync()
            {
                if (_locator != null)
                {
                    await _locator.WaitForAsync(new() { State = WaitForSelectorState.Visible, Timeout = _timeout });
                }
                return this;
            }

            public async Task<SmartWait> ToBeHiddenAsync()
            {
                if (_locator != null)
                {
                    await _locator.WaitForAsync(new() { State = WaitForSelectorState.Hidden, Timeout = _timeout });
                }
                return this;
            }

            public async Task<SmartWait> AndEnabledAsync()
            {
                if (_locator != null)
                {
                    await WaitForCondition(
                        async () => await _locator.IsEnabledAsync(),
                        timeout: _timeout,
                        errorMessage: "Element not enabled"
                    );
                }
                return this;
            }

            public async Task<SmartWait> AndContainsTextAsync(string text)
            {
                if (_locator != null)
                {
                    await WaitForCondition(
                        async () =>
                        {
                            var content = await _locator.TextContentAsync();
                            return content != null && content.Contains(text);
                        },
                        timeout: _timeout,
                        errorMessage: $"Element does not contain text: {text}"
                    );
                }
                return this;
            }
        }
    }
}
