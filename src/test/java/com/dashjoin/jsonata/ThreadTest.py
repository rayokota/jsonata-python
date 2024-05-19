# JAVA TO PYTHON CONVERTER TASK: Java 'import static' statements are not converted by Java to Python Converter:
#import static com.dashjoin.jsonata.Jsonata.jsonata
from org.junit.jupiter.api import Assertions
from org.junit.jupiter.api import Test
from com.dashjoin.jsonata import Jsonata.Frame

class ThreadTest:

# JAVA TO PYTHON CONVERTER TASK: Java annotations have no direct Python equivalent:
# ORIGINAL LINE: @Test public void testReuse()
    def testReuse(self):
        expr = jsonata("a")
        org.junit.jupiter.api.Assertions.assertEquals(1, expr.evaluate(java.util.Map.of("a", 1)))
        org.junit.jupiter.api.Assertions.assertEquals(1, expr.evaluate(java.util.Map.of("a", 1)))

# JAVA TO PYTHON CONVERTER TASK: Java annotations have no direct Python equivalent:
# ORIGINAL LINE: @Test public void testNow() throws InterruptedException
# JAVA TO PYTHON CONVERTER WARNING: Method 'throws' clauses are not available in Python:
    def testNow(self):
        now = jsonata("$now()")
        r1 = now.evaluate(None)
        Thread.sleep(42)
        r2 = now.evaluate(None)
        org.junit.jupiter.api.Assertions.assertNotEquals(r1, r2)

# JAVA TO PYTHON CONVERTER TASK: Java annotations have no direct Python equivalent:
# ORIGINAL LINE: @Test public void testReuseWithVariable() throws InterruptedException, java.util.concurrent.ExecutionException
# JAVA TO PYTHON CONVERTER WARNING: Method 'throws' clauses are not available in Python:
    def testReuseWithVariable(self):
        expr = jsonata("($x := a; $wait(a); $x)")
# JAVA TO PYTHON CONVERTER TASK: Only expression lambdas are converted by Java to Python Converter:
        #    expr.registerFunction("wait", (Integer a) ->
        #    {
        #      try
        #      {
        #        Thread.sleep(a)
        #      }
        #      catch (InterruptedException e)
        #      {
        #        e.printStackTrace()
        #      }
        #      return null
        #    }
        #    )

        # start a thread that sets x=100 and waits 100 before returning x
        outer = java.util.concurrent.Executors.newSingleThreadExecutor().submit(lambda : expr.evaluate(java.util.Map.of("a", 100)))

        # make sure outer thread is initialized and in $wait
        Thread.sleep(10)

        # this thread uses the same expr and terminates before thread is done
        org.junit.jupiter.api.Assertions.assertEquals(30, expr.evaluate(java.util.Map.of("a", 30)))

        # the outer thread is unaffected by the previous operations
        org.junit.jupiter.api.Assertions.assertEquals(100, outer.get())

# JAVA TO PYTHON CONVERTER TASK: Java annotations have no direct Python equivalent:
# ORIGINAL LINE: @Test public void testAddEnvAndInput() throws Exception
# JAVA TO PYTHON CONVERTER WARNING: Method 'throws' clauses are not available in Python:
    def testAddEnvAndInput(self):
        expr = jsonata("$eval('$count($keys($))')")
        input1 = { "input": 1 }
        input2 = { "input": 2, "other": 3 }
        frame1 = expr.createFrame()
        frame2 = expr.createFrame()
        frame1.bind("variable", 1)
        frame2.bind("variable", 2)

        count = 10000
# JAVA TO PYTHON CONVERTER TASK: Only expression lambdas are converted by Java to Python Converter:
        #    Future<?> out = Executors.newSingleThreadExecutor().submit(() ->
        #    {
        #      int sum = 0
        #      for (int i = 0; i < count; i++)
        #      {
        #        sum += (int) expr.evaluate(input1)
        #      }
        #      return sum
        #    }
        #    )

        sum = 0
        for i in range(0, count):
            sum += int(expr.evaluate(input2))

        org.junit.jupiter.api.Assertions.assertEquals(count, out.get())
        org.junit.jupiter.api.Assertions.assertEquals(2 * count, sum)
