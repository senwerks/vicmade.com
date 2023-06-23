import os
import psycopg2

conn = psycopg2.connect(
    # host="dpg-ci97vkh8g3ne2egtvuk0-a",
    host="postgres://dpg-ci97vkh8g3ne2egtvuk0-a.singapore-postgres.render.com",
    database="vicmadesql",
    user=os.getenv("DB_USERNAME"),
    password=os.getenv("DB_PASSWORD"),
)
# Open a cursor to perform database operations
cur = conn.cursor()

# Create some sample posts in the database
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
cur.execute(
    "INSERT INTO posts (title, repoid, markdownurl, linkurl, content)"
    "VALUES (%s, %s, %s, %s, %s)",
    (
        "Solving the Australian Signals Directorate cryptography challenge coin",
        "VicMade.com",
        "https://raw.githubusercontent.com/obsoletenerd/obsoletenerd.github.io/main/_posts/2022-09-01-Solving-the-Australian-Signals-Directorate-cryptography-challenge-coin.md",
        "http://obsoletenerd.com/2022/09/01/solving-the-australian-signals-directorate-cryptography-challenge-coin",
        "Today the *Australian Signals Directorate* announced their 75th Anniversary Commemorative Coin, which is a standard Australian 50 cent coin with various cryptographic puzzles embedded in it. I'm not a cryptography expert, but I've always loved this stuff from the sidelines of physical pentesting and teen-years script-kiddying, so I thought I'd give it a go. Along with a mate in our local Hackerspace's slack channel, we started bouncing ideas back and forth, and below is a write-up of the eventual path to solving all the puzzles on the coin (though as you'll see, not necessarily in the order they intended).",
    ),
)
cur.execute(
    "INSERT INTO posts (title, repoid, markdownurl, linkurl, content)"
    "VALUES (%s, %s, %s, %s, %s)",
    (
        "DIY LiPo Battery for the Original Gameboy",
        "Obsoletenerd.com",
        "https://raw.githubusercontent.com/obsoletenerd/obsoletenerd.github.io/main/_posts/2021-07-20-DIY-LiPo-Battery-Pack-for-Original-Gameboy.md",
        "http://obsoletenerd.com/2021/07/20/diy-lipo-battery-pack-for-original-gameboy",
        "I was pretty sick of worrying about the AA batteries for my original Gameboy, and just wanted a LiPo pack I could recharge via micro USB like so many of my modern devices. I found some existing projects that require cutting up the Gameboy, or modifying it in various ways... or some products from overseas that cost a fair bit and are basically just a LiPo + controller jammed into the battery cavity. I wanted something that didn't require any modification to the original Gameboy, and could be swapped back and forth with normal AAs if required.",
    ),
)

# Create some sample Git repos to pull posts from
cur.execute("DROP TABLE IF EXISTS repos;")
cur.execute(
    "CREATE TABLE repos (id serial PRIMARY KEY,"
    "owner varchar (150) NOT NULL,"
    "repourl varchar (256) NOT NULL,"
    "date_added date DEFAULT CURRENT_TIMESTAMP);"
)
cur.execute(
    "INSERT INTO repos (owner, repourl)" "VALUES (%s, %s)",
    ("ObsoleteNerd.com", "https://github.com/obsoletenerd/obsoletenerd.github.io/"),
)
cur.execute(
    "INSERT INTO repos (owner, repourl)" "VALUES (%s, %s)",
    ("VicMade.com", "https://github.com/obsoletenerd/vicmade.com"),
)

conn.commit()

cur.close()
conn.close()
