import json
import csv
import os.path
import sys
import shutil

# Load Data
TEMP_FILE = 'draft_in_progress.csv'

class dummyRequest():
    def __init__(self, method, json=None) -> None:
        self.method = method
        self.json = json
    
    def get_json(self):
        return self.json


def load_data(file_name):
    if os.path.exists(TEMP_FILE):
        with open(os.path.join(sys.path[0],TEMP_FILE), mode ='r') as file:
            return [json.dumps(d) for d in csv.DictReader(file)]
    else:
        try:
            with open(os.path.join(sys.path[0], file_name), mode ='r') as file:
                shutil.copyfile(os.path.join(sys.path[0], file_name), os.path.join(sys.path[0],TEMP_FILE))    
                return [json.dumps(d) for d in csv.DictReader(file)]
        except FileNotFoundError:
            print(f'Missing File {file_name}')


def overwrite_csv(new_json, file_name):
    with open(os.path.join(sys.path[0], file_name),"w",newline="") as f:  
            title = list(new_json[0].keys())
            cw = csv.DictWriter(f,title,delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            cw.writeheader()
            cw.writerows(new_json)

def players(request):
    print("Players endpoint reached...")
    if request.method == "GET":
        json_player_list = load_data('players_fp_hppr.csv')
        return json_player_list
    if request.method == "POST":
        received_data = request.get_json()
        print(f"received data: {received_data}")
        new_json = load_data('players_fp_hppr.csv')
        new_json = [json.loads(x) for x in new_json if json.loads(x)["PLAYER NAME"] != received_data['player']]
        overwrite_csv(new_json, 'draft_in_progress.csv')
        return f"{received_data['player']} was drafted"
    
if __name__ == "__main__":
    # Make dummy request GET
    dummy_get = dummyRequest("GET")
    # Make dummy request POST
    dummy_post = dummyRequest("POST", {'player': 'Christian McCaffrey'})
    response = players(dummy_post)
    print(response)