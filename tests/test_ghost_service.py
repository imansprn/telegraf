import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from services.ghost_service import GhostService
from config.config import Config

@pytest.fixture
def mock_config(mocker):
    # Create a real Config instance but mock its attributes
    config = Config()
    config.ghost_url = "https://test.com"
    config.ghost_api_key = "test_api_key"
    mocker.patch('config.config.Config', return_value=config)
    return config

@pytest.fixture
def ghost_service(mock_config):
    return GhostService()

@pytest.mark.asyncio
async def test_ghost_service_execute_success(ghost_service, mocker):
    # Mock successful post creation
    mock_response = mocker.AsyncMock()
    mock_response.status = 201
    mock_response.json.return_value = {
        "posts": [{
            "id": "123",
            "title": "Test Post",
            "url": "https://test.com/test-post",
            "status": "draft"
        }]
    }

    mock_session = mocker.MagicMock()
    mock_session.__aenter__.return_value = mock_session
    mock_session.__aexit__.return_value = None
    mock_session.post.return_value.__aenter__.return_value = mock_response
    mocker.patch('aiohttp.ClientSession', return_value=mock_session)

    # Test execution
    result = await ghost_service.execute(
        title="Test Post",
        content="Test content",
        status="draft"
    )

    # Assertions
    assert result["posts"][0]["id"] == "123"
    assert result["posts"][0]["title"] == "Test Post"
    assert result["posts"][0]["url"] == "https://test.com/test-post"
    assert result["posts"][0]["status"] == "draft"

@pytest.mark.asyncio
async def test_ghost_service_execute_error(ghost_service, mocker):
    # Mock error response
    mock_response = mocker.AsyncMock()
    mock_response.status = 400
    mock_response.json.return_value = {
        "errors": [{
            "message": "Invalid API key",
            "context": "Authentication failed"
        }]
    }

    mock_session = mocker.MagicMock()
    mock_session.__aenter__.return_value = mock_session
    mock_session.__aexit__.return_value = None
    mock_session.post.return_value.__aenter__.return_value = mock_response
    mocker.patch('aiohttp.ClientSession', return_value=mock_session)

    # Test execution with error
    with pytest.raises(Exception) as exc_info:
        await ghost_service.execute(
            title="Test Post",
            content="Test content",
            status="draft"
        )

    # Assert error message
    assert "Failed to publish to Ghost" in str(exc_info.value)
    assert "Invalid API key" in str(exc_info.value)
    assert "Status: 400" in str(exc_info.value) 