import jsonata


#
# see https://docs.jsonata.org/string-functions#string
# 
class TestString:

    def test_string(self):
        res = jsonata.Jsonata("$string($)").evaluate("abc")
        assert res == "abc"

    def test_boolean(self):
        assert jsonata.Jsonata("$string($)").evaluate(True) == "true"

    def test_number(self):
        assert jsonata.Jsonata("$string(5)").evaluate(None) == "5"

    def test_array(self):
        assert jsonata.Jsonata("[1..5].$string()").evaluate(None) == ["1", "2", "3", "4", "5"]

    def test_map(self):
        assert jsonata.Jsonata("$string($)").evaluate({}) == "{}"

    def test_map2(self):
        assert jsonata.Jsonata("$string($)").evaluate({"x": 1}) == "{\"x\":1}"

    def test_escape(self):
        assert jsonata.Jsonata("$string($)").evaluate({"a": str('"')}) == "{\"a\":\"\\\"\"}"
        assert jsonata.Jsonata("$string($)").evaluate({"a": str('\\')}) == "{\"a\":\"\\\\\"}"
        assert jsonata.Jsonata("$string($)").evaluate({"a": str('\t')}) == "{\"a\":\"\\t\"}"
        assert jsonata.Jsonata("$string($)").evaluate({"a": str('\n')}) == "{\"a\":\"\\n\"}"
        assert jsonata.Jsonata("$string($)").evaluate({"a": "</"}) == "{\"a\":\"</\"}"

    def test_replace(self):
        assert jsonata.Jsonata("$replace('hello', '.', '')").evaluate(None) == "hello"
        assert jsonata.Jsonata("$replace('hello', 'l', 'x')").evaluate(None) == "hexxo"
        assert jsonata.Jsonata("$replace('h.ello', '.', '')").evaluate(None) == "hello"
        assert jsonata.Jsonata("$replace('h.e.l.l.o', '.', '',2)").evaluate(None) == "hel.l.o"

    def test_regex(self):
        assert (jsonata.Jsonata("($matcher := $eval('/^' & 'foo' & '/i'); $.$spread()[$.$keys() ~> $matcher])")
                .evaluate({"foo": 1, "bar": 2}) == {"foo": 1})

    def test_regex_literal(self):
        expr = jsonata.Jsonata("/^test.*$/")
        result = expr.evaluate(None)
        assert result.pattern == "^test.*$"

    def test_eval_regex(self):
        expr = jsonata.Jsonata("$eval('/^test.*$/')")
        result = expr.evaluate(None)
        assert result.pattern == "^test.*$"

    def test_eval_regex_check_answer_data(self):
        expr = jsonata.Jsonata("(\n    $matcher := $eval('/l/');\n    ('Hello World' ~> $matcher);\n)")
        result = expr.evaluate(None)
        assert result["match"] == "l"
        assert result["start"] == 2
        assert result["end"] == 3
        assert result["groups"] == ["l"]
        assert callable(result["next"].function)

    def test_eval_regex_call_next_and_check_result(self):
        expr = jsonata.Jsonata("(\n    $matcher := $eval('/l/');\n    ('Hello World' ~> $matcher).next();\n)")
        result = expr.evaluate(None)
        assert result["match"] == "l"
        assert result["start"] == 3
        assert result["end"] == 4
        assert result["groups"] == ["l"]

    def test_eval_sees_enclosing_variable_binding(self):
        # $eval's dynamically-parsed expression must see variables bound in
        # the enclosing scope (here, via an in-expression := assignment),
        # not just the static top-level environment.
        expr = jsonata.Jsonata('($x := 5; $eval("$x + 1"))')
        assert expr.evaluate(None) == 6

    def test_eval_sees_explicit_top_level_bindings(self):
        # Same as above, but for bindings passed via evaluate()'s bindings
        # argument rather than an in-expression assignment.
        expr = jsonata.Jsonata('$eval("$x")')
        assert expr.evaluate(None, {"x": 42}) == 42

    def test_eval_unaffected_by_sibling_argument_scope(self):
        # $eval's second (focus) argument is evaluated before its own body
        # runs, and here contains a nested block with its own environment.
        # Without saving/restoring the evaluation context around each
        # nested eval() call, evaluating that sibling argument would leave
        # the tracked "current" environment pointing at the inner block's
        # scope, causing $eval to resolve $x (from the outer scope) as
        # undefined instead of 5.
        expr = jsonata.Jsonata('($x := 5; $eval("$x", (($y := 1; $y))))')
        assert expr.evaluate(None) == 5

    #
    # Additional $split tests
    #   
    def test_split(self):
        # Splitting on an undefined value
        res = jsonata.Jsonata("$split(a, '-')").evaluate({})
        assert res == None

        # Splitting on an undefined value, equivalent to above
        res = jsonata.Jsonata("a ~> $split('-')").evaluate({})
        assert res == None

        # Splitting empty string with empty separator must return empty list
        res = jsonata.Jsonata("$split('', '')").evaluate(None)
        assert res == []

        # Split characters with limit
        res = jsonata.Jsonata("$split('a1b2c3d4', '', 4)").evaluate(None)
        assert res == ["a", "1", "b", "2"]

        # Check string is not treated as regexp
        res = jsonata.Jsonata("$split('this..is.a.test', '.')").evaluate(None)
        # System.out.println( Functions.string(res, false))
        assert res == ["this", "", "is", "a", "test"]

        # Check trailing empty strings
        res = jsonata.Jsonata("$split('this..is.a.test...', '.')").evaluate(None)
        # System.out.println( Functions.string(res, false))
        assert res == ["this", "", "is", "a", "test", "", "", ""]

        # Check trailing empty strings
        res = jsonata.Jsonata("$split('this..is.a.test...', /\\./)").evaluate(None)
        assert res == ["this", "", "is", "a", "test", "", "", ""]

        # Check string is not treated as regexp, trailing empty strings, and limit
        res = jsonata.Jsonata("$split('this.*.*is.*a.*test.*.*.*.*.*.*', '.*', 8)").evaluate(None)
        assert res == ["this", "", "is", "a", "test", "", "", ""]

        # Escaped regexp, trailing empty strings, and limit
        res = jsonata.Jsonata("$split('this.*.*is.*a.*test.*.*.*.*.*.*', /\\.\\*/, 8)").evaluate(None)
        assert res == ["this", "", "is", "a", "test", "", "", ""]

    def test_fieldname_with_special_char(self):
        expr = jsonata.Jsonata("$ ~> |$|{}|")
        o = {"a\nb": "c\nd"}
        assert expr.evaluate(o) == o

    def test_trim(self):
        assert jsonata.Jsonata("$trim(\"\n\")").evaluate(None) == ""
        assert jsonata.Jsonata("$trim(\" \")").evaluate(None) == ""
        assert jsonata.Jsonata("$trim(\"\")").evaluate(None) == ""
        assert jsonata.Jsonata("$trim(notthere)").evaluate(None) is None
