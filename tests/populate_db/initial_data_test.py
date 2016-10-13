from app import application

from tests import base_test_case
from app.models.carrier import Carrier
from manage_commands import populate


class InitialdataTestCase(base_test_case.BaseTestCase):
    def populate(self):
        pass

    def test_save_carriers(self):
        with application.app_context():
            populate()
            carriers = Carrier.query.all()
            carriersFiltered = Carrier.query.filter(Carrier.mnc == 9).all()

            assert len(carriers) == 14
            assert len(carriersFiltered) == 1
            assert carriersFiltered[0].name == "WOM"
