from datetime import datetime

from app import app
from . import base_test_case


class APITestCase(base_test_case.BaseTestCase):
    '''
    Unit tests for the API
    '''
    def test_registration(self):
        from app.models.sim import Sim
        from app.models.device import Device

        with app.app_context():
            date = datetime.now().date()
            request = self.app.post('/api/registration', data=dict(
                    serial_number=123,
                    carrier_id=456,
                    brand="brand test",
                    board="board test",
                    build_id="build id test",
                    device="device test",
                    hardware="hardware test",
                    manufacturer="manufacturer test",
                    model="model test",
                    release="release test",
                    release_type="release type test",
                    product="product test",
                    sdk=4
            ))
            assert request.status_code == 201
            #assert SIM
            sim = Sim.query.all()
            assert len(sim) == 1
            assert sim[0].serial_number == 123
            assert sim[0].creation_date == date

            #assert Device
            devices = Device.query.all()
            assert len(devices) == 1
            assert devices[0].brand == "brand test"
            assert devices[0].board == "board test"
            assert devices[0].build_id == "build id test"
            assert devices[0].device == "device test"
            assert devices[0].hardware == "hardware test"
            assert devices[0].manufacturer == "manufacturer test"
            assert devices[0].model == "model test"
            assert devices[0].release == "release test"
            assert devices[0].release_type == "release type test"
            assert devices[0].product == "product test"
            assert devices[0].sdk == 4

            # TODO: Cambiar última comprobación por una diferencia de tiempo en vez de la fecha