from unittest import TestCase
from encounter_generator import EncounterGenerator

from models.event import Event


class EncounterGeneratorTests(TestCase):
    def setUp(self):
        self.ec = EncounterGenerator()
        self.events = [
            Event(
                "123456",
                "Sacred Heart",
                "ER",
                "Chest Pain",
                "Admission",
                "2017-02-13T06:01:00-05:00",
            ),
            Event(
                "123456",
                "Sacred Heart",
                "Inpatient",
                "Angina",
                "Discharge",
                "2017-02-16T06:01:00-05:00",
            ),
            Event(
                "654321",
                "Sacred Heart",
                "ER",
                "Chest Pain",
                "Admission",
                "2017-03-13T06:01:00-05:00",
            ),
            Event(
                "654321",
                "Sacred Heart",
                "ER",
                "Chest Pain",
                "Discharge",
                "2017-03-16T06:01:00-05:00",
            ),
        ]

    def test_group_by_pt(self):
        """It tests that Events are grouped by patient id."""
        grouped_events = self.ec.group_by_pt(self.events)
        self.assertIsNotNone(grouped_events.get("123456"))
        self.assertEqual(len(grouped_events["123456"]), 2)
        self.assertIsNotNone(grouped_events.get("654321"))
        self.assertEqual(len(grouped_events["654321"]), 2)

    def test_generate_encounters(self):
        """It tests that Encounters are generated."""
        # Get first two events for pt_id '123456'
        events = self.events[:2]
        encounters = self.ec.generate_encounters(events)
        self.assertEqual(len(encounters), 1)
        self.assertEqual(encounters[0].begin_time, "2017-02-13T06:01:00-05:00")
        self.assertEqual(encounters[0].end_time, "2017-02-16T06:01:00-05:00")
        self.assertEqual(encounters[0].pt_complaint, "Angina")
        self.assertEqual(encounters[0].enc_class, "Inpatient")
        self.assertEqual(encounters[0].stay_length, "72.0")

    def test_multiple_events(self):
        """It tests an valid Encounter is generated when there are more then two events"""
        # Get first two events for pt_id '123456'
        events = self.events[:2]
        events.append(
            Event(
                "123456",
                "Sacred Heart",
                "Inpatient",
                "Angina",
                "Admission",
                "2017-02-15T06:01:00-05:00",
            ),
        )
        encounters = self.ec.generate_encounters(events)
        self.assertEqual(len(encounters), 1)
        self.assertEqual(encounters[0].begin_time, "2017-02-13T06:01:00-05:00")
        self.assertEqual(encounters[0].end_time, "2017-02-16T06:01:00-05:00")
        self.assertEqual(encounters[0].pt_complaint, "Angina")
        self.assertEqual(encounters[0].enc_class, "Inpatient")
        self.assertEqual(encounters[0].stay_length, "72.0")

    def test_same_pt_multiple_encounters(self):
        """It tests multiple Encounters are generated for one patient."""
        # Mock another admission/discharge event for pt "123456"
        self.events[2].pt_identifier = "123456"
        self.events[3].pt_identifier = "123456"
        encounters = self.ec.generate_encounters(self.events)
        self.assertEqual(len(encounters), 2)
        self.assertEqual(encounters[0].begin_time, "2017-02-13T06:01:00-05:00")
        self.assertEqual(encounters[0].end_time, "2017-02-16T06:01:00-05:00")
        self.assertEqual(encounters[1].begin_time, "2017-03-13T06:01:00-05:00")
        self.assertEqual(encounters[1].end_time, "2017-03-16T06:01:00-05:00")
