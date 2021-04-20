from unittest import TestCase
from hamcrest import assert_that, is_

from kaf import AbstractRuleBuilder


class RulegenTests(TestCase):
    def test_rule(self):
        sut = AbstractRuleBuilder('test/simple.scene')
        rules = sut.build()

        assert_that(len(rules), is_(1))
