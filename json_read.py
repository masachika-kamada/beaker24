import json


with open("./prefecture.json", mode="r", encoding="utf-8") as f:
    raw = f.read()
    print(raw)
    d = json.loads(raw)

print(d)
