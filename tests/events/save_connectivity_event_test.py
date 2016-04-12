from datetime import datetime

from app import app
from app.models.connectivity_event import ConnectivityEvent
from tests import base_test_case
from tests.events.one_event_in_type_json import events_json
from config import AppTokens


class SaveConnectivityEventTestCase(base_test_case.BaseTestCase):
    '''
    Unit tests for the API
    '''

    def populate(self):
        '''
        Populate the model with test data
        '''
        pass

    # test de guardado de eventos: 1 wifi traffic event y 2 state change event
    def test_save_normal_events(self):
        with app.app_context():
            request = self.app.post('/api/send_file', data=dict(
                    events=events_json
            ), headers={'Authorization': 'token ' + list(AppTokens.tokens.keys())[0]})

            assert request.status_code == 201
            connectivity_events = ConnectivityEvent.query.all()
            assert len(connectivity_events) == 1

            connectivity_event = connectivity_events[0]

            assert connectivity_event.available == True
            assert connectivity_event.connected == True
            assert connectivity_event.connection_type == 6
            assert connectivity_event.detailed_state == 4
            assert connectivity_event.date == datetime.fromtimestamp(1330641527540 / 1000).date()
            assert connectivity_event.app_version_code == "0.0a"

            assert connectivity_event.sim.serial_number == "8000000000000000000"
            assert connectivity_event.device.device_id == "8000000000000000000"
