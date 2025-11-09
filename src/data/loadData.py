import json
import pandas as pd

def loadData():
    with open("src/data/mockData.json", "r") as f:
        data = json.load(f)
        return data
    
# I'm testing (nafisa)
if __name__ == "__main__":
    data = loadData()
    print("Data keys:", data.keys())
    print("Number of reviews:", len(data.get("reviews", [])))
    print("First 3 reviews:")
    import pprint
    pprint.pprint(data["reviews"][:3])