# C# Playwright Framework - Docker Usage Guide

## Overview
The C# Playwright framework is fully containerized using Docker, allowing for consistent test execution across different environments.

## Prerequisites
- Docker Desktop installed (Windows/Mac) or Docker Engine (Linux)
- docker-compose installed (usually comes with Docker Desktop)

## Quick Start

### 1. Build the Docker Image
```bash
docker-compose build
```

### 2. Run Tests in Docker

#### Run Default Tests (Smoke Suite)
```bash
docker-compose up playwright-tests-csharp
```

#### Run Specific Test Suite
```bash
# Run regression tests
docker-compose --profile regression up playwright-regression-csharp

# Run API tests only
docker-compose --profile api up playwright-api-csharp
```

#### Run with Custom Environment
```bash
# Run tests in staging environment
TEST_ENV=staging docker-compose up playwright-tests-csharp

# Run tests in dev with Firefox
TEST_ENV=dev BROWSER=firefox docker-compose up playwright-tests-csharp
```

### 3. View Reports
After test execution, reports are available in:
- Test Results: `PlaywrightFramework/TestResults/`
- Screenshots: `PlaywrightFramework/screenshots/`
- Traces: `PlaywrightFramework/traces/`
- HTML Report: `PlaywrightFramework/TestResults/test-results.html`

## Advanced Usage

### Run Interactive Shell in Container
```bash
docker-compose run playwright-tests-csharp /bin/bash
```

Then inside the container:
```bash
# Run specific tests
dotnet test --filter "FullyQualifiedName~LoginTests"

# Run with different browser
dotnet test --filter "Category=smoke"

# Run specific test method
dotnet test --filter "FullyQualifiedName~Test_SuccessfulLogin"
```

### Pass Custom dotnet test Arguments
```bash
docker-compose run playwright-tests-csharp dotnet test --filter "Category=e2e" --logger:"console;verbosity=detailed"
```

### Build without Cache (Fresh Build)
```bash
docker-compose build --no-cache
```

### Remove Containers and Images
```bash
# Stop and remove containers
docker-compose down

# Remove everything including volumes
docker-compose down -v

# Remove images
docker-compose down --rmi all
```

## CI/CD Integration

### GitHub Actions Example
```yaml
- name: Run C# Tests in Docker
  run: |
    docker-compose up --abort-on-container-exit --exit-code-from playwright-tests-csharp
```

### Azure Pipelines Example
```yaml
- task: DockerCompose@0
  displayName: 'Run Playwright C# Tests'
  inputs:
    dockerComposeFile: 'docker-compose.yml'
    action: 'Run services'
    serviceName: 'playwright-tests-csharp'
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `TEST_ENV` | `qa` | Test environment (dev/qa/staging/prod) |
| `BROWSER` | `chrome` | Browser to use (chrome/firefox/webkit) |
| `HEADLESS` | `true` | Run in headless mode |

## Test Filtering

```bash
# By category
docker-compose run playwright-tests-csharp dotnet test --filter "Category=smoke"
docker-compose run playwright-tests-csharp dotnet test --filter "Category=regression"
docker-compose run playwright-tests-csharp dotnet test --filter "Category=api"

# By test class
docker-compose run playwright-tests-csharp dotnet test --filter "FullyQualifiedName~LoginTests"

# By test method
docker-compose run playwright-tests-csharp dotnet test --filter "FullyQualifiedName~Test_SuccessfulLogin"

# Exclude categories
docker-compose run playwright-tests-csharp dotnet test --filter "Category!=slow"
```

## Troubleshooting

### Container Exits Immediately
```bash
# Check logs
docker-compose logs playwright-tests-csharp

# Verify Dockerfile syntax
# Ensure base image is accessible
```

### Tests Fail in Docker but Pass Locally
- Check environment variables are set correctly
- Verify mounted volumes
- Ensure network connectivity for external APIs

### Permission Issues with Test Results
```bash
# Fix permissions on Linux/Mac
sudo chown -R $USER:$USER PlaywrightFramework/TestResults/
sudo chown -R $USER:$USER PlaywrightFramework/screenshots/
sudo chown -R $USER:$USER PlaywrightFramework/traces/
```

### Out of Memory
```bash
# Increase Docker memory in Docker Desktop settings
# Or add resource limits in docker-compose.yml:
services:
  playwright-tests-csharp:
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 4G
```

## Best Practices

1. **Use specific image tags** in production (not `latest`)
2. **Mount test results directories** to access reports after container stops
3. **Use profiles** to organize different test suites
4. **Set resource limits** in production environments
5. **Use .dockerignore** to exclude unnecessary files

## Container Size Optimization

The Dockerfile uses:
- Official Playwright .NET base image with browsers pre-installed
- Multi-stage build to separate build and runtime
- Only necessary files copied to final image

Expected image size: ~3GB (includes .NET SDK + Chrome + Firefox + WebKit)

## Running with Retry

```bash
# Tests automatically retry due to [Retry] attribute in BaseTest
docker-compose up playwright-tests-csharp

# Override retry count
docker-compose run playwright-tests-csharp dotnet test -- NUnit.MaxRetryCount=3
```

## Debugging Failed Tests

```bash
# Run in non-headless mode (requires X11 forwarding on Linux)
HEADLESS=false docker-compose run playwright-tests-csharp

# Keep container running after tests
docker-compose run playwright-tests-csharp tail -f /dev/null
# Then in another terminal:
docker exec -it playwright-csharp-tests /bin/bash

# Access traces for failed tests
# They are automatically saved to traces/ directory
```

## Viewing HTML Reports

After running tests:
```bash
# Open the HTML report in your browser
# On Windows:
start PlaywrightFramework/TestResults/test-results.html

# On Mac:
open PlaywrightFramework/TestResults/test-results.html

# On Linux:
xdg-open PlaywrightFramework/TestResults/test-results.html
```

## Parallel Execution in Docker

```bash
# Use NUnit's parallel execution (configured in .runsettings)
docker-compose run playwright-tests-csharp dotnet test --settings:.runsettings
```
