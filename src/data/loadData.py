import json
import pandas as pd
import os

def loadData():
    # Get the directory of this file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, "mockData.json")

    with open(json_path, "r") as f:
        data = json.load(f)
        return data
    


# # Tester for Nafisa
# if __name__ == "__main__":
#     data = loadData()
#     print(type(data))         
#     print(data.keys())   
#     print(data["ratings"][:2])     


