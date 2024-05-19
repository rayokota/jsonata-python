# JAVA TO PYTHON CONVERTER TASK: Java 'import static' statements are not converted by Java to Python Converter:
#import static com.dashjoin.jsonata.Jsonata.jsonata
from org.junit.jupiter.api import Assertions
from org.junit.jupiter.api import Test
from com.dashjoin.jsonata import Jsonata.JFunction
from com.dashjoin.jsonata import Jsonata.JFunctionCallable

class SignatureTest:

# JAVA TO PYTHON CONVERTER TASK: Java annotations have no direct Python equivalent:
# ORIGINAL LINE: @Test public void testParametersAreConvertedToArrays()
    def testParametersAreConvertedToArrays(self):
        expr = jsonata("$greet(1,null,3)")
# JAVA TO PYTHON CONVERTER TASK: Java annotations have no direct Python equivalent:
# ORIGINAL LINE: expr.registerFunction("greet", new com.dashjoin.jsonata.Jsonata.JFunction(new com.dashjoin.jsonata.Jsonata.JFunctionCallable()
        expr.registerFunction("greet", com.dashjoin.jsonata.Jsonata.JFunction(JFunctionCallableAnonymousInnerClass(self)
        , "<a?a?a?a?:s>"))
        org.junit.jupiter.api.Assertions.assertEquals("[[1], [null], [3], [null]]", expr.evaluate(None))

    class JFunctionCallableAnonymousInnerClass(com.dashjoin.jsonata.Jsonata.JFunctionCallable):

        def __init__(self, outerInstance):
            self._outerInstance = outerInstance


# JAVA TO PYTHON CONVERTER TASK: Java annotations have no direct Python equivalent:
# ORIGINAL LINE: public Object call(Object input, @SuppressWarnings("rawtypes") java.util.List args) throws Throwable
# JAVA TO PYTHON CONVERTER WARNING: Method 'throws' clauses are not available in Python:
        def call(self, input, args):
            return str(args)

# JAVA TO PYTHON CONVERTER TASK: Java annotations have no direct Python equivalent:
# ORIGINAL LINE: @Test public void testError()
    def testError(self):
        expr = jsonata("$foo()")
# JAVA TO PYTHON CONVERTER TASK: Java annotations have no direct Python equivalent:
# ORIGINAL LINE: expr.registerFunction("foo", new com.dashjoin.jsonata.Jsonata.JFunction(new com.dashjoin.jsonata.Jsonata.JFunctionCallable()
        expr.registerFunction("foo", com.dashjoin.jsonata.Jsonata.JFunction(JFunctionCallableAnonymousInnerClass2(self)
        , "(sao)"))

        # null not allowed
        org.junit.jupiter.api.Assertions.assertThrows(JException.class, lambda : expr.evaluate(None))

        # boolean not allowed
        org.junit.jupiter.api.Assertions.assertThrows(JException.class, lambda : expr.evaluate(True))

    class JFunctionCallableAnonymousInnerClass2(com.dashjoin.jsonata.Jsonata.JFunctionCallable):

        def __init__(self, outerInstance):
            self._outerInstance = outerInstance


# JAVA TO PYTHON CONVERTER TASK: Java annotations have no direct Python equivalent:
# ORIGINAL LINE: public Object call(Object input, @SuppressWarnings("rawtypes") java.util.List args) throws Throwable
# JAVA TO PYTHON CONVERTER WARNING: Method 'throws' clauses are not available in Python:
        def call(self, input, args):
            return None
