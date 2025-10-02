import requests
import csv
import time
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv('TOKEN')

if not GITHUB_TOKEN:
    print("ERRO: Token não encontrado no .env")
    exit(1)

repos = []
with open("../data/repositories.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        repos.append(row["repo_name"])

headers = {
    "Accept": "application/vnd.github.v3+json",
    "Authorization": f"token {GITHUB_TOKEN}"
}

TIMEOUT = 30
MAX_RETRIES = 3
BASE_DELAY = 2

def make_request(url, headers, params=None, max_retries=MAX_RETRIES):
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, params=params, timeout=TIMEOUT)
            
            if response.status_code == 403:
                reset_time = int(response.headers.get('X-RateLimit-Reset', 0))
                current_time = int(time.time())
                sleep_time = max(reset_time - current_time, 3600)
                print(f"Rate limit excedido. Aguardando {sleep_time} segundos...")
                time.sleep(sleep_time)
                continue
            elif response.status_code == 429:
                retry_after = int(response.headers.get('Retry-After', 60))
                print(f"Too Many Requests. Aguardando {retry_after} segundos...")
                time.sleep(retry_after)
                continue
            elif response.status_code in [500, 502, 503, 504]:
                print(f"Erro do servidor {response.status_code}. Tentativa {attempt + 1}/{max_retries}")
                time.sleep(BASE_DELAY * (2 ** attempt))
                continue
                
            return response
            
        except (requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError) as e:
            print(f"Timeout/Connection error (tentativa {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                sleep_time = BASE_DELAY * (2 ** attempt)
                print(f"Aguardando {sleep_time} segundos antes de tentar novamente...")
                time.sleep(sleep_time)
            else:
                return None
        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição: {e}")
            return None
    
    return None

processed_repos = set()
try:
    with open("../data/pull_requests.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            processed_repos.add(row["repo_name"])
    print(f"Encontrados {len(processed_repos)} repositórios já processados")
except FileNotFoundError:
    print("Arquivo pull_requests.csv não encontrado. Iniciando do zero.")

remaining_repos = [repo for repo in repos if repo not in processed_repos]
print(f"Restam {len(remaining_repos)} repositórios para processar")

mode = "a" if processed_repos else "w"
with open("../data/pull_requests.csv", mode, newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    
    if not processed_repos:
        writer.writerow([
            "repo_name", "pr_number", "state", "created_at", "closed_at", "merged_at",
            "additions", "deletions", "changed_files", "body_length", "comments",
            "review_comments", "participants_count"
        ])

    total_repos = len(remaining_repos)
    total_prs_collected = 0
    
    for idx, repo in enumerate(remaining_repos, 1):
        print(f"Processando repositório {idx}/{total_repos}: {repo}")
        
        page = 1
        prs_processed = 0
        max_pages = 3
        
        while page <= max_pages:
            url = f"https://api.github.com/repos/{repo}/pulls"
            params = {
                "state": "all",
                "sort": "updated",
                "direction": "desc", 
                "per_page": 50,
                "page": page
            }
            
            response = make_request(url, headers, params)
            
            if response is None:
                break
                
            if response.status_code != 200:
                print(f"Erro HTTP {response.status_code} para {repo}")
                break
                
            prs = response.json()
            if not prs:
                break
            
            print(f"Página {page}: {len(prs)} PRs encontrados")
            
            for pr in prs:
                created_at = pr["created_at"]
                closed_at = pr["closed_at"]
                
                if not closed_at:
                    continue
                
                try:
                    created_dt = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                    closed_dt = datetime.fromisoformat(closed_at.replace('Z', '+00:00'))
                    time_diff = (closed_dt - created_dt).total_seconds()
                    
                    if time_diff < 3600:
                        continue
                except (ValueError, TypeError):
                    continue
                
                pr_number = pr["number"]
                pr_url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}"
                pr_details_response = make_request(pr_url, headers)
                
                if pr_details_response is None or pr_details_response.status_code != 200:
                    continue
                    
                pr_details = pr_details_response.json()
                
                review_comments = pr_details.get("review_comments", 0)
                comments = pr_details.get("comments", 0)
                
                if review_comments == 0 and comments == 0:
                    continue
                
                merged_at = pr["merged_at"]
                state = pr["state"]
                
                writer.writerow([
                    repo, pr_number, state, created_at, closed_at, merged_at,
                    pr_details.get("additions", 0),
                    pr_details.get("deletions", 0),
                    pr_details.get("changed_files", 0),
                    len(pr_details.get("body", "") or ""),
                    comments,
                    review_comments,
                    pr_details.get("participants", 0)
                ])
                
                prs_processed += 1
                total_prs_collected += 1
                
                time.sleep(0.3)
            
            page += 1
            time.sleep(1)
            
            if prs_processed >= 10:
                break
        
        print(f"Repositório {repo} concluído: {prs_processed} PRs salvos")
        time.sleep(2)

print(f"Coleta concluída. Total de PRs coletados nesta sessão: {total_prs_collected}")