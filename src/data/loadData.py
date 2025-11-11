import json
import pandas as pd

def loadData():
    with open("data/mockData.json", "r") as f:
        data = json.load(f)
        return data
    


# # Tester for Nafisa
# if __name__ == "__main__":
#     data = loadData()
#     print(type(data))         
#     print(data.keys())   
#     print(data["ratings"][:2])     


