import aiohttp
import base64
from services.base_service import BaseService
from config.config import Config

class WordPressService(BaseService):
    def __init__(self):
        config = Config()
        self.base_url = config.wp_url.rstrip('/')
        self.auth = base64.b64encode(
            f"{config.wp_username}:{config.wp_app_pass}".encode()
        ).decode()
        self.headers = {
            "Authorization": f"Basic {self.auth}",
            "Content-Type": "application/json"
        }

    async def execute(self, title, content, status="draft"):
        post_data = {
            "title": title,
            "content": content,
            "status": status
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/wp-json/wp/v2/posts",
                json=post_data,
                headers=self.headers
            ) as response:
                if response.status in (200, 201):
                    data = await response.json()
                    return data
                else:
                    raise Exception(f"Failed to publish to WordPress: {response.status}") 