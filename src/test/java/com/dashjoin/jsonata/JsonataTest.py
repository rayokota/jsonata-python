import math

# JAVA TO PYTHON CONVERTER TASK: Java 'import static' statements are not converted by Java to Python Converter:
#import static org.junit.jupiter.api.Assertions.assertEquals


from org.apache.commons.io import IOUtils
from org.junit.jupiter.api import Disabled
from org.junit.jupiter.api import Test

# JAVA TO PYTHON CONVERTER TASK: Java 'import static' statements are not converted by Java to Python Converter:
#import static com.dashjoin.jsonata.Jsonata.jsonata
from com.dashjoin.jsonata import Jsonata.Frame
from com.dashjoin.jsonata.json import Json
from com.fasterxml.jackson.core import JsonProcessingException
from com.fasterxml.jackson.core.exc import StreamReadException
from com.fasterxml.jackson.databind import DatabindException
from com.fasterxml.jackson.databind import DeserializationFeature
from com.fasterxml.jackson.databind import JsonMappingException
from com.fasterxml.jackson.databind import ObjectMapper

# JAVA TO PYTHON CONVERTER TASK: Java 'import static' statements are not converted by Java to Python Converter:
#import static com.dashjoin.jsonata.Jsonata.NULL_VALUE

# JAVA TO PYTHON CONVERTER TASK: Java annotations have no direct Python equivalent:
# ORIGINAL LINE: @SuppressWarnings({"rawtypes", "unchecked"}) public class JsonataTest
class JsonataTest:

    def __init__(self):
        # instance fields found by Java to Python Converter:
        self.testFiles = 0
        self.testCases = 0
        self.groupDir = "jsonata/test/test-suite/groups/"
        self.debug = "-Xrunjdwp:transport" in str(java.lang.management.ManagementFactory.getRuntimeMXBean().getInputArguments())
        self.ignoreOverrides = False


    def testExpr(self, expr, data, bindings, expected, code):
        success = True
        try:

            if self.debug:
                print("Expr=" + expr + " Expected=" + expected + " ErrorCode=" + code)
            if self.debug:
                print(data)

            bindingFrame = None
            if bindings is not None:
                # If we have bindings, create a binding env with the settings
                bindingFrame = com.dashjoin.jsonata.Jsonata.Frame(None)
                for e in bindings.entrySet():
                    bindingFrame.bind(e.getKey(), e.getValue())

            jsonata = jsonata(expr)
            if bindingFrame is not None:
                bindingFrame.setRuntimeBounds(500000 if self.debug else 1000, 303)
            result = jsonata.evaluate(data, bindingFrame)
            if code is not None:
                success = False

            if expected is not None and expected is not result:
                # if ((""+expected).equals(""+result))
                #     System.out.println("Value equals failed, stringified equals = true. Result = "+result)
                # else
                success = False

            if expected is None and result is not None:
                success = False

            if self.debug and success:
                print("--Result = " + result)

            if not success:
                print("--Expr=" + expr + " Expected=" + expected + " ErrorCode=" + code)
                print("--Data=" + data)
                print("--Result = " + result + " Class=" + (type(result) if result is not None else None))
                print("--Expect = " + expected + " ExpectedError=" + code)
                print("WRONG RESULT")

            #assertEquals("Must be equal", expected, ""+result)
        except Throwable as t:
            if code is None:
                print("--Expr=" + expr + " Expected=" + expected + " ErrorCode=" + code)
                print("--Data=" + data)

                if isinstance(t, JException):
                    je = t
                    print("--Exception     = " + je.error + "  --> " + je)
                else:
                    print("--Exception     = " + t)

                print("--ExpectedError = " + code + " Expected=" + expected)
                print("WRONG RESULT (exception)")
                success = False
            if not success:
                t.printStackTrace(System.out)
            if self.debug and success:
                print("--Exception = " + t)
            #if (true) System.exit(-1)
        return success

    om = com.fasterxml.jackson.databind.ObjectMapper().configure(com.fasterxml.jackson.databind.DeserializationFeature.USE_LONG_FOR_INTS, True)
    def getObjectMapper(self):
        return com.dashjoin.jsonata.JsonataTest.om

# JAVA TO PYTHON CONVERTER WARNING: Method 'throws' clauses are not available in Python:
# ORIGINAL LINE: Object toJson(String jsonStr) throws JsonMappingException, com.fasterxml.jackson.core.JsonProcessingException
    def toJson(self, jsonStr):
        #ObjectMapper om = getObjectMapper()
        #Object json = om.readValue(jsonStr, Object.class)
        json = com.dashjoin.jsonata.json.Json.parseJson(jsonStr)
        return json

# JAVA TO PYTHON CONVERTER WARNING: Method 'throws' clauses are not available in Python:
# ORIGINAL LINE: Object readJson(String name) throws StreamReadException, DatabindException, java.io.IOException
    def readJson(self, name):
        #ObjectMapper om = getObjectMapper()
        #Object json = om.readValue(new java.io.FileReader(name, Charset.forName("UTF-8")), Object.class)

        json = com.dashjoin.jsonata.json.Json.parseJson(java.io.FileReader(name, java.nio.charset.Charset.forName("UTF-8")))
        return json

