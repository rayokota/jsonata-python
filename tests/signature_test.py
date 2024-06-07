import jsonata
import pytest


class TestSignature:

    def test_parameters_are_converted_to_arrays(self):
        expr = jsonata.Jsonata("$greet(1,null,3)")
        expr.register_function("greet", jsonata.Jsonata.JFunction(TestSignature.JFunctionCallable1(), "<a?a?a?a?:s>"))
        assert expr.evaluate(None) == "[[1], [null], [3], [None]]"

    class JFunctionCallable1(jsonata.Jsonata.JFunctionCallable):

        def call(self, input, args):
            return str(args)

    def test_error(self):
        expr = jsonata.Jsonata("$foo()")
        expr.register_function("foo", jsonata.Jsonata.JFunction(TestSignature.JFunctionCallable2(), "(sao)"))

        # null not allowed
        with pytest.raises(jsonata.JException):
            expr.evaluate(None)

        # boolean not allowed
        with pytest.raises(jsonata.JException):
            expr.evaluate(True)

    class JFunctionCallable2(jsonata.Jsonata.JFunctionCallable):

        def call(self, input, args):
            return None
