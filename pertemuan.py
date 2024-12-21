import feedparser
from html import escape, unescape
import os
import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

# URL RSS feed Medium
FEED_URL = "https://medium.com/feed/@dikaelsaputra"
output_folder = "output-images"
os.makedirs(output_folder, exist_ok=True)

def fetch_medium_post_summary(feed_url, post_link):
    feed = feedparser.parse(feed_url)
    
    for entry in feed.entries:
        if entry.link == post_link:
            summary = entry.summary
            return summary

    return "Summary not found."

def update_readme(summary, readme_path, post_link):
    # Unescape HTML entities in the summary
    summary = unescape(summary)

    # Read the existing README content
    with open(readme_path, 'r', encoding='utf-8') as f:
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

    # Prepare new content with URL and summary
    new_content = f'[Baca di Medium]({post_link})\n\n{summary}\n'

    # If markers are found, replace the content in between
    if start_idx is not None and end_idx is not None:
        updated_content = readme_content[:start_idx + 1] + [new_content] + readme_content[end_idx:]

        # Write the updated content back to README.md
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.writelines(updated_content)

def fetch_post_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    thumbnail_url = soup.find('meta', {'property': 'og:image'})
    thumbnail_url = thumbnail_url['content'] if thumbnail_url else None
    publish_date = soup.find('span', {'data-testid': 'storyPublishDate'})
    publish = publish_date.text.strip() if publish_date else '0'
    readers_count = soup.find('span', {'data-testid': 'storyReadTime'})
    readers = readers_count.text.strip() if readers_count else '0'
    return thumbnail_url, publish, readers

def create_post_image(post_data, index):
    width, height = 400, 550
    image = Image.new('RGBA', (width, height), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    font_size = 62
    font = ImageFont.truetype('Helvetica-Bold.ttf', font_size)
    
    if post_data[0]:
        try:
            response = requests.get(post_data[0])
            img = Image.open(BytesIO(response.content))
            img.thumbnail((400, 400))  
            image.paste(img, (0, 0))
        except Exception as e:
            print(f"Error loading image: {e}")
     
    text_claps = [f"{post_data[2]}", f"{post_data[1]}"]
    line_height = 10  
    text_x = 0       
    text_y = 415      
    
    for line in text_claps:
        draw.text((text_x, text_y), line, font=font, fill='black')
        text_y += font_size + line_height  
    
    output_path = os.path.join(output_folder, f'post_{index + 1}.png')
    image.save(output_path, "PNG")

if __name__ == "__main__":
    posts = [
        ("https://medium.com/@dikaelsaputra/panduan-lengkap-pyspark-dan-pandas-instalasi-praktik-dasar-dan-lanjutan-86ab9ce4ea55?source=rss-272e0aace4a6------2", 'pertemuan-1/README.md'),
        ("https://medium.com/@dikaelsaputra/instalasi-dan-konfigurasi-hadoop-serta-spark-di-windows-f7f3582def93?source=rss-272e0aace4a6------2", 'pertemuan-2/README.md'),
        ("https://medium.com/@dikaelsaputra/implementasi-mapreduce-hadoop-sederhana-b413cfc67f5c?source=rss-272e0aace4a6------2", 'pertemuan-3/README.md'),
        ("https://medium.com/@dikaelsaputra/ekosistem-hadoop-pig-dan-hive-43b48d369828?source=rss-272e0aace4a6------2", 'pertemuan-4/README.md'),
        ("https://medium.com/@dikaelsaputra/tutorial-lengkap-mongodb-atlas-dengan-mongodb-compass-d3b015cf4712?source=rss-272e0aace4a6------2", 'pertemuan-5/README.md'),
        ("https://medium.com/@dikaelsaputra/data-processing-dengan-apache-spark-14af61b5c22b?source=rss-272e0aace4a6------2", 'pertemuan-6/README.md'),
        ("https://medium.com/@dikaelsaputra/operasi-dasar-sql-di-spark-sql-b09121677bac?source=rss-272e0aace4a6------2", 'pertemuan-9/README.md'),
        ("https://medium.com/@dikaelsaputra/implementasi-nosql-database-mongodb-dengan-pymongo-689ae79ac6c6?source=rss-272e0aace4a6------2", 'pertemuan-10/README.md'),
        ("https://medium.com/@dikaelsaputra/advanced-mongodb-operations-and-data-query-6403253b25a4?source=rss-272e0aace4a6------2", 'pertemuan-11/README.md'),
        ("https://medium.com/@dikaelsaputra/data-cleaning-preparation-and-visualization-7ec75116b408?source=rss-272e0aace4a6------2", 'pertemuan-12-13/README.md'),
        ("https://medium.com/@dikaelsaputra/advanced-machine-learning-using-spark-mllib-1e5fe3e00ae2?source=rss-272e0aace4a6------2", 'pertemuan-14/README.md'),
        ("https://medium.com/@dikaelsaputra/memprediksi-keberhasilan-tmdb-konten-tv-7b6826951b50?source=rss-272e0aace4a6------2", 'proyek-akhir/README.md')
    ]
    
    for post_link, readme_path in posts:
        summary = fetch_medium_post_summary(FEED_URL, post_link)
        update_readme(summary, readme_path, post_link)

    for index, post_url in enumerate(posts[0]):
        post_data = fetch_post_data(post_url)
        create_post_image(post_data, index)