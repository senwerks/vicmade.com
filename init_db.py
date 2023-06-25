############################################################################
#  Wipes the database and reinitialises it with dummy data                 #
############################################################################

import os
import psycopg2

try:
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(
        # host="dpg-ci97vkh8g3ne2egtvuk0-a",
        host="postgres://dpg-ci97vkh8g3ne2egtvuk0-a.singapore-postgres.render.com",
        database="vicmadesql",
        user=os.getenv("DB_USERNAME"),
        password=os.getenv("DB_PASSWORD"),
    )
except:
    print("Could not connect to the PostgreSQL database.")
    conn = None

if conn != None:
    cur = conn.cursor()

    # Create some sample posts in the database
    print("Dropping existing posts...")
    cur.execute("DROP TABLE IF EXISTS posts;")
    cur.execute(
        "CREATE TABLE posts (id serial PRIMARY KEY,"
        "title varchar (150) NOT NULL,"
        "repoid varchar (150) NOT NULL,"
        "markdownurl varchar (256) NOT NULL,"
        "linkurl varchar (256) NOT NULL,"
        "content text,"
        "date_added date DEFAULT CURRENT_TIMESTAMP);"
    )

    print("Inserting sample post...")
    cur.execute(
        "INSERT INTO posts (title, repoid, markdownurl, linkurl, content)"
        "VALUES (%s, %s, %s, %s, %s)",
        (
            "Introduction to BallaratMade.com",
            "BallaratMade.com",
            "https://raw.githubusercontent.com/obsoletenerd/ballaratmade.com/main/_posts/2023-06-25-Introduction-to-BallaratMade.com.md",
            "http://ballaratmade.com/",
            "BallaratMade.com is an open-source git-backed multi-user blog that allows our local group of makers/hackers to share their projects and project updates in a single place. This post is a test post used in the development of the project, and will be replaced/updated later with more details.",
        ),
    )

    # Create some sample Git repos to pull posts from
    print("Dropping existing repos...")
    cur.execute("DROP TABLE IF EXISTS repos;")
    cur.execute(
        "CREATE TABLE repos (id serial PRIMARY KEY,"
        "owner varchar (150) NOT NULL,"
        "repourl varchar (256) NOT NULL,"
        "date_added date DEFAULT CURRENT_TIMESTAMP);"
    )
    print("Creating sample repos...")
    approved_repos = {
        "ObsoleteNerd.com": "obsoletenerd/obsoletenerd.github.io",
        "BallaratMade.com": "obsoletenerd/vicmade.com",
    }

    for repo in approved_repos:
        cur.execute(
            "INSERT INTO repos (owner, repourl)" "VALUES (%s, %s)",
            (repo, approved_repos[repo]),
        )
        print("Added %s!" % repo)

    conn.commit()
    print("DB reinitialised!")
    cur.close()
    conn.close()
