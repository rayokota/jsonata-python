# JAVA TO PYTHON CONVERTER TASK: Java 'import static' statements are not converted by Java to Python Converter:
#import static com.dashjoin.jsonata.Jsonata.jsonata

from org.junit.jupiter.api import Assertions
from org.junit.jupiter.api import Test

class NullSafetyTest:
# JAVA TO PYTHON CONVERTER TASK: Java annotations have no direct Python equivalent:
# ORIGINAL LINE: @Test public void testNullSafety()
    def testNullSafety(self):
        res = None
        res = jsonata("$sift(undefined, $uppercase)").evaluate(None)
        org.junit.jupiter.api.Assertions.assertEquals(None, res)

        res = jsonata("$each(undefined, $uppercase)").evaluate(None)
        org.junit.jupiter.api.Assertions.assertEquals(None, res)

        res = jsonata("$keys(null)").evaluate(None)
        org.junit.jupiter.api.Assertions.assertEquals(None, res)

        res = jsonata("$map(null, $uppercase)").evaluate(None)
        org.junit.jupiter.api.Assertions.assertEquals(None, res)

        res = jsonata("$filter(null, $uppercase)").evaluate(None)
        org.junit.jupiter.api.Assertions.assertEquals(None, res)

        res = jsonata("$single(null, $uppercase)").evaluate(None)
        org.junit.jupiter.api.Assertions.assertEquals(None, res)

        res = jsonata("$reduce(null, $uppercase)").evaluate(None)
        org.junit.jupiter.api.Assertions.assertEquals(None, res)

        res = jsonata("$lookup(null, 'anykey')").evaluate(None)
        org.junit.jupiter.api.Assertions.assertEquals(None, res)

        res = jsonata("$spread(null)").evaluate(None)
        org.junit.jupiter.api.Assertions.assertEquals(None, res)
