import aiohttp
import random
from services.base_service import BaseService

class LeetCodeService(BaseService):
    def __init__(self):
        self.graphql_url = "https://leetcode.com/graphql"
        self.headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0"
        }

    async def execute(self):
        query = """
        query randomQuestion($categorySlug: String, $filters: QuestionListFilterInput) {
            randomQuestion(categorySlug: $categorySlug, filters: $filters) {
                title
                titleSlug
                content
                difficulty
                topicTags {
                    name
                    slug
                }
            }
        }
        """
        
        variables = {
            "categorySlug": "",
            "filters": {}
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.graphql_url,
                json={"query": query, "variables": variables},
                headers=self.headers
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("data", {}).get("randomQuestion")
                else:
                    raise Exception(f"Failed to fetch LeetCode problem: {response.status}") 