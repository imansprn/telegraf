import aiohttp
from services.blog_service import BlogService
from config.config import Config
import jwt
import time

class GhostService(BlogService):
    def __init__(self):
        config = Config()
        self.base_url = config.ghost_url.rstrip('/')
        self.api_key = config.ghost_api_key

    async def execute(self, title, content, status="published"):
        # Validate status - must be one of: 'published', 'draft', 'scheduled', 'sent'
        valid_statuses = ['published', 'draft', 'scheduled', 'sent']
        if status not in valid_statuses:
            print(f"Warning: Invalid status '{status}'. Defaulting to 'published'.")
            status = 'published'
        # Generate a fresh JWT for every request
        id, secret = self.api_key.split(':')
        now = int(time.time())
        iat = now
        exp = now + 120  # 2 minutes after now
        print(f"[GhostService JWT Debug] iat: {iat}, exp: {exp}, now: {now}")
        header = {'alg': 'HS256', 'typ': 'JWT', 'kid': id}
        payload = {
            'iat': iat,
            'exp': exp,
            'aud': '/admin/'
        }
        # Check if secret is in hex format (for testing environments)
        try:
            secret_bytes = bytes.fromhex(secret)
        except ValueError:
            # For testing, use the secret as-is if it's not hex
            secret_bytes = secret.encode()
            
        token = jwt.encode(payload, secret_bytes, algorithm='HS256', headers=header)
        headers = {
            "Authorization": f"Ghost {token}",
            "Content-Type": "application/json",
            "Accept-Version": "v5.0"
        }

        # Create a slug from the title
        slug = title.lower().replace(' ', '-')
        # Remove special characters from slug
        import re
        slug = re.sub(r'[^a-z0-9-]', '', slug)
        
        # Create a proper mobiledoc structure with the content
        # This is a simplified approach - for complex content, a proper mobiledoc parser would be better
        import json
        
        # First, create a basic mobiledoc structure
        mobiledoc = {
            "version": "0.3.1",
            "atoms": [],
            "cards": [
                ["html", { "html": content }]  # Use the HTML card to include raw HTML
            ],
            "markups": [],
            "sections": [
                [10, 0]  # This references the HTML card defined above
            ]
        }
        
        post_data = {
            "posts": [{
                "title": title,
                "html": content,  # Include HTML for backward compatibility
                "mobiledoc": json.dumps(mobiledoc),  # Include properly formatted mobiledoc
                "status": status,
                "featured": False,
                "visibility": "public",
                "slug": slug
            }]
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/ghost/api/admin/posts/",
                json=post_data,
                headers=headers
            ) as response:
                if response.status in (200, 201):
                    data = await response.json()
                    print(f"\nGhost API Response: {data}\n")
                    return data
                else:
                    error_data = await response.json()
                    error_message = error_data.get('errors', [{}])[0].get('message', 'Unknown error')
                    print(f"Ghost API Error: {error_data}")
                    raise Exception(f"Failed to publish to Ghost: {error_message} (Status: {response.status})")