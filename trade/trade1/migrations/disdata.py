import requests
import json

channelIds = [738943464259059752, 952916697008984154, 1058040359038492712]
def retrieve_messages(channelid):
    headers = {
        'authorization': 'NjU2NDcxODMwMjEwNTQzNjY2.GjZ4hN.n57uUhed5xWb7huPyxlT-PSBFJhe2T3M9aV5LM'
    }
    r = requests.get(
        f'https://discord.com/api/v9/channels/{channelid}/messages?limit=50',headers=headers
        )
    jsonn = json.loads(r.text)
    return (jsonn)


print(retrieve_messages(972215994770673664))