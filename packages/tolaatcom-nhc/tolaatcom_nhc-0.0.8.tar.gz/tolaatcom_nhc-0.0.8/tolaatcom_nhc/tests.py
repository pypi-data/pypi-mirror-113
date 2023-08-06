import unittest
from tolaatcom_nhc import nethamishpat
from tolaatcom_nhc import pdf_generator

class SimpleTestCase(unittest.TestCase):

    def setUp(self):
        print('set up')

    def test_metadata(self):
        api = nethamishpat.NethamishpatApiClient()
        r = api.parse_everything({'CaseType': 'n', 'CaseDisplayIdentifier': '52512-02-18'})
        self.assertEqual(r['case']['CourtName'].strip(), 'מחוזי מרכז')
        self.assertEqual(r['case']['CaseID'], 75263135)
        self.assertEqual(2, len(r['sittings']))
        self.assertEqual(5, len(r['decisions']))
        self.assertEqual(0, len(r['verdicts']))

    def test_metadata2(self):
        api = nethamishpat.NethamishpatApiClient()
        r = api.parse_everything({'CaseType': 'n', 'CaseDisplayIdentifier': '52512-02-18'})
        from os.path import expanduser
        with open(expanduser('~/a.pdf'), 'wb') as f:
            f.write(r['decisions'][4]['pdf'].read())
        print('done')

    def test_does_not_exist(self):
        api = nethamishpat.NethamishpatApiClient()
        r = api.parse_everything({'CaseType': 'n', 'CaseDisplayIdentifier': '26078-04-17'})
        self.assertIsNone(r)
