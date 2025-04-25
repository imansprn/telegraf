from strategies.base_strategy import BaseStrategy

class GoPostStrategy(BaseStrategy):
    def build_prompt(self, problem_data):
        title = problem_data.get('title', '')
        content = problem_data.get('content', '')
        difficulty = problem_data.get('difficulty', '')
        tags = [tag['name'] for tag in problem_data.get('topicTags', [])]

        prompt = f"""Create a detailed blog post about solving the LeetCode problem "{title}" using Go programming language. Return ONLY the HTML content without any wrapper text, introduction, or explanation.

Problem Details:
- Title: {title}
- Difficulty: {difficulty}
- Tags: {', '.join(tags)}

Problem Description:
{content}

Return ONLY the HTML content starting with <h1> and ending with </h2>. Do not include any wrapper text, backticks, or markdown formatting.

Required HTML structure:

<h1>Solving the LeetCode "{title}" Problem in Go</h1>
<p class="meta">Difficulty: {difficulty} | Tags: {', '.join(tags)}</p>

<h2>Introduction</h2>
<p>Brief problem overview and importance.</p>

<h2>Problem Analysis</h2>
<p>Detailed explanation with examples.</p>

<h2>Solution Approach</h2>
<p>Step-by-step explanation with visual aids if needed.</p>

<h2>Go Implementation</h2>
<pre><code class="language-go">
// Your Go code here
</code></pre>

<h2>Complexity Analysis</h2>
<p>Time and space complexity explanations.</p>

<h2>Testing and Examples</h2>
<p>Test cases and edge cases.</p>

<h2>Best Practices and Tips</h2>
<p>Key takeaways and tips.</p>

Remember:
- Return ONLY the HTML content
- Start with <h1> and end with the last </p> in Best Practices section
- No wrapper text or backticks
- No markdown formatting
- No introduction or explanation outside the HTML
- No meta description or featured image suggestions
"""
        return prompt 