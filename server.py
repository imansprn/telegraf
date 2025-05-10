from flask import Flask, jsonify, send_from_directory
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
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import logging
import os

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

scheduler = None

@app.route('/')
def index():
    return send_from_directory('public', 'index.html')

@app.route('/api/status')
def api_status():
    next_run_time = None
    if scheduler:
        jobs = scheduler.get_jobs()
        if jobs:
            next_run_time = min((job.next_run_time for job in jobs if job.next_run_time), default=None)
    now_utc = datetime.now(timezone.utc)
    next_run_utc = next_run_time.astimezone(timezone.utc).isoformat() if next_run_time else None
    return jsonify({
        'status': 'running',
        'message': 'Blog generator service is running',
        'current_time': now_utc.isoformat(),
        'next_run': next_run_utc,
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

def start_scheduler():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger('telegraf-scheduler')
    config = Config()
    config.validate_config()
    global scheduler
    scheduler = BackgroundScheduler(timezone=timezone.utc)
    for schedule_time in config.cron_schedules:
        hour, minute = map(int, schedule_time.split(':'))
        scheduler.add_job(
            run_async_task,
            CronTrigger(hour=hour, minute=minute),
            name=f'blog_generator_{hour:02d}_{minute:02d}',
            misfire_grace_time=3600
        )
        logger.info(f"Scheduled task for {schedule_time} UTC")
    scheduler.start()
    logger.info("Scheduler started successfully")
    return scheduler

start_scheduler()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3001)