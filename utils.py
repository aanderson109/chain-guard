import subprocess
import hashlib
from sigstore.sign import Signer
from github import Github
from pypi_simple import PyPISimple
from git import Repo
import json
import csv


def get_git_metrics(target):
    """
    Uses GitPython to analyze commit history of cloned repository.
    """
    repo = Repo(target)
    commits = list(repo.iter_commits())
    return commits

def get_pypi_metrics(target):
    """
    Uses pypi_simple to retrieve metadata about the PyPI repository associated with the package.
    """
    client = PyPISimple()
    releases = client.get_releases(target)
    return releases

def get_github_metrics(target, token):
    """
    Uses PyGitHub wrapper to pull metrics about the target repository.
    """
    g = Github(token)
    repo = g.get_repo(target)
    stars = repo.stargazers_count
    open_issues = repo.open_issues_count
    forks = repo.forks_count
    return stars, open_issues, forks

def sign_artifact(artifact):
    """
    Uses sigstore to create a signature of a specified artifact
    """
    signer = Signer.staging()
    signature = signer.sign(artifact)
    return signature

def run_pip_audit():
    """
    Runs pip-audit
    """
    result = subprocess.run(["pip-audit", "--json"], capture_output=True, text=True)
    return result.stdout

def run_grype(target):
    """
    Runs Grype against a provided target
    """
    try:
        result = subprocess.run(
            ["grype", target, "-o", "json"],
            capture_output=True,
            text=True
        )
        result.check_returncode() # Raise CalledProcessError if the command fails
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Grype failed: {e.stderr}")
        return None
    except FileNotFoundError:
        print("Grype is not installed or not in PATH")
        return None

def run_trivy(target):
    """
    Runs Trivy against a provided target
    """
    try:
        result = subprocess.run(
            ["trivy", "fs", target, "--format", "json"],
            capture_output=True,
            text=True
        )
        result.check_returncode()
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Trivy failed; {e.stderr}")
        return None
    except FileNotFoundError as er:
        print("Trivy is not installed or not in PATH")
        return er

def generate_sbom(target):
    """
    Uses Syft and subprocess to generate an SPDX SBOM
    """
    result = subprocess.run(["syft", target, "-o", "spdx-json"], capture_output=True, text=True)
    if result.returncode == 0:
        print("SBOM Generated:", result.stdout)
        return result.stdout
    else:
        print("Error:", result.stderr)
        return None

def analyze_sbom(sbom_file):
    """
    Uses Trivy to analyze a provied SBOM
    """
    result = subprocess.run(["trivy", "sbom", sbom_file], capture_output=True, text=True)
    return result.stdout

def calculate_hash(file_path):
    """
    Calculates a SHA-256 digest for the provided file
    """
    hash_sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()

def verify_hash(file_path, known_hash):
    """
    Verifies if a known good hash is equal to one calculated on the fly
    """
    current_hash = calculate_hash(file_path)
    return current_hash == known_hash

def save_to_json(data, output_file):
    """
    Saves data to a JSON file.
    """
    try:
        with open(output_file, "w") as f:
            json.dump(data, f, indent=4)
        print(f"Report saved to {output_file}")
    except Exception as e:
        print(f"Error saving report: {e}")

def save_to_csv(data, output_file):
    """
    Saves data to a CSV file.
    """
    try:
        with open(output_file, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
        print(f"CSV report saved to {output_file}")
    except Exception as e:
        print(f"Error saving CSV report: {e}")