# JAVA TO PYTHON CONVERTER TASK: Java annotations have no direct Python equivalent:
# ORIGINAL LINE: @Test public void testSimple()
    def testSimple(self):
        self.testExpr("42", None, None, 42,None)
        self.testExpr("(3*(4-2)+1.01e2)/-2", None, None, -53.5,None)

# JAVA TO PYTHON CONVERTER TASK: Java annotations have no direct Python equivalent:
# ORIGINAL LINE: @Test public void testPath() throws Exception
# JAVA TO PYTHON CONVERTER WARNING: Method 'throws' clauses are not available in Python:
    def testPath(self):
        data = self.readJson("jsonata/test/test-suite/datasets/dataset0.json")
        print(data)
        self.testExpr("foo.bar", data, None, 42,None)

    class TestDef:

        def __init__(self):
            # instance fields found by Java to Python Converter:
            self.expr = None
            self.dataset = None
            self.bindings = None
            self.result = None



# JAVA TO PYTHON CONVERTER WARNING: Method 'throws' clauses are not available in Python:
# ORIGINAL LINE: public void runCase(String name) throws Exception
    def runCase(self, name):
        if not self.runTestSuite(name):
            raise Exception()

# JAVA TO PYTHON CONVERTER WARNING: Method 'throws' clauses are not available in Python:
# ORIGINAL LINE: public void runSubCase(String name, int subNr) throws Exception
    def runSubCase(self, name, subNr):
        cases = self.readJson(name)
        if not self.runTestCase(name + "_" + str(subNr), cases[subNr]):
            raise Exception()

# JAVA TO PYTHON CONVERTER WARNING: Method 'throws' clauses are not available in Python:
# ORIGINAL LINE: boolean runTestSuite(String name) throws Exception
    def runTestSuite(self, name):

        #System.out.println("Running test "+name)
        self.testFiles += 1

        success = True

        testCase = self.readJson(name)
        if isinstance(testCase, java.util.List):
            # some cases contain a list of test cases
            # loop over the case definitions
            for testDef in (testCase):
                print("Running sub-test")
                success &= self.runTestCase(name, testDef)
        else:
            success &= self.runTestCase(name, testCase)
        return success

    def replaceNulls(self, o):
        if isinstance(o, java.util.List):
            index = 0
            for i in (o):
                if i is None:
                    (o)[index] = Jsonata.NULL_VALUE
                else:
                    self.replaceNulls(i)
                index += 1
        if isinstance(o, java.util.Map):
            for e in (o).entrySet():
                if e.getValue() is None:
                    e.setValue(Jsonata.NULL_VALUE)
                else:
                    self.replaceNulls(e.getValue())

    class TestOverride:

        def __init__(self):
            # instance fields found by Java to Python Converter:
            self.name = None
            self.ignoreError = False
            self.alternateResult = None
            self.alternateCode = None
            self.reason = None


    class TestOverrides:

        def __init__(self):
            # instance fields found by Java to Python Converter:
            self.override = None


    testOverrides = None

    @staticmethod
    def getTestOverrides():
        if com.dashjoin.jsonata.JsonataTest.testOverrides is not None:
            return com.dashjoin.jsonata.JsonataTest.testOverrides

        try:
            com.dashjoin.jsonata.JsonataTest.testOverrides = (com.fasterxml.jackson.databind.ObjectMapper()).readValue(java.io.File("test/test-overrides.json"), TestOverrides.class)
        except java.io.IOException as e:
            e.printStackTrace()
            raise RuntimeException(e)
        return com.dashjoin.jsonata.JsonataTest.testOverrides

    def getOverrideForTest(self, name):
        if self.ignoreOverrides:
            return None

        tos = com.dashjoin.jsonata.JsonataTest.getTestOverrides()
        for to in tos.override:
            if name.find(to.name) >= 0:
                return to
        return None

# JAVA TO PYTHON CONVERTER WARNING: Method 'throws' clauses are not available in Python:
# ORIGINAL LINE: boolean runTestCase(String name, java.util.Map<String, Object> testDef) throws Exception
    def runTestCase(self, name, testDef):

        self.testCases += 1
        if self.debug:
            print("\nRunning test " + name)

        expr = str(testDef["expr"])

        if expr is None:
            exprFile = str(testDef["expr-file"])
            fileName = name[0:name.rfind("/")] + "/" + exprFile
            expr = org.apache.commons.io.IOUtils.toString(java.io.FileInputStream(fileName))

        dataset = str(testDef["dataset"])
        bindings = testDef["bindings"]
        result = testDef["result"]

        # if (result == null)
        #   if (testDef.containsKey("result"))
        #     result = Jsonata.NULL_VALUE

        #replaceNulls(result)

        code = str(testDef["code"])

        if isinstance(testDef["error"], java.util.Map):
            code = str((testDef["error"])["code"])

        #System.out.println(""+bindings)

        data = testDef["data"]
        if data is None and dataset is not None:
            data = self.readJson("jsonata/test/test-suite/datasets/" + dataset + ".json")

        to = self.getOverrideForTest(name)
        if to is not None:
            print("OVERRIDE used : " + to.name + " for " + name + " reason=" + to.reason)
            if to.alternateResult is not None:
                result = to.alternateResult
            if to.alternateCode is not None:
                code = to.alternateCode
        res = False
        if self.debug and expr == "(  $inf := function(){$inf()};  $inf())":
            System.err.println("DEBUG MODE: skipping infinity test: " + expr)
            res = True
        else:
            res = self.testExpr(expr, data, bindings, result, code)

        if to is not None:
            # There is an override/alternate result for this defined...
            if res == False and to.ignoreError is not None and to.ignoreError:
                print("Test " + name + " failed, but override allows failure")
                res = True

        return res


