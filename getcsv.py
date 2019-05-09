import praw
import pandas as pd
import sys

credential_file = "credentials.key"

try:
    with open(credential_file, 'r') as f:
        creds = f.read().split('\n')
    personal = creds[0]
    secret = creds[1]
    username = creds[2]
    password = creds[3]
except IOError as e:
    print("You didn't create a credential file! Please see sample_credentials.key")
    print("Then go to http://www.storybench.org/how-to-scrape-reddit-with-python/")
    print("And register a new app named fastai_reddit in your reddit account.")
    print("And insert the values into sample_credentials.key and save it as {}.".format(credential_file))
    raise(e)

reddit = praw.Reddit(client_id=personal, client_secret=secret, user_agent='fastai_reddit', username=username, \
                     password=password)

def get_posts(sub):
    subreddit = reddit.subreddit(sub)
    top = list(subreddit.top(limit=1000))
    new = list(subreddit.new(limit=1000))
    rising = list(subreddit.rising(limit=1000))
    controversial = list(subreddit.controversial(limit=1000))
    gilded = list(subreddit.gilded(limit=1000))
    allposts = list(set(top + new + rising + controversial + gilded))
    return allposts

def get_df(posts):
    df = pd.DataFrame()
    urls = []
    imgurls = []
    for p in posts:
        try:
            url = p.preview['images'][0]['source']['url']
            try:
                imgurl = "https://reddit.com" + p.permalink
            except AttributeError:
                imgurl = ""
            urls.append(url)
            imgurls.append(imgurl)
        except (IndexError, KeyError, AttributeError):
            pass
    df['url'] = urls
    df['imgurl'] = imgurls
    return df

if __name__ == "__main__":
    sub = sys.argv[1]
    if len(sys.argv) > 2:
        outfile = sys.argv[2]
    else:
        outfile = sub + ".csv"
    posts = get_posts(sub)
    df = get_df(posts)
    df.to_csv(outfile)