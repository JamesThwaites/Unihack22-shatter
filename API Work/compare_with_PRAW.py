import praw, re, pandas, time
from psaw import PushshiftAPI

TIME = time.time()
ONE_DAY_AGO = int(TIME - 86400)

api = PushshiftAPI()

SUBREDDIT_1 = 'austas'
SUBREDDIT_2 = 'interesting'

reddit = praw.Reddit(
    client_id='QjE7iZuv-YKAAmQVK6UcXA',
    client_secret='fuV5lGnvsghAJMEpLV5atZYXk6GGUA',
    user_agent='ShatterSimilarity:v0.0.1'
)

sub1 = reddit.subreddit(SUBREDDIT_1)
sub2 = reddit.subreddit(SUBREDDIT_2)

print(sub1.description)


'''
commenters = {}

gen = api.search_comments(after=ONE_DAY_AGO, subreddit=SUBREDDIT_1)
count = 0
for comment in list(gen):
    print(comment.author)
    count += 1

print(count)


submissions = sub1.hot(limit=25)

for submission in submissions:
    submission.comments.replace_more(limit=0)
    for comment in submission.comments.list():
        if comment.author != None:
            if comment.author.name in commenters:
                commenters[comment.author.name] += 1
            else:
                commenters[comment.author.name] = 1

df = pandas.DataFrame.from_dict(commenters, orient='index', columns=['# of comments'])
print(len(df))
df = df.sort_values('# of comments', ascending=False)
print(df.head(15))

'''