import aiohttp
import random
import json
from services.base_service import BaseService

class LeetCodeService(BaseService):
    def __init__(self):
        self.graphql_url = "https://leetcode.com/graphql"
        self.headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Accept": "application/json",
            "Accept-Language": "en-US,en;q=0.9",
            "Origin": "https://leetcode.com",
            "Referer": "https://leetcode.com/problemset/all/"
        }

    async def execute(self, difficulty=None, topics=None, company_tags=None):
        query = """
        query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {
            problemsetQuestionList: questionList(
                categorySlug: $categorySlug
                limit: $limit
                skip: $skip
                filters: $filters
            ) {
                totalNum
                data {
                    title
                    titleSlug
                    content
                    difficulty
                    acRate
                    topicTags {
                        name
                        slug
                    }
                }
            }
        }
        """
        
        variables = {
            "categorySlug": "",
            "limit": 50,
            "skip": 0,
            "filters": {}
        }

        if difficulty:
            variables["filters"]["difficulty"] = difficulty.upper()
        
        if topics:
            variables["filters"]["tags"] = topics

        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.graphql_url,
                json={"query": query, "variables": variables},
                headers=self.headers
            ) as response:
                if response.status == 200:
                    response_json = await response.json()
                    problems = response_json.get("data", {}).get("problemsetQuestionList", {}).get("data", [])
                    
                    if not problems:
                        raise Exception("No problems found matching the criteria")
                    
                    # Validate problem data structure
                    for problem in problems:
                        if not all(key in problem for key in ["title", "titleSlug", "content", "difficulty", "acRate", "topicTags"]):
                            raise Exception("Invalid problem data structure received from LeetCode API")
                    
                    # Select a random problem from the filtered list
                    selected_problem = random.choice(problems)
                    
                    # Add additional interview-specific metadata
                    selected_problem["interview_metadata"] = {
                        "acceptance_rate": selected_problem.get("acRate", 0),
                        "topics": [tag["name"] for tag in selected_problem.get("topicTags", [])],
                        "companies": []  # Public API doesn't provide company tags
                    }
                    
                    return selected_problem
                else:
                    error_text = await response.text()
                    try:
                        error_json = json.loads(error_text)
                        error_message = error_json.get("errors", [{}])[0].get("message", "Unknown error")
                    except json.JSONDecodeError:
                        error_message = error_text
                    raise Exception(f"Failed to fetch LeetCode problem: {response.status}. Error: {error_message}") 