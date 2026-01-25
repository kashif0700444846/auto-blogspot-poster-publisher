import requests
from bs4 import BeautifulSoup
import time
import random

# Headers to mimic a real browser to avoid being blocked
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
}

def google_search(query, num_results=3):
    """
    Performs a Google search and returns a list of URLs.
    """
    # Note: scraping Google Search results directly is against TOS and can be blocked.
    # We will try to use the URLs provided by the Trends RSS first.
    # If we must search, we use a basic search URL.

    search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}&num={num_results}"
    try:
        response = requests.get(search_url, headers=HEADERS)
        if response.status_code != 200:
            print(f"Failed to search Google: {response.status_code}")
            return []

        soup = BeautifulSoup(response.text, 'html.parser')
        links = []

        # This selector is fragile and changes often.
        # Currently, look for generic search result containers.
        # usually class 'g' -> 'a' href
        for result in soup.select('.g a'):
            link = result.get('href')
            if link and link.startswith('http') and 'google.com' not in link:
                links.append(link)
                if len(links) >= num_results:
                    break
        return links
    except Exception as e:
        print(f"Error searching Google: {e}")
        return []

def extract_text_from_url(url):
    """
    Downloads the page and extracts the main text content.
    """
    try:
        # random sleep to be polite
        time.sleep(random.uniform(0.5, 1.5))

        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code != 200:
            return ""

        soup = BeautifulSoup(response.text, 'html.parser')

        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header", "aside"]):
            script.decompose()

        # Get text
        text = soup.get_text(separator=' ')

        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)

        # Simple heuristic to get the "body": take the longest contiguous text block?
        # Or just return everything (AI can filter it).
        # Returning everything is safer but noisy.
        # Let's truncate to first 5000 chars to avoid token limits if it's huge.
        return text[:10000]

    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return ""

def research_topic(topic, provided_urls=None):
    """
    Researches a topic by scraping provided URLs or searching for new ones.
    Returns a string of combined context.
    """
    urls = provided_urls if provided_urls else []

    # If no URLs provided, search
    if not urls:
        print(f"Searching for articles about: {topic}...")
        urls = google_search(topic)

    if not urls:
        return "No information found."

    combined_text = f"Research for Topic: {topic}\n\n"

    count = 0
    for url in urls:
        if count >= 3: break # Limit to 3 articles
        print(f"Reading: {url}...")
        text = extract_text_from_url(url)
        if text:
            combined_text += f"--- Source: {url} ---\n{text}\n\n"
            count += 1

    return combined_text

if __name__ == "__main__":
    # Test
    # topic = "Test Topic"
    # print(research_topic(topic))
    pass
