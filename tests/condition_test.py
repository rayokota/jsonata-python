import jsonata


#
# The left-hand side of ?: and ?? is both the condition and the result
#
class TestConditionOperators:

    def test_default_negative_number(self):
        assert jsonata.Jsonata("-5 ?: 99").evaluate(None) == -5

    def test_default_negative_index(self):
        assert jsonata.Jsonata("[1,2,3][-1] ?: 42").evaluate(None) == 3
        assert jsonata.Jsonata("[true][-1] ?: \"no\"").evaluate(None) is True

    def test_coalescing_negative_number(self):
        assert jsonata.Jsonata("-5 ?? 99").evaluate(None) == -5

    def test_coalescing_negative_index(self):
        assert jsonata.Jsonata("[1,2,3][-1] ?? 42").evaluate(None) == 3
        assert jsonata.Jsonata("[1,2,3][-5] ?? 42").evaluate(None) == 42
