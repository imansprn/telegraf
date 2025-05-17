# Development Guide

## Architecture Overview

This project follows a clean architecture with several key components:

1. **Core Services**:
   - `LeetCodeService`: Fetches random LeetCode problems via GraphQL API
   - `DeepSeekService`: Generates content using DeepSeek AI
   - `BlogService`: Abstract factory pattern for WordPress/Ghost publishing

2. **Content Generation Strategy**:
   - `GoPostStrategy`: Builds prompts for generating Go-specific solution explanations

3. **Web Server**:
   - Flask application with health checks and manual triggers
   - Scheduled job execution using APScheduler

## Development Setup

1. Install development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```

2. Run tests with coverage:
   ```bash
   pytest --cov=. --cov-report=html
   ```

3. Check code style:
   ```bash
   black .
   flake8
   ```

## Testing

The project uses pytest for testing and pytest-cov for coverage reporting.

### Running Tests

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

## Troubleshooting

Common issues and solutions:

1. **API Authentication Errors**
   - Verify your DeepSeek API key is correctly set in environment variables
   - Check that your blog platform credentials are valid

2. **Content Generation Issues**
   - If content appears malformatted, check the HTML processing in DeepSeekService
   - For code formatting issues, verify the Go code beautification logic

3. **Scheduling Problems**
   - Ensure CRON_SCHEDULE is properly formatted in your environment variables
   - Check server logs for scheduling errors
