import feedparser
from bs4 import BeautifulSoup
from html import escape
import re

FEED_URL = "https://medium.com/feed/@dikaelsaputra"

def fetch_medium_posts(feed_url, num_posts=10, category_filter='big-data'):
    feed = feedparser.parse(feed_url)
    posts = []

    for entry in feed.entries:
        categories = [tag.term for tag in entry.tags] if hasattr(entry, 'tags') else []
        if category_filter not in categories:
            continue
        
        title = entry.title
        link = entry.link
        summary_html = entry.summary
        soup = BeautifulSoup(summary_html, 'html.parser')
        img_tag = soup.find('img')
        image_url = img_tag['src'] if img_tag else None
        summary = soup.get_text()[:100] + '...' if len(soup.get_text()) > 100 else soup.get_text()
        
        posts.append((title, link, image_url, summary))
        
        if len(posts) >= num_posts:
            break

    return posts

def extract_existing_posts(readme_content):
    start_marker = "<!--START_SECTION:medium-->"
    end_marker = "<!--END_SECTION:medium-->"
    try:
        start_idx = readme_content.index(start_marker) + 1
        end_idx = readme_content.index(end_marker)
        section_content = readme_content[start_idx:end_idx]
        existing_links = re.findall(r'<a href="(.*?)"', ''.join(section_content))
        return set(existing_links)
    except ValueError:
        return set()

def update_readme(posts):
    with open('README.md', 'r', encoding='utf-8') as f:
        readme_content = f.readlines()

    existing_links = extract_existing_posts(readme_content)
    new_posts = [post for post in posts if post[1] not in existing_links]
    
    if not new_posts:
        print("Tidak ada post baru yang perlu ditambahkan.")
        return

    start_marker = "<!--START_SECTION:medium-->"
    end_marker = "<!--END_SECTION:medium-->"
    start_idx, end_idx = None, None

    for idx, line in enumerate(readme_content):
        if start_marker in line:
            start_idx = idx
        if end_marker in line:
            end_idx = idx

    if start_idx is None or end_idx is None:
        readme_content.append("\n" + start_marker + "\n" + end_marker + "\n")
        start_idx = len(readme_content) - 2
        end_idx = len(readme_content) - 1

    updated_content = "\n"

    old_section = readme_content[start_idx + 1:end_idx]
    new_section = []

    for post in new_posts:
        title, link, image_url, summary = post
        row = f'<p><a href="{link}" target="_blank" style="text-decoration: none;"><strong>{escape(title)}</strong></a></p>'
        row += f'<p>{escape(summary)}</p>'
        if image_url:
            row += f'<img src="{image_url}" alt="Post Image" style="width: 100px; height: auto;" />\n'
        new_section.append(row)

    updated_content += ''.join(new_section + old_section)
    
    readme_content = readme_content[:start_idx + 1] + [updated_content] + readme_content[end_idx:]

    with open('README.md', 'w', encoding='utf-8') as f:
        f.writelines(readme_content)

    print(f"{len(new_posts)} post baru ditambahkan ke README.md.")

if __name__ == "__main__":
    posts = fetch_medium_posts(FEED_URL, category_filter='big-data')
    update_readme(posts)
