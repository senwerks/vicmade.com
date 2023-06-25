############################################################################
#  Re-pulls all posts from the approved repos and adds them to our DB      #
############################################################################

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


# Set up a connection to the database
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

# Get the list of approved repos from the database
cur.execute("SELECT * FROM repos;")
repos = cur.fetchall()

for repo in repos:
    repo_name = repo[1]
    print("Processing repo: %s" % repo_name)

    repo_url = repo[2]
    print("Repo URL: %s" % repo_url)

    # Get the repo and pull the posts
    repo = g.get_repo(repo_url)

    # TODO: Need error catching if posts dir doesn't exist
    contents = repo.get_contents("_posts")

    # Loop through each file in the "_posts" directory
    for content_file in contents:
        if content_file.path.lower().endswith((".md")):  # Only markdown files
            # Get the markdown so we can parse it and add the relevant parts to the database
            post_markdown = repo.get_contents(content_file.path).decoded_content.decode(
                "utf-8"
            )
            sections = post_markdown.split("---")
            metadata = sections[1].strip()
            metadata_lines = metadata.split("\n")

            # Prepopulate with the user's root URL in case we cant find posturl later
            post_url = repo_url

            # Build a title from the filename, in case they didn't put one in the metadata
            post_title = content_file.name.split(".")[0].replace("-", " ")[11:]

            for metadata_items in metadata_lines:
                # Get the post title from the markdown metadata:
                if metadata_items.split(":")[0] == "title":
                    post_title = metadata_items.split(":")[1]
                    print("Found Title: %s" % post_title)

                # Get the post tags from the markdown metadata:
                elif metadata_items.split(":")[0] == "tags":
                    post_tags = metadata_items.split(":")[1]
                    print("Found Tags: %s" % post_tags)

                # Get the user's own post URL so we can link to the post on their blog
                elif metadata_items.split(":")[0] == "posturl":
                    post_url = metadata_items.split(":")[1]
                    print("Found PostURL: %s" % post_url)

                # TODO: Add this to the DB structure for posts tied to a Github repository:
                elif metadata_items.split(":")[0] == "github":
                    post_github = metadata_items.split(":")[1]
                    print("Found Github: %s" % post_github)

                # TODO: Need to check if the above values are empty before trying to add

            # Everything left after the metadata is the content of the post:
            post_content = sections[2]

            # Insert the post into the database:
            cur.execute(
                "INSERT INTO posts (title, repoid, markdownurl, linkurl, content)"
                "VALUES (%s, %s, %s, %s, %s)",
                (
                    post_title,  # The title of the post pulled from the metadata
                    repo_name,  # The user's website name/URL
                    content_file.html_url,  # URL to the source Markdown file
                    post_url,  # URL to the post on the user's blog
                    post_content,  # The markdown content of the post
                ),
            )

conn.commit()

cur.close()
conn.close()
