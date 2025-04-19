import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from services.leetcode_service import LeetCodeService

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
                "total": 1,
                "questions": [{
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
    assert result["interview_metadata"]["acceptance_rate"] == 45.5
    assert result["interview_metadata"]["topics"] == ["Array"]

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