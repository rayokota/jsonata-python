import jsonata


class TestArray:

    def test_array(self):
        assert jsonata.Jsonata("$.[{ }] ~> $reduce($append)").evaluate([True, True]) == [{}, {}]
