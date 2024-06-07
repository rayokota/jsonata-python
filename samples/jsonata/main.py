import jsonata


#
# Feed JSON in internal representation format.
#
def main():
    data = {"example": [{"value": 4}, {"value": 7}, {"value": 13}]}

    expression = jsonata.Jsonata("$sum(example.value)")
    result = expression.evaluate(data)  # returns 24
    print(result)


if __name__ == '__main__':
    main()
