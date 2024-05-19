# JAVA TO PYTHON CONVERTER TASK: Java 'import static' statements are not converted by Java to Python Converter:
#import static com.dashjoin.jsonata.Jsonata.jsonata
from com.dashjoin.jsonata import Functions
from com.dashjoin.jsonata.json import Json

class MainJson:

    #    *
    #     * Built-in JSON parser usage.
    #     
    @staticmethod
    def main(args):

        json = "{\n" + "  \"example\":   [\n" + "    {\n" + "      \"value\": 4\n" + "    },\n" + "    {\n" + "      \"value\": 7\n" + "    },\n" + "    {\n" + "      \"value\": 13\n" + "    }\n" + "  ]\n" + "}"

        data = com.dashjoin.jsonata.json.Json.parseJson(json)

        print(com.dashjoin.jsonata.Functions.string(data,True))

        expression = jsonata("$sum(example.value)")
        result = expression.evaluate(data) # returns 24
        print(result)
