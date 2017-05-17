from app import application
from app.models.carrier import Carrier
from app.models.gsm_event import GsmEvent
from app.models.mobile_traffic_event import MobileTrafficEvent
from app.models.sim import Sim
from config import AppTokens
from tests import base_test_case
from tests.events.new_carrier_events_json import events_json
from tests.populate_db.populate_methods import populate_standard_test


class SaveNewCarrierEventsTestCase(base_test_case.BaseTestCase):
    """
    Unit tests for the API
    """

    def populate(self):
        """
        Populate the model with test data
        """
        # Create the default sim
        populate_standard_test()

    # Saving event test: 1 gsm observation event and 1 state record, both whit a non-existent telco
    def test_save_new_telco_events(self):
        with application.app_context():
            token = list(AppTokens.tokens.keys())[0]
            request = self.app.post("/api/events", data=dict(
                events=events_json
            ), headers={"Authorization": "token " + token})

            assert request.status_code == 201

            gsm_events = GsmEvent.query.all()
            assert len(gsm_events) == 1
            gsm_event = gsm_events[0]

            mobile_events = MobileTrafficEvent.query.all()
            assert len(mobile_events) == 1

            sim = Sim.query.filter(Sim.serial_number == "800000000000000000000").first()
            assert sim

            carrier = Carrier.query.filter(Carrier.mnc == 99, Carrier.mcc == 9999).first()
            assert carrier

            assert carrier.id == 999999

            assert sim.carrier.mnc == 99
            assert sim.carrier.mcc == 9999

            assert len(carrier.gsm_events.all()) == 1

            assert carrier.gsm_events[0].id == gsm_event.id
