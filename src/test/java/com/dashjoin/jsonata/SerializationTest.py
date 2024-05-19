# JAVA TO PYTHON CONVERTER TASK: Java 'import static' statements are not converted by Java to Python Converter:
#import static com.dashjoin.jsonata.Jsonata.jsonata
from org.junit.jupiter.api import Assertions
from org.junit.jupiter.api import Test
from com.dashjoin.jsonata import Jsonata.JFunction
from com.dashjoin.jsonata import Jsonata.JFunctionCallable
from com.fasterxml.jackson.databind import ObjectMapper

class SerializationTest:

# JAVA TO PYTHON CONVERTER TASK: Java annotations have no direct Python equivalent:
# ORIGINAL LINE: @Test public void testJFunction() throws Exception
# JAVA TO PYTHON CONVERTER WARNING: Method 'throws' clauses are not available in Python:
    def testJFunction(self):
        # return the function and test its serialization
        expr = jsonata("$foo")
# JAVA TO PYTHON CONVERTER TASK: Java annotations have no direct Python equivalent:
# ORIGINAL LINE: expr.registerFunction("foo", new com.dashjoin.jsonata.Jsonata.JFunction(new com.dashjoin.jsonata.Jsonata.JFunctionCallable()
        expr.registerFunction("foo", com.dashjoin.jsonata.Jsonata.JFunction(JFunctionCallableAnonymousInnerClass(self)
        , None))
        om = com.fasterxml.jackson.databind.ObjectMapper()
        print(type(expr.evaluate(None)))
        om.writeValueAsString(expr.evaluate(None))

    class JFunctionCallableAnonymousInnerClass(com.dashjoin.jsonata.Jsonata.JFunctionCallable):

        def __init__(self, outerInstance):
            self._outerInstance = outerInstance


# JAVA TO PYTHON CONVERTER TASK: Java annotations have no direct Python equivalent:
# ORIGINAL LINE: @SuppressWarnings("rawtypes") @Override public Object call(Object input, java.util.List args) throws Throwable
# JAVA TO PYTHON CONVERTER WARNING: Method 'throws' clauses are not available in Python:
        def call(self, input, args):
            return None


    #  *
    #   * wrapper class that makes Jsonata serializable
    #   
    class SerializableExpression:

        #    *
        #     * jsonata expression
        #     

        #    *
        #     * parsed / transient expression
        #     

        #    *
        #     * constructor calls init
        #     
        def __init__(self, expression):
            # instance fields found by Java to Python Converter:
            self.expression = None
            self.jsonata = None

            self.init(expression)

        #    *
        #     * init the object before calling evaluate
        #     
        def init(self, expression):
            # remember jsonata string
            self.expression = expression

            # parse expression
            self.jsonata = jsonata(expression)

            # register any custom functions
            self.jsonata.registerFunction("hi", lambda : "hello world")

        SERIAL_VERSION_UID = 7675531659407424684

        #    *
        #     * custom serializer
        #     
# JAVA TO PYTHON CONVERTER WARNING: Method 'throws' clauses are not available in Python:
# ORIGINAL LINE: private void writeObject(java.io.ObjectOutputStream out) throws java.io.IOException
        def _writeObject(self, out):
            # only write jsonata string
            out.writeUTF(self.expression)

        #    *
        #     * custom deserializer
        #     
# JAVA TO PYTHON CONVERTER WARNING: Method 'throws' clauses are not available in Python:
# ORIGINAL LINE: private void readObject(java.io.ObjectInputStream in) throws IOException, ClassNotFoundException
        def _readObject(self, in_):
            # read jsonata string and init
            self.init(in_.readUTF())

    #  *
    #   * test RMI / hazelcast serialization
    #   
# JAVA TO PYTHON CONVERTER TASK: Java annotations have no direct Python equivalent:
# ORIGINAL LINE: @Test public void testSerializable() throws Exception
# JAVA TO PYTHON CONVERTER WARNING: Method 'throws' clauses are not available in Python:
    def testSerializable(self):
        # sample expression with custom function
        expr = SerializableExpression("$hi() & '!'")

        # test output
        org.junit.jupiter.api.Assertions.assertEquals("hello world!", expr.jsonata.evaluate(None))

        # buffer (i.e. network or file transport)
        buffer = java.io.ByteArrayOutputStream()

        # write to buffer
        oos = java.io.ObjectOutputStream(buffer)
        oos.writeObject(expr)

        # read from buffer
        ois = java.io.ObjectInputStream(java.io.ByteArrayInputStream(buffer.toByteArray()))
        clone = ois.readObject()

        # clone has same result
        org.junit.jupiter.api.Assertions.assertEquals(expr.jsonata.evaluate(None), clone.jsonata.evaluate(None))
