from strategies.base_strategy import BaseStrategy

class GoPostStrategy(BaseStrategy):
    def build_prompt(self, problem_data):
        title = problem_data.get('title', '')
        content = problem_data.get('content', '')
        difficulty = problem_data.get('difficulty', '')
        tags = [tag['name'] for tag in problem_data.get('topicTags', [])]

        prompt = f"""Create a detailed blog post about solving the LeetCode problem "{title}" using Go programming language.

Problem Details:
- Title: {title}
- Difficulty: {difficulty}
- Tags: {', '.join(tags)}

Problem Description:
{content}

Please write a blog post that:
1. Explains the problem in simple terms
2. Discusses the approach to solve it
3. Provides a complete Go implementation with detailed comments
4. Explains the time and space complexity
5. Includes test cases and examples
6. Provides tips and best practices for solving similar problems

Format the response in Markdown with proper headings, code blocks, and explanations."""

        return prompt 