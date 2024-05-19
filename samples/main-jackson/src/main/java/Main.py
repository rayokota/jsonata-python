# JAVA TO PYTHON CONVERTER TASK: Java 'import static' statements are not converted by Java to Python Converter:
#import static com.dashjoin.jsonata.Jsonata.jsonata
from com.fasterxml.jackson.databind import ObjectMapper

class Main:

    #    *
    #     * Interoperability with Jackson Databind library.
    #     
    @staticmethod
# JAVA TO PYTHON CONVERTER WARNING: Method 'throws' clauses are not available in Python:
# ORIGINAL LINE: public static void main(String[] args) throws Throwable
# JAVA TO PYTHON CONVERTER TASK: Python does not allow method overloads:
    def main(args):

        json = "{\n" + "  \"example\":   [\n" + "    {\n" + "      \"value\": 4\n" + "    },\n" + "    {\n" + "      \"value\": 7\n" + "    },\n" + "    {\n" + "      \"value\": 13\n" + "    }\n" + "  ]\n" + "}"

        data = (com.fasterxml.jackson.databind.ObjectMapper()).readValue(json, Object.class)

        expression = jsonata("$sum(example.value)")
        result = expression.evaluate(data) # returns 24
        print(result)
