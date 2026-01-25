import os
import time
import sys
from getpass import getpass

# Import our modules
import trends
import research
import writer
import publisher

def setup_environment():
    """
    Checks for necessary keys and files.
    """
    print("=== Auto Blogspot Poster Setup ===")

    # 1. Google Gemini API Key
    api_key = os.environ.get('GOOGLE_API_KEY')
    if not api_key:
        print("\n[AI Setup] Google API Key not found in environment.")
        print("You can get a free key from: https://aistudio.google.com/app/apikey")
        api_key = getpass("Enter your Google API Key: ").strip()
        if api_key:
            os.environ['GOOGLE_API_KEY'] = api_key
            # Ideally save this to a .env file or config, but for now memory is fine

    try:
        writer.configure_ai(api_key)
        print("✅ AI Configured.")
    except Exception as e:
        print(f"❌ AI Configuration Failed: {e}")
        return False

    # 2. Blogger Client Secret
    if not os.path.exists('client_secret.json'):
        print("\n[Blogger Setup] 'client_secret.json' not found.")
        print("Please download your OAuth Client Secret JSON from Google Cloud Console")
        print("and save it as 'client_secret.json' in this folder.")
        # Check if user wants to wait or exit
        resp = input("Have you placed the file? (y/n): ")
        if resp.lower() != 'y':
            return False

    # 3. Authenticate Blogger
    print("\n[Blogger Setup] Authenticating...")
    creds = publisher.get_credentials()
    if not creds:
        print("❌ Blogger Authentication Failed.")
        return False
    print("✅ Blogger Authenticated.")

    return True

def run_post_cycle(topic_data=None):
    """
    Runs a single cycle of Research -> Write -> Post.
    If topic_data is None, it picks a fresh trending topic.
    """
    try:
        if not topic_data:
            # Fetch fresh trends
            print("\nFetching fresh trends...")
            current_trends = trends.get_trending_topics()
            if not current_trends:
                print("No trends found.")
                return
            topic_data = current_trends[0] # Pick the top one

        topic_title = topic_data['title']
        print(f"\n🚀 Starting cycle for topic: {topic_title}")

        # Research
        print("🔍 Researching...")
        # Collect URLs if available
        urls = [item['url'] for item in topic_data.get('news_items', [])]
        context = research.research_topic(topic_title, urls)

        if not context or "No information found" in context:
            print("⚠️ Not enough info found. Skipping.")
            return

        # Write
        print("✍️ Writing content...")
        title, content = writer.write_blog_post(topic_title, context)

        if not title or not content:
            print("❌ AI failed to generate content.")
            return

        print(f"✅ Content generated: {title}")

        # Publish
        print("Cc Publishing to Blogger...")
        success = publisher.publish_post(title, content)

        if success:
            print("🎉 Post published successfully!")
        else:
            print("❌ Publishing failed.")

    except Exception as e:
        print(f"Error in post cycle: {e}")

def main():
    if not setup_environment():
        print("Exiting setup.")
        return

    # First Run Test
    print("\n=== First Run Verification ===")
    test = input("Do you want to run a Test Post now? (y/n): ")
    if test.lower() == 'y':
        print("Creating a test post...")
        publisher.publish_post("Test Post from Auto-Poster", "<p>This is a test post to verify automation.</p>", is_draft=True)
        print("Test post created (as Draft if possible, or published).")

    # Main Mode
    while True:
        print("\n=== Main Menu ===")
        print("1. View Trending Topics & Post One")
        print("2. Start Auto-Poster (Schedule)")
        print("3. Exit")

        choice = input("Select an option: ")

        if choice == '1':
            topic_list = trends.get_trending_topics()
            print("\nTop Trending Topics:")
            for i, t in enumerate(topic_list[:10], 1):
                print(f"{i}. {t['title']} ({t['traffic']})")

            sel = input("\nEnter number to post (or 0 to cancel): ")
            try:
                idx = int(sel) - 1
                if 0 <= idx < len(topic_list):
                    run_post_cycle(topic_list[idx])
                elif idx == -1:
                    pass
                else:
                    print("Invalid number.")
            except ValueError:
                print("Invalid input.")

        elif choice == '2':
            try:
                count = int(input("How many posts do you want to publish today? "))
                print(f"Scheduling {count} posts for today...")

                # Calculate interval
                # Assuming "today" means next 12 hours or 24 hours?
                # Let's simple loop: publish one now, then sleep appropriately.
                # Or use 'schedule' library to space them out.

                # For simplicity in this session:
                if count > 0:
                    print("Starting loop. Press Ctrl+C to stop.")

                    # Get all trends once or fetch fresh each time?
                    # Fetching fresh is better.

                    for i in range(count):
                        print(f"\n--- Processing Post {i+1}/{count} ---")

                        # Fetch trends
                        all_trends = trends.get_trending_topics()
                        # Pick the i-th trend to avoid duplicates if possible,
                        # or pick random?
                        # Using i-th trend from the list might work if list is long enough.
                        if i < len(all_trends):
                            target_trend = all_trends[i]
                            run_post_cycle(target_trend)
                        else:
                            print("⚠️ No more unique trending topics available for this batch.")
                            break

                        if i < count - 1:
                            wait_min = 60 # wait 1 hour between posts?
                            # User might want faster.
                            print(f"Waiting 10 minutes before next post...")
                            time.sleep(600)

                print("Batch complete.")

            except ValueError:
                print("Invalid number.")

        elif choice == '3':
            sys.exit()

if __name__ == "__main__":
    main()
