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


# We'd loop through the list of approved repos here ultimately, this is just for testing.
repo = g.get_repo("obsoletenerd/vicmade.com")
contents = repo.get_contents("posts")
for content_file in contents:
    if content_file.path.lower().endswith((".md")):
        print(content_file.decoded_content)
        post_title = content_file.name.split(".")[0].replace("-", " ")[11:]

        cur.execute(
            "INSERT INTO posts (title, repoid, markdownurl, linkurl, content)"
            "VALUES (%s, %s, %s, %s, %s)",
            (
                post_title,
                "Users-Domain.tld",
                content_file.html_url,
                "http://users-blog.tld/post-path/",
                content_file.decoded_content,
            ),
        )

conn.commit()

cur.close()
conn.close()
