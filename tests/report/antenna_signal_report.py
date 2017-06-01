from datetime import datetime, timedelta

from app import application, db
from app.models.carrier import Carrier
from app.models.gsm_event import GsmEvent
from app.models.antenna import Antenna
from app.report.antenna_signal_report_generation import signal_strength_mean_for_antenna
from tests import base_test_case

delta = 0.01


class AntennaSignalReportTestCase(base_test_case.BaseTestCase):
    '''
    Unit tests for the API
    '''

    def populate(self):
        #antennas
        antenna1 = Antenna(carrier_id=1)
        antenna2 = Antenna(carrier_id=2)
        antenna3 = Antenna(carrier_id=2)

        # carriers
        carrier1 = Carrier(name="test_carrier_1")
        carrier2 = Carrier(name="test_carrier_2")

        carrier1.antennas.append(antenna1)
        carrier2.antennas.append(antenna2)
        carrier2.antennas.append(antenna3)

        # GSM events
        event1 = GsmEvent(date=datetime.now() + timedelta(days=-2), antenna_id=1,
                          signal_strength_mean=10, signal_strength_size=1)
        event2 = GsmEvent(date=datetime.now(), antenna_id=1,
                          signal_strength_mean=1, signal_strength_size=2)
        event3 = GsmEvent(date=datetime.now(), antenna_id=2,
                          signal_strength_mean=10, signal_strength_size=1)
        event4 = GsmEvent(date=datetime.now(), antenna_id=3,
                          signal_strength_mean=0, signal_strength_size=2)
        event5 = GsmEvent(date=datetime.now(), antenna_id=3,
                          signal_strength_mean=-20, signal_strength_size=1)

        carrier1.gsm_events = [event1, event2]
        carrier2.gsm_events = [event3, event4, event5]

        db.session.add(carrier1)
        db.session.add(carrier2)
        db.session.commit()

    def test_signal_report_generation(self):
        with application.app_context():
            antenna_network_report = signal_strength_mean_for_antenna()
            self.assertEqual(len(antenna_network_report), 3)
            antenna_network_report.sort(key=lambda d: (d['carrier_id'], d['antenna_id']))
            antenna_network_report_expected = [
                {'carrier_id': 1, 'antenna_id': 1, 'observations': 3, 'signal_mean': 6.20408517},
                {'carrier_id': 2, 'antenna_id': 2, 'observations': 1, 'signal_mean': 10},
                {'carrier_id': 2, 'antenna_id': 3, 'observations': 3, 'signal_mean': -1.739251973}]

            for i in range(3):
                self.assertEqual(antenna_network_report[i]['carrier_id'],
                                 antenna_network_report_expected[i]['carrier_id'])
                self.assertEqual(antenna_network_report[i]['antenna_id'],
                                 antenna_network_report_expected[i]['antenna_id'])
                self.assertEqual(antenna_network_report[i]['observations'],
                                 antenna_network_report_expected[i]['observations'])
                self.assertAlmostEqual(antenna_network_report[i]['signal_mean'],
                                       antenna_network_report_expected[i]['signal_mean'],
                                       delta=delta)


    def test_signal_report_filters_events_by_date(self):
        with application.app_context():
            antenna_network_report = signal_strength_mean_for_antenna(
                min_date=datetime.now() + timedelta(days=-1))
            self.assertEqual(len(antenna_network_report), 3)
            antenna_network_report.sort(key=lambda d: (d['carrier_id'], d['antenna_id']))
            antenna_network_report_expected = [
                {'carrier_id': 1, 'antenna_id': 1, 'observations': 2, 'signal_mean': 1},
                {'carrier_id': 2, 'antenna_id': 2, 'observations': 1, 'signal_mean': 10},
                {'carrier_id': 2, 'antenna_id': 3, 'observations': 3, 'signal_mean': -1.739251973}]

            for i in range(3):
                self.assertEqual(antenna_network_report[i]['carrier_id'],
                                 antenna_network_report_expected[i]['carrier_id'])
                self.assertEqual(antenna_network_report[i]['antenna_id'],
                                 antenna_network_report_expected[i]['antenna_id'])
                self.assertEqual(antenna_network_report[i]['observations'],
                                 antenna_network_report_expected[i]['observations'])
                self.assertAlmostEqual(antenna_network_report[i]['signal_mean'],
                                       antenna_network_report_expected[i]['signal_mean'],
                                       delta=delta)
