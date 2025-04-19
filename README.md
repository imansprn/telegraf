# LeetCode Blog Post Generator

An automated system that fetches random LeetCode problems, generates blog posts about solving them in Go, and publishes them to WordPress.

## Features

- Fetches random LeetCode problems using GraphQL API
- Generates detailed blog posts using DeepSeek AI
- Publishes content to WordPress automatically
- Implements clean architecture with design patterns:
  - Factory Pattern for service management
  - Strategy Pattern for content generation
  - Singleton Pattern for configuration
- Automated daily execution via GitHub Actions

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
├── main.py                 # Main entry point
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
└── README.md              # This file
```

## Prerequisites

- Python 3.8+
- WordPress site with REST API enabled
- DeepSeek API key
- WordPress Application Password

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd leetcode-blog-generator
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

## Usage

Run the main script:
```bash
python main.py
```

The script will:
1. Fetch a random LeetCode problem
2. Generate a blog post about solving it in Go
3. Publish the post to your WordPress site

## Design Patterns Used

### Factory Pattern
- Each service (LeetCode, DeepSeek, WordPress) is created through its own factory method
- Makes it easy to add new services or modify existing ones

### Strategy Pattern
- Different blog post generation strategies can be implemented
- Currently implements `GoPostStrategy` for Go-specific content
- Easy to add new strategies for other programming languages

### Singleton Pattern
- Configuration management is handled through a singleton
- Ensures consistent configuration across the application

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

## GitHub Actions Setup

The project includes a GitHub Actions workflow that automatically runs the blog generator daily. To set it up:

1. Fork this repository to your GitHub account
2. Go to your repository's Settings > Secrets and variables > Actions
3. Add the following secrets:
   - `DEEPSEEK_API_KEY`: Your DeepSeek API key
   - `WP_USERNAME`: Your WordPress username
   - `WP_APP_PASS`: Your WordPress application password
   - `WP_URL`: Your WordPress site URL

The workflow will:
- Run automatically at 00:00 UTC every day
- Can be triggered manually from the Actions tab
- Upload logs as artifacts if the job fails

To manually trigger the workflow:
1. Go to the Actions tab in your repository
2. Select "Scheduled Blog Generator" from the workflows list
3. Click "Run workflow" 