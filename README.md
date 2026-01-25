# Auto-Blogspot-Poster-Publisher

An all-in-one Blogger automation tool designed to streamline the process of creating and publishing content on Blogspot blogs. This project includes functionalities such as automatic posting, publishing, and overall blog management.

## Features

- **Trend Discovery**: Fetches top trending topics from Google Trends (Daily RSS).
- **Automated Research**: Scrapes relevant news articles and summarizes them.
- **AI Content Generation**: Uses Google Gemini AI (Free Tier) to write engaging, HTML-formatted blog posts.
- **Auto-Publishing**: Authentication via Google OAuth to post directly to your Blogger account.
- **Scheduling**: Can run in a loop to publish multiple posts per day.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/kashif0700444846/auto-blogspot-poster-publisher.git
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup Credentials**:
   - **Google API Key (for AI)**:
     - Go to [Google AI Studio](https://aistudio.google.com/app/apikey) and get a free API Key.
     - You will be prompted to enter this when you run the script (or set `GOOGLE_API_KEY` env var).
   - **Blogger Client Secret**:
     - Go to [Google Cloud Console](https://console.cloud.google.com/).
     - Create a project and enable the **Blogger API v3**.
     - Create Credentials -> OAuth Client ID (Desktop App).
     - Download the JSON file, rename it to `client_secret.json`, and place it in the project folder.

## Usage

Run the main controller:

```bash
python main.py
```

Follow the on-screen prompts to:
1. Authenticate (first time only).
2. Choose to view trends and post manually.
3. Start the auto-poster loop.

## Files

- `main.py`: The main script orchestrating the flow.
- `trends.py`: Handles fetching trending topics.
- `research.py`: Scrapes web content for context.
- `writer.py`: Generates blog posts using AI.
- `publisher.py`: Handles Blogger API interactions.
