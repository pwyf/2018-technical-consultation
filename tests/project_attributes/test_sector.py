from os.path import dirname, join, realpath
from unittest import TestCase

from bdd_tester import bdd_tester
from lxml import etree


class TestSector(TestCase):
    def setUp(self):
        self.FILEPATH = dirname(realpath(__file__))
        steps_path = join(self.FILEPATH, '..', '..', 'test_definitions',
                          'step_definitions.py')
        feature_path = join(self.FILEPATH, '..', '..', 'test_definitions',
                            'project_attributes', '20_sector.feature')

        self.codelists = {'Sector': ['11110', '11120']}
        tester = bdd_tester(steps_path)
        self.feature = tester.load_feature(feature_path)
        for test in self.feature.tests:
            # remove the current data test
            test.steps.pop(0)
        self.test = self.feature.tests[0]

    def test_sector_is_present(self):
        xml = '''
        <iati-activity>
          <sector code="11110"/>
        </iati-activity>
        '''

        activity = etree.fromstring(xml)
        result = self.test(activity)

        assert result is True

    def test_sector_not_present(self):
        xml = '''
        <iati-activity>
        </iati-activity>
        '''

        activity = etree.fromstring(xml)
        result = self.test(activity)

        assert result is False

    def test_sector_uses_dac_no_vocab(self):
        xml = '''
        <iati-activity>
          <sector code="11110"/>
        </iati-activity>
        '''

        activity = etree.fromstring(xml)
        test = self.feature.tests[1]
        result = test(activity, codelists=self.codelists)

        assert result is True

    def test_sector_uses_dac_and_vocab(self):
        xml = '''
        <iati-activity>
          <sector vocabulary="{}" code="11110"/>
        </iati-activity>
        '''

        test = self.feature.tests[1]
        for vocab in ["DAC", "1"]:
            activity = etree.fromstring(xml.format(vocab))
            result = test(activity, codelists=self.codelists)

            assert result is True

    def test_sector_does_not_use_dac(self):
        xml = '''
        <iati-activity>
          <sector vocabulary="99" code="11110"/>
        </iati-activity>
        '''

        activity = etree.fromstring(xml)
        test = self.feature.tests[1]
        result = test(activity, codelists=self.codelists)

        assert result is False

    def test_multiple_sector_vocabs(self):
        xml = '''
        <iati-activity>
          <sector vocabulary="99" code="999"/>
          <sector code="11110"/>
        </iati-activity>
        '''

        activity = etree.fromstring(xml)
        test = self.feature.tests[1]
        result = test(activity, codelists=self.codelists)

        assert result is True
