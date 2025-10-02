import requests
import csv

url = "https://api.github.com/search/repositories"
headers = {"Accept": "application/vnd.github.v3+json"}

repositories = []

# Duas páginas de 100 repositórios cada
for page in range(1, 3):
    params = {
        "q": "stars:>1",
        "sort": "stars",
        "order": "desc",
        "per_page": 100,
        "page": page
    }
    
    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        repositories.extend(data["items"])
    else:
        print(f"Erro na página {page}: {response.status_code}")
        break

# Salvar no CSV
with open("../data/repositories.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["repo_name", "stargazers_count", "forks_count"])
    for repo in repositories:
        writer.writerow([repo["full_name"], repo["stargazers_count"], repo["forks_count"]])

print(f"Total de repositórios salvos: {len(repositories)}")