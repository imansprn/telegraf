import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from server import app, generate_blog_post
import json

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def mock_config(mocker):
    # Set up environment variables for testing
    test_env = {
        'DEEPSEEK_API_KEY': 'test_api_key',
        'BLOG_PLATFORM': 'ghost',
        'GHOST_URL': 'https://test.ghost.com',
        'GHOST_API_KEY': 'test_ghost_key',
        'WP_USERNAME': 'test_wp_user',
        'WP_APP_PASS': 'test_wp_pass',
        'WP_URL': 'https://test.wordpress.com',
        'CRON_SCHEDULE': '00:00'
    }
    
    # Mock os.getenv to return our test values
    def mock_getenv(key, default=None):
        return test_env.get(key, default)
    
    mocker.patch('os.getenv', side_effect=mock_getenv)
    
    # Create a real Config instance that will use our mocked environment
    from config.config import Config
    Config.reset_instance()  # Reset any existing instance
    config = Config()
    return config

def test_health_check(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json == {"status": "healthy"}

def test_home_endpoint(client):
    response = client.get('/')
    assert response.status_code == 200
    assert "status" in response.json
    assert "message" in response.json
    assert "next_run" in response.json

def test_trigger_endpoint_success(client, mocker):
    mock_thread = mocker.patch('threading.Thread')
    response = client.post('/trigger')
    assert response.status_code == 200
    assert response.json["status"] == "success"
    mock_thread.assert_called_once()

def test_trigger_endpoint_error(client, mocker):
    mock_thread = mocker.patch('threading.Thread')
    mock_thread.side_effect = Exception("Test error")
    response = client.post('/trigger')
    assert response.status_code == 500
    assert response.json["status"] == "error"

@pytest.mark.asyncio
async def test_generate_blog_post_ghost(mock_config, mocker):
    # Set platform to Ghost
    mock_config.blog_platform = "ghost"
    
    # Mock all service calls
    mock_leetcode = mocker.AsyncMock()
    mock_leetcode.execute.return_value = {
        "title": "Test Problem",
        "difficulty": "MEDIUM",
        "interview_metadata": {
            "acceptance_rate": 45.5,
            "companies": ["Google"],
            "topics": ["Array"]
        }
    }
    mocker.patch('server.LeetCodeService', return_value=mock_leetcode)
    
    mock_deepseek = mocker.AsyncMock()
    mock_deepseek.execute.return_value = "Test blog content"
    mocker.patch('server.DeepSeekService', return_value=mock_deepseek)
    
    mock_ghost = mocker.AsyncMock()
    mock_ghost.execute.return_value = {"id": 123}
    mocker.patch('services.ghost_service.GhostService', return_value=mock_ghost)
    
    # Test execution
    result = await generate_blog_post()
    
    # Verify result
    assert result["id"] == 123
    mock_leetcode.execute.assert_called_once()
    mock_deepseek.execute.assert_called_once()
    mock_ghost.execute.assert_called_once()

@pytest.mark.asyncio
async def test_generate_blog_post_wordpress(mock_config, mocker):
    # Set platform to WordPress
    mock_config.blog_platform = "wordpress"
    mock_config.wp_url = "https://blog.example.com"  # Not a wordpress.com URL
    mock_config.wp_username = "test_user"
    mock_config.wp_app_pass = "test_pass"
    
    # Mock all service calls
    mock_leetcode = mocker.AsyncMock()
    mock_leetcode.execute.return_value = {
        "title": "Test Problem",
        "difficulty": "MEDIUM",
        "interview_metadata": {
            "acceptance_rate": 45.5,
            "companies": ["Google"],
            "topics": ["Array"]
        }
    }
    mocker.patch('server.LeetCodeService', return_value=mock_leetcode)
    
    mock_deepseek = mocker.AsyncMock()
    mock_deepseek.execute.return_value = "Test blog content"
    mocker.patch('server.DeepSeekService', return_value=mock_deepseek)
    
    mock_wordpress = mocker.AsyncMock()
    mock_wordpress.execute.return_value = {"id": 123}
    mocker.patch('services.wordpress_service.WordPressService', return_value=mock_wordpress)
    
    # Test execution
    result = await generate_blog_post()
    
    # Verify result
    assert result["id"] == 123
    mock_leetcode.execute.assert_called_once()
    mock_deepseek.execute.assert_called_once()
    mock_wordpress.execute.assert_called_once() 