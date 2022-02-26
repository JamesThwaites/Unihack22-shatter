import praw, re, json, prawcore, copy
from pmaw import PushshiftAPI

api = PushshiftAPI()

with open('stored_descs.json', 'r') as store:
    stored_descs = json.load(store)

reddit = praw.Reddit(
    client_id='QjE7iZuv-YKAAmQVK6UcXA',
    client_secret='fuV5lGnvsghAJMEpLV5atZYXk6GGUA',
    user_agent='ShatterSimilarity:v0.0.1'
)

subreddit_sizes = {}

subreddit_list = [key for key in stored_descs]

count = 1
TOTAL = len(subreddit_list)
csv = open('subreddits.csv', 'w')

for sub in subreddit_list:
    try:
        csv.write(sub)
    except UnicodeEncodeError:
        pass
    
    csv.write(',')

    '''
    try:
        subcount = reddit.subreddit(sub).subscribers
        subreddit_sizes[sub] = subcount

    except prawcore.exceptions.Redirect:
        subreddit_sizes[sub] = 1
        #Subreddit does not exist (402)

    except prawcore.exceptions.Forbidden:
        subreddit_sizes[sub] = 1
        #Subreddit is private (403)

    except prawcore.exceptions.NotFound:
        subreddit_sizes[sub] = 1
        #Subreddit 404
    '''


    count += 0
    #print(f'{sub}: {subcount}   ---   Remaining: {TOTAL - count}')

csv.close()

'''
with open('subreddit_sizes.json', 'w') as subsizes:
    json.dump(subreddit_sizes, subsizes, indent=2)
'''