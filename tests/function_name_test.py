import pytest

import jsonata


#
# Signature errors (T0410) name the function the way jsonata-js does: by the name used at the call site
# (its registered name or the variable it is bound to). Ported from jsonata-java (FunctionNameTest).
#
class Echo(jsonata.Jsonata.JFunctionCallable):
    def call(self, input, args):
        return args[0]


def _error(expr, input=None, error="T0410"):
    e = jsonata.Jsonata(expr)
    e.register_function("test", jsonata.Jsonata.JFunction(Echo(), "<s:s>"))
    with pytest.raises(jsonata.JException) as exc_info:
        e.evaluate(input)
    assert exc_info.value.error == error
    assert "<class" not in str(exc_info.value)
    return exc_info.value


class TestFunctionName:

    def test_registered_function(self):
        ex = _error("$test(1)")
        assert ex.expected == "test"
        assert str(ex) == "Argument 1 of Object test does not match Object signature"

    def test_registered_function_via_variable(self):
        ex = _error("($f := $test; $f(1))")
        assert ex.expected == "f"
        assert str(ex) == "Argument 1 of Object f does not match Object signature"

    def test_transform_via_variable(self):
        assert _error("($t := |$|{}|; $t(123))").expected == "t"

    # jsonata-js: token=undefined
    def test_transform_via_apply(self):
        ex = _error("$ ~> |$|{}|", 123)
        assert ex.expected is None
        assert str(ex) == "Argument 1 of Object undefined does not match Object signature"

    def test_transform_called_directly(self):
        assert _error("(|$|{}|)(123)").expected is None

    def test_lambda_via_variable(self):
        assert _error("($f := function($x)<n:n>{ $x }; $f('a'))").expected == "f"

    # binding a function to a variable doesn't rename it elsewhere
    def test_binding_does_not_rename(self):
        assert _error("($g := $test; $test(1))").expected == "test"
        jsonata.Jsonata("($s := $substringBefore; 1)").evaluate(None)
        assert _error("$substringBefore(1, 2)").expected == "substringBefore"
        assert _error("($f := function($x)<n:n>{ $x }; $g := $f; $f('a'))").expected == "f"

    # an error raised while a higher-order function calls its function argument is named after the
    # higher-order function, the innermost call site
    def test_function_argument(self):
        assert _error("$map(['a'], function($x)<n:n>{ $x })").expected == "map"

    # an error from a nested call keeps the name of that call. (A call in tail position is run by the
    # trampoline in apply(), so like in jsonata-js it is named after the outer call.)
    def test_nested_call(self):
        assert _error("($f := function($x){ [$test($x)] }; $f(1))").expected == "test"
        assert _error("($f := function($x){ $test($x) }; $f(1))").expected == "f"

    # T0412 errors of a function without a name are named at the call site too
    def test_array_type_error(self):
        e = jsonata.Jsonata("($f := $sumAll; $f(['a']))")
        e.register_function("sumAll", jsonata.Jsonata.JFunction(Echo(), "<a<n>:n>"))
        with pytest.raises(jsonata.JException) as exc_info:
            e.evaluate(None)
        assert exc_info.value.error == "T0412"
        assert str(exc_info.value) == "Argument 1 of Object f must be an array of n"
        # a builtin keeps its own name
        assert _error("$sum(['a'])", error="T0412").expected == "sum"

    def test_lambda_array_type_error(self):
        ex = _error("($f := function($x)<a<n>:n>{ $x }; $f(['a']))", error="T0412")
        assert str(ex) == "Argument 1 of Object f must be an array of n"

    # {{{token}}} placeholders are replaced with the value, like {{token}}
    def test_triple_brace_placeholder(self):
        ex = _error("($f := 1; f())", {}, error="T1005")
        assert str(ex) == "Attempted to invoke a non-function. Did you mean $f?"

    # like jsonata-js, the error names the first argument that doesn't match
    @pytest.mark.parametrize("expr, message", [
        ("$substring('abc', 'x')", "Argument 2 of Object substring does not match Object signature"),
        ("$substring('abc', 1, 'x')", "Argument 3 of Object substring does not match Object signature"),
        ("$substringBefore(1, 2)", "Argument 1 of Object substringBefore does not match Object signature"),
        ("$join('a', 'b', 'c')", "Argument 3 of Object join does not match Object signature"),
        ("$replace('a', 'a', 'b', 'x')", "Argument 4 of Object replace does not match Object signature"),
        ("$lookup({}, 1)", "Argument 2 of Object lookup does not match Object signature"),
    ])
    def test_argument_index(self, expr, message):
        assert str(_error(expr)) == message
