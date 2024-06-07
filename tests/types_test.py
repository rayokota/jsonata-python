import jsonata
import pytest


class TestTypes:

    def test_illegal_types(self):
        with pytest.raises(ValueError):
            res = jsonata.Jsonata("$").evaluate(set())

    def test_legal_types(self):
        # map
        assert jsonata.Jsonata("a").evaluate({"a": 1}) == 1
        # list
        assert jsonata.Jsonata("$[0]").evaluate([1, 2]) == 1
        # string
        assert jsonata.Jsonata("$").evaluate("string") == "string"
        # int
        assert jsonata.Jsonata("$").evaluate(1) == 1
        # boolean
        assert jsonata.Jsonata("$").evaluate(True)
        # float
        assert jsonata.Jsonata("$").evaluate(1.0) == 1.0

    def test_ignore(self):
        expr = jsonata.Jsonata("a")
        a_set = {1}

        # set causes exception
        with pytest.raises(ValueError):
            expr.evaluate({"a": a_set})

        # turn off validation, Date is "passed" via $
        expr.set_validate_input(False)
        assert expr.evaluate({"a": a_set}) == a_set

        # change expression to a computation that involves a, we get an error again because concat
        # cannot deal with Date
        expr2 = jsonata.Jsonata("a & a")
        expr2.set_validate_input(False)
        with pytest.raises(TypeError):
            expr2.evaluate({"a": a_set})
