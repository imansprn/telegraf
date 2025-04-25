import pytest
from unittest.mock import Mock, patch, AsyncMock
import aiohttp
from services.deepseek_service import DeepSeekService, DeepSeekAPIError

@pytest.fixture
def mock_config():
    with patch('services.deepseek_service.Config') as mock:
        mock.return_value.deepseek_api_key = 'test_key'
        yield mock

@pytest.fixture
def service(mock_config):
    return DeepSeekService(max_retries=2, retry_delay=0.1)

@pytest.mark.asyncio
async def test_deepseek_service_execute_success(service):
    """Test successful execution"""
    mock_response = {
        "choices": [{
            "message": {
                "content": "Test content"
            }
        }]
    }
    
    with patch('aiohttp.ClientSession.post') as mock_post:
        mock_context = AsyncMock()
        mock_context.status = 200
        mock_context.json = AsyncMock(return_value=mock_response)
        mock_post.return_value.__aenter__.return_value = mock_context
        
        result = await service.execute("Test prompt")
        assert result == "Test content"

@pytest.mark.asyncio
async def test_deepseek_service_execute_error(service):
    """Test error handling"""
    with patch('aiohttp.ClientSession.post') as mock_post:
        mock_context = AsyncMock()
        mock_context.status = 400
        mock_context.text = AsyncMock(return_value="Bad request")
        mock_post.return_value.__aenter__.return_value = mock_context
        
        with pytest.raises(DeepSeekAPIError) as exc_info:
            await service.execute("Test prompt")
        
        assert exc_info.value.status == 400
        assert "Bad request" in str(exc_info.value)

@pytest.mark.asyncio
async def test_deepseek_service_execute_empty_response(service):
    """Test empty response handling"""
    mock_response = {
        "choices": [{
            "message": {
                "content": ""
            }
        }]
    }
    
    with patch('aiohttp.ClientSession.post') as mock_post:
        mock_context = AsyncMock()
        mock_context.status = 200
        mock_context.json = AsyncMock(return_value=mock_response)
        mock_post.return_value.__aenter__.return_value = mock_context
        
        result = await service.execute("Test prompt")
        assert result == ""

@pytest.mark.asyncio
async def test_rate_limit_retry(service):
    """Test rate limit retry logic"""
    with patch('aiohttp.ClientSession.post') as mock_post:
        mock_context = AsyncMock()
        mock_context.status = 429
        mock_context.text = AsyncMock(return_value="Rate limit exceeded")
        mock_post.return_value.__aenter__.return_value = mock_context
        
        with pytest.raises(DeepSeekAPIError) as exc_info:
            await service.execute("Test prompt")
        
        assert exc_info.value.status == 429
        assert "Rate limit persisted" in str(exc_info.value)
        assert mock_post.call_count == 2

@pytest.mark.asyncio
async def test_network_error_retry(service):
    """Test network error retry logic"""
    with patch('aiohttp.ClientSession.post') as mock_post:
        mock_post.side_effect = [
            aiohttp.ClientError(),
            AsyncMock(
                __aenter__=AsyncMock(
                    return_value=AsyncMock(
                        status=200,
                        json=AsyncMock(
                            return_value={
                                "choices": [{
                                    "message": {
                                        "content": "Test content"
                                    }
                                }]
                            }
                        )
                    )
                )
            )
        ]
        
        result = await service.execute("Test prompt")
        assert result == "Test content"
        assert mock_post.call_count == 2

@pytest.mark.asyncio
async def test_persistent_error(service):
    """Test persistent error handling"""
    with patch('aiohttp.ClientSession.post') as mock_post:
        mock_post.side_effect = aiohttp.ClientError()
        
        with pytest.raises(DeepSeekAPIError) as exc_info:
            await service.execute("Test prompt")
        
        assert "Network error" in str(exc_info.value)
        assert mock_post.call_count == 2

@pytest.mark.asyncio
async def test_other_api_error(service):
    """Test other API error handling"""
    with patch('aiohttp.ClientSession.post') as mock_post:
        mock_context = AsyncMock()
        mock_context.status = 500
        mock_context.text = AsyncMock(return_value="Internal server error")
        mock_post.return_value.__aenter__.return_value = mock_context
        
        with pytest.raises(DeepSeekAPIError) as exc_info:
            await service.execute("Test prompt")
        
        assert exc_info.value.status == 500
        assert "Internal server error" in str(exc_info.value)

@pytest.mark.parametrize("input_content,expected_output", [
    (
        "Here's a blog post\nTest content",
        "Test content"
    ),
    (
        "Raw content without wrapper",
        "Raw content without wrapper"
    ),
    (
        "Here's the implementation\n```\nTest\n```",
        "Test"
    )
])
def test_content_cleaning(service, input_content, expected_output):
    """Test content cleaning with various input formats"""
    assert service._clean_content(input_content) == expected_output