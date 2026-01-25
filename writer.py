import google.generativeai as genai
import os

def configure_ai(api_key=None):
    """
    Configures the Google Gemini AI with the provided API Key.
    """
    if not api_key:
        api_key = os.environ.get('GOOGLE_API_KEY')

    if not api_key:
        raise ValueError("Google API Key is required. Please set GOOGLE_API_KEY environment variable or pass it to the function.")

    genai.configure(api_key=api_key)

def write_blog_post(topic, research_context):
    """
    Generates a blog post title and content using Gemini.

    Returns:
        tuple: (title, html_content)
    """
    model = genai.GenerativeModel('gemini-pro')

    prompt = f"""
    You are an expert news blogger and journalist. Your task is to write a high-quality, engaging blog post about the following topic based on the provided research.

    TOPIC: {topic}

    RESEARCH CONTEXT:
    {research_context}

    INSTRUCTIONS:
    1. Write a catchy, click-worthy Headline (Title).
    2. Write the body of the post in clean HTML format (use <p>, <h2>, <ul>, etc.). Do not include <html> or <body> tags, just the content.
    3. The tone should be professional yet accessible and engaging.
    4. Synthesize the information from the research context. Do not make up facts not present in the context (unless it's general knowledge).
    5. At the end, include a "Conclusion" or "Takeaway" section.

    OUTPUT FORMAT:
    Please output the response in this exact format:

    TITLE: [Your Title Here]
    CONTENT:
    [Your HTML Content Here]
    """

    try:
        response = model.generate_content(prompt)
        text = response.text

        # Parse the output
        title = "Untitled Post"
        content = text

        if "TITLE:" in text and "CONTENT:" in text:
            parts = text.split("CONTENT:")
            title_part = parts[0].replace("TITLE:", "").strip()
            content_part = parts[1].strip()

            title = title_part
            content = content_part

        # Clean up markdown code blocks if Gemini added them
        content = content.replace("```html", "").replace("```", "")

        return title, content

    except Exception as e:
        print(f"Error generating content: {e}")
        return None, None

if __name__ == "__main__":
    # Test (will fail without key)
    try:
        configure_ai("TEST_KEY")
        # print(write_blog_post("Test", "Context"))
    except Exception as e:
        print(e)
