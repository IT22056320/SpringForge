import os
import requests
import subprocess
import time

# ==============================
# CONFIGURATION
# ==============================
GITHUB_TOKEN = ""  # 
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}

# Search queries for each architecture
ARCHITECTURE_QUERIES = {
    "mvc": "spring boot mvc architecture",
    "layered": "spring boot layered architecture",
    "clean": "spring boot clean architecture"
}

# Target number of repositories per architecture
TARGET_COUNT = 500

# Save directory
BASE_DIR = "spring_architectures"
os.makedirs(BASE_DIR, exist_ok=True)


# ==============================
# FUNCTIONS
# ==============================
def search_repositories(query, per_page=50, max_pages=20):
    """
    Search GitHub repositories by query with pagination.
    Returns a generator of repositories.
    """
    for page in range(1, max_pages + 1):
        url = f"https://api.github.com/search/repositories?q={query}+language:Java&sort=stars&order=desc&per_page={per_page}&page={page}"
        response = requests.get(url, headers=HEADERS)

        if response.status_code == 403:  # Rate limit
            print("⚠️ Rate limit reached. Waiting 60 seconds...")
            time.sleep(60)
            continue

        response.raise_for_status()
        repos = response.json().get("items", [])
        if not repos:
            break
        yield from repos


def clone_repository(repo_url, save_dir):
    """Clone a GitHub repository into the given directory."""
    if os.path.exists(save_dir):
        print(f"⏩ Already exists, skipping: {save_dir}")
        return False
    try:
        subprocess.run(["git", "clone", "--depth", "1", repo_url, save_dir], check=True)
        print(f"✅ Cloned: {repo_url}")
        return True
    except Exception as e:
        print(f"❌ Failed to clone {repo_url}: {e}")
        return False


# ==============================
# MAIN SCRIPT
# ==============================
def main():
    for arch, query in ARCHITECTURE_QUERIES.items():
        print(f"\n🔎 Collecting repositories for architecture: {arch.upper()}")

        # Create directory for this architecture
        arch_dir = os.path.join(BASE_DIR, arch)
        os.makedirs(arch_dir, exist_ok=True)

        # Count existing repos
        existing = set(os.listdir(arch_dir))
        print(f"ℹ️ Already have {len(existing)} repos for {arch}")

        collected = len(existing)

        # Continue until target reached
        for repo in search_repositories(query, per_page=50, max_pages=100):
            if collected >= TARGET_COUNT:
                break
            repo_name = repo["name"]
            if repo_name in existing:
                continue
            repo_url = repo["clone_url"]
            save_path = os.path.join(arch_dir, repo_name)
            success = clone_repository(repo_url, save_path)
            if success:
                collected += 1

        print(f"🎯 Finished {arch}: {collected}/{TARGET_COUNT} repos\n")

    print("\n🎉 Dataset collection completed!")


if __name__ == "__main__":
    main()
