from unittest import TestCase
from hamcrest import assert_that, is_

from kaaf import AbstractRuleBuilder, AbstractRule, SconeClient


class RulegenTests(TestCase):
    def setUp(self):
        self.scone = SconeClient(host='localhost', port=6517)
    
    def tearDown(self):
        self.scone.close()

    def test_fact_rule(self):
        sut = AbstractRuleBuilder(self.scone, 'test/fact.scene')
        sut.build()

        expected = AbstractRule(
            left = [{
                'agent': 'room-1-ms',
                'value': 'occupancy'
            }],
            right = [{
                'location': 'room-1',
                'value': 'occupied room'
            }])

        assert_that(sut.rules, is_([expected]))
    
    def test_action_rule(self):
        sut = AbstractRuleBuilder(self.scone, 'test/action.scene')
        sut.build()

        expected = AbstractRule(
            left = [{
                'location': 'room-1',
                'value': 'occupied room'
            }],
            right = [{
                'action': 'provide light',  # FIXME: provide light -> turn on
                'object': 'room-1-b'
            }])

        assert_that(sut.rules, is_([expected]))