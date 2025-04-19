from abc import ABC, abstractmethod
from services.base_service import BaseService
from config.config import Config

class BlogService(BaseService, ABC):
    """Abstract base class for blog services (WordPress, Ghost, etc.)"""
    @abstractmethod
    async def execute(self, title: str, content: str, status: str = "draft"):
        """Publish a blog post to the platform"""
        pass

class BlogServiceFactory:
    """Factory class to create the appropriate blog service"""
    @staticmethod
    def create(platform: str = None) -> BlogService:
        """Create a blog service instance based on configuration"""
        config = Config()
        
        # If platform is not specified, use the configured default
        if not platform:
            platform = config.blog_platform.lower()
        
        if platform == "wordpress":
            from services.wordpress_service import WordPressService
            return WordPressService()
        elif platform == "ghost":
            from services.ghost_service import GhostService
            return GhostService()
        else:
            raise ValueError(f"Unsupported blog platform: {platform}") 