# JAVA TO PYTHON CONVERTER TASK: Java 'import static' statements are not converted by Java to Python Converter:
#import static com.dashjoin.jsonata.Jsonata.jsonata
from com.google.gson import Gson

class Main:

    #    *
    #     * Interoperability with GSON library.
    #     
    @staticmethod
# JAVA TO PYTHON CONVERTER TASK: Python does not allow method overloads:
    def main(args):

        json = "{\n" + "  \"example\":   [\n" + "    {\n" + "      \"value\": 4\n" + "    },\n" + "    {\n" + "      \"value\": 7\n" + "    },\n" + "    {\n" + "      \"value\": 13\n" + "    }\n" + "  ]\n" + "}"

        gson = com.google.gson.Gson()
        data = gson.fromJson(json, Object.class)

        expression = jsonata("$sum(example.value)")
        result = expression.evaluate(data) # returns 24
        print(result)
