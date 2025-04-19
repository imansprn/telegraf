# LeetCode Blog Post Generator

[![Tests](https://github.com/imansprn/telegraf/actions/workflows/test.yml/badge.svg)](https://github.com/imansprn/telegraf/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/imansprn/telegraf/branch/main/graph/badge.svg)](https://codecov.io/gh/imansprn/telegraf)
[![Python Version](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An automated system that fetches random LeetCode problems, generates blog posts about solving them in Go, and publishes them to WordPress. The service runs continuously and generates posts on a daily schedule.

## Features

- Fetches random LeetCode problems using GraphQL API
- Generates detailed blog posts using DeepSeek AI
- Publishes content to WordPress automatically
- Runs as a web service with scheduled tasks
- Implements clean architecture with design patterns

## Project Structure

```
.
├── config/
│   └── config.py           # Configuration management (Singleton)
├── services/
│   ├── base_service.py     # Base service interface
│   ├── leetcode_service.py # LeetCode problem fetcher
│   ├── deepseek_service.py # AI content generator
│   └── wordpress_service.py# WordPress publisher
├── strategies/
│   ├── base_strategy.py    # Base strategy interface
│   └── go_post_strategy.py # Go-specific blog post generator
├── tests/                  # Test files
│   ├── test_leetcode_service.py
│   ├── test_server.py
│   └── test_wordpress_service.py
├── server.py              # Main web server and scheduler
├── requirements.txt       # Python dependencies
├── Procfile              # Web server configuration
├── .env.example          # Environment variables template
├── pytest.ini           # pytest configuration
├── .codecov.yml         # Codecov configuration
└── README.md            # This file
```

## Prerequisites

- Python 3.13+
- WordPress site with REST API enabled
- DeepSeek API key
- WordPress Application Password

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
   DEEPSEEK_API_KEY=your_deepseek_api_key_here
   WP_USERNAME=your_wordpress_username
   WP_APP_PASS=your_wordpress_application_password
   WP_URL=https://your-wordpress-site.com
   ```

## Local Development

Run the server locally:
```bash
python server.py
```

The server will:
1. Start a web server on port 3000
2. Schedule blog post generation for midnight UTC
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

- `tests/test_leetcode_service.py`: Tests for LeetCode API integration
- `tests/test_wordpress_service.py`: Tests for WordPress publishing
- `tests/test_server.py`: Tests for web server endpoints

### Coverage Reports

View the HTML coverage report:
```bash
open htmlcov/index.html  # On macOS
xdg-open htmlcov/index.html  # On Linux
start htmlcov/index.html  # On Windows
```

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
   - Posts are generated daily at midnight UTC
   - Schedule can be modified in server.py
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