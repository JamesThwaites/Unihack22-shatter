import json

with open("nodes.json", "r") as sample:
    
    obj = json.load(sample)
    
with open("nodes.json", "w") as sample:
    
    json.dump(obj, sample, indent = 4)