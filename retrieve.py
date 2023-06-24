import os
from github import Github
from github import Auth


auth = Auth.Token(os.getenv("GITHUB_KEY"))
g = Github(auth=auth)

repo = g.get_repo("obsoletenerd/vicmade.com")
contents = repo.get_contents("")
for content_file in contents:
    print(content_file)

# contents = repo.get_contents(repo_filename)
# print(contents)
