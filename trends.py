import feedparser

def get_trending_topics(geo='US'):
    """
    Fetches trending topics from Google Trends RSS feed.

    Args:
        geo (str): The country code (e.g., 'US', 'GB', 'IN').

    Returns:
        list: A list of dictionaries containing topic details.
              Each dictionary has 'title', 'link', 'traffic', 'news_items'.
    """
    # Updated URL that works as of 2025
    rss_url = f'https://trends.google.com/trending/rss?geo={geo}'
    feed = feedparser.parse(rss_url)

    trends = []

    if feed.bozo:
        print(f"Error parsing feed: {feed.bozo_exception}")
        # Sometimes feedparser reports bozo for minor XML errors but still parses content.
        if not feed.entries:
            return []

    for entry in feed.entries:
        topic_data = {
            'title': entry.title,
            'link': entry.link,
            'pubDate': getattr(entry, 'published', 'N/A'),
            'traffic': getattr(entry, 'ht_approx_traffic', 'N/A'),
            'news_items': []
        }

        # feedparser puts repeated elements like <ht:news_item> into a specific list if defined,
        # or we might need to look at 'ht_news_item' (singular) if it only captures the first one
        # or 'ht_news_item_title' etc.

        # In recent feedparser versions with this feed:
        # entry.ht_news_item might be a list of dictionaries if multiple exist.

        # Let's try to extract news items safely.
        # Often 'ht_news_item' is the list.
        news_items = getattr(entry, 'ht_news_item', [])

        # If it's a single item (dict) instead of list, wrap it
        if isinstance(news_items, dict):
            news_items = [news_items]

        for item in news_items:
            # item is a dictionary-like object (FeedParserDict)
            # The keys inside might be 'ht_news_item_title', 'ht_news_item_url', etc.
            # OR simple 'title', 'url' depending on how feedparser flattened it.
            # Based on standard feedparser behavior for namespaced elements:

            title = item.get('ht_news_item_title') or item.get('title')
            url = item.get('ht_news_item_url') or item.get('url')
            source = item.get('ht_news_item_source') or item.get('source')

            if title and url:
                topic_data['news_items'].append({
                    'title': title,
                    'url': url,
                    'source': source
                })

        # Fallback: sometimes feedparser maps flattened attributes to the entry itself
        # if the structure is simple or if it only captured the first one.
        if not topic_data['news_items']:
            # Check for flattened attributes like 'ht_news_item_title'
            title = getattr(entry, 'ht_news_item_title', None)
            url = getattr(entry, 'ht_news_item_url', None)
            if title and url:
                topic_data['news_items'].append({
                    'title': title,
                    'url': url,
                    'source': getattr(entry, 'ht_news_item_source', None)
                })

        trends.append(topic_data)

    return trends

if __name__ == "__main__":
    # Test the function
    topics = get_trending_topics()
    print(f"Found {len(topics)} trending topics.")
    for i, t in enumerate(topics[:5], 1):
        print(f"{i}. {t['title']} ({t['traffic']})")
        for news in t['news_items'][:2]:
            print(f"   - {news['title']} ({news['source']})")
