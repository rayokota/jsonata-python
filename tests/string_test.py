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

    def test_trim(self):
        assert jsonata.Jsonata("$trim(\"\n\")").evaluate(None) == ""
        assert jsonata.Jsonata("$trim(\" \")").evaluate(None) == ""
        assert jsonata.Jsonata("$trim(\"\")").evaluate(None) == ""
        assert jsonata.Jsonata("$trim(notthere)").evaluate(None) is None
