import requests

# Konfigurasi
GITHUB_API_URL = 'https://api.github.com/repos/{owner}/{repo}/contents'
README_PATH = 'README.md'
START_TAG = '<!--START:structure-->'
END_TAG = '<!--END:structure-->'

def fetch_repo_contents(owner, repo, path=''):
    url = GITHUB_API_URL.format(owner=owner, repo=repo) + path
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def generate_markdown_tree(contents, base_url='', level=0):
    markdown = ''
    for item in contents:
        item_url = f'{base_url}/{item["name"]}' if base_url else f'/{item["name"]}'
        indent = '  ' * level
        if item['type'] == 'dir':
            markdown += f'{indent}- [{item["name"]}]({item_url})\n'
            sub_contents = fetch_repo_contents(owner, repo, '/' + item['path'])
            markdown += generate_markdown_tree(sub_contents, item_url, level + 1)
        else:
            markdown += f'{indent}- [{item["name"]}]({item_url})\n'
    return markdown

def update_readme_with_structure(readme_path, structure):
    with open(readme_path, 'r') as file:
        content = file.read()
    
    start_idx = content.find(START_TAG) + len(START_TAG)
    end_idx = content.find(END_TAG)
    
    if start_idx == -1 or end_idx == -1:
        raise ValueError("Tags not found in README.md")

    new_content = content[:start_idx] + '\n' + structure + '\n' + content[end_idx:]
    
    with open(readme_path, 'w') as file:
        file.write(new_content)

def main():
    global owner, repo
    owner = 'figuran04'
    repo = 'big-data'

    contents = fetch_repo_contents(owner, repo)
    markdown_structure = generate_markdown_tree(contents)
    
    update_readme_with_structure(README_PATH, markdown_structure)
    print("README.md telah diperbarui dengan struktur folder.")

if __name__ == '__main__':
    main()
