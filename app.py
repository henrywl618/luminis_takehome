from flask import Flask, Response, jsonify, request
import werkzeug.exceptions
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
    try:
        csv_string = request.form.get("csv")
        if csv_string == None:
            return Response("CSV not found", status=400)
        ec = EncounterGenerator()
        events = ec.parse_csv(csv_string)
        facility_events = ec.group_by_facility(events)
        all_encounters: List[Encounter] = []
        for facility, f_events in facility_events.items():
            patient_events = ec.group_by_pt(f_events)
            for pt_id, p_events in patient_events.items():
                pt_encounters = ec.generate_encounters(p_events)
                for encounter in pt_encounters:
                    all_encounters.append(encounter)
        output = ec.write_to_csv(all_encounters)
        return jsonify(output)
    except:
        raise werkzeug.exceptions.BadRequest 

@app.errorhandler(werkzeug.exceptions.BadRequest)
def handle_bad_request(e):
    return 'Invalid CSV!', 400

@app.errorhandler(werkzeug.exceptions.NotFound)
def handle_not_found(e):
    return '404 Not Found!', 404


