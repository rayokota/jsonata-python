# JAVA TO PYTHON CONVERTER TASK: Java 'import static' statements are not converted by Java to Python Converter:
#import static com.dashjoin.jsonata.Jsonata.jsonata

class Main:

    #    *
    #     * Feed JSON in internal representation format.
    #     
    @staticmethod
# JAVA TO PYTHON CONVERTER TASK: Python does not allow method overloads:
    def main(args):

        data = java.util.Map.of("example", java.util.List.of(java.util.Map.of("value", 4), java.util.Map.of("value", 7), java.util.Map.of("value", 13)))

        expression = jsonata("$sum(example.value)")
        result = expression.evaluate(data) # returns 24
        print(result)
