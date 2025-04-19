import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from services.wordpress_service import WordPressService
from config.config import Config

@pytest.fixture
def mock_config(mocker):
    config = mocker.Mock(spec=Config)
    config.wp_username = "test_user"
    config.wp_app_pass = "test_pass"
    config.wp_url = "https://test.com"
    mocker.patch('config.config.Config', return_value=config)
    return config

@pytest.fixture
def wordpress_service(mock_config):
    return WordPressService()

@pytest.mark.asyncio
async def test_wordpress_service_execute_success(wordpress_service, mocker):
    # Mock successful post creation
    mock_response = mocker.AsyncMock()
    mock_response.status = 201
    mock_response.json.return_value = {
        "id": 123,
        "title": {"rendered": "Test Post"},
        "link": "https://test.com/test-post"
    }

    mock_session = mocker.MagicMock()
    mock_session.__aenter__.return_value = mock_session
    mock_session.__aexit__.return_value = None
    mock_session.post.return_value.__aenter__.return_value = mock_response
    mocker.patch('aiohttp.ClientSession', return_value=mock_session)

    # Test execution
    result = await wordpress_service.execute(
        title="Test Post",
        content="Test content",
        status="draft"
    )

    # Assertions
    assert result["id"] == 123
    assert result["title"]["rendered"] == "Test Post"
    assert result["link"] == "https://test.com/test-post"

@pytest.mark.asyncio
async def test_wordpress_service_execute_error(wordpress_service, mocker):
    # Mock error response
    mock_response = mocker.AsyncMock()
    mock_response.status = 401

    mock_session = mocker.MagicMock()
    mock_session.__aenter__.return_value = mock_session
    mock_session.__aexit__.return_value = None
    mock_session.post.return_value.__aenter__.return_value = mock_response
    mocker.patch('aiohttp.ClientSession', return_value=mock_session)

    # Test execution and assertion
    with pytest.raises(Exception, match="Failed to publish to WordPress: 401"):
        await wordpress_service.execute(
            title="Test Post",
            content="Test content"
        ) 