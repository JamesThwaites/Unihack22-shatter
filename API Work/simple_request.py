import json, requests


auth = requests.auth.HTTPBasicAuth('QjE7iZuv-YKAAmQVK6UcXA', 'fuV5lGnvsghAJMEpLV5atZYXk6GGUA')

data = {
    'grant_type' : 'client_credentials',
    'redirect_uri' : 'http://localhost:5555'
}

headers = {'User-Agent' : 'ShatterSimilarity/0.0.1'}


res = requests.post('https://www.reddit.com/api/v1/access_token',
                    auth=auth, data=data, headers=headers)

TOKEN = res.json()["access_token"]
print(TOKEN)

headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}
print(headers)

with open('simple_request_store.json', 'w') as store: 
    res = requests.get("https://oauth.reddit.com/r/news/about", headers=headers)
    json.dump(res.json(),store, indent = 4)


# DO LAST
res = requests.post('https://www.reddit.com/api/v1/revoke_token', auth=auth, data={'token': TOKEN, 'token_type_hint' : 'access_token'})