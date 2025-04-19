import aiohttp
import random
import json
from services.base_service import BaseService

class LeetCodeService(BaseService):
    def __init__(self):
        self.graphql_url = "https://leetcode.com/graphql"
        self.headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9",
        }

    async def execute(self, difficulty=None, topics=None, company_tags=None):
        query = """
        query problemsetQuestionList {
            problemsetQuestionList: allQuestions {
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
        """
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.graphql_url,
                json={"query": query},
                headers=self.headers
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    questions = data.get("data", {}).get("problemsetQuestionList", [])
                    
                    if not questions:
                        raise Exception("No problems found matching the criteria")
                    
                    # Filter questions based on parameters
                    filtered_questions = questions
                    
                    if difficulty:
                        filtered_questions = [q for q in filtered_questions 
                                           if q["difficulty"].lower() == difficulty.lower()]
                    
                    if topics:
                        filtered_questions = [q for q in filtered_questions 
                                           if any(tag["name"].lower() in [t.lower() for t in topics] 
                                                for tag in q["topicTags"])]
                    
                    if not filtered_questions:
                        raise Exception("No problems found matching the criteria after filtering")
                    
                    # Select a random problem from the filtered list
                    selected_problem = random.choice(filtered_questions)
                    
                    # Add additional interview-specific metadata
                    selected_problem["interview_metadata"] = {
                        "acceptance_rate": selected_problem.get("acRate", 0),
                        "topics": [tag["name"] for tag in selected_problem.get("topicTags", [])],
                        "companies": []  # Public API doesn't provide company tags
                    }
                    
                    return selected_problem
                else:
                    raise Exception(f"Failed to fetch LeetCode problem: {response.status}") 