# JAVA TO PYTHON CONVERTER WARNING: Method 'throws' clauses are not available in Python:
# ORIGINAL LINE: boolean runTestGroup(String group) throws Exception
    def runTestGroup(self, group):

        dir = java.io.File(self.groupDir, group)
        print("Run group " + dir)
        files = dir.listFiles()
        files.sort()
        success = True
        count = 0
        good = 0
        for f in files:
            name = f.getName()
            if name.endswith(".json"):
                res = self.runTestSuite(self.groupDir + group + "/" + name)
                success &= res

                count += 1
                if res:
                    good += 1
        successPercentage = math.trunc(100 * good / float(count))
        print("Success: " + str(good) + " / " + str(count) + " = " + (math.trunc(100 * good / float(count))) + "%")
        assertEquals(count, good, str(successPercentage) + "% succeeded")
        #assertEquals("100% test runs must succeed", 100, successPercentage)
        return success



    # For local dev: @Test
# JAVA TO PYTHON CONVERTER WARNING: Method 'throws' clauses are not available in Python:
# ORIGINAL LINE: public void testSuite() throws Exception
    def testSuite(self):
        #runTestSuite("jsonata/test/test-suite/groups/boolean-expresssions/test.jsonx")
        #runTestSuite("jsonata/test/test-suite/groups/boolean-expresssions/case017.json")
        #runTestSuite("jsonata/test/test-suite/groups/fields/case000.json")
        #runTestGroup("fields")
        #runTestGroup("comments")
        #runTestGroup("comparison-operators")
        #runTestGroup("boolean-expresssions")
        #runTestGroup("array-constructor")
        #runTestGroup("transform")
        #runTestGroup("function-substring")
        #runTestGroup("wildcards")
        #runTestSuite("jsonata/test/test-suite/groups/function-substring/case012.json")
        #runTestSuite("jsonata/test/test-suite/groups/transform/case030.json")
        #runTestSuite("jsonata/test/test-suite/groups/array-constructor/case006.json")
        # Filter:
        #runTestSuite("jsonata/test/test-suite/groups/array-constructor/case017.json")
        s = "jsonata/test/test-suite/groups/wildcards/case003.json"
        s = "jsonata/test/test-suite/groups/flattening/large.json"
        s = "jsonata/test/test-suite/groups/function-sum/case006.json"
        s = "jsonata/test/test-suite/groups/function-substring/case016.json"
        s = "jsonata/test/test-suite/groups/null/case001.json"
        s = "jsonata/test/test-suite/groups/context/case003.json"
        s = "jsonata/test/test-suite/groups/object-constructor/case008.json"
        self.runTestSuite(s)
        #String g = "function-applications"; // partly
        #String g = "higher-order-functions"; // works!
        #String g = "hof-map"
        #String g = "joins"
        #String g = "function-join"; // looks good
        #String g = "descendent-operator"; // nearly
        #String g = "object-constructor"
        #String g = "flattening"
        #String g = "parent-operator"
        #String g = "function-substring"; // nearly - unicode encoding issues
        #String g = "function-substringBefore"; // works!
        #String g = "function-substringAfter"; // works!
        #String g = "function-sum"; // works! rounding error delta
        #String g = "function-max"; // nearly - [-1,-5] second unary wrong!!!
        #String g = "function-average"; // nearly - [-1,-5] second unary wrong!!!
        #String g = "function-pad"; // nearly - unicode
        #String g = "function-trim"; // works!
        #String g = "function-contains"; // works NO regexp
        #String g = "function-join"; // works NO regexp
        #runTestGroup(g)

        #runAllTestGroups()

# JAVA TO PYTHON CONVERTER WARNING: Method 'throws' clauses are not available in Python:
# ORIGINAL LINE: void runAllTestGroups() throws Exception
    def runAllTestGroups(self):
        dir = java.io.File(self.groupDir)
        groups = dir.listFiles()
        groups.sort()
        for g in groups:
            name = g.getName()
            print("@Test")
            print("public void runTestGroup_" + name.replaceAll("-","_") + "() {")
            print("\trunTestGroup(\"" + name + "\");")
            print("}")
            #runTestGroup(name)

        print("Total test files=" + str(self.testFiles) + " cases=" + str(self.testCases))
