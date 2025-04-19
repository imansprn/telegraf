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

def test_health_check(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json == {"status": "healthy"}

def test_home_endpoint(client):
    response = client.get('/')
    assert response.status_code == 200
    data = response.json
    assert data["status"] == "running"
    assert "message" in data
    assert "next_run" in data

def test_trigger_endpoint_success(client, mocker):
    # Mock the async blog generation
    mock_generate = mocker.patch('server.run_async_task')
    
    response = client.post('/trigger')
    assert response.status_code == 200
    assert response.json["status"] == "success"
    assert response.json["message"] == "Blog generation started"
    mock_generate.assert_called_once()

def test_trigger_endpoint_error(client, mocker):
    # Mock an error in blog generation
    mock_generate = mocker.patch('server.run_async_task', side_effect=Exception("Test error"))
    
    response = client.post('/trigger')
    assert response.status_code == 500
    assert response.json["status"] == "error"
    assert "Test error" in response.json["message"]

@pytest.mark.asyncio
async def test_generate_blog_post(mocker):
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
    mocker.patch('server.WordPressService', return_value=mock_wordpress)

    # Test execution
    result = await generate_blog_post(
        difficulty="medium",
        topics=["array"],
        companies=["google"]
    )

    # Assertions
    assert result["id"] == 123
    mock_leetcode.execute.assert_called_once()
    mock_deepseek.execute.assert_called_once()
    mock_wordpress.execute.assert_called_once() 