import asyncio
from services.leetcode_service import LeetCodeService
from services.deepseek_service import DeepSeekService
from services.wordpress_service import WordPressService
from strategies.go_post_strategy import GoPostStrategy
from config.config import Config

async def main():
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

        # Fetch random LeetCode problem
        print("Fetching random LeetCode problem...")
        problem_data = await leetcode_service.execute()
        
        if not problem_data:
            raise Exception("Failed to fetch LeetCode problem")

        # Generate blog post content
        print("Generating blog post content...")
        prompt = go_strategy.build_prompt(problem_data)
        blog_content = await deepseek_service.execute(prompt)

        # Publish to WordPress
        print("Publishing to WordPress...")
        title = f"Solving {problem_data['title']} in Go"
        result = await wordpress_service.execute(title, blog_content)
        
        print(f"Successfully published post! WordPress post ID: {result.get('id')}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main()) 