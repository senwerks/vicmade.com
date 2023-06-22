import schedule  # https://schedule.readthedocs.io
import time


def check_posts():
    print("This is where we would get the posts from Git and process them")


schedule.every().hour.do(check_posts)

# def function(param):
#    print(f"Running job: {param}")
# schedule.every().hour.do(function, param="Something")

while True:
    schedule.run_pending()
    time.sleep(1)
