import feedparser
from html import escape, unescape

# URL RSS feed Medium
FEED_URL = "https://medium.com/feed/@dikaelsaputra"

def fetch_medium_post_summary(feed_url, post_link):
    feed = feedparser.parse(feed_url)
    
    for entry in feed.entries:
        if entry.link == post_link:
            summary = entry.summary
            return summary

    return "Summary not found."

def update_readme(summary):
    # Unescape HTML entities in the summary
    summary = unescape(summary)

    # Read the existing README content
    with open('pertemuan-3/README.md', 'r', encoding='utf-8') as f:
        readme_content = f.readlines()

    # Find the section to update
    start_marker = "<!--START_SECTION:medium-->"
    end_marker = "<!--END_SECTION:medium-->"
    start_idx = None
    end_idx = None

    for idx, line in enumerate(readme_content):
        if start_marker in line:
            start_idx = idx
        if end_marker in line:
            end_idx = idx

    # Prepare new content
    new_content = f'{summary}\n'

    # If markers are found, replace the content in between
    if start_idx is not None and end_idx is not None:
        updated_content = readme_content[:start_idx + 1] + [new_content] + readme_content[end_idx:]

    # Write the updated content back to README.md
    with open('pertemuan-3/README.md', 'w', encoding='utf-8') as f:
        f.writelines(updated_content)

if __name__ == "__main__":
    post_link = "https://medium.com/@dikaelsaputra/implementasi-mapreduce-hadoop-sederhana-b413cfc67f5c?source=rss-272e0aace4a6------2"
    summary = fetch_medium_post_summary(FEED_URL, post_link)
    update_readme(summary)