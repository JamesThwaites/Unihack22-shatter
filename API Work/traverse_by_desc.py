import praw, re, json, prawcore

with open('stored_descs.json', 'r') as store:
    stored_descs = json.load(store)

#current_sub = 'news'

reddit = praw.Reddit(
    client_id='QjE7iZuv-YKAAmQVK6UcXA',
    client_secret='fuV5lGnvsghAJMEpLV5atZYXk6GGUA',
    user_agent='ShatterSimilarity:v0.0.1'
)


def getLinkedSubs(sub_name):
    if sub_name not in stored_descs:

        try:
            linked_subs = list(set(re.findall(r'r/\w+',reddit.subreddit(sub_name).description)))
            if f'r/{sub_name}' in linked_subs:
                linked_subs.remove(f'r/{sub_name}')

            stored_descs[sub_name] = [x[2:].lower() for x in linked_subs]

        except prawcore.exceptions.Redirect:
            stored_descs[sub_name] = False
            #Subreddit does not exist (402)

        except prawcore.exceptions.Forbidden:
            stored_descs[sub_name] = False
            #Subreddit is private (403)

        except prawcore.exceptions.NotFound:
            stored_descs[sub_name] = False
            #Subreddit 404

    return stored_descs[sub_name]

def populateLinkTree(origin, depth = 0):
    origin = origin.lower()

    count = 0

    new_branches = set()
    explored = set()
    queue = set(getLinkedSubs(origin))

    explored = explored.union(queue)
    while queue and count < depth:
        new_branches.clear()

        for sub_name in queue:
            print(f"Populating r/{sub_name}")
            links = getLinkedSubs(sub_name)
            if links:
                new_branches = new_branches.union(set(links))

            

        queue = new_branches.difference(explored)
        explored = explored.union(new_branches)

        count += 1

    print(f"{count} subreddits catalogued!")

for sub in stored_descs:
    if sub[sub]:
        if sub in sub[sub]:
            sub[sub].remove(sub)

#populateLinkTree('news', depth = 3)
#print(reddit.subreddit('misc').description)
#print(re.findall(r'r/\w+',reddit.subreddit('misc').description))



with open('stored_descs.json', 'w') as store:
    json.dump(stored_descs, store, indent=2)

# prawcore.exceptions.Redirect

