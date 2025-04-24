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

@pytest.mark.asyncio
async def test_deepseek_service_clean_html_content(deepseek_service, mocker):
    # Mock response with wrapper text and HTML
    mock_response = mocker.AsyncMock()
    mock_response.status = 200
    mock_response.json.return_value = {
        "choices": [{
            "message": {
                "content": """Here's a blog post about the problem
```html
Testing
```"""
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
    assert result == "Testing"

@pytest.mark.asyncio
async def test_deepseek_service_leetcode_content(deepseek_service, mocker):
    # Mock response with the LeetCode problem content
    mock_response = mocker.AsyncMock()
    mock_response.status = 200
    mock_response.json.return_value = {
        "choices": [{
            "message": {
                "content": """Here's a blog post about the problem
```html
<h1>Solving the LeetCode "Search in Rotated Sorted Array II" Problem in Go</h1>
<p class="meta">Difficulty: Medium | Tags: Array, Binary Search</p>

<h2>Introduction</h2>
<p>The "Search in Rotated Sorted Array II" problem is an interesting variation of the classic binary search problem that introduces additional complexity due to potential duplicate elements in the array. This problem tests your ability to adapt standard algorithms to handle edge cases and non-ideal data conditions.</p>

<p>What makes this problem particularly valuable is that it mimics real-world scenarios where data isn't perfectly clean or sorted, requiring robust search algorithms that can handle such imperfections. The solution demonstrates how to modify binary search for rotated arrays with duplicates, a skill that's applicable in many practical software engineering situations.</p>

<h2>Problem Analysis</h2>
<p>The problem presents us with a rotated sorted array that may contain duplicate elements. Our task is to determine whether a given target value exists in this array. The key challenges are:</p>

<ul>
    <li>The array was originally sorted in non-decreasing order but has been rotated at an unknown pivot point</li>
    <li>The array may contain duplicate elements, which complicates the search process</li>
    <li>We need to implement an efficient solution with optimal time complexity</li>
</ul>

<p>Consider these examples:</p>

<p>Example 1:<br>
Input: nums = [2,5,6,0,0,1,2], target = 0<br>
Output: true</p>

<p>Example 2:<br>
Input: nums = [2,5,6,0,0,1,2], target = 3<br>
Output: false</p>

<p>The main difference from the standard rotated sorted array problem is the presence of duplicates, which means we can't always determine which half of the array is sorted by simply comparing the middle element with the endpoints.</p>

<h2>Solution Approach</h2>
<p>Our solution uses a modified binary search approach to handle the rotation and duplicates. Here's the step-by-step strategy:</p>

<ol>
    <li>Initialize two pointers (left and right) at the start and end of the array</li>
    <li>While left ≤ right:
        <ul>
            <li>Calculate the middle index</li>
            <li>If the middle element equals the target, return true</li>
            <li>Handle the case where nums[left] == nums[middle] == nums[right] by incrementing left and decrementing right</li>
            <li>Determine which half of the array is properly sorted:
                <ul>
                    <li>If the left half is sorted, check if the target lies within this range</li>
                    <li>Otherwise, check the right half</li>
                </ul>
            </li>
        </ul>
    </li>
    <li>If the loop completes without finding the target, return false</li>
</ol>

<p>The key insight is that even with duplicates, at least one half of the array (left or right of the middle) will always be sorted, allowing us to eliminate that portion if the target doesn't fall within its range.</p>

<h2>Go Implementation</h2>
<pre><code class="language-go">
func search(nums []int, target int) bool {
    left, right := 0, len(nums)-1
    
    for left <= right {
        mid := left + (right-left)/2
        
        // Found the target
        if nums[mid] == target {
            return true
        }
        
        // Handle duplicates: when we can't determine which side is sorted
        if nums[left] == nums[mid] && nums[mid] == nums[right] {
            left++
            right--
            continue
        }
        
        // Check if left side is sorted
        if nums[left] <= nums[mid] {
            if nums[left] <= target && target < nums[mid] {
                right = mid - 1
            } else {
                left = mid + 1
            }
        } else { // Right side is sorted
            if nums[mid] < target && target <= nums[right] {
                left = mid + 1
            } else {
                right = mid - 1
            }
        }
    }
    
    return false
}
</code></pre>

<p>The code handles the edge case where nums[left], nums[mid], and nums[right] are all equal by incrementing left and decrementing right, effectively skipping these duplicates. This ensures we don't get stuck in an infinite loop when many duplicates are present.</p>

<h2>Complexity Analysis</h2>
<p>The time and space complexity of this solution are:</p>

<ul>
    <li>Time Complexity: O(n) in the worst case when all elements are duplicates and we need to check each element. In the average case, it's O(log n) like standard binary search.</li>
    <li>Space Complexity: O(1) as we're using constant extra space regardless of input size.</li>
</ul>

<p>The presence of duplicates affects the worst-case runtime because we might need to perform linear scans when we can't determine which half of the array is sorted. However, in practice, the algorithm performs much better than linear search for most cases.</p>

<h2>Testing and Examples</h2>
<p>Let's examine how the algorithm works with some test cases:</p>

<pre><code class="language-go">
// Test Case 1: Target exists in the array
nums := []int{2,5,6,0,0,1,2}
target := 0
// Output: true

// Test Case 2: Target doesn't exist
nums := []int{2,5,6,0,0,1,2}
target := 3
// Output: false

// Test Case 3: All elements same
nums := []int{1,1,1,1,1,1,1}
target := 1
// Output: true

// Test Case 4: All elements same but target different
nums := []int{1,1,1,1,1,1,1}
target := 2
// Output: false
</code></pre>

<p>Edge cases to consider:</p>

<ul>
    <li>Array with all identical elements</li>
    <li>Target at the first or last position</li>
    <li>Empty array (though constraints say length ≥ 1)</li>
    <li>Array with only two elements</li>
</ul>

<h2>Best Practices and Tips</h2>
<p>When solving similar rotated array problems:</p>

<ul>
    <li>Always consider duplicates: The presence of duplicates is what makes this problem different from the standard version.</li>
    <li>Visualize the array: Drawing the array can help identify the sorted portions and rotation point.</li>
    <li>Test edge cases: Pay special attention to cases with many duplicates or small arrays.</li>
    <li>Optimize carefully: While the worst case is O(n), the average case is still O(log n), which is acceptable for most scenarios.</li>
</ul>

<p>For similar problems, remember that binary search can often be adapted to handle special conditions like rotation or duplicates by adding additional checks and fallback conditions.</p>

<p>Featured Image Suggestion: A visual representation of a rotated sorted array with some duplicate elements highlighted, showing the binary search process.</p>

<p>Meta Description: Learn how to solve the LeetCode "Search in Rotated Sorted Array II" problem in Go with a modified binary search approach that handles duplicates efficiently. Complete with code implementation and complexity analysis.</p>
```"""
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
    assert result.startswith('<h1>')
    assert 'Solving the LeetCode "Search in Rotated Sorted Array II" Problem in Go' in result
    assert result.endswith('</p>') 