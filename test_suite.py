import unittest
from unittest.mock import MagicMock, patch
import trends
import research
import writer
import publisher

class TestAutoPoster(unittest.TestCase):

    def test_trends_fetching(self):
        # Mock feedparser
        with patch('trends.feedparser.parse') as mock_parse:
            mock_entry = MagicMock()
            mock_entry.title = "Test Trend"
            mock_entry.link = "http://test.com"
            mock_entry.ht_news_item = [{'ht_news_item_title': 'News', 'ht_news_item_url': 'http://news.com'}]

            mock_parse.return_value.entries = [mock_entry]

            topics = trends.get_trending_topics()
            self.assertEqual(len(topics), 1)
            self.assertEqual(topics[0]['title'], "Test Trend")

    def test_research_scraping(self):
        with patch('research.requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.text = "<html><body><p>Test content.</p></body></html>"

            text = research.extract_text_from_url("http://test.com")
            self.assertIn("Test content", text)

    def test_writer_config(self):
        # Test that it raises error without key
        with self.assertRaises(ValueError):
            writer.configure_ai(api_key=None)

if __name__ == '__main__':
    # Set dummy env key for other tests if needed
    # os.environ['GOOGLE_API_KEY'] = 'TEST'
    unittest.main()
