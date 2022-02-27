from math import log
import json, copy
import gen_random_subs

parent = [1]
child = [0]
grandparent = [1, 1]
grandchild = [0, 0]
sibling = [1, 0]
spouse = [0, 1]
uncle = [1, 1, 0]
sibpar = [1, 0, 1]
greatgp = [1, 1, 1]
greatgc = [0, 0, 0]


scores = {
    (1) : 10,
    (0) : 10,
    (1, 1) : 6,
    (0, 0) : 6,
    (1, 0) : 8,
    (0, 1) : 5,
    (1, 1, 0) : 2,
    (1, 1, 1) : 3,
    (0, 0, 0) : 3
}


class Link:
    def __init__(self,start,path=[],dir=None, old = []):
        self.path = path
        if dir != None:
            self.path.append(dir)

        self.history = old[:]
        self.history.append(start)

        self.sub = start
        self.depth = len(self.path)
        


def getParents(sub_name, stored_descs, exclude = None):
    if stored_descs[sub_name] == False:
        return []

    parents = stored_descs[sub_name]['parents'][:]

    if exclude == None:
        return parents

    if exclude in parents:
        parents.remove(exclude)

    return parents

def getChildren(sub_name, stored_descs, exclude = None):
    if stored_descs[sub_name] == False:
        return []

    children = stored_descs[sub_name]['children'][:]

    if exclude == None:
        return children

    if exclude in children:
        children.remove(exclude)

    return children


def findLinks(sub1, sub2):
    
    with open('stored_descs.json', 'r') as store:
        stored_descs = json.load(store)
        
    
    if sub1 not in stored_descs or stored_descs[sub1] == False:
        #print(f'r/{sub1} not found.') #debug
        return []

    if sub2 not in stored_descs or stored_descs[sub2] == False:
        #print(f'r/{sub2} not found.') #debug
        return []

    forward_links = [Link(sub1)]
    backward_links = [Link(sub2)]

    actual_links = []
    found_links = []
    depth = 0
    while depth < 2:
        found_path = []
        forward_links = iterForward(forward_links, sub1, stored_descs)
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
        backward_links = iterBackward(backward_links, sub2, stored_descs)
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
            
            #print(sub_path) #debug

        counter += 1
            
    return true_paths

def iterForward(links, origin, stored_descs):
    next_iter = []

    for link in links:
        if link.sub != -1:
            #up
            for parent in getParents(link.sub, stored_descs, exclude = origin):
                next_iter.append(Link(parent,link.path[:],1,link.history))

            #down
            for child in getChildren(link.sub, stored_descs, exclude = origin):
                next_iter.append(Link(child,link.path[:],0,link.history))

    return next_iter

def iterBackward(links, origin, stored_descs):
    next_iter = []

    for link in links:
        if link.sub != -1:
            #up
            for parent in getParents(link.sub, stored_descs, exclude = origin):
                next_iter.append(Link(parent,link.path[:],0,link.history))

            #down
            for child in getChildren(link.sub, stored_descs, exclude = origin):
                next_iter.append(Link(child,link.path[:],1,link.history))

    return next_iter


def scoreLinks(links):
    ratings = []
    for link in links:
        if tuple(link) in scores:
            ratings.append(scores[tuple(link)])
        else:
            ratings.append(1)
            
    return ratings


def calculateSimilarity(ratings):
    count = {}
    for rating in ratings:
        if rating in count:
            count[rating] += 1
        else:
            count[rating] = 1
            
    total = 0
    for score in count:
        total += int(score*10)*log(count[score])

    if 10 in count:
        total *= 1.8
    elif 8 in count or 6 in count or 5 in count:
        total *= 1.5

    #print(total, len(ratings))
    
    return min(int(total),100)
    


def compareTwoSubs(sub1, sub2):
    links = findLinks(sub1, sub2)
    #print(links)
    
    ratings = scoreLinks(links)
    
    return calculateSimilarity(ratings)



def genPairs(sub_list):
    pairs = []
    for i in range(len(sub_list) - 1):
        for j in range(i+1, len(sub_list)):
            pairs.append((sub_list[i], sub_list[j]))
            
    return pairs

def compareSubList(sub_list):
    sub_list = sub_list.split(',')
    pairs = genPairs(sub_list)
    
    sub_names_and_ids = {sub_list[x] : x  for x in range(len(sub_list))}
    
    with open('subreddit_sizes.json', 'r') as sizes:
        data = json.load(sizes)
    
    obj1 = {"nodes" : [], "links" : []}
    for sub in sub_list:
        obj1['nodes'].append({"id": sub_names_and_ids[sub], "name": sub, "size": data[sub]})
    
    
    for pair in pairs:
        rating = compareTwoSubs(pair[0],pair[1])
        
        if rating > 0:
            print(f'{pair[0]} + {pair[1]}: {rating}')
            obj1['links'].append({"source" : sub_names_and_ids[pair[0]], "target" : sub_names_and_ids[pair[1]], "similarity" : rating})
    
    with open("nodesample.json", 'w') as nodes:
        json.dump(obj1, nodes)
    
    
#compareSubList('fantasy,books,scifi')
    
compareSubList(gen_random_subs.gen(20))