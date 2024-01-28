import csv
from io import StringIO
from datetime import datetime
from models.event import Event
from models.encounter import Encounter
from typing import TypeAlias, List, Dict

GroupedEvents: TypeAlias = Dict[str, List[Event]]


class EncounterGenerator:
    events: List[Event]

    def __init__(self) -> None:
        self.events = []

    def parse_csv(self, csv_string: str) -> List[Event]:
        reader = csv.DictReader(StringIO(csv_string), delimiter=",")
        for row in reader:
            self.events.append(
                Event(
                    row["PATIENT_IDENTIFIER"],
                    row["FACILITY"],
                    row["PATIENT_CLASS"],
                    row["PATIENT_COMPLAINT"],
                    row["EVENT_TYPE"],
                    row["EVENT_TIME"],
                )
            )
        return self.events

    def write_to_csv(self, encounters: List[Encounter]) -> str:
        header = [
            "PatientIdentifier",
            "Facility",
            "PatientComplaint",
            "EncounterClass",
            "EncounterBeginTime",
            "EncounterEndTime",
            "Length of Stay (hrs)",
        ]
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(header)
        for encounter in encounters:
            writer.writerow(
                [
                    encounter.pt_identifier,
                    encounter.facility,
                    encounter.pt_complaint,
                    encounter.enc_class,
                    encounter.begin_time,
                    encounter.end_time,
                    encounter.stay_length,
                ]
            )
        return output.getvalue()

    def group_by_pt(self, events: List[Event]) -> GroupedEvents:
        """Groups events by patient identifier

        Args:
            events (List[Event])

        Returns:
            GroupedEvents: Dict with patient id as the key and a list of events
            as the value.
        """
        grouped_events: GroupedEvents = {}
        for event in events:
            pt_id = event.pt_identifier
            if pt_id in grouped_events:
                grouped_events[pt_id].append(event)
            else:
                grouped_events[pt_id] = [event]
        return grouped_events

    def generate_encounters(self, events: List[Event]) -> List[Encounter]:
        """Generates encounters by the earliest
        admission event and subsequent discharge.

        Args:
            events (List[Event])

        Returns:
            List[Encounter]
        """
        start_event: Event | None = None
        encounters: List[Encounter] = []
        events.sort(key=lambda event: event.event_time)
        for event in events:
            if not start_event and event.event_type == "Admission":
                start_event = event
            elif event.event_type == "Discharge":
                start_time = start_event.event_time if start_event else "N/A"
                stay_length_hrs: str
                if start_event:
                    stay_length_sec = (
                        datetime.fromisoformat(event.event_time)
                        - datetime.fromisoformat(start_event.event_time)
                    ).total_seconds()
                    stay_length_hrs = str(round(stay_length_sec / (60 * 60), 2))
                else:
                    stay_length_hrs = "N/A"

                encounter = Encounter(
                    event.pt_identifier,
                    event.facility,
                    event.pt_complaint,
                    event.pt_class,
                    start_time,
                    event.event_time,
                    stay_length_hrs,
                )
                start_event = None
                encounters.append(encounter)
        return encounters
