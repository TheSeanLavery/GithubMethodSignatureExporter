import base64
import os
import requests
import re
from github import Github   
from typing import List
from githubTokenHelper import get_token

def get_all_files(repo, path: str = "") -> List[str]:
    files = []
    contents = repo.get_contents(path)
    for content in contents:
        if content.type == "file" and content.path.endswith(".py"):
            files.append(content.path)
        elif content.type == "dir":
            files.extend(get_all_files(repo, content.path))
    return files

def get_repo_files(github: Github, repo_full_name: str) -> List[str]:
    repo = github.get_repo(repo_full_name)
    return get_all_files(repo)

def get_method_signatures(file_content: str) -> List[str]:
    signatures = []
    method_pattern = re.compile(r"def\s+(\w+)\s*\((.*?)\):")
    return_pattern = re.compile(r":return:.*\n.*:rtype: (\w+)")
    for match in method_pattern.finditer(file_content):
        method_name, args = match.groups()
        return_type = "Unknown"
        docstring_start = match.end()
        docstring_match = re.search(r"('''|\"\"\")", file_content[docstring_start:])
        if docstring_match:
            docstring_start += docstring_match.end()
            docstring_end = file_content.find(docstring_match.group(1), docstring_start)
            if docstring_end != -1:
                docstring = file_content[docstring_start:docstring_end].strip()
                return_match = return_pattern.search(docstring)
                if return_match:
                    return_type = return_match.group(1)
        signature = f"{method_name}({args}) -> {return_type}"
        signatures.append(signature)
    return signatures

def main():
    repo_url = input("Enter the public GitHub URL of the repository: ")
    repo_url = repo_url.rstrip("/")
    repo_full_name = "/".join(repo_url.split("/")[-2:])

    output_file = f"{repo_full_name.replace('/', '_')}_signatures.txt"

    pat = get_token()
    
    github = Github(pat)
    file_paths = get_repo_files(github, repo_full_name)

    if not os.path.exists("output"):
        os.makedirs("output")

    with open(f"output/{output_file}", "w") as outfile:
        for file_path in file_paths:
            repo = github.get_repo(repo_full_name)
            content = repo.get_contents(file_path)
            decoded_content = base64.b64decode(content.content).decode("utf-8")
            signatures = get_method_signatures(decoded_content)
            if signatures:
                outfile.write(f"Signatures in {file_path}:\n")
                outfile.write("\n".join(signatures))
                outfile.write("\n\n")

    print(f"Method signatures saved to: output/{output_file}")

if __name__ == "__main__":
    main()
