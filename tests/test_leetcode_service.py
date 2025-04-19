import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from services.leetcode_service import LeetCodeService
from unittest.mock import AsyncMock

@pytest.fixture
def leetcode_service():
    return LeetCodeService()

@pytest.mark.asyncio
async def test_leetcode_service_execute_success(leetcode_service, mocker):
    # Mock the aiohttp ClientSession
    mock_response = mocker.AsyncMock()
    mock_response.status = 200
    mock_response.json.return_value = {
        "data": {
            "problemsetQuestionList": {
                "data": [{
                    "title": "Test Problem",
                    "titleSlug": "test-problem",
                    "content": "Test content",
                    "difficulty": "MEDIUM",
                    "acRate": 45.5,
                    "topicTags": [{"name": "Array", "slug": "array"}]
                }]
            }
        }
    }

    mock_session = mocker.MagicMock()
    mock_session.__aenter__.return_value = mock_session
    mock_session.__aexit__.return_value = None
    mock_session.post.return_value.__aenter__.return_value = mock_response
    mocker.patch('aiohttp.ClientSession', return_value=mock_session)

    # Test execution
    result = await leetcode_service.execute(
        difficulty="medium",
        topics=["array"]
    )

    # Assertions
    assert result["title"] == "Test Problem"
    assert result["difficulty"] == "MEDIUM"
    assert "interview_metadata" in result
    assert result["interview_metadata"]["acceptance_rate"] == 45.5
    assert "Array" in result["interview_metadata"]["topics"]

@pytest.mark.asyncio
async def test_leetcode_service_execute_no_problems(leetcode_service, mocker):
    # Mock empty response
    mock_response = mocker.AsyncMock()
    mock_response.status = 200
    mock_response.json.return_value = {
        "data": {
            "problemsetQuestionList": {
                "total": 0,
                "questions": []
            }
        }
    }

    mock_session = mocker.MagicMock()
    mock_session.__aenter__.return_value = mock_session
    mock_session.__aexit__.return_value = None
    mock_session.post.return_value.__aenter__.return_value = mock_response
    mocker.patch('aiohttp.ClientSession', return_value=mock_session)

    # Test execution and assertion
    with pytest.raises(Exception, match="No problems found matching the criteria"):
        await leetcode_service.execute()

@pytest.mark.asyncio
async def test_leetcode_service_execute_api_error(leetcode_service, mocker):
    # Mock error response
    mock_response = mocker.AsyncMock()
    mock_response.status = 400
    mock_response.text = mocker.AsyncMock(return_value="Bad Request")

    mock_session = mocker.MagicMock()
    mock_session.__aenter__.return_value = mock_session
    mock_session.__aexit__.return_value = None
    mock_session.post.return_value.__aenter__.return_value = mock_response
    mocker.patch('aiohttp.ClientSession', return_value=mock_session)

    # Test execution and assertion
    with pytest.raises(Exception, match="Failed to fetch LeetCode problem: 400"):
        await leetcode_service.execute()

@pytest.mark.asyncio
async def test_leetcode_service_execute_invalid_data_structure(leetcode_service, mocker):
    # Mock response with invalid problem data structure
    mock_response = mocker.AsyncMock()
    mock_response.status = 200
    mock_response.json.return_value = {
        "data": {
            "problemsetQuestionList": {
                "data": [
                    {
                        "title": "Test Problem",
                        "titleSlug": "test-problem",
                        # Missing required fields: content, difficulty, acRate, topicTags
                    }
                ]
            }
        }
    }
    
    mock_session = mocker.MagicMock()
    mock_session.__aenter__.return_value = mock_session
    mock_session.__aexit__.return_value = None
    mock_session.post.return_value.__aenter__.return_value = mock_response
    mocker.patch('aiohttp.ClientSession', return_value=mock_session)

    with pytest.raises(Exception) as exc_info:
        await leetcode_service.execute()
    
    assert "Invalid problem data structure received from LeetCode API" in str(exc_info.value) 