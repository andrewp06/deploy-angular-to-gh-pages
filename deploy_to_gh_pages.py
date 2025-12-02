import subprocess
import os
import shutil

GITHUB_URL = "https://www.github.com"

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


def run_all(username, repo_name, project_name = None):
    if project_name is None:
        project_name = repo_name
    clone_repo(username, repo_name)
    angular_install(username, repo_name, project_name)
    build_angular(username, repo_name, project_name)
    deploy_angular(username, repo_name, project_name)
    delete_repo(repo_name)
