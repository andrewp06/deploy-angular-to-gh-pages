import subprocess
import os
import shutil

GITHUB_URL = "https://www.github.com"
PROJECT_NAME = ""
REPO_NAME = ""
USERNAME = ""

"""
Directions for use:

Replace the project_name, repo_name and Username constants with your github username and your project and repo name.
For this to work your project must be at the top level of your repository
You also must have the package angular-cli-ghpages installed. Run "npm install -g angular-cli-ghpages" if not

Then just run the program.

The program will:
    * clone the repository 
    * Build the angular project
    * Deploy the angular project to gh-pages
    * delete the local repository
"""

def clone_repo():
    remote_repo_url = get_repo_url()
    if remote_repo_url:
        try:
            subproc = subprocess.Popen(["git", "clone", remote_repo_url],
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            subproc.wait()
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

def get_repo_url():
    return f"{GITHUB_URL}/{USERNAME}/{REPO_NAME}.git"

def delete_repo():
    if os.path.exists(REPO_NAME):
        shutil.rmtree(REPO_NAME)

def build_angular():
    if PROJECT_NAME and USERNAME:
        try:
            subproc = subprocess.Popen(["ng", "build", "--configuration", "production", "--base-href", f'"/{PROJECT_NAME}/"'],
                cwd=f"{REPO_NAME}/{PROJECT_NAME}", stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            subproc.wait()
            if subproc.returncode:
                print("finished with error")
                stdout, _ = subproc.communicate()
                print(stdout)
        except Exception as e:
            print("Failed to build repository (probably does not exist):", 
                    REPO_NAME)
            print(e)
    else:
        print("repo or username is missing")

def deploy_angular():
    if PROJECT_NAME and USERNAME:
        try:
            subproc = subprocess.Popen(["npx", "angular-cli-ghpages", f"--dir=dist/{PROJECT_NAME}/browser"],
                cwd=f"{REPO_NAME}/{PROJECT_NAME}", stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            subproc.wait()
            if subproc.returncode:
                print("finished with error")
                stdout, _ = subproc.communicate()
                print(stdout)
        except Exception as e:
            print("Failed to deploy repository (probably does not exist):", 
                    REPO_NAME)
            print(e)
    else:
        print("repo or username is missing")

def angular_install():
    if PROJECT_NAME and USERNAME:
        try:
            subproc = subprocess.Popen(["npm", "install"],
                cwd=f"{REPO_NAME}/{PROJECT_NAME}", stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            subproc.wait()
            if subproc.returncode:
                print("finished with error")
                stdout, _ = subproc.communicate()
                print(stdout)
        except Exception as e:
            print("Failed to install dependancies (probably does not exist):", 
                    PROJECT_NAME)
            print(e)
    else:
        print("repo or username is missing")


def main():
    clone_repo()
    angular_install()
    build_angular()
    deploy_angular()
    delete_repo()

if __name__ == "__main__":
    main()