import os
from github import Github
from github import Auth
import markdown  # https://www.digitalocean.com/community/tutorials/how-to-use-python-markdown-to-convert-markdown-text-to-html


auth = Auth.Token(os.getenv("GITHUB_KEY"))
g = Github(auth=auth)

repo = g.get_repo("obsoletenerd/vicmade.com")
contents = repo.get_contents("posts")
for content_file in contents:
    if content_file.path.lower().endswith((".md")):
        # Get the title out of the file name
        post_title = content_file.name.split(".")[0].replace("-", " ")[11:]
        print("Title: %s" % post_title)

        # Get the source markdown URL
        post_source = content_file.html_url
        print("Markdown URL: %s" % post_source)

        # Get the markdown contents and parse it into a dictionary
        post_markdown = repo.get_contents(content_file.path).decoded_content.decode(
            "utf-8"
        )
        # print("Markdown: %s" % post_markdown.decoded_content.decode("utf-8"))

        sections = post_markdown.split("---")
        metadata = sections[1].strip()
        metadata_lines = metadata.split("\n")

        for metadata_items in metadata_lines:
            if metadata_items.split(":")[0] == "title":
                print("Title: %s" % metadata_items.split(":")[1])
            elif metadata_items.split(":")[0] == "tags":
                print("Tags: %s" % metadata_items.split(":")[1])
        print("--------")
        print("Main Content:")
        print(sections[2])
