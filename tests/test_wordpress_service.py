import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from services.wordpress_service import WordPressService
from config.config import Config

@pytest.fixture
def mock_config():
    with patch('services.wordpress_service.Config') as mock:
        mock.return_value.wp_url = "https://example.com"
        mock.return_value.wp_username = "test_user"
        mock.return_value.wp_app_pass = "test_pass"
        yield mock

@pytest.fixture
def wordpress_service(mock_config):
    return WordPressService()

@pytest.mark.asyncio
async def test_successful_post_creation(wordpress_service):
    mock_response = AsyncMock()
    mock_response.status = 201
    mock_response.json = AsyncMock(return_value={
        "id": 123,
        "title": "Test Post",
        "content": "Test Content",
        "status": "draft"
    })

    with patch('aiohttp.ClientSession.post') as mock_post:
        mock_post.return_value.__aenter__.return_value = mock_response
        
        result = await wordpress_service.execute(
            title="Test Post",
            content="Test Content",
            status="draft"
        )
        
        assert result["id"] == 123
        assert result["title"] == "Test Post"
        assert result["content"] == "Test Content"
        assert result["status"] == "draft"

@pytest.mark.asyncio
async def test_failed_post_creation(wordpress_service):
    mock_response = AsyncMock()
    mock_response.status = 400
    mock_response.json = AsyncMock(return_value={
        "message": "Invalid post data"
    })

    with patch('aiohttp.ClientSession.post') as mock_post:
        mock_post.return_value.__aenter__.return_value = mock_response
        
        with pytest.raises(Exception) as exc_info:
            await wordpress_service.execute(
                title="Test Post",
                content="Test Content"
            )
        
        assert "Failed to publish to WordPress" in str(exc_info.value)
        assert "Status: 400" in str(exc_info.value)

def test_service_initialization(mock_config):
    service = WordPressService()
    
    assert service.base_url == "https://example.com"
    assert "Authorization" in service.headers
    assert "Content-Type" in service.headers
    assert service.headers["Content-Type"] == "application/json"

@pytest.mark.asyncio
async def test_network_error_handling(wordpress_service):
    with patch('aiohttp.ClientSession.post') as mock_post:
        mock_post.side_effect = Exception("Network error")
        
        with pytest.raises(Exception) as exc_info:
            await wordpress_service.execute(
                title="Test Post",
                content="Test Content"
            )
        
        assert "Network error" in str(exc_info.value) 