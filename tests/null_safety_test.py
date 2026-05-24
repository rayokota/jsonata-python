import jsonata


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
