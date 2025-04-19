# LeetCode Blog Post Generator

[![Tests](https://github.com/imansprn/telegraf/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/imansprn/telegraf/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/imansprn/telegraf/branch/main/graph/badge.svg)](https://codecov.io/gh/imansprn/telegraf)
[![Python Version](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An automated system that fetches random LeetCode problems, generates blog posts about solving them in Go, and publishes them to either WordPress or Ghost. The service runs continuously and generates posts on a configurable schedule.

## Features

- Fetches random LeetCode problems using GraphQL API
- Generates detailed blog posts using DeepSeek AI
- Flexible publishing platform support (WordPress or Ghost)
- Runs as a web service with configurable schedules
- Implements clean architecture with design patterns
- Comprehensive test coverage (94%)
- Continuous Integration with GitHub Actions

## Project Structure

```
.
├── config/                    # Configuration management
│   ├── __init__.py
│   └── config.py             # Singleton configuration manager
│
├── services/                  # Core service implementations
│   ├── __init__.py
│   ├── base_service.py       # Abstract base service interface
│   ├── blog_service.py       # Blog platform factory and strategy
│   ├── leetcode_service.py   # LeetCode problem fetcher
│   ├── deepseek_service.py   # AI content generator
│   ├── ghost_service.py      # Ghost publishing service
│   └── wordpress_service.py  # WordPress publishing service
│
├── strategies/                # Content generation strategies
│   ├── __init__.py
│   ├── base_strategy.py      # Abstract base strategy interface
│   └── go_post_strategy.py   # Go-specific blog post generator
│
├── tests/                    # Test suite
│   ├── __init__.py
│   ├── conftest.py          # Test configuration and fixtures
│   ├── test_blog_service.py # Blog service tests
│   ├── test_deepseek_service.py # AI service tests
│   ├── test_ghost_service.py # Ghost service tests
│   ├── test_leetcode_service.py # LeetCode service tests
│   ├── test_server.py       # Server endpoint tests
│   └── test_wordpress_service.py # WordPress service tests
│
├── .github/                  # GitHub configuration
│   └── workflows/
│       └── test.yml         # CI/CD workflow configuration
│
├── server.py                # Main application server
├── requirements.txt         # Python dependencies
├── Procfile                # Process configuration
├── .env.example            # Environment variables template
├── pytest.ini             # Test configuration
├── .codecov.yml           # Coverage configuration
└── README.md              # Project documentation
```

## Prerequisites

- Python 3.13+
- Either WordPress or Ghost site with REST API enabled
- DeepSeek API key
- Platform-specific credentials:
  - For WordPress: Username and Application Password
  - For Ghost: Admin API Key

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/imansprn/telegraf.git
   cd telegraf
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Copy the environment template and fill in your credentials:
   ```bash
   cp .env.example .env
   ```

5. Edit `.env` with your actual credentials:
   ```
   DEEPSEEK_API_KEY=your_deepseek_api_key
   
   # WordPress Configuration (if using WordPress)
   WP_USERNAME=your_wordpress_username
   WP_APP_PASS=your_wordpress_application_password
   WP_URL=https://your-wordpress-site.com
   
   # Ghost Configuration (if using Ghost)
   GHOST_URL=https://your-ghost-site.com
   GHOST_ADMIN_API_KEY=your_ghost_admin_api_key
   
   CRON_SCHEDULE=00:00,12:00,18:00  # Optional: Schedule posts for midnight, noon, and 6 PM UTC
   ```

## Local Development

Run the server locally:
```bash
python server.py
```

The server will:
1. Start a web server on port 3000
2. Schedule blog post generation based on CRON_SCHEDULE
3. Provide API endpoints for monitoring and manual triggers

## API Endpoints

- `GET /` - Check service status and next scheduled run
- `GET /health` - Health check endpoint
- `POST /trigger` - Manually trigger blog post generation

## Testing

The project uses pytest for testing and pytest-cov for coverage reporting.

### Running Tests

1. Install test dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run tests with coverage:
   ```bash
   pytest
   ```

This will:
- Run all tests
- Generate a coverage report in the terminal
- Create a detailed HTML coverage report in `htmlcov/`

### Test Structure

- `tests/test_blog_service.py`: Tests for blog platform factory
- `tests/test_deepseek_service.py`: Tests for AI content generation
- `tests/test_leetcode_service.py`: Tests for LeetCode API integration
- `tests/test_server.py`: Tests for web server endpoints

### Coverage Reports

View the HTML coverage report:
```bash
open htmlcov/index.html  # On macOS
xdg-open htmlcov/index.html  # On Linux
start htmlcov/index.html  # On Windows
```

## Continuous Integration

The project uses GitHub Actions for continuous integration:

- Runs on every push and pull request
- Executes all tests with coverage reporting
- Uploads coverage reports to Codecov
- Validates code quality and test coverage

## Deployment

The service can be deployed to any platform that supports Python web applications. Key considerations for deployment:

1. Environment Setup
   - Set all required environment variables
   - Ensure Python 3.13+ is available
   - Install dependencies from requirements.txt

2. Server Configuration
   - The service runs on port 3000 by default
   - Uses the Procfile for web server configuration
   - Supports standard web server interfaces

3. Monitoring
   - Use the /health endpoint for uptime monitoring
   - Check service status via the root endpoint
   - View logs for debugging and monitoring

4. Scheduling
   - Posts are generated at the times specified in CRON_SCHEDULE
   - If CRON_SCHEDULE is not set, posts will be generated at midnight UTC (00:00)
   - Multiple times can be specified as a comma-separated list (e.g., "00:00,12:00,18:00")
   - Times should be in 24-hour format (HH:MM) in UTC
   - Invalid time formats will raise an error during startup
   - Manual triggers available via API

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [LeetCode](https://leetcode.com/) for their GraphQL API
- [DeepSeek](https://deepseek.com/) for their AI capabilities
- [WordPress](https://wordpress.org/) for their REST API 