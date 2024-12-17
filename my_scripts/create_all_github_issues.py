import os, hashlib, requests, time
from bs4 import BeautifulSoup

def generate_md5(path):
    return hashlib.md5(path.encode('utf-8')).hexdigest()

def check_existing_issues(config, labels):
    url = f"https://api.github.com/repos/{config['owner']}/{config['repo']}/issues"
    headers = {
        "Authorization": f"token {config['token']}",
        "Accept": "application/vnd.github.v3+json"
    }
    params = {
        "labels": ",".join(labels)
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        issues = response.json()
        return True if issues else False
    else:
        print(f"Error issues: {response.status_code}, {response.text}")
        return False

def extract_title_from_html(directory_path):
    index_html_path = os.path.join(directory_path, "index.html")
    if os.path.exists(index_html_path):
        with open(index_html_path, "r", encoding="utf-8") as file:
            content = file.read()
            soup = BeautifulSoup(content, "html.parser")
            title_tag = soup.find("title")
            if title_tag:
                return title_tag.text.strip()
    return None  # Если тега <title> не найдено, вернем None

def create_github_issue(file_name, title, config):    
    path_md5 = generate_md5(file_name)
    labels = ["gitalk", path_md5]
    if check_existing_issues(config, labels):
        print(f"Skipped, already exists for: {file_name}")
        return
         
    url = f"https://api.github.com/repos/{config['owner']}/{config['repo']}/issues"
    headers = {
        "Authorization": f"token {config['token']}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    data = {
        "title": title,
        "labels": ["gitalk", path_md5]
    }
    
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 201:
        print(f"Issue created successfully: {response.json()['url']} for {file_name}")
    else:
        print(f"Error creating issue for {file_name}: {response.status_code}, {response.text}")

github_token = os.getenv("GITHUB_TOKEN")
config = {
    "owner": "spiiin",
    "repo": "spiiin.github.io",
    "token": github_token
}

def create_issues_for_all_directories(base_path, config):
    for root, dirs, files in os.walk(base_path):
        for i, dir_name in enumerate(dirs):
            dir_path = f"/blog/{dir_name}/"
            title = extract_title_from_html(os.path.join(root, dir_name))
            print(f"{i} {dir_path} - {title}")
            create_github_issue(dir_path, title, config)
            time.sleep(3.0)

base_directory = "../public/blog/"
create_issues_for_all_directories(base_directory, config)