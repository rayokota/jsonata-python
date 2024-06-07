import jsonata
import pytest
import time


class TestThread:

    def test_reuse(self):
        expr = jsonata.Jsonata("a")
        assert expr.evaluate({"a": 1}) == 1
        assert expr.evaluate({"a": 1}) == 1

    def test_now(self):
        now = jsonata.Jsonata("$now()")
        r1 = now.evaluate(None)
        time.sleep(1)
        r2 = now.evaluate(None)
        assert r1 != r2

    @pytest.mark.asyncio
    async def test_reuse_with_variable(self):
        expr = jsonata.Jsonata("($x := a; $wait(a); $x)")

        def lambda1(a):
            time.sleep(a)
            return None

        expr.register_lambda("wait", lambda1)

        async def threaded_function():
            return expr.evaluate({"a": 10})

        # make sure outer thread is initialized and in $wait
        time.sleep(5)

        # this thread uses the same expr and terminates before thread is done
        assert expr.evaluate({"a": 3}) == 3

        # the outer thread is unaffected by the previous operations
        outer = await threaded_function()
        assert outer == 10

    @pytest.mark.asyncio
    async def test_add_env_and_input(self):
        expr = jsonata.Jsonata("$eval('$count($keys($))')")
        input1 = {"input": 1}
        input2 = {"input": 2, "other": 3}
        frame1 = expr.create_frame()
        frame2 = expr.create_frame()
        frame1.bind("variable", 1)
        frame2.bind("variable", 2)

        count = 10000

        async def threaded_function():
            total = 0
            for i in range(0, count):
                total += int(expr.evaluate(input1))
            return total

        total = 0
        for i in range(0, count):
            total += int(expr.evaluate(input2))

        outer = await threaded_function()
        assert outer == count
        assert total == 2 * count
