import aiohttp
import base64
from services.base_service import BaseService
from config.config import Config

class GhostService(BaseService):
    def __init__(self):
        config = Config()
        self.base_url = config.ghost_url.rstrip('/')
        self.api_key = config.ghost_api_key
        self.headers = {
            "Authorization": f"Ghost {self.api_key}",
            "Content-Type": "application/json",
            "Accept-Version": "v5.0"
        }

    async def execute(self, title, content, status="draft"):
        post_data = {
            "posts": [{
                "title": title,
                "html": content,
                "status": status,
                "featured": False,
                "visibility": "public"
            }]
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/ghost/api/admin/posts/",
                json=post_data,
                headers=self.headers
            ) as response:
                if response.status in (200, 201):
                    data = await response.json()
                    return data
                else:
                    error_data = await response.json()
                    error_message = error_data.get('errors', [{}])[0].get('message', 'Unknown error')
                    raise Exception(f"Failed to publish to Ghost: {error_message} (Status: {response.status})") 