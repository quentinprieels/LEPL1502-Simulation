import unittest
from main.treatment.ReaderCSV import ReaderCSV


class ReaderCSVTests(unittest.TestCase):
    def setUp(self):
        self.test_csv = ReaderCSV('../data/exemple.csv', 'exemple', ['S1, S2, S3, S4'])

    def test_accessors(self):
        self.assertEqual(self.test_csv.getPath(), '../data/exemple.csv')
        self.assertEqual(self.test_csv.getName(), 'exemple')
        self.assertEqual(self.test_csv.getNumberSignals(), 4)
        self.assertEqual(self.test_csv.getSignalsNames(), ['S1, S2, S3, S4'])
        self.assertEqual(self.test_csv.getSignalsUnits(), ['kV', 'pV', 'mV', 'V'])
        self.assertEqual(self.test_csv.getPreferredUnit(), 'V')
        self.assertEqual(self.test_csv.getAxisUnits(), ['ms', 'V'])
        self.assertEqual(self.test_csv.getAxisNames(), ['Temps', 'Tension'])

    def test_setName(self):
        self.test_csv.setName('nouveau nom')
        self.assertEqual(self.test_csv.getName(), 'nouveau nom')

    def test_setPreferredUnit_1(self):
        self.test_csv.setPreferredUnit('iV')
        self.assertEqual(self.test_csv.getPreferredUnit(), 'iV')
        self.assertEqual(self.test_csv.getAxisUnits(), ['ms', 'iV'])
        self.assertEqual(self.test_csv.getSignalsUnits(), ['kV', 'pV', 'mV', 'V'])

    def test_setPreferredUnit_2(self):
        self.test_csv.setPreferredUnit('mL')
        self.assertEqual(self.test_csv.getPreferredUnit(), 'V')
        self.assertEqual(self.test_csv.getAxisUnits(), ['ms', 'V'])

    def test_setAxisNames(self):
        self.test_csv.setAxisNames('axe 1', 'axe 2')
        self.assertEqual(self.test_csv.getAxisNames(), ['axe 1', 'axe 2'])


if __name__ == '__main__':
    unittest.main()
