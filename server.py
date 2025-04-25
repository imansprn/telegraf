from flask import Flask, jsonify
import asyncio
import argparse
import json
from datetime import datetime, timezone
from services.leetcode_service import LeetCodeService
from services.deepseek_service import DeepSeekService
from services.blog_service import BlogServiceFactory
from strategies.go_post_strategy import GoPostStrategy
from config.config import Config
import threading

app = Flask(__name__)

def parse_arguments():
    parser = argparse.ArgumentParser(description='Generate blog posts from LeetCode problems')
    parser.add_argument('--difficulty', type=str, default='medium',
                      choices=['easy', 'medium', 'hard'],
                      help='Problem difficulty level')
    parser.add_argument('--topics', type=str, default='["array","hash-table","two-pointers"]',
                      help='Problem topics as JSON array')
    parser.add_argument('--companies', type=str, default='["google","amazon","facebook","microsoft","apple"]',
                      help='Company tags as JSON array')
    return parser.parse_args()

async def generate_blog_post(difficulty='medium', topics=None, companies=None):
    """Generate a blog post from a LeetCode problem"""
    try:
        # Initialize configuration
        config = Config()
        config.validate_config()

        # Initialize services
        leetcode_service = LeetCodeService()
        deepseek_service = DeepSeekService()
        blog_service = BlogServiceFactory.create()

        # Initialize strategy
        go_strategy = GoPostStrategy()

        # Parse topics and companies if they're strings
        if isinstance(topics, str):
            topics = json.loads(topics)
        if isinstance(companies, str):
            companies = json.loads(companies)

        # Fetch random LeetCode problem with interview filters
        print("Fetching random LeetCode problem for interview preparation...")
        problem_data = await leetcode_service.execute(
            difficulty=difficulty,
            topics=topics,
            company_tags=companies
        )
        
        if not problem_data:
            raise Exception("Failed to fetch LeetCode problem")

        # Print problem metadata
        print(f"\nSelected Problem:")
        print(f"Title: {problem_data['title']}")
        print(f"Difficulty: {problem_data['difficulty']}")
        print(f"Acceptance Rate: {problem_data['interview_metadata']['acceptance_rate']:.2f}%")
        print(f"Companies: {', '.join(problem_data['interview_metadata']['companies'])}")
        print(f"Topics: {', '.join(problem_data['interview_metadata']['topics'])}")

        # Generate blog post content
        print("\nGenerating blog post content...")
        prompt = go_strategy.build_prompt(problem_data)
        blog_content = await deepseek_service.execute(prompt)

        # Publish to blog platform
        print(f"\nPublishing to {config.blog_platform}...")
        title = f"{problem_data['title']} - Go Solution"
        result = await blog_service.execute(title, blog_content, status="publish")
        
        print(f"\nSuccessfully published post! Post ID: {result.get('id')}")
        return result

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise

def run_async_task():
    """Run the async blog generator"""
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(generate_blog_post())
    except Exception as e:
        print(f"Error in async task: {str(e)}")
    finally:
        loop.close()

next_run = None

@app.route('/')
def home():
    """Health check endpoint."""
    return jsonify({
        'status': 'running',
        'message': 'Blog generator service is running',
        'current_time': datetime.now(timezone.utc).isoformat(),
        'next_run': next_run.isoformat() if next_run else None
    })

@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy'
    })

@app.route('/trigger', methods=['POST'])
def trigger():
    """Manually trigger the blog generator"""
    try:
        thread = threading.Thread(target=run_async_task)
        thread.start()
        return jsonify({
            'status': 'success',
            'message': 'Blog generation started'
        })
    except Exception as e:
        print(f"Error in trigger endpoint: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3001)