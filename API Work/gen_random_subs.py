import json, random

def gen(num):
    with open('stored_descs.json', 'r') as store:
        stored_descs = json.load(store)
        
    sub_list = [key for key in stored_descs]
        
    poses = []
    for i in range(num):
        a = random.randrange(0,len(sub_list))
        while a in poses:
            a = random.randrange(0,len(sub_list))
        poses.append(a)
        
    subs = []
    for i in poses:
        subs.append(sub_list[i])
        
    print(','.join(subs))
    return ','.join(subs)
 
if __name__ == '__main__':
    gen(5)