from flask import Flask, jsonify
import schedule
import time
import threading
import asyncio
import argparse
import json
from services.leetcode_service import LeetCodeService
from services.deepseek_service import DeepSeekService
from services.wordpress_service import WordPressService
from strategies.go_post_strategy import GoPostStrategy
from config.config import Config

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
        wordpress_service = WordPressService()

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

        # Publish to WordPress
        print("\nPublishing to WordPress...")
        title = f"Interview Problem: {problem_data['title']} - Go Solution"
        result = await wordpress_service.execute(title, blog_content)
        
        print(f"\nSuccessfully published post! WordPress post ID: {result.get('id')}")
        return result

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise

def run_scheduled_task():
    """Run the blog generator on a schedule"""
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

def run_async_task():
    """Run the async blog generator"""
    asyncio.run(generate_blog_post())

@app.route('/')
def home():
    return jsonify({
        "status": "running",
        "message": "Blog generator service is running",
        "next_run": schedule.next_run().isoformat() if schedule.next_run() else "No scheduled runs"
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

@app.route('/trigger', methods=['POST'])
def trigger():
    """Manually trigger the blog generator"""
    try:
        # Create an event to track thread completion
        thread_error = [None]
        
        def run_with_error_handling():
            try:
                run_async_task()
            except Exception as e:
                thread_error[0] = e
        
        # Run in a separate thread to avoid blocking
        thread = threading.Thread(target=run_with_error_handling)
        thread.start()
        thread.join(timeout=1)  # Wait briefly to catch immediate errors
        
        if thread_error[0]:
            raise thread_error[0]
            
        return jsonify({
            "status": "success",
            "message": "Blog generation started"
        })
    except Exception as e:
        print(f"Error in trigger endpoint: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == '__main__':
    # Schedule the blog generator to run daily at midnight UTC
    schedule.every().day.at("00:00").do(run_async_task)
    
    # Start the scheduler in a separate thread
    scheduler_thread = threading.Thread(target=run_scheduled_task)
    scheduler_thread.daemon = True
    scheduler_thread.start()
    
    # Run the Flask app
    app.run(host='0.0.0.0', port=3001) 