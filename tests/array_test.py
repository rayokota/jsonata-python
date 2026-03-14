import jsonata
import pytest


class TestArray:

    def test_negative_index(self):
        expr = jsonata.Jsonata("item[-1]")
        assert expr.evaluate({"item": []}) is None
        expr = jsonata.Jsonata("$[-1]")
        assert expr.evaluate([]) is None

    def test_array(self):
        assert jsonata.Jsonata("$.[{ }] ~> $reduce($append)").evaluate([True, True]) == [{}, {}]

    def test_wildcard(self):
        expr = jsonata.Jsonata("*")
        assert expr.evaluate([{"x": 1}]) == {"x": 1}

    def test_index(self):
        expr = jsonata.Jsonata("($x:=['a','b']; $x#$i.$i)")
        assert expr.evaluate(1) == [0, 1]
        assert expr.evaluate(None) == [0, 1]

    def test_wildcard_filter(self):
        value1 = {"value": {"Name": "Cell1", "Product": "Product1"}}
        value2 = {"value": {"Name": "Cell2", "Product": "Product2"}}
        data = [value1, value2]

        expression = jsonata.Jsonata("*[value.Product = 'Product1']")
        assert expression.evaluate(data) == value1

        expression2 = jsonata.Jsonata("**[value.Product = 'Product1']")
        assert expression2.evaluate(data) == value1

    def test_assert_custom_message(self):
        expr = jsonata.Jsonata("$assert(false, 'custom error')")
        with pytest.raises(jsonata.JException) as exc_info:
            expr.evaluate(None)
        assert "custom error" in str(exc_info.value)
