# JAVA TO PYTHON CONVERTER TASK: Java 'import static' statements are not converted by Java to Python Converter:
#import static com.dashjoin.jsonata.Jsonata.jsonata
from org.junit.jupiter.api import Assertions
from org.junit.jupiter.api import Test

#*
# * see https://docs.jsonata.org/string-functions#string
# 
class StringTest:

# JAVA TO PYTHON CONVERTER TASK: Java annotations have no direct Python equivalent:
# ORIGINAL LINE: @Test public void stringTest()
    def stringTest(self):
        org.junit.jupiter.api.Assertions.assertEquals("abc", jsonata("$string($)").evaluate("abc"))

# JAVA TO PYTHON CONVERTER TASK: Java annotations have no direct Python equivalent:
# ORIGINAL LINE: @Test public void booleanTest()
    def booleanTest(self):
        org.junit.jupiter.api.Assertions.assertEquals("true", jsonata("$string($)").evaluate(True))

# JAVA TO PYTHON CONVERTER TASK: Java annotations have no direct Python equivalent:
# ORIGINAL LINE: @Test public void numberTest()
    def numberTest(self):
        org.junit.jupiter.api.Assertions.assertEquals("5", jsonata("$string(5)").evaluate(None))

# JAVA TO PYTHON CONVERTER TASK: Java annotations have no direct Python equivalent:
# ORIGINAL LINE: @Test public void arrayTest()
    def arrayTest(self):
        org.junit.jupiter.api.Assertions.assertEquals(java.util.Arrays.asList("1", "2", "3", "4", "5"), jsonata("[1..5].$string()").evaluate(None))

# JAVA TO PYTHON CONVERTER TASK: Java annotations have no direct Python equivalent:
# ORIGINAL LINE: @Test public void mapTest()
    def mapTest(self):
        org.junit.jupiter.api.Assertions.assertEquals("{}", jsonata("$string($)").evaluate(java.util.Map.of()))

# JAVA TO PYTHON CONVERTER TASK: Java annotations have no direct Python equivalent:
# ORIGINAL LINE: @Test public void map2Test()
    def map2Test(self):
        org.junit.jupiter.api.Assertions.assertEquals("{\"x\":1}", jsonata("$string($)").evaluate(java.util.Map.of("x", 1)))

# JAVA TO PYTHON CONVERTER TASK: Java annotations have no direct Python equivalent:
# ORIGINAL LINE: @Test public void escapeTest()
    def escapeTest(self):
        org.junit.jupiter.api.Assertions.assertEquals("{\"a\":\"\\\"\"}", jsonata("$string($)").evaluate(java.util.Map.of("a", "" + '"')))
        org.junit.jupiter.api.Assertions.assertEquals("{\"a\":\"\\\\\"}", jsonata("$string($)").evaluate(java.util.Map.of("a", "" + '\\')))
        org.junit.jupiter.api.Assertions.assertEquals("{\"a\":\"\\t\"}", jsonata("$string($)").evaluate(java.util.Map.of("a", "" + '\t')))
        org.junit.jupiter.api.Assertions.assertEquals("{\"a\":\"\\n\"}", jsonata("$string($)").evaluate(java.util.Map.of("a", "" + '\n')))
        org.junit.jupiter.api.Assertions.assertEquals("{\"a\":\"</\"}", jsonata("$string($)").evaluate(java.util.Map.of("a", "</")))

    #  *
    #   * Additional $split tests
    #   
# JAVA TO PYTHON CONVERTER TASK: Java annotations have no direct Python equivalent:
# ORIGINAL LINE: @Test public void splitTest()
    def splitTest(self):
        res = None

        # Splitting empty string with empty separator must return empty list
        res = jsonata("$split('', '')").evaluate(None)
        org.junit.jupiter.api.Assertions.assertEquals(java.util.Arrays.asList(), res)

        # Split characters with limit
        res = jsonata("$split('a1b2c3d4', '', 4)").evaluate(None)
        org.junit.jupiter.api.Assertions.assertEquals(java.util.Arrays.asList("a", "1", "b", "2"), res)

        # Check string is not treated as regexp
        res = jsonata("$split('this..is.a.test', '.')").evaluate(None)
        #System.out.println( Functions.string(res, false))
        org.junit.jupiter.api.Assertions.assertEquals(java.util.Arrays.asList("this","","is","a","test"), res)

        # Check trailing empty strings
        res = jsonata("$split('this..is.a.test...', '.')").evaluate(None)
        #System.out.println( Functions.string(res, false))
        org.junit.jupiter.api.Assertions.assertEquals(java.util.Arrays.asList("this","","is","a","test","","",""), res)

        # Check trailing empty strings
        res = jsonata("$split('this..is.a.test...', /\\./)").evaluate(None)
        org.junit.jupiter.api.Assertions.assertEquals(java.util.Arrays.asList("this","","is","a","test","","",""), res)

        # Check string is not treated as regexp, trailing empty strings, and limit
        res = jsonata("$split('this.*.*is.*a.*test.*.*.*.*.*.*', '.*', 8)").evaluate(None)
        org.junit.jupiter.api.Assertions.assertEquals(java.util.Arrays.asList("this","","is","a","test","","",""), res)

        # Escaped regexp, trailing empty strings, and limit
        res = jsonata("$split('this.*.*is.*a.*test.*.*.*.*.*.*', /\\.\\*/, 8)").evaluate(None)
        org.junit.jupiter.api.Assertions.assertEquals(java.util.Arrays.asList("this","","is","a","test","","",""), res)

# JAVA TO PYTHON CONVERTER TASK: Java annotations have no direct Python equivalent:
# ORIGINAL LINE: @Test public void trimTest()
    def trimTest(self):
        org.junit.jupiter.api.Assertions.assertEquals("", jsonata("$trim(\"\n\")").evaluate(None))
        org.junit.jupiter.api.Assertions.assertEquals("", jsonata("$trim(\" \")").evaluate(None))
        org.junit.jupiter.api.Assertions.assertEquals("", jsonata("$trim(\"\")").evaluate(None))
        org.junit.jupiter.api.Assertions.assertEquals(None, jsonata("$trim(notthere)").evaluate(None))
