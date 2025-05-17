# Usage Guide

## Running as a Web Service

```bash
# Start the web server (includes built-in scheduler)
gunicorn server:app
```

The server will:
- Start a web server on port 3001 (configurable)
- Automatically start the scheduler based on CRON_SCHEDULE
- Provide API endpoints for monitoring and manual triggers

## API Endpoints

- `GET /` - Check service status and next scheduled run
- `GET /health` - Health check endpoint
- `POST /trigger` - Manually trigger blog post generation

## Programmatic Usage

```python
import asyncio
from services.leetcode_service import LeetCodeService
from services.deepseek_service import DeepSeekService
from services.blog_service import BlogServiceFactory
from strategies.go_post_strategy import GoPostStrategy

async def generate_post():
    # Initialize services
    leetcode_service = LeetCodeService()
    deepseek_service = DeepSeekService()
    blog_service = BlogServiceFactory.create()  # Uses config to determine platform
    go_strategy = GoPostStrategy()
    
    # Fetch a random LeetCode problem
    problem_data = await leetcode_service.execute(difficulty='medium')
    
    # Generate content using the Go strategy
    prompt = go_strategy.build_prompt(problem_data)
    blog_content = await deepseek_service.execute(prompt)
    
    # Publish to configured platform
    title = f"{problem_data['title']} - Go Solution"
    result = await blog_service.execute(title, blog_content, status="publish")
    print(f"Published post with ID: {result.get('id')}")

# Run the async function
asyncio.run(generate_post())
```

## Scheduling Options

- Posts are generated at the times specified in CRON_SCHEDULE
- Multiple times can be specified as a comma-separated list (e.g., "00:00,12:00,18:00")
- Times should be in 24-hour format (HH:MM) in UTC
- If CRON_SCHEDULE is not set, posts will be generated at midnight UTC (00:00)
