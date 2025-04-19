import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from services.blog_service import BlogServiceFactory
from services.wordpress_service import WordPressService
from services.ghost_service import GhostService
from config.config import Config

@pytest.fixture
def mock_config(mocker):
    config = Config()
    config.blog_platform = "ghost"  # Default platform
    config.ghost_url = "https://test.com"
    config.ghost_api_key = "test_api_key"
    config.wp_url = "https://test.com"
    config.wp_username = "test_user"
    config.wp_app_pass = "test_pass"
    mocker.patch('config.config.Config', return_value=config)
    return config

def test_blog_service_factory_create_ghost(mock_config):
    # Test Ghost service creation
    service = BlogServiceFactory.create("ghost")
    assert isinstance(service, GhostService)
    
def test_blog_service_factory_create_wordpress(mock_config):
    # Test WordPress service creation
    service = BlogServiceFactory.create("wordpress")
    assert isinstance(service, WordPressService)

def test_blog_service_factory_create_default(mock_config):
    # Test default service creation (based on config)
    service = BlogServiceFactory.create()
    assert isinstance(service, GhostService)  # Default is Ghost

def test_blog_service_factory_create_invalid(mock_config):
    # Test invalid platform
    with pytest.raises(ValueError) as exc_info:
        BlogServiceFactory.create("invalid")
    assert "Unsupported blog platform: invalid" in str(exc_info.value)

def test_blog_service_factory_create_wordpress_default(mock_config):
    # Test WordPress as default platform
    mock_config.blog_platform = "wordpress"
    service = BlogServiceFactory.create()
    assert isinstance(service, WordPressService) 