import pytest

import jsonata
from jsonata import Functions


#
# Partial application of native functions follows jsonata-js: the partial is a lambda whose body is
# the native function itself, so applying it calls the native directly, without looking it up by name
# and without validating its signature again. Ported from jsonata-java (PartialTest, OldPrsTest and
# EachMergeTest).
#
class Add(jsonata.Jsonata.JFunctionCallable):
    def call(self, input, args):
        return args[0] + args[1]


class TestPartial:

    # jsonata-java #79
    def test_each_empty_array(self):
        assert jsonata.Jsonata("[] ~> $each(?, function($v) { $v })").evaluate({}) is None

    def test_each_array_with_data(self):
        assert jsonata.Jsonata("[123, 321] ~> $each(?, function($v) { $v })").evaluate({}) == [123, 321]

    # like JS for..in, $each iterates array indexes; the signature is not checked for a partially
    # applied native
    def test_each_array(self):
        assert jsonata.Jsonata("[5,6] ~> $each(?, function($v,$k) { $k })").evaluate(None) == ["0", "1"]

    # the signature is still checked when the function is called directly
    def test_each_array_direct(self):
        with pytest.raises(jsonata.JException) as exc_info:
            jsonata.Jsonata("$each([5,6], function($v,$k) { $k })").evaluate(None)
        assert exc_info.value.error == "T0410"

    def test_merge_with_array(self):
        assert jsonata.Jsonata("$ ~> $merge(?)").evaluate([[], {"test": "data"}]) == {"test": "data"}

    # jsonata-java #86, #87
    def test_map_append(self):
        assert jsonata.Jsonata("{'systems': 'asd2'}.$map($, $append(?))").evaluate(None) == {"systems": "asd2"}
        assert jsonata.Jsonata("$map($, $append(?))").evaluate({"systems": "asd"}) == {"systems": "asd"}

    # the native is called without validating its signature, but arguments it can't handle are
    # still reported as a signature error, named after the native rather than the higher-order
    # function calling it
    @pytest.mark.parametrize("expr", [
        "$substring(?, 1)(123)", "$map([1, 2], $substring(?, 1))",
        "$substring(?, 'x')('abc')", "$map(['abc'], $substring(?, 'x'))",
        "$substring(?, null)('abc')", "$map(['abc'], $substring(?, null))"])
    def test_argument_of_wrong_type(self, expr):
        with pytest.raises(jsonata.JException) as exc_info:
            jsonata.Jsonata(expr).evaluate(None)
        assert exc_info.value.error == "T0410"
        assert exc_info.value.expected == "substring"

    # a function argument that isn't a function
    def test_invalid_function_argument(self):
        with pytest.raises(jsonata.JException) as exc_info:
            jsonata.Jsonata("$sort(?, 42)([1, 2])").evaluate(None)
        assert str(exc_info.value) == "Argument 2 of Object sort does not match Object signature"

    @pytest.mark.parametrize("expr", ["$uppercase(?)(123)", "$map([123], $uppercase(?))"])
    def test_number_for_string(self, expr):
        with pytest.raises(jsonata.JException) as exc_info:
            jsonata.Jsonata(expr).evaluate(None)
        assert exc_info.value.error == "T0410"
        assert str(exc_info.value) == "Argument 1 of Object uppercase does not match Object signature"

    # an AttributeError of a function the native calls is kept
    def test_function_argument_attribute_error_kept(self):
        e = jsonata.Jsonata("$map([1], $upper)")
        e.register_lambda("upper", lambda s: s.upper())
        with pytest.raises(AttributeError):
            e.evaluate(None)
        e = jsonata.Jsonata("$map(?, $upper)([1])")
        e.register_lambda("upper", lambda s: s.upper())
        with pytest.raises(AttributeError):
            e.evaluate(None)

    def test_argument_of_wrong_type_index(self):
        with pytest.raises(jsonata.JException) as exc_info:
            jsonata.Jsonata("$substring(?, 'x')('abc')").evaluate(None)
        assert str(exc_info.value) == "Argument 2 of Object substring does not match Object signature"

    # errors of arguments that match the signature are kept
    def test_native_error_for_matching_arguments(self):
        with pytest.raises(jsonata.JException) as exc_info:
            jsonata.Jsonata("$match(?, /b/, -1)('abc')").evaluate(None)
        assert exc_info.value.error == "D3040"

    # errors of a function the native calls are kept, though $each was given an array that doesn't
    # match its signature
    @pytest.mark.parametrize("expr, error", [
        ("[5,6] ~> $each(?, function($v){ $error('oops') })", "D3137"),
        ("$each(?, function($v){ $assert(false, 'boom') })([5,6])", "D3141")])
    def test_function_argument_error_kept(self, expr, error):
        with pytest.raises(jsonata.JException) as exc_info:
            jsonata.Jsonata(expr).evaluate(None)
        assert exc_info.value.error == error

    # errors of a registered function are kept, as in a direct call
    def test_registered_function_error_kept(self):
        def parse_int(s):
            return int(s)

        for expr in ["$parseInt('x')", "$parseInt(?)('x')"]:
            e = jsonata.Jsonata(expr)
            e.register_lambda("parseInt", parse_int)
            with pytest.raises(ValueError):
                e.evaluate(None)

    # a missing required argument is passed as None, like in jsonata-js
    def test_missing_required_args(self):
        assert jsonata.Jsonata("$substring(?)('abc')").evaluate(None) == "abc"
        assert jsonata.Jsonata("$pad(?)('abc')").evaluate(None) == "abc"

    # an unnamed signature error of a function argument is named after the native calling it, as
    # when it is called directly
    @pytest.mark.parametrize("expr", [
        "$map(['a'], function($x)<n:n>{ $x })", "$map(?, function($x)<n:n>{ $x })(['a'])"])
    def test_function_argument_error(self, expr):
        with pytest.raises(jsonata.JException) as exc_info:
            jsonata.Jsonata(expr).evaluate(None)
        assert exc_info.value.error == "T0410"
        assert exc_info.value.expected == "map"

    def test_missing_args_bound(self):
        assert jsonata.Jsonata("$substring(?, 1)('hello')").evaluate(None) == "ello"

    # jsonata-java #80
    def test_map_in_pipe(self):
        data = {"buildings": {
            "home": {"address": "home address", "period": "11 month on 12",
                     "presentation": {"first": {"widget": {"data": "home widget"}}}},
            "work": {"address": "work address",
                     "presentation": {"first": {"widget": {"data": "work widget"}}}},
            "vacancy": {"address": "vacancy address", "period": "1 month on 12",
                        "presentation": {"first": {"widget": {"data": "vacancy widget"}}}},
            "old": {"address": "old address", "period": "2 month on 12",
                    "presentation": {"first": {"widget": {"data": "old widget"}}}},
            "operation": {"address": "operation address", "period": "3 month on 12",
                          "presentation": {"first": {"widget": {"data": "operation widget"}}}}}}
        expr = jsonata.Jsonata(
            "$sift($.buildings, function($v, $k) { $k ~> /o/ and $v.presentation.*.widget})"
            " ~> $each(?, function($v, $key) {{ $key: $sift($v.presentation, function($v, $k){ $v.widget }) }})"
            " ~> $map(?, function($v){($v.*)})")
        assert expr.evaluate(data) == [
            {"first": {"widget": {"data": "home widget"}}},
            {"first": {"widget": {"data": "work widget"}}},
            {"first": {"widget": {"data": "old widget"}}},
            {"first": {"widget": {"data": "operation widget"}}}]

    # forgot the leading $
    def test_missing_dollar(self):
        with pytest.raises(jsonata.JException) as exc_info:
            jsonata.Jsonata("substring(?, 1)").evaluate(None)
        assert exc_info.value.error == "T1007"
        assert str(exc_info.value) == "Attempted to partially apply a non-function. Did you mean $substring?"

    # jsonata-java #83: custom functions, with or without a signature
    def test_custom_function(self):
        expr = jsonata.Jsonata("$add(1, 2) ~> $add(?, 3)")
        expr.register_function("add", jsonata.Jsonata.JFunction(Add(), "<nn:n>"))
        assert expr.evaluate(None) == 6

    def test_custom_function_without_signature(self):
        expr = jsonata.Jsonata("$add(1, 2) ~> $add(?, 3)")
        expr.register_function("add", jsonata.Jsonata.JFunction(Add(), None))
        assert expr.evaluate(None) == 6

    # like a direct call, the partial passes every declared parameter, omitted ones as None
    def test_custom_function_optional_args(self):
        class Args(jsonata.Jsonata.JFunctionCallable):
            def call(self, input, args):
                return [args[0], args[1]]

        for expression in ["$f(5)", "$f(?)(5)", "$map([5], $f(?))"]:
            expr = jsonata.Jsonata(expression)
            expr.register_function("f", jsonata.Jsonata.JFunction(Args(), "<nn?:a>"))
            assert expr.evaluate(None) == [5, None], expression

    def test_lambda(self):
        expr = jsonata.Jsonata("$add(1, 2) ~> $add(?, 3)")
        expr.register_lambda("add", lambda a, b: a + b)
        assert expr.evaluate(None) == 6

    def test_lambda_with_var_args(self):
        expr = jsonata.Jsonata("$add(1, 2) ~> $add(?, 3)")
        expr.register_lambda("add", lambda *args: sum(args))
        assert expr.evaluate(None) == 6

    # every parameter of the partial gets a valid name, however many there are
    def test_lambda_with_many_args(self):
        args = ", ".join(str(i) for i in range(1, 31))
        expr = jsonata.Jsonata("$add(?, " + args + ")(100)")
        expr.register_lambda("add", lambda *args: sum(args))
        assert expr.evaluate(None) == 100 + sum(range(1, 31))

    # the partial calls the function itself, not a function looked up by name, so a function bound
    # only in the frame passed to evaluate() can be partially applied
    def test_function_bound_in_frame(self):
        expr = jsonata.Jsonata("$f(1, 2) ~> $f(?, 3)")
        frame = expr.create_frame()
        frame.bind("f", jsonata.Jsonata.JLambda(lambda a, b: a + b))
        assert expr.evaluate(None, frame) == 6

    def test_function_bound_to_variable(self):
        expr = jsonata.Jsonata("($g := $add; $g(?, 3)(4))")
        expr.register_lambda("add", lambda a, b: a + b)
        assert expr.evaluate(None) == 7

    # jsonata-java #85: the input is passed to a function called directly
    def test_function_with_input_data(self):
        class Multiply(jsonata.Jsonata.JFunctionCallable):
            def call(self, input, args):
                second = args[1] if len(args) > 1 else int(input["factor"])
                return args[0] * second

        expr = jsonata.Jsonata("$multiply(3) ~> $multiply(?, 2)")
        expr.register_function("multiply", jsonata.Jsonata.JFunction(Multiply(), None))
        assert expr.evaluate({"factor": "3"}) == 18


#
# $each and $merge iterate arrays like JS for..in. Functions without a signature let arrays reach them.
#
def _eval_raw(expr, input=None):
    e = jsonata.Jsonata(expr)
    e.register_lambda("eachRaw", lambda obj, func: Functions.each(obj, func))
    e.register_lambda("mergeRaw", lambda arg: Functions.merge(arg))
    return e.evaluate(input)


class TestEachMerge:

    def test_each_array_keys(self):
        assert _eval_raw("$eachRaw([5,6], function($v,$k) { $k })") == ["0", "1"]

    def test_each_array_values(self):
        assert _eval_raw("$eachRaw([5,6], function($v) { $v })") == [5, 6]

    def test_each_array_all_args(self):
        assert _eval_raw("[$eachRaw($, function($v,$k,$o) { {'v': $v, 'k': $k, 'o': $o} })]", [5]) == \
            [{"v": 5, "k": "0", "o": [5]}]

    def test_each_array_skips_undefined(self):
        assert _eval_raw("$eachRaw([5,6,7], function($v) { $v > 5 ? $v })") == [6, 7]

    def test_each_empty_array_and_undefined(self):
        assert _eval_raw("$eachRaw([], function($v) { $v })") is None
        assert _eval_raw("$eachRaw(nothing, function($v) { $v })") is None

    def test_each_map(self):
        assert _eval_raw("$eachRaw({'a': 1, 'b': 2}, function($v, $k) { $k & '=' & $v })") == ["a=1", "b=2"]
        assert jsonata.Jsonata("$each({'a': 1, 'b': 2}, function($v, $k) { $k & '=' & $v })").evaluate(None) == \
            ["a=1", "b=2"]

    def test_merge_array(self):
        assert _eval_raw("$mergeRaw([[5,6]])") == {"0": 5, "1": 6}

    def test_merge_array_and_map(self):
        assert _eval_raw("$mergeRaw($)", [[], {"test": "data"}]) == {"test": "data"}

    def test_merge_skips_other_values(self):
        assert _eval_raw("$mergeRaw([{'a': 1}, 5, 'x'])") == {"a": 1}

    def test_merge_maps(self):
        assert jsonata.Jsonata("$merge([{'a':1,'b':2},{'b':3}])").evaluate(None) == {"a": 1, "b": 3}
