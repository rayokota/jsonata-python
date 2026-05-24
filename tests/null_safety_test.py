import jsonata

from tests.jsonata_test import TestJsonata as JsonataTestRunner, UNDEFINED, evaluate_jsonata


def _execute_jsonata_raw(expr, input):
    """Evaluate without output NULL_VALUE conversion."""
    j = jsonata.Jsonata(expr)
    j.set_output_convert_nulls(False)
    return j.evaluate(input)


class TestNullSafety:

    def test_null_safety(self):
        res = None
        res = jsonata.Jsonata("$sift(undefined, $uppercase)").evaluate(None)
        assert res is None

        res = jsonata.Jsonata("$each(undefined, $uppercase)").evaluate(None)
        assert res is None

        res = jsonata.Jsonata("$keys(null)").evaluate(None)
        assert res is None

        res = jsonata.Jsonata("$map(null, $uppercase)").evaluate(None)
        assert res is None

        res = jsonata.Jsonata("$filter(null, $uppercase)").evaluate(None)
        assert res is None

        res = jsonata.Jsonata("$single(null, $uppercase)").evaluate(None)
        assert res is None

        res = jsonata.Jsonata("$reduce(null, $uppercase)").evaluate(None)
        assert res is None

        res = jsonata.Jsonata("$lookup(null, 'anykey')").evaluate(None)
        assert res is None

        res = jsonata.Jsonata("$spread(null)").evaluate(None)
        assert res is None

    def test_array_index_preserves_null(self):
        # Indexing into an array element that is JSON null must yield null,
        # not be filtered out as if it were undefined.
        data = {"data": [[1, None, 3], [2, None, 4], [3, None, 5]]}
        res = jsonata.Jsonata("[$map(data, function($row) { $row[1] })]").evaluate(data)
        assert res == [None, None, None]

    def test_output_convert_nulls(self):
        j = jsonata.Jsonata("$")
        j2 = jsonata.Jsonata("$")
        j2.set_output_convert_nulls(False)

        assert j.is_output_convert_nulls() is True
        assert j2.is_output_convert_nulls() is False

        res = j.evaluate(jsonata.Utils.NULL_VALUE)
        res2 = j2.evaluate(jsonata.Utils.NULL_VALUE)
        assert res is None
        assert res2 is jsonata.Utils.NULL_VALUE

        res = j.evaluate(None)
        res2 = j2.evaluate(None)
        assert res is None
        assert res2 is None

    def test_python_null_vs_undefined(self):
        test = JsonataTestRunner()

        assert test.run_test_case("test-undefined", {
            "expr": "undefined",
            "undefinedResult": True,
        })

        assert test.run_test_case("test-null", {
            "expr": "null",
            "result": None,
        })

        # raw vs cooked, returning null or undefined
        res = _execute_jsonata_raw("null", None)
        assert res is jsonata.Utils.NULL_VALUE

        res = _execute_jsonata_raw("$", jsonata.Utils.NULL_VALUE)
        assert res is jsonata.Utils.NULL_VALUE

        res = _execute_jsonata_raw("$", None)
        assert res is None

        res = _execute_jsonata_raw("no_match", None)
        assert res is None

        res = evaluate_jsonata("null", None, None)
        assert res is None

        res = evaluate_jsonata("no_match", None, None)
        assert res == UNDEFINED

        res = evaluate_jsonata("{}.a", None, None)
        assert res == UNDEFINED

        res = _execute_jsonata_raw('{"a":null}.a', None)
        assert res is jsonata.Utils.NULL_VALUE

        res = evaluate_jsonata('{"a":null}.a', None, None)
        assert res is None

        res = _execute_jsonata_raw('{"a":null}.b', None)
        assert res is None

        res = evaluate_jsonata('{"a":null}.b', None, None)
        assert res == UNDEFINED

        res = evaluate_jsonata("[a,null,b][0]", None, None)
        assert res is None

        res = _execute_jsonata_raw("$[1]", [42, jsonata.Utils.NULL_VALUE])
        assert res is jsonata.Utils.NULL_VALUE

        res = _execute_jsonata_raw("$[2]", [42, jsonata.Utils.NULL_VALUE])
        assert res is None

        res = evaluate_jsonata("$[2]", [42, jsonata.Utils.NULL_VALUE], None)
        assert res == UNDEFINED

        res = jsonata.Jsonata("$").evaluate(jsonata.Utils.NULL_VALUE)
        assert res is None

        res = _execute_jsonata_raw("{'a':$}", jsonata.Utils.NULL_VALUE)
        assert res["a"] is jsonata.Utils.NULL_VALUE

        res = _execute_jsonata_raw("{'a':$}", None)
        assert res == {}

        res = _execute_jsonata_raw("{'a':{'b':$}}", None)
        assert res == {"a": {}}

        res = _execute_jsonata_raw("[$]", [jsonata.Utils.NULL_VALUE, jsonata.Utils.NULL_VALUE])
        assert res == [jsonata.Utils.NULL_VALUE, jsonata.Utils.NULL_VALUE]

        res = evaluate_jsonata("[$]", [jsonata.Utils.NULL_VALUE, jsonata.Utils.NULL_VALUE], None)
        assert res == [None, None]
