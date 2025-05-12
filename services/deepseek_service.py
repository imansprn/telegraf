import aiohttp
import asyncio
from typing import Optional
from services.base_service import BaseService
from config.config import Config

class DeepSeekAPIError(Exception):
    """Custom exception for DeepSeek API errors."""
    def __init__(self, status: int, message: str):
        self.status = status
        self.message = message
        super().__init__(f"DeepSeek API Error (Status {status}): {message}")

class DeepSeekService(BaseService):
    def __init__(self, max_retries: int = 3, retry_delay: float = 1.0):
        config = Config()
        self.api_key = config.deepseek_api_key
        self.api_url = "https://api.deepseek.com/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        self.max_retries = max_retries
        self.retry_delay = retry_delay

    def _clean_content(self, content: str) -> str:
        """Clean and format the content from DeepSeek response.
        
        This method performs the following cleaning steps:
        1. Removes common wrapper text prefixes
        2. Extracts content from code blocks (both HTML and non-HTML)
        3. Handles markdown formatting
        4. Cleans up whitespace and newlines
        
        Args:
            content (str): Raw content from DeepSeek response
            
        Returns:
            str: Cleaned and formatted content
        """
        if not content:
            return ""
            
        # Remove any wrapper text before HTML
        wrapper_texts = [
            'Here\'s a WordPress-formatted HTML blog post for solving the LeetCode',
            'Here\'s a WordPress-formatted HTML blog post for solving the "',
            'Here\'s a WordPress-formatted HTML blog post about',
            'Here\'s a WordPress-formatted HTML blog post',
            'Here\'s a blog post about',
            'Here\'s a blog post',
            'Here\'s the blog post',
            'Here\'s the content',
            'Here\'s the HTML',
            'Here\'s the post',
            'Here\'s the article',
            'Here\'s the solution',
            'Here\'s the implementation',
            'Here\'s the code',
            'Here\'s the explanation',
            'Here\'s the analysis',
            'Here\'s the approach',
            'Here\'s the strategy',
            'Here\'s the method',
            'Here\'s the technique',
            'Here\'s the algorithm'
        ]
        
        # Try to find and remove the wrapper text
        for text in wrapper_texts:
            if content.lower().startswith(text.lower()):
                content = content[len(text):]
                break
        
        # Handle code blocks
        if '```' in content:
            # Split by code block markers
            parts = content.split('```')
            
            # Look for HTML content first
            for i, part in enumerate(parts):
                part = part.strip()
                if part.lower().startswith('html'):
                    # Get the next part which contains the HTML content
                    if i + 1 < len(parts):
                        html_content = parts[i + 1].strip()
                        # Clean up whitespace and newlines
                        html_content = html_content.strip()
                        # Remove any trailing or leading quotes
                        html_content = html_content.strip('"\'')
                        # Clean up excessive newlines
                        lines = [line.strip() for line in html_content.splitlines() if line.strip()]
                        # If we have lines, return the first HTML-like line
                        if lines:
                            for line in lines:
                                if line.startswith('<') and line.endswith('>'):
                                    return line
                            # If no HTML-like line found, return the first line
                            return lines[0]
                        return ""
            
            # If no HTML block found, try to get content from the first code block
            if len(parts) >= 2:
                # Skip any language identifier
                code_content = parts[1].strip()
                if '\n' in code_content:
                    code_content = code_content[code_content.find('\n')+1:]
                code_content = code_content.strip()
                if code_content:
                    return code_content
        
        # Clean up whitespace and newlines
        content = content.strip()
        
        # Remove any trailing or leading quotes
        content = content.strip('"\'')
        
        # Clean up excessive newlines
        lines = [line.strip() for line in content.splitlines() if line.strip()]
        
        # Join all lines back together to preserve the full HTML content
        return "\n".join(lines)

    async def _make_api_call(self, payload: dict) -> Optional[str]:
        """Make an API call to DeepSeek with retry logic."""
        for attempt in range(self.max_retries):
            try:
                print(f"\nMaking API call (attempt {attempt + 1}/{self.max_retries})...")
                async with aiohttp.ClientSession() as session:
                    print(f"API URL: {self.api_url}")
                    async with session.post(
                        self.api_url,
                        json=payload,
                        headers=self.headers,
                        timeout=60  # Increase timeout to 60 seconds
                    ) as response:
                        print(f"Response status: {response.status}")
                        if response.status == 200:
                            data = await response.json()
                            print(f"Response data: {data}")
                            choices = data.get("choices", [])
                            if not choices:
                                return ""
                            return choices[0].get("message", {}).get("content", "")
                        elif response.status == 429:  # Rate limit
                            error_data = await response.text()
                            print(f"Rate limit hit (attempt {attempt + 1}/{self.max_retries}): {error_data}")
                            if attempt < self.max_retries - 1:
                                await asyncio.sleep(self.retry_delay * (attempt + 1))  # Exponential backoff
                                continue
                        else:
                            error_data = await response.text()
                            print(f"API Error: {error_data}")
                            raise DeepSeekAPIError(response.status, error_data)
            except aiohttp.ClientError as e:
                if attempt < self.max_retries - 1:
                    print(f"Network error (attempt {attempt + 1}/{self.max_retries}): {str(e)}")
                    await asyncio.sleep(self.retry_delay * (attempt + 1))
                    continue
                raise DeepSeekAPIError(0, f"Network error after {self.max_retries} attempts: {str(e)}")
        
        raise DeepSeekAPIError(429, f"Rate limit persisted after {self.max_retries} attempts")

    async def execute(self, prompt: str) -> str:
        """Execute the DeepSeek API call and return formatted content."""
        payload = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 2000
        }

        content = await self._make_api_call(payload)
        return self._clean_content(content)