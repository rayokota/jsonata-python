﻿from jsonata import jsonata


class TestCustomFunction:

    def test_supplier(self):
        expression = jsonata.Jsonata("$greet()")
        expression.register_lambda("greet", lambda: "Hello world")
        assert expression.evaluate(None) == "Hello world"

    def test_unary(self):
        expression = jsonata.Jsonata("$echo(123)")
        expression.register_lambda("echo", lambda x: x)
        assert expression.evaluate(None) == 123

    def test_binary(self):
        expression = jsonata.Jsonata("$add(21, 21)")
        expression.register_lambda("add", lambda a, b: a + b)
        assert expression.evaluate(None) == 42

    def test_ternary(self):
        expression = jsonata.Jsonata("$abc(a,b,c)")
        expression.register_lambda("abc", lambda x, y, z: str(x) + str(y) + str(z))
        assert expression.evaluate({"a": "a", "b": "b", "c": "c"}) == "abc"
