from org.junit.jupiter.api import Assertions
from org.junit.jupiter.api import Test
from com.dashjoin.jsonata import Jsonata.JFunction
from com.dashjoin.jsonata import Jsonata.JFunctionCallable

class CustomFunctionTest:

# JAVA TO PYTHON CONVERTER TASK: Java annotations have no direct Python equivalent:
# ORIGINAL LINE: @Test public void testSupplier()
    def testSupplier(self):
        expression = Jsonata.jsonata("$greet()")
        expression.registerFunction("greet", lambda : "Hello world")
        org.junit.jupiter.api.Assertions.assertEquals("Hello world", expression.evaluate(None))

# JAVA TO PYTHON CONVERTER TASK: Java annotations have no direct Python equivalent:
# ORIGINAL LINE: @Test public void testUnary()
    def testUnary(self):
        expression = Jsonata.jsonata("$echo(123)")
        expression.registerFunction("echo", lambda x : x)
        org.junit.jupiter.api.Assertions.assertEquals(123, expression.evaluate(None))

# JAVA TO PYTHON CONVERTER TASK: Java annotations have no direct Python equivalent:
# ORIGINAL LINE: @Test public void testBinary()
    def testBinary(self):
        expression = Jsonata.jsonata("$add(21, 21)")
        expression.registerFunction("add", lambda a, b : a + b)
        org.junit.jupiter.api.Assertions.assertEquals(42, expression.evaluate(None))

# JAVA TO PYTHON CONVERTER TASK: Java annotations have no direct Python equivalent:
# ORIGINAL LINE: @Test public void testTernary()
    def testTernary(self):
        expression = Jsonata.jsonata("$abc(a,b,c)")
# JAVA TO PYTHON CONVERTER TASK: Java annotations have no direct Python equivalent:
# ORIGINAL LINE: expression.registerFunction("abc", new com.dashjoin.jsonata.Jsonata.JFunction(new com.dashjoin.jsonata.Jsonata.JFunctionCallable()
        expression.registerFunction("abc", com.dashjoin.jsonata.Jsonata.JFunction(JFunctionCallableAnonymousInnerClass(self)
        , "<sss:s>"))
        org.junit.jupiter.api.Assertions.assertEquals("abc", expression.evaluate(java.util.Map.of("a", "a", "b", "b", "c", "c")))

    class JFunctionCallableAnonymousInnerClass(com.dashjoin.jsonata.Jsonata.JFunctionCallable):

        def __init__(self, outerInstance):
            self._outerInstance = outerInstance

# JAVA TO PYTHON CONVERTER TASK: Java annotations have no direct Python equivalent:
# ORIGINAL LINE: @SuppressWarnings("rawtypes") @Override public Object call(Object input, java.util.List args) throws Throwable
# JAVA TO PYTHON CONVERTER WARNING: Method 'throws' clauses are not available in Python:
        def call(self, input, args):
            return str(args[0]) + str(args[1]) + str(args[2])

    #  *
    #   * Lambdas use no signature - in case of an error, a ClassCastException is thrown
    #   
# JAVA TO PYTHON CONVERTER TASK: Java annotations have no direct Python equivalent:
# ORIGINAL LINE: @Test public void testLambdaSignatureError()
    def testLambdaSignatureError(self):
        expression = Jsonata.jsonata("$append(1, 2)")
        expression.registerFunction("append", lambda a, b : "" + a + b)
        org.junit.jupiter.api.Assertions.assertThrowsExactly(ClassCastException.class, lambda : expression.evaluate(None))

    #  *
    #   * provide signature: number, boolean => string
    #   
# JAVA TO PYTHON CONVERTER TASK: Java annotations have no direct Python equivalent:
# ORIGINAL LINE: @Test public void testJFunctionSignatureError()
    def testJFunctionSignatureError(self):
        expression = Jsonata.jsonata("$append(1, 2)")
# JAVA TO PYTHON CONVERTER TASK: Java annotations have no direct Python equivalent:
# ORIGINAL LINE: expression.registerFunction("append", new com.dashjoin.jsonata.Jsonata.JFunction(new com.dashjoin.jsonata.Jsonata.JFunctionCallable()
        expression.registerFunction("append", com.dashjoin.jsonata.Jsonata.JFunction(JFunctionCallableAnonymousInnerClass2(self)
        , "<nb:s>"))
        ex = org.junit.jupiter.api.Assertions.assertThrowsExactly(JException.class, lambda : expression.evaluate(None))
        org.junit.jupiter.api.Assertions.assertEquals("T0410", ex.getError())
        org.junit.jupiter.api.Assertions.assertEquals("append", ex.getExpected())

    class JFunctionCallableAnonymousInnerClass2(com.dashjoin.jsonata.Jsonata.JFunctionCallable):

        def __init__(self, outerInstance):
            self._outerInstance = outerInstance

# JAVA TO PYTHON CONVERTER TASK: Java annotations have no direct Python equivalent:
# ORIGINAL LINE: public Object call(Object input, @SuppressWarnings("rawtypes") java.util.List args) throws Throwable
# JAVA TO PYTHON CONVERTER WARNING: Method 'throws' clauses are not available in Python:
        def call(self, input, args):
            return "" + args[0] + args[1]
