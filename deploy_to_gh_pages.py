import subprocess
import os
import shutil
from pathlib import Path
import json


GITHUB_URL = "https://www.github.com"

PAD_WIDTH = 4
INPUT_DIR = Path("new_photos")


"""
Directions for use:

For this to work your project must be at the top level of your repository
You also must have the package angular-cli-ghpages installed. Run "npm install -g angular-cli-ghpages" if not

Then just run the program.

The program will:
    * clone the repository 
    * Build the angular project
    * Deploy the angular project to gh-pages
    * delete the local repository
"""

def clone_repo(username, repo_name):
    remote_repo_url = get_repo_url(username, repo_name)
    if remote_repo_url:
        try:
            print("clone repo started")
            subproc = subprocess.Popen(["git", "clone", remote_repo_url],
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            subproc.wait()
            print("clone repo finished")

            if subproc.returncode:
                print("finished with error")
                stdout, _ = subproc.communicate()
                print(stdout)
        except Exception as e:
            print("Failed to clone repository (probably does not exist):", 
                    remote_repo_url)
            print(e)
    else:
        print("repo url is missing")

def get_repo_url(username, repo_name):
    return f"{GITHUB_URL}/{username}/{repo_name}.git"

def delete_repo(repo_name):
    if os.path.exists(repo_name):
        shutil.rmtree(repo_name)


def add_commit_push(repo_name):
    try:
        print("stage started")
        print(run_git(["add", "."],repo_name))
        print("stage finished")

        # If nothing changed, commit will fail; detect that cleanly.
        status = run_git(["status", "--porcelain"],repo_name)
        if status.strip() == "":
            print("No changes to commit.")
            return

        print("commit started")
        print(run_git(["commit", "-m", "added photos for build"], repo_name))
        print("commit finished")

        print("push started")
        print(run_git(["push"], repo_name))
        print("push finished")

    except Exception as e:
        print("Failed to commit and push:", e)

def run_git(args: list[str],repo_name):
    subproc = subprocess.Popen(
        ["git", *args],
        cwd=str(repo_name),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    out, _ = subproc.communicate()
    if subproc.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed:\n{out}")
    return out

    

def build_angular(username, repo_name, project_name):
    if project_name and username:
        try:
            print("build angular started")
            subproc = subprocess.Popen(["ng", "build", "--configuration", "production", "--base-href", f'/{project_name}/'],
                cwd=f"{repo_name}/{project_name}", stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            subproc.wait()
            print("build angular finished")

            if subproc.returncode:
                print("finished with error")
                stdout, _ = subproc.communicate()
                print(stdout)
        except Exception as e:
            print("Failed to build repository (probably does not exist):", 
                    repo_name)
            print(e)
    else:
        print("repo or username is missing")

def deploy_angular(username, repo_name, project_name):
    if project_name and username:
        try:
            print("deploy agular started")
            subproc = subprocess.Popen(["npx", "angular-cli-ghpages", f"--dir=dist/{project_name}/browser"],
                cwd=f"{repo_name}/{project_name}", stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            subproc.wait()
            print("deploy agular finished")

            if subproc.returncode:
                print("finished with error")
                stdout, _ = subproc.communicate()
                print(stdout)
        except Exception as e:
            print("Failed to deploy repository (probably does not exist):", 
                    repo_name)
            print(e)
    else:
        print("repo or username is missing")

def angular_install(username, repo_name, project_name):
    if project_name and username:
        try:
            print("angular_install started")
            subproc = subprocess.Popen(["npm", "install"],
                cwd=f"{repo_name}/{project_name}", stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            subproc.wait()
            print("angular_install complete")
            if subproc.returncode:
                print("finished with error")
                stdout, _ = subproc.communicate()
                print(stdout)
        except Exception as e:
            print("Failed to install dependancies (probably does not exist):", 
                    project_name)
            print(e)
    else:
        print("repo or username is missing")


def load_list(json_path) -> list[str]:
    with json_path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list) or not all(isinstance(x, str) for x in data):
        raise ValueError("JSON must be an array of strings like [\"0001\", \"0002\", ...]")
    return data

def max_existing_number(existing: list[str]) -> int:
    best = 0
    for s in existing:
        if s.isdigit():
            best = max(best, int(s))
    return best

def list_input_files() -> list[Path]:
    files = [
        p for p in INPUT_DIR.iterdir()
        if p.is_file()
    ]
    return sorted(files, key=lambda p: p.name.lower())


def add_photos_to_build(repo_name, project_name):
    if not INPUT_DIR.exists():
        raise FileNotFoundError(f"Missing input dir: {INPUT_DIR}")
    json_path = Path(repo_name+"/"+project_name+"/src/assets/photos/photos.json")
    
    if not json_path.exists():
        raise FileNotFoundError(f"Missing JSON file: {json_path}")
    
    output_dir = Path(repo_name+"/"+project_name+"/src/assets/photos")

    output_dir.mkdir(parents=True, exist_ok=True)

    existing = load_list(json_path)
    width = PAD_WIDTH
    next_num = max_existing_number(existing) + 1

    files = list_input_files()
    if not files:
        print("No matching files found.")
        return

    new_names: list[str] = []

    for src in files:
        base = str(next_num).zfill(width)
        dst = output_dir / f"{base}.jpg"

        # Avoid overwriting if already exists; bump until free
        while dst.exists():
            next_num += 1
            base = str(next_num).zfill(width)
            dst = output_dir / f"{base}.jpg"

        shutil.copy2(src, dst)
        new_names.append(base)
        next_num += 1

    # Append to JSON list and write back
    existing.extend(new_names)
    with json_path.open("w", encoding="utf-8") as f:
        json.dump(existing, f, indent=2, ensure_ascii=False)



def run_all(username, repo_name, project_name = None):
    if project_name is None:
        project_name = repo_name
    clone_repo(username, repo_name)
    add_photos_to_build(repo_name,project_name)
    add_commit_push(repo_name)
    angular_install(username, repo_name, project_name)
    build_angular(username, repo_name, project_name)
    deploy_angular(username, repo_name, project_name)
    delete_repo(repo_name)

def main():
    run_all("andrewp06", "sams-website")

if __name__ == "__main__":
    main()