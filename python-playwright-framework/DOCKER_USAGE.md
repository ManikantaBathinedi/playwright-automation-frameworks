# Docker Usage Guide

## Overview
The Playwright framework is fully containerized using Docker, allowing for consistent test execution across different environments.

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
docker-compose up playwright-tests
```

#### Run Specific Test Suite
```bash
# Run regression tests
docker-compose --profile regression up playwright-regression

# Run API tests only
docker-compose --profile api up playwright-api
```

#### Run with Custom Environment
```bash
# Run tests in staging environment
TEST_ENV=staging docker-compose up playwright-tests

# Run tests in dev with Firefox
TEST_ENV=dev BROWSER=firefox docker-compose up playwright-tests
```

### 3. View Reports
After test execution, reports are available in the `reports/` directory:
- HTML Report: `reports/html-report/index.html`
- Screenshots: `reports/screenshots/`
- Videos: `reports/videos/`
- Logs: `reports/logs/`

## Advanced Usage

### Run Interactive Shell in Container
```bash
docker-compose run playwright-tests /bin/bash
```

Then inside the container:
```bash
# Run specific tests
pytest tests/auth/test_login.py -v

# Run with different browser
pytest -v --browser firefox

# Run specific test
pytest tests/auth/test_login.py::test_successful_login -v
```

### Pass Custom pytest Arguments
```bash
docker-compose run playwright-tests pytest -v -k "login" --maxfail=1
```

###Build without Cache (Fresh Build)
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
- name: Run Tests in Docker
  run: |
    docker-compose up --abort-on-container-exit --exit-code-from playwright-tests
```

### Azure Pipelines Example
```yaml
- task: DockerCompose@0
  displayName: 'Run Playwright Tests'
  inputs:
    dockerComposeFile: 'docker-compose.yml'
    action: 'Run services'
    serviceName: 'playwright-tests'
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `TEST_ENV` | `qa` | Test environment (dev/qa/staging/prod) |
| `BROWSER` | `chrome` | Browser to use (chrome/firefox/webkit) |
| `HEADLESS` | `true` | Run in headless mode |
| `WORKERS` | `auto` | Number of parallel workers |

## Troubleshooting

### Container Exits Immediately
- Check logs: `docker-compose logs playwright-tests`
- Verify Dockerfile syntax
- Ensure base image is accessible

### Tests Fail in Docker but Pass Locally
- Check environment variables are set correctly
- Verify mounted volumes
- Ensure network connectivity for external APIs

### Permission Issues with Reports
```bash
# Fix permissions on Linux/Mac
sudo chown -R $USER:$USER reports/
```

### Out of Memory
```bash
# Increase Docker memory in Docker Desktop settings
# Or limit parallel workers
WORKERS=2 docker-compose up playwright-tests
```

## Best Practices

1. **Always use specific image tags** in production (not `latest`)
2. **Mount reports directory** to access results after container stops
3. **Use profiles** to organize different test suites
4. **Set resource limits** in docker-compose for production:
   ```yaml
   deploy:
     resources:
       limits:
         cpus: '2.0'
         memory: 4G
   ```
5. **Use .dockerignore** to exclude unnecessary files (node_modules, venv, __pycache__)

## Container Size Optimization

The current Dockerfile uses:
- Official Playwright Python base image with browsers pre-installed
- Multi-stage build pattern (can be enhanced further)
- No unnecessary dependencies

Expected image size: ~2.5GB (includes Chrome, Firefox, WebKit browsers)

## Running Specific Test Markers

```bash
# Smoke tests
docker-compose run playwright-tests pytest -m smoke -v

# Regression tests
docker-compose run playwright-tests pytest -m regression -v

# API tests only
docker-compose run playwright-tests pytest -m api -v

# Exclude slow tests
docker-compose run playwright-tests pytest -m "not slow" -v
```

## Debugging Failed Tests

```bash
# Run in non-headless mode (requires X11 forwarding on Linux)
HEADLESS=false docker-compose run playwright-tests pytest -v

# Run with trace enabled
docker-compose run playwright-tests pytest -v --tracing on

# Keep container running after tests
docker-compose run playwright-tests tail -f /dev/null
# Then in another terminal:
docker exec -it playwright-python-tests /bin/bash
```
