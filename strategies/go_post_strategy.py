from strategies.base_strategy import BaseStrategy

class GoPostStrategy(BaseStrategy):
    def build_prompt(self, problem_data):
        title = problem_data.get('title', '')
        content = problem_data.get('content', '')
        difficulty = problem_data.get('difficulty', '')
        tags = [tag['name'] for tag in problem_data.get('topicTags', [])]

        prompt = f"""Create a detailed blog post about solving the LeetCode problem "{title}" using Go programming language. Format the content for WordPress with proper HTML tags and structure.

Problem Details:
- Title: {title}
- Difficulty: {difficulty}
- Tags: {', '.join(tags)}

Problem Description:
{content}

Please write a WordPress-formatted blog post that includes:

1. Introduction (h2)
   - Brief problem overview
   - Why this problem is interesting/important

2. Problem Analysis (h2)
   - Detailed explanation of the problem
   - Key constraints and requirements
   - Example scenarios

3. Solution Approach (h2)
   - Step-by-step explanation of the solution
   - Algorithm design decisions
   - Visual explanation if helpful

4. Go Implementation (h2)
   - Complete Go code with syntax highlighting
   - Detailed comments explaining each part
   - Use <pre><code class="language-go"> for code blocks

5. Complexity Analysis (h2)
   - Time complexity explanation
   - Space complexity explanation
   - Performance considerations

6. Testing and Examples (h2)
   - Test cases with expected outputs
   - Edge cases to consider
   - Example walkthroughs

7. Best Practices and Tips (h2)
   - Key takeaways
   - Common pitfalls to avoid
   - Tips for similar problems

Formatting Requirements:
- Use proper HTML tags for headings (<h2>, <h3>)
- Use <p> tags for paragraphs
- Use <ul> and <li> for lists
- Use <pre><code class="language-go"> for code blocks
- Use <strong> for important terms
- Include proper spacing between sections
- Add relevant WordPress categories and tags
- Include a featured image suggestion
- Add meta description for SEO

Make the content engaging and easy to read while maintaining technical accuracy."""

        return prompt 