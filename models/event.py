class Event:
    def __init__(
        self,
        pt_identifier: str,
        facility: str,
        pt_class: str,
        pt_complaint: str,
        event_type: str,
        event_time: str,
    ):
        self.pt_identifier = pt_identifier
        self.facility = facility
        self.pt_class = pt_class
        self.pt_complaint = pt_complaint
        self.event_type = event_type
        self.event_time = event_time

    def __repr__(self):
        return f"ID: {self.pt_identifier}, Facility: {self.facility}, Class: {self.pt_class}"
