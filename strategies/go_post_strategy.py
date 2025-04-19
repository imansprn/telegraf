from strategies.base_strategy import BaseStrategy

class GoPostStrategy(BaseStrategy):
    def build_prompt(self, problem_data):
        title = problem_data.get('title', '')
        content = problem_data.get('content', '')
        difficulty = problem_data.get('difficulty', '')
        tags = [tag['name'] for tag in problem_data.get('topicTags', [])]

        prompt = f"""Create a detailed blog post about solving the LeetCode problem "{title}" using Go programming language. Format the content in HTML for WordPress.

Problem Details:
- Title: {title}
- Difficulty: {difficulty}
- Tags: {', '.join(tags)}

Problem Description:
{content}

Please write a WordPress-formatted blog post using HTML tags. Here's the required structure:

1. Title and Meta (h1)
   <h1>Solving the LeetCode "{title}" Problem in Go</h1>
   <p class="meta">Difficulty: {difficulty} | Tags: {', '.join(tags)}</p>

2. Introduction (h2)
   <h2>Introduction</h2>
   <p>Brief problem overview and importance.</p>

3. Problem Analysis (h2)
   <h2>Problem Analysis</h2>
   <p>Detailed explanation with examples.</p>

4. Solution Approach (h2)
   <h2>Solution Approach</h2>
   <p>Step-by-step explanation with visual aids if needed.</p>

5. Go Implementation (h2)
   <h2>Go Implementation</h2>
   <pre><code class="language-go">
   // Your Go code here
   </code></pre>

6. Complexity Analysis (h2)
   <h2>Complexity Analysis</h2>
   <p>Time and space complexity explanations.</p>

7. Testing and Examples (h2)
   <h2>Testing and Examples</h2>
   <p>Test cases and edge cases.</p>

Important formatting rules:
- Use HTML tags for all formatting (no markdown)
- Wrap code in <pre><code class="language-go"> tags
- Use <h1> for title, <h2> for sections
- Use <p> for paragraphs
- Use <ul> and <li> for lists
- Use <strong> for bold text
- Use <em> for italic text
- Use <blockquote> for quotes

Do not use any markdown syntax. Use only HTML tags for formatting.

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