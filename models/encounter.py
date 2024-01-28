class Encounter:
    def __init__(
        self,
        pt_identifier: str,
        facility: str,
        pt_complaint: str,
        enc_class: str,
        begin_time: str,
        end_time: str,
        stay_length: str,
    ):
        self.pt_identifier = pt_identifier
        self.facility = facility
        self.pt_complaint = pt_complaint
        self.enc_class = enc_class
        self.begin_time = begin_time
        self.end_time = end_time
        self.stay_length = stay_length
