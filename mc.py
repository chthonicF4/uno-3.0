
import requests , json

data = requests.get("https://api.mcsrvstat.us/2/mc.chthonicf4.xyz:30000")
data = data.text
data = json.loads(data)
print(data["online"],data["players"],data['motd']['clean'])