import os
import psycopg2

conn = psycopg2.connect(
    host="postgres://dpg-ci97vkh8g3ne2egtvuk0-a.singapore-postgres.render.com",
    database="vicmadesql",
    user=os.getenv("DB_USERNAME"),
    password=os.getenv("DB_PASSWORD"),
)
# Open a cursor to perform database operations
cur = conn.cursor()

# Create some sample Git repos to pull posts from
cur.execute("DROP TABLE IF EXISTS repos;")
cur.execute(
    "CREATE TABLE repos (id serial PRIMARY KEY,"
    "owner varchar (150) NOT NULL,"
    "repourl varchar (256) NOT NULL,"
    "date_added date DEFAULT CURRENT_TIMESTAMP);"
)

# List of approved repos, add/remove as required then re-run this file.
# The API will check each of these repos for markdown posts, diff them to what we have stored, and update the database accordingly.

# These are test repos, we'll add the real ones when the site works better.
approved_repos = {
    "ObsoleteNerd": "https://github.com/obsoletenerd/obsoletenerd.github.io/tree/main/_posts",
    "BallaratMade": "https://github.com/vicmade/ballaratmademade.com/tree/main/_posts",
}

for repo in approved_repos:
    print("Adding %s" % repo)
    cur.execute(
        "INSERT INTO repos (owner, repourl)" "VALUES (%s, %s)",
        (repo, approved_repos[repo]),
    )

conn.commit()

cur.close()
conn.close()
