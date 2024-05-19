import datetime

# JAVA TO PYTHON CONVERTER TASK: Java 'import static' statements are not converted by Java to Python Converter:
#import static com.dashjoin.jsonata.Jsonata.jsonata
from org.junit.jupiter.api import Assertions
from org.junit.jupiter.api import Test
from com.fasterxml.jackson.databind import ObjectMapper

class TypesTest:

# JAVA TO PYTHON CONVERTER TASK: Java annotations have no direct Python equivalent:
# ORIGINAL LINE: @Test public void testIllegalTypes()
    def testIllegalTypes(self):
        # array
        org.junit.jupiter.api.Assertions.assertThrows(IllegalArgumentException.class, lambda : jsonata("$").evaluate([0, 1, 2, 3]))
        # char
        org.junit.jupiter.api.Assertions.assertThrows(IllegalArgumentException.class, lambda : jsonata("$").evaluate('c'))
        # date
        org.junit.jupiter.api.Assertions.assertThrows(IllegalArgumentException.class, lambda : jsonata("$").evaluate(datetime.datetime.now()))

# JAVA TO PYTHON CONVERTER TASK: Java annotations have no direct Python equivalent:
# ORIGINAL LINE: @Test public void testLegalTypes()
    def testLegalTypes(self):
        # map
        org.junit.jupiter.api.Assertions.assertEquals(1, jsonata("a").evaluate(java.util.Map.of("a", 1)))
        # list
        org.junit.jupiter.api.Assertions.assertEquals(1, jsonata("$[0]").evaluate(java.util.Arrays.asList(1, 2)))
        # string
        org.junit.jupiter.api.Assertions.assertEquals("string", jsonata("$").evaluate("string"))
        # int
        org.junit.jupiter.api.Assertions.assertEquals(1, jsonata("$").evaluate(1))
        # long
        org.junit.jupiter.api.Assertions.assertEquals(1, jsonata("$").evaluate(1))
        # boolean
        org.junit.jupiter.api.Assertions.assertEquals(True, jsonata("$").evaluate(True))
        # double
        org.junit.jupiter.api.Assertions.assertEquals(1.0, jsonata("$").evaluate(1.0))
        # float
        org.junit.jupiter.api.Assertions.assertEquals(float(1.0), jsonata("$").evaluate(float(1.0)))
        # big decimal
        org.junit.jupiter.api.Assertions.assertEquals(java.math.BigDecimal(3.14), jsonata("$").evaluate(java.math.BigDecimal(3.14)))

    class Pojo:

        def __init__(self):
            # instance fields found by Java to Python Converter:
            self.c = 'c'
            self.d = datetime.datetime.now()
            self.arr = [0, 1, 2, 3]


# JAVA TO PYTHON CONVERTER TASK: Java annotations have no direct Python equivalent:
# ORIGINAL LINE: @Test public void testJacksonConversion()
    def testJacksonConversion(self):
        om = com.fasterxml.jackson.databind.ObjectMapper()
        input = om.convertValue(Pojo(), Object.class)
        org.junit.jupiter.api.Assertions.assertEquals("c", jsonata("c").evaluate(input))
        org.junit.jupiter.api.Assertions.assertEquals(0, jsonata("arr[0]").evaluate(input))
        org.junit.jupiter.api.Assertions.assertEquals(Long.class, type(jsonata("d").evaluate(input)))

        output = jsonata("$").evaluate(input)
        org.junit.jupiter.api.Assertions.assertEquals('c', om.convertValue(output, Pojo.class).c)

# JAVA TO PYTHON CONVERTER TASK: Java annotations have no direct Python equivalent:
# ORIGINAL LINE: @SuppressWarnings("unchecked") @Test public void testCustomFunction()
    def testCustomFunction(self):
        om = com.fasterxml.jackson.databind.ObjectMapper()
        fn = jsonata("$foo()")
        fn.registerFunction("foo", lambda : om.convertValue(Pojo(), Object.class))
        res = fn.evaluate(None)
        org.junit.jupiter.api.Assertions.assertEquals("c", res["c"])

# JAVA TO PYTHON CONVERTER TASK: Java annotations have no direct Python equivalent:
# ORIGINAL LINE: @Test public void testIgnore()
    def testIgnore(self):
        expr = jsonata("a")
        date = datetime.datetime.now()

        # date causes exception
        org.junit.jupiter.api.Assertions.assertThrows(IllegalArgumentException.class, lambda : expr.evaluate(java.util.Map.of("a", date)))

        # turn off validation, Date is "passed" via $
        expr.setValidateInput(False)
        org.junit.jupiter.api.Assertions.assertEquals(date, expr.evaluate(java.util.Map.of("a", date)))

        # change expression to a computation that involves a, we get an error again because concat
        # cannot deal with Date
        expr2 = jsonata("a & a")
        expr2.setValidateInput(False)
        org.junit.jupiter.api.Assertions.assertThrows(IllegalArgumentException.class, lambda : expr2.evaluate(java.util.Map.of("a", date)))
