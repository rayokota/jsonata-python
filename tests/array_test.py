import jsonata


class TestArray:

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
