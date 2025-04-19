import aiohttp
from services.base_service import BaseService
from config.config import Config

class DeepSeekService(BaseService):
    def __init__(self):
        config = Config()
        self.api_key = config.deepseek_api_key
        self.api_url = "https://api.deepseek.com/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    async def execute(self, prompt):
        payload = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 2000
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.api_url,
                json=payload,
                headers=self.headers
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
                    
                    # Clean up the response by removing any opening/closing statements
                    content = content.replace('Here\'s a WordPress-formatted HTML blog post for solving the LeetCode', '')
                    content = content.replace('\"`html', '')
                    content = content.replace('\"`', '')
                    content = content.replace('Interview Problem:', '')
                    content = content.strip()
                    
                    return content
                else:
                    raise Exception(f"Failed to generate content with DeepSeek: {response.status}") 