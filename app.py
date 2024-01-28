from crypt import methods
from flask import Flask, Response, jsonify, request
from flask_cors import CORS
from encounter_generator import EncounterGenerator
from models.encounter import Encounter
from typing import List


app = Flask(__name__)
CORS(app)

@app.route('/')
def home_page():
    return ""

@app.route('/encounters', methods=["POST"])
def generate_encounters():
    csv_string = request.form.get("csv")
    if csv_string == None:
        return Response("Record not found", status=400)
    ec = EncounterGenerator()
    events = ec.parse_csv(csv_string)
    grouped_events = ec.group_by_pt(events)
    all_encounters: List[Encounter] = []
    for pt_id, events in grouped_events.items():
        pt_encounters = ec.generate_encounters(events)
        for encounter in pt_encounters:
            all_encounters.append(encounter)
    output = ec.write_to_csv(all_encounters)
    return jsonify(output)


