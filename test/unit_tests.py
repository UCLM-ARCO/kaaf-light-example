from unittest import TestCase
from hamcrest import assert_that, is_

import Ice
from kaf import AbstractRuleBuilder, AbstractRule,  Semantic


class RulegenTests(TestCase):
    def setUp(self):
        ic = Ice.initialize()
        proxy = ic.stringToProxy('scone -t:tcp -p 5001')
        self.scone = Semantic.SconeServicePrx.checkedCast(proxy)

    def test_rule(self):
        sut = AbstractRuleBuilder(self.scone, 'test/simple.scene')
        sut.build()

        # expected = AbstractRule(
        #     left = [{
        #         'agent': 'room-1-ms',
        #         'value': 'occupancy'
        #     }],
        #     right = [{
        #         'location': 'living-room',
        #         'value': 'occupied room'
        #     }])

        expected = AbstractRule(
            left = [{
                'agent': 'room-1-ms',
                'value': 'motion event'
            }],
            right = [{
                'location': 'room-1',
                'value': 'occupancy'
            }])

        assert_that(sut.rules, is_([expected]))

# motion event from living-room-ms
# living-room: occupied room