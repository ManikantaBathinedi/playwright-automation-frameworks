# C# Playwright Framework - Dockerfile
# Multi-stage build for efficient image size

FROM mcr.microsoft.com/playwright/dotnet:v1.40.0-focal AS base
WORKDIR /app

# Build stage
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src

# Copy solution and project files
COPY PlaywrightFramework.sln ./
COPY PlaywrightFramework/PlaywrightFramework.csproj PlaywrightFramework/

# Restore dependencies
RUN dotnet restore PlaywrightFramework.sln

# Copy the rest of the code
COPY . .

# Build the project
WORKDIR /src/PlaywrightFramework
RUN dotnet build PlaywrightFramework.csproj -c Release -o /app/build

# Test stage
FROM build AS test
WORKDIR /src/PlaywrightFramework

# Install Playwright browsers
RUN pwsh bin/Release/net8.0/playwright.ps1 install chrome firefox webkit

# Set environment variables
ENV TEST_ENV=qa \
    BROWSER=chrome \
    HEADLESS=true

# Run tests
ENTRYPOINT ["dotnet", "test", "--no-build", "--configuration", "Release", "--logger:console;verbosity=detailed"]

# Production runtime stage
FROM base AS runtime
COPY --from=build /app/build .

# Install Playwright browsers
RUN pwsh playwright.ps1 install chrome firefox webkit
RUN pwsh playwright.ps1 install-deps

# Set environment variables
ENV TEST_ENV=qa \
    BROWSER=chrome \
    HEADLESS=true

ENTRYPOINT ["dotnet", "test", "PlaywrightFramework.dll"]
