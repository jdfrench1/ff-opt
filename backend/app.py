from flask import Flask, request
import flask
from flask_cors import CORS
import json
import csv
import os.path
import sys
import shutil
from opp_cost import best_options
import pandas as pd
import logging

logging.basicConfig(filename='record.log', level=logging.DEBUG)

# Load Data
TEMP_ECR = 'ecr_in_progress.csv'
TEMP_MY_RANK = 'my_rank_in_progress.csv'
turn = 0

def load_data(file_name, temp_file_name):
    if os.path.exists(os.path.join(sys.path[0],temp_file_name)):
        with open(os.path.join(sys.path[0],temp_file_name), mode ='r') as file:
            return [json.dumps(d) for d in csv.DictReader(file)]
    else:
        try:
            with open(os.path.join(sys.path[0], file_name), mode ='r') as file:
                shutil.copyfile(os.path.join(sys.path[0], file_name), os.path.join(sys.path[0],temp_file_name))    
                return [json.dumps(d) for d in csv.DictReader(file)]
        except FileNotFoundError:
            print(f'Missing File {file_name}')


def overwrite_csv(new_json, file_name):
    with open(os.path.join(sys.path[0], file_name),"w",newline="") as f:  
            title = list(new_json[0].keys())
            cw = csv.DictWriter(f,title,delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            cw.writeheader()
            cw.writerows(new_json)


app = Flask(__name__)
CORS(app)

@app.route('/')
def main():
  # showing different logging levels
  app.logger.debug("debug log info")
  app.logger.info("Info log information")
  app.logger.warning("Warning log info")
  app.logger.error("Error log info")
  app.logger.critical("Critical log info")
  return "testing logging levels."

@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/players", methods=["GET", "POST", "DELETE"])
def players():
    global turn 
    print("Players endpoint reached...")
    if request.method == "GET":
        json_player_list = load_data('players_fp_hppr.csv', TEMP_ECR)
        load_data('my_hppr_rank.csv', TEMP_MY_RANK)
        return json_player_list
    
    elif request.method == "POST":
        received_data = request.get_json()
        print(f"received data: {received_data}")

        new_ecr_json = load_data('players_fp_hppr.csv', TEMP_ECR)
        new_ecr_json = [json.loads(x) for x in new_ecr_json if json.loads(x)["PLAYER NAME"] != received_data['player']]
        overwrite_csv(new_ecr_json, TEMP_ECR)

        new_rank_json = load_data('my_hppr_rank.csv', TEMP_MY_RANK)
        new_rank_json = [json.loads(x) for x in new_rank_json if json.loads(x)["Player Name"] != received_data['player']]
        overwrite_csv(new_rank_json, TEMP_MY_RANK)
        turn += 1
        return {"turn": turn,
                "message": f"{received_data['player']} was drafted"}
    
    elif request.method == "DELETE":
        print(f'Reset Requested')
        if os.path.exists(TEMP_ECR):
            os.remove(TEMP_ECR)
        else:
            print("The file does not exist")

        if os.path.exists(TEMP_MY_RANK):
            os.remove(TEMP_MY_RANK)
        else:
            print("The file does not exist")

        turn = 0
        return f"Reset request processed"

@app.route("/recommendation", methods=["GET"])
def recommendation():
    global turn
    my_temp_rank = pd.read_csv(TEMP_MY_RANK)
    temp_ecr = pd.read_csv(TEMP_ECR)
    return best_options(turn, 12, my_temp_rank, temp_ecr)


if __name__ == "__main__":
    
    app.run("localhost", 5000, debug=True)