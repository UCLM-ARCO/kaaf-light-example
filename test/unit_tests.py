from unittest import TestCase
from hamcrest import assert_that, is_

import Ice
from kaf import AbstractRuleBuilder, AbstractRule,  Semantic


class RulegenTests(TestCase):
    def setUp(self):
        self.ic = Ice.initialize()
        proxy = self.ic.stringToProxy('scone -t:tcp -p 5001')
        self.scone = Semantic.SconeServicePrx.checkedCast(proxy)
    
    def tearDown(self):
        self.ic.destroy()

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