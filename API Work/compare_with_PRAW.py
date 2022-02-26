import praw, re

SUBREDDIT_1 = 'MadeMeSmile'
SUBREDDIT_2 = 'interesting'

reddit = praw.Reddit(
    client_id='QjE7iZuv-YKAAmQVK6UcXA',
    client_secret='fuV5lGnvsghAJMEpLV5atZYXk6GGUA',
    user_agent='ShatterSimilarity:v0.0.1'
)

sub1 = reddit.subreddit(SUBREDDIT_1)
sub2 = reddit.subreddit(SUBREDDIT_2)

print(sub1.post_requirements()['domain_blacklist'])