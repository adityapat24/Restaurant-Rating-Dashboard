import json
import pandas as pd

def loadData():
    with open("data/mockData.json", "r") as f:
        data = json.load(f)
        return data