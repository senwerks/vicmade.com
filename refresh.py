import os
import psycopg2
from github import Github
from github import Auth

auth = Auth.Token(os.getenv("GITHUB_KEY"))
g = Github(auth=auth)

# Hacky solution to develop both locally and on Render.com
dev_host = os.uname()[1]
if dev_host == "Phantom.localdomain":
    print("Running locally, using full Render.com DB path")
    db_host = "postgres://dpg-ci97vkh8g3ne2egtvuk0-a.singapore-postgres.render.com"
else:
    print("Running on Render.com, using local DB path")
    db_host = "dpg-ci97vkh8g3ne2egtvuk0-a"


def get_db_connection():
    conn = psycopg2.connect(
        host=db_host,
        database="vicmadesql",
        user=os.getenv("DB_USERNAME"),
        password=os.getenv("DB_PASSWORD"),
    )
    return conn


conn = get_db_connection()
cur = conn.cursor()


# We'd loop through the list of approved repos here ultimately, this is just for testing.
repo_name = "obsoletenerd/vicmade.com"
repo = g.get_repo(repo_name)

contents = repo.get_contents(
    "posts"
)  # TODO: Need error catching if posts dir doesn't exist

# Loop through each file in the "posts" directory
for content_file in contents:
    if content_file.path.lower().endswith((".md")):  # Only markdown files
        # post_title = content_file.name.split(".")[0].replace("-", " ")[11:]

        # Get the markdown so we can parse it and add the relevant parts to the database
        post_markdown = repo.get_contents(content_file.path).decoded_content.decode(
            "utf-8"
        )
        sections = post_markdown.split("---")
        metadata = sections[1].strip()
        metadata_lines = metadata.split("\n")

        for metadata_items in metadata_lines:
            # Get the post title from the markdown metadata:
            if metadata_items.split(":")[0] == "title":
                post_title = metadata_items.split(":")[1]
                print("Found Title: %s" % post_title)

            # Get the post tags from the markdown metadata:
            elif metadata_items.split(":")[0] == "tags":
                post_tags = metadata_items.split(":")[1]
                print("Found Tags: %s" % post_tags)

            # TODO: Add this to the DB structure for posts tied to a Github repository:
            elif metadata_items.split(":")[0] == "github":
                post_github = metadata_items.split(":")[1]
                print("Found Github: %s" % post_github)

        # Everything left after the metadata is the content of the post:
        post_content = sections[2]

        # Insert the post into the database:
        cur.execute(
            "INSERT INTO posts (title, repoid, markdownurl, linkurl, content)"
            "VALUES (%s, %s, %s, %s, %s)",
            (
                post_title,
                "Users-Domain.tld",  # This should be the user's domain
                content_file.html_url,  # URL to the source Markdown file
                "http://users-blog.tld/post-path/",  # This should be the URL to the post on the user's blog
                post_content,
            ),
        )

conn.commit()

cur.close()
conn.close()
