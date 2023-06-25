import os
import psycopg2  # https://www.psycopg.org/docs/
from flask import Flask, render_template, request, url_for, redirect
import markdown  # https://www.digitalocean.com/community/tutorials/how-to-use-python-markdown-to-convert-markdown-text-to-html

app = Flask(__name__)

# Hacky solution to develop both locally and on Render.com
dev_host = os.uname()[1]
if dev_host == "Phantom.localdomain":
    from dotenv_vault import load_dotenv

    load_dotenv()  # take environment variables from .env.
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


@app.route("/")
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM posts;")
    posts = cur.fetchall()
    cur.execute("SELECT * FROM repos;")
    repos = cur.fetchall()
    cur.close()
    conn.close()

    # Loop through the posts list and in each tuple replace the markdown with html
    formatted_posts = []
    for post in posts:
        markdown_text = markdown.markdown(post[5])
        new_tuple = tuple(post[:5]) + (markdown_text,) + post[6:]
        formatted_posts.append(new_tuple)

    return render_template("index.html", posts=formatted_posts, repos=repos)


@app.route("/post/<int:post_id>")
def index(post_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM posts WHERE id = %s;", (post_id,))
    posts = cur.fetchall()
    cur.close()
    conn.close()

    # Loop through the posts list and in each tuple replace the markdown with html
    formatted_posts = []
    for post in posts:
        markdown_text = markdown.markdown(post[5])
        new_tuple = tuple(post[:5]) + (markdown_text,) + post[6:]
        formatted_posts.append(new_tuple)

    return render_template("index.html", posts=formatted_posts)


@app.route("/about")
def about():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM repos;")
    repos = cur.fetchall()
    cur.close()
    conn.close()

    return render_template("about.html", repos=repos)
