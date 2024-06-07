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
