import json

with open("sample.json", "r") as sample:
    
    obj = json.load(sample)
    print(obj)

for sub in obj:
    print(obj[sub]['sub_name'])