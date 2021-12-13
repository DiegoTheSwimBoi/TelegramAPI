import json



def getNews():
    with open('data.json', encoding='utf-8') as f:
        data=json.load(f)
        return data


