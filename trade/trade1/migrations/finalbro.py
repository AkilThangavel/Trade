import requests
import json
from ib_insync import *
import re






def retrieve_messages(channelid):
    headers = {
        'authorization': 'NjU2NDcxODMwMjEwNTQzNjY2.GjZ4hN.n57uUhed5xWb7huPyxlT-PSBFJhe2T3M9aV5LM'
    }
    r = requests.get(
        f'https://discord.com/api/v9/channels/{channelid}/messages?limit=2',headers=headers
        )
    jsonn = json.loads(r.text)
    return jsonn


retrieve_messages(1058040359038492712)