import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from services.deepseek_service import DeepSeekService
from config.config import Config

@pytest.fixture
def mock_config(mocker):
    config = Config()
    config.deepseek_api_key = "test_api_key"
    mocker.patch('config.config.Config', return_value=config)
    return config

@pytest.fixture
def deepseek_service(mock_config):
    return DeepSeekService()

@pytest.mark.asyncio
async def test_deepseek_service_execute_success(deepseek_service, mocker):
    # Mock successful API response
    mock_response = mocker.AsyncMock()
    mock_response.status = 200
    mock_response.json.return_value = {
        "choices": [{
            "message": {
                "content": "Generated blog post content"
            }
        }]
    }

    mock_session = mocker.MagicMock()
    mock_session.__aenter__.return_value = mock_session
    mock_session.__aexit__.return_value = None
    mock_session.post.return_value.__aenter__.return_value = mock_response
    mocker.patch('aiohttp.ClientSession', return_value=mock_session)

    # Test execution
    result = await deepseek_service.execute("Test prompt")

    # Assertions
    assert result == "Generated blog post content"
    mock_session.post.assert_called_once_with(
        "https://api.deepseek.com/v1/chat/completions",
        json={
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": "Test prompt"}],
            "temperature": 0.7,
            "max_tokens": 2000
        },
        headers={
            "Authorization": "Bearer test_api_key",
            "Content-Type": "application/json"
        }
    )

@pytest.mark.asyncio
async def test_deepseek_service_execute_error(deepseek_service, mocker):
    # Mock error response
    mock_response = mocker.AsyncMock()
    mock_response.status = 400

    mock_session = mocker.MagicMock()
    mock_session.__aenter__.return_value = mock_session
    mock_session.__aexit__.return_value = None
    mock_session.post.return_value.__aenter__.return_value = mock_response
    mocker.patch('aiohttp.ClientSession', return_value=mock_session)

    # Test execution with error
    with pytest.raises(Exception) as exc_info:
        await deepseek_service.execute("Test prompt")

    # Assert error message
    assert "Failed to generate content with DeepSeek: 400" in str(exc_info.value)

@pytest.mark.asyncio
async def test_deepseek_service_execute_empty_response(deepseek_service, mocker):
    # Mock empty response
    mock_response = mocker.AsyncMock()
    mock_response.status = 200
    mock_response.json.return_value = {}

    mock_session = mocker.MagicMock()
    mock_session.__aenter__.return_value = mock_session
    mock_session.__aexit__.return_value = None
    mock_session.post.return_value.__aenter__.return_value = mock_response
    mocker.patch('aiohttp.ClientSession', return_value=mock_session)

    # Test execution
    result = await deepseek_service.execute("Test prompt")

    # Assert empty response handling
    assert result == "" 