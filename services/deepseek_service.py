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
                    
                    # Find the start of HTML content
                    html_start = content.find('<')
                    if html_start != -1:
                        content = content[html_start:]
                    
                    # Remove any closing backticks or wrapper text
                    if content.endswith('```'):
                        content = content[:-3]
                    
                    # Remove any opening backticks with html
                    if content.startswith('```html'):
                        content = content[7:]
                    
                    # Remove any wrapper text before HTML
                    wrapper_texts = [
                        'Here\'s a WordPress-formatted HTML blog post for solving the LeetCode',
                        'Here\'s a WordPress-formatted HTML blog post for solving the "',
                        'Here\'s a WordPress-formatted HTML blog post about',
                        'Here\'s a WordPress-formatted HTML blog post',
                        'Here\'s a blog post about',
                        'Here\'s a blog post',
                        'Here\'s the blog post',
                        'Here\'s the content',
                        'Here\'s the HTML',
                        'Here\'s the post',
                        'Here\'s the article',
                        'Here\'s the solution',
                        'Here\'s the implementation',
                        'Here\'s the code',
                        'Here\'s the explanation',
                        'Here\'s the analysis',
                        'Here\'s the approach',
                        'Here\'s the strategy',
                        'Here\'s the method',
                        'Here\'s the technique',
                        'Here\'s the algorithm',
                        'Here\'s the solution',
                        'Here\'s the implementation',
                        'Here\'s the code',
                        'Here\'s the explanation',
                        'Here\'s the analysis',
                        'Here\'s the approach',
                        'Here\'s the strategy',
                        'Here\'s the method',
                        'Here\'s the technique',
                        'Here\'s the algorithm'
                    ]
                    
                    for text in wrapper_texts:
                        if content.startswith(text):
                            content = content[len(text):]
                            break
                    
                    content = content.strip()
                    return content
                else:
                    raise Exception(f"Failed to generate content with DeepSeek: {response.status}") 