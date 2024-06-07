import jsonata
import json

#
# Built-in JSON parser usage.
#
def main():
    json_str = ("{\n" + "  \"example\":   [\n" + "    {\n" + "      \"value\": 4\n" + "    },\n" + "    {\n" +
                "      \"value\": 7\n" + "    },\n" + "    {\n" + "      \"value\": 13\n" + "    }\n" + "  ]\n" + "}")

    data = json.loads(json_str)

    print(jsonata.Functions.string(data, True))

    expression = jsonata.Jsonata("$sum(example.value)")
    result = expression.evaluate(data)  # returns 24
    print(result)


if __name__ == '__main__':
    main()
