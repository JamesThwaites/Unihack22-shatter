import praw, re, json, prawcore, copy

with open('stored_descs.json', 'r') as store:
    stored_descs = json.load(store)

#current_sub = 'news'

reddit = praw.Reddit(
    client_id='QjE7iZuv-YKAAmQVK6UcXA',
    client_secret='fuV5lGnvsghAJMEpLV5atZYXk6GGUA',
    user_agent='ShatterSimilarity:v0.0.1'
)

class Link:
    def __init__(self,start,path=[],dir=None, old = []):
        self.path = path
        if dir != None:
            self.path.append(dir)

        self.history = old[:]
        self.history.append(start)

        self.sub = start
        self.depth = len(self.path)


def getLinkedSubs(sub_name):
    sub_name = sub_name.lower()
    if sub_name not in stored_descs:

        try:
            #print(1)
            linked_subs = list(set(re.findall(r'r/\w+',reddit.subreddit(sub_name).description)))
            #print(2)

            linked_subs = [x[2:].lower() for x in linked_subs]
            linked_subs = list(set(linked_subs))

            if sub_name in linked_subs:
                linked_subs.remove(sub_name)

            stored_descs[sub_name] = list(linked_subs)
            #print(3)

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

    depthcount = 0
    count = 0

    new_branches = set()
    explored = set()
    queue = set(getLinkedSubs(origin))

    explored.add(origin)
    explored = explored.union(queue)
    while queue and depthcount < depth:
        new_branches.clear()

        for sub_name in queue:
            print(f"Populating r/{sub_name}")
            links = getLinkedSubs(sub_name)
            if links:
                new_branches = new_branches.union(set(links))
            count += 1

            

        queue = new_branches.difference(explored)
        explored = explored.union(new_branches)
        depthcount += 1
        

    print(f"{count} subreddits catalogued!")

def getParents(sub_name, exclude = None):
    if stored_descs[sub_name] == False:
        return []

    parents = stored_descs[sub_name]['parents'][:]

    if exclude == None:
        return parents

    if exclude in parents:
        parents.remove(exclude)

    return parents

def getChildren(sub_name, exclude = None):
    if stored_descs[sub_name] == False:
        return []

    children = stored_descs[sub_name]['children'][:]

    if exclude == None:
        return children

    if exclude in children:
        children.remove(exclude)

    return children

def subredditReport(sub_name):

    if sub_name not in stored_descs:
        print("Subreddit not found!")
        return

    parents = getParents(sub_name)
    children = getChildren(sub_name)
    siblings = []
    for x in parents:
        siblings.extend(getChildren(x))
    siblings = list(set(siblings))

    print(f'{len(parents)} Parents: {parents}')
    print(f'{len(children)} Children: {children}')
    print(f'{len(siblings)} Siblings: {siblings}')


def findLinks(sub1, sub2):
    if sub1 not in stored_descs or stored_descs[sub1] == False:
        print(f'r/{sub1} not found.')
        return []

    if sub2 not in stored_descs or stored_descs[sub2] == False:
        print(f'r/{sub2} not found.')
        return []

    forward_links = [Link(sub1)]
    backward_links = [Link(sub2)]

    actual_links = []
    found_links = []
    depth = 0
    while depth < 2:
        found_path = []
        forward_links = iterForward(forward_links, sub1)
        for link in forward_links:
            #print(link.path)
            for target in backward_links:
                if link.sub == target.sub:
                    target.path.reverse()
                    found_path = link.path[:]
                    found_path.extend(target.path)
                    found_links.append(found_path[:])
                    actual_links.append(copy.deepcopy(link))
                    actual_links.append(copy.deepcopy(target))
                    target.path.reverse()
                    

        found_path = []
        backward_links = iterBackward(backward_links, sub2)
        for link in forward_links:
            for target in backward_links:
                if link.sub == target.sub:
                    target.path.reverse()
                    found_path = link.path[:]
                    found_path.extend(target.path)
                    found_links.append(found_path[:])
                    actual_links.append(copy.deepcopy(link))
                    actual_links.append(copy.deepcopy(target))
                    target.path.reverse()
                    
        depth += 1

    sub_paths = []
    for index in range(0, len(actual_links), 2):
        actual_links[index+1].history.reverse()
        sub_paths.append([*actual_links[index].history[:-1], *actual_links[index+1].history])
   
    true_paths_text = []
    true_paths = []
    counter = 0
    for sub_path in sub_paths:
        if len(set(sub_path)) == len(sub_path):
            true_paths_text.append(sub_path)
            true_paths.append(found_links[counter])
            
            print(sub_path)

        counter += 1
            
            
            

    return true_paths

def iterForward(links, origin):
    next_iter = []

    for link in links:
        if link.sub != -1:
            #up
            for parent in getParents(link.sub, exclude = origin):
                next_iter.append(Link(parent,link.path[:],1,link.history))

            #down
            for child in getChildren(link.sub, exclude = origin):
                next_iter.append(Link(child,link.path[:],0,link.history))

    return next_iter

def iterBackward(links, origin):
    next_iter = []

    for link in links:
        if link.sub != -1:
            #up
            for parent in getParents(link.sub, exclude = origin):
                next_iter.append(Link(parent,link.path[:],0,link.history))

            #down
            for child in getChildren(link.sub, exclude = origin):
                next_iter.append(Link(child,link.path[:],1,link.history))

    return next_iter


print(findLinks('jokes','tifu'))

#subredditReport('news')


#for sub in stored_descs:
#    if stored_descs[sub] != False:
#        stored_descs[sub] = {'children' : list(set(stored_descs[sub])), 'parents' : list()}


'''
temp = {}

for sub in stored_descs:
    if stored_descs[sub] != False:
        for child in stored_descs[sub]['children']:
            if child not in stored_descs:
                temp[child] = {'children' : list(), 'parents' : list()}
                temp[child]['parents'].append(sub)

            elif stored_descs[child] != False:
                stored_descs[child]['parents'].append(sub)

stored_descs = stored_descs | temp
'''

#populateLinkTree('evenwithcontext', depth = 3)
#print(reddit.subreddit('misc').description)
#print(re.findall(r'r/\w+',reddit.subreddit('misc').description))



with open('stored_descs.json', 'w') as store:
    json.dump(stored_descs, store, indent=2)

# prawcore.exceptions.Redirect

