# Installation Guide

## Prerequisites

- Python 3.13+
- Either WordPress or Ghost site with REST API enabled
- DeepSeek API key
- Platform-specific credentials:
  - For WordPress: Username and Application Password
  - For Ghost: Admin API Key

## Installation Steps

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

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```

5. Run tests to verify installation:
   ```bash
   pytest -v
   ```

## Configuration

Create a `.env` file in the root directory with the following variables:

```bash
# DeepSeek API Configuration
DEEPSEEK_API_KEY=your_deepseek_api_key_here

# Blog Platform Selection (wordpress or ghost)
BLOG_PLATFORM=ghost

# WordPress Configuration (if using WordPress)
WP_USERNAME=your_wordpress_username
WP_APP_PASS=your_wordpress_application_password
WP_URL=https://your-wordpress-site.com

# Ghost Configuration (if using Ghost)
GHOST_URL=https://your-ghost-site.com
GHOST_API_KEY=your_ghost_admin_api_key_here

# Schedule Configuration
CRON_SCHEDULE=00:00,12:00,18:00  # Run at midnight, noon, and 6 PM UTC
```
