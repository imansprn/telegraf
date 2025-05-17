# LeetCode Blog Post Generator

[![Tests](https://github.com/imansprn/telegraf/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/imansprn/telegraf/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/imansprn/telegraf/branch/main/graph/badge.svg)](https://codecov.io/gh/imansprn/telegraf)
[![Python Version](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An automated system that fetches random LeetCode problems, generates blog posts about solving them in Go, and publishes them to either WordPress or Ghost. The service runs continuously and generates posts on a configurable schedule.

## Features

- Fetches random LeetCode problems using GraphQL API
- Generates detailed blog posts using DeepSeek AI
- Supports multiple publishing platforms (WordPress/Ghost)
- Runs as a web service with configurable schedules
- Implements clean architecture with design patterns
- Comprehensive test coverage (98%)

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your API keys

# Run the server
gunicorn server:app
```

## Documentation

For detailed documentation, see the following guides:

- [Installation Guide](docs/INSTALLATION.md) - Setup and configuration
- [Usage Guide](docs/USAGE.md) - Running the service and API endpoints
- [Development Guide](docs/DEVELOPMENT.md) - Architecture and testing

## Requirements

- Python 3.13+
- DeepSeek API key
- WordPress or Ghost blog with API access

## Contributing

Contributions are welcome! See [Development Guide](docs/DEVELOPMENT.md) for details.

## License

MIT