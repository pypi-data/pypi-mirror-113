import unittest
from tolaatcom_nhc import nethamishpat

class SimpleTestCase(unittest.TestCase):

    def setUp(self):
        print('set up')

    def test_pdf_1(self):
        api = nethamishpat.NethamishpatApiClient()
        r = api.parse_everything({'CaseType': 'n', 'CaseDisplayIdentifier': '52512-02-18'})
        self.assertEqual(r['case']['CourtName'].strip(), 'מחוזי מרכז')
        self.assertEqual(r['case']['CaseID'], 75263135)
        self.assertEqual(2, len(r['sittings']))
        self.assertEqual(5, len(r['decisions']))
        self.assertEqual(0, len(r['verdicts']))