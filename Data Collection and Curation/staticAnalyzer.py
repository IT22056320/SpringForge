import os
import re
import csv
from collections import Counter

BASE_DIR = "spring_architectures"

# Regex patterns for annotations
ANNOTATIONS = {
    "controller": r"@Controller|@RestController",
    "service": r"@Service",
    "repository": r"@Repository",
    "configuration": r"@Configuration",
    "component": r"@Component",
    "springboot_app": r"@SpringBootApplication"
}

# Package keywords
PACKAGE_KEYWORDS = ["controller", "service", "repository", "domain", "usecase", "infrastructure", "application"]

# Import-based features
IMPORT_KEYWORDS = {
    "import_web": r"import\s+org\.springframework\.web",
    "import_stereotype": r"import\s+org\.springframework\.stereotype",
    "import_data": r"import\s+org\.springframework\.data",
    "import_jpa": r"import\s+javax\.persistence",
    "import_boot": r"import\s+org\.springframework\.boot"
}

def analyze_java_file(filepath):
    """Extract features from a single Java file."""
    features = Counter()
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

            # Count annotations
            for key, pattern in ANNOTATIONS.items():
                features[key] += len(re.findall(pattern, content))

            # Count imports
            for key, pattern in IMPORT_KEYWORDS.items():
                features[key] += len(re.findall(pattern, content))

            # Count class roles
            if re.search(r"class\s+\w*Controller", content):
                features["class_controller"] += 1
            if re.search(r"class\s+\w*Service", content):
                features["class_service"] += 1
            if re.search(r"class\s+\w*Repository", content):
                features["class_repository"] += 1
            if re.search(r"class\s+\w*Config", content):
                features["class_config"] += 1

            # Count architecture keywords in file path
            for kw in PACKAGE_KEYWORDS:
                if kw in filepath.lower():
                    features[f"pkg_{kw}"] += 1

    except Exception as e:
        print(f"Error reading {filepath}: {e}")
    return features

def analyze_repo(repo_path):
    """Analyze all Java files in a repository."""
    repo_features = Counter()
    file_count = 0
    max_depth = 0

    for root, _, files in os.walk(repo_path):
        depth = len(root.replace(repo_path, "").split(os.sep))
        max_depth = max(max_depth, depth)
        for file in files:
            if file.endswith(".java"):
                file_count += 1
                filepath = os.path.join(root, file)
                repo_features.update(analyze_java_file(filepath))
            if file in ["application.properties", "application.yml"]:
                repo_features["has_app_config"] = 1

    repo_features["total_java_files"] = file_count
    repo_features["max_package_depth"] = max_depth
    return repo_features

def build_dataset(base_dir=BASE_DIR, output_file="architecture_features_rich.csv"):
    """Build dataset from all repos with enhanced features."""
    rows = []
    for arch in os.listdir(base_dir):
        arch_dir = os.path.join(base_dir, arch)
        if not os.path.isdir(arch_dir):
            continue
        for repo in os.listdir(arch_dir):
            repo_path = os.path.join(arch_dir, repo)
            print(f"Analyzing {repo_path} ...")
            features = analyze_repo(repo_path)
            features["repo_name"] = repo
            features["architecture"] = arch
            rows.append(features)

    keys = set(k for row in rows for k in row.keys())
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(keys))
        writer.writeheader()
        writer.writerows(rows)

    print(f"\n✅ Enhanced dataset saved to {output_file}")

if __name__ == "__main__":
    build_dataset()
