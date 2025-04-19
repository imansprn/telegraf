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

    async def execute(self, difficulty=None, topics=None, company_tags=None):
        query = """
        query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {
            problemsetQuestionList(
                categorySlug: $categorySlug
                limit: $limit
                skip: $skip
                filters: $filters
            ) {
                total
                questions {
                    title
                    titleSlug
                    content
                    difficulty
                    frequency
                    acRate
                    topicTags {
                        name
                        slug
                    }
                    companyTags {
                        name
                        slug
                    }
                    isPaidOnly
                }
            }
        }
        """
        
        # Default filters for interview preparation
        filters = {
            "status": "AC",  # Only accepted problems
            "listId": "wpwgkgt",  # Top Interview Questions list
            "premiumOnly": False,  # Exclude premium problems
        }

        # Add difficulty filter if specified
        if difficulty and difficulty.lower() in ['easy', 'medium', 'hard']:
            filters["difficulty"] = difficulty.upper()

        # Add topic filters if specified
        if topics:
            filters["tags"] = topics

        # Add company tags if specified
        if company_tags:
            filters["companyTags"] = company_tags

        variables = {
            "categorySlug": "",
            "limit": 50,  # Fetch 50 problems to choose from
            "skip": 0,
            "filters": filters
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.graphql_url,
                json={"query": query, "variables": variables},
                headers=self.headers
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    questions = data.get("data", {}).get("problemsetQuestionList", {}).get("questions", [])
                    
                    if not questions:
                        raise Exception("No problems found matching the criteria")
                    
                    # Select a random problem from the filtered list
                    selected_problem = random.choice(questions)
                    
                    # Add additional interview-specific metadata
                    selected_problem["interview_metadata"] = {
                        "frequency": selected_problem.get("frequency", 0),
                        "acceptance_rate": selected_problem.get("acRate", 0),
                        "companies": [tag["name"] for tag in selected_problem.get("companyTags", [])],
                        "topics": [tag["name"] for tag in selected_problem.get("topicTags", [])]
                    }
                    
                    return selected_problem
                else:
                    raise Exception(f"Failed to fetch LeetCode problem: {response.status}") 