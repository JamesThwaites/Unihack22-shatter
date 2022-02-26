import json

with open("sample.json", "r") as sample:
    
    obj = json.load(sample)
    print(obj)

print(obj['similarities'])