#*
# * jsonata-java is the JSONata Java reference port
# * 
# * Copyright Dashjoin GmbH. https://dashjoin.com
# * 
# * Licensed under the Apache License, Version 2.0 (the "License")
# * you may not use this file except in compliance with the License.
# * You may obtain a copy of the License at
# *
# *    http://www.apache.org/licenses/LICENSE-2.0
# *
# * Unless required by applicable law or agreed to in writing, software
# * distributed under the License is distributed on an "AS IS" BASIS,
# * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# * See the License for the specific language governing permissions and
# * limitations under the License.
# 


from com.dashjoin.jsonata import JException
from com.dashjoin.jsonata import Utils

#*
# * Vanilla JSON parser
# * 
# * Uses classes JsonParser + JsonHandler from:
# * https://github.com/ralfstx/minimal-json
# 
class Json:

    class _JsonHandler(JsonHandler):

        def __init__(self):
            # instance fields found by Java to Python Converter:
            self.value = None


        def startArray(self):
            return []

        def startObject(self):
            return java.util.LinkedHashMap()

        def endNull(self):
            self.value = None

        def endBoolean(self, bool):
            self.value = bool

        def endString(self, string):
            self.value = string

        def endNumber(self, string):
            d = float(string)
            try:
                self.value = com.dashjoin.jsonata.Utils.convertNumber(d)
            except com.dashjoin.jsonata.JException as e:
                # TODO Auto-generated catch block
                e.printStackTrace()

# JAVA TO PYTHON CONVERTER TASK: Python does not allow method overloads:
        def endArray(self, array):
            self.value = array

# JAVA TO PYTHON CONVERTER TASK: Python does not allow method overloads:
        def endObject(self, object):
            self.value = object

# JAVA TO PYTHON CONVERTER TASK: Python does not allow method overloads:
        def endArrayValue(self, array):
            array.append(self.value)

# JAVA TO PYTHON CONVERTER TASK: Python does not allow method overloads:
        def endObjectValue(self, object, name):
            object[name] = self.value

        def getValue(self):
            return self.value


    #    *
    #     * Parses the given JSON string
    #     * 
    #     * @param json
    #     * @return Parsed object
    #     
    @staticmethod
# JAVA TO PYTHON CONVERTER TASK: Python does not allow method overloads:
    def parseJson(json):
        handler = _JsonHandler()
        jp = JsonParser(handler)
        jp.parse(json)
        return handler.getValue()

    #    *
    #     * Parses the given JSON
    #     * 
    #     * @param json
    #     * @return Parsed object
    #     * @throws IOException
    #     
    @staticmethod
# JAVA TO PYTHON CONVERTER WARNING: Method 'throws' clauses are not available in Python:
# ORIGINAL LINE: public static Object parseJson(java.io.Reader json) throws java.io.IOException
# JAVA TO PYTHON CONVERTER TASK: Python does not allow method overloads:
    def parseJson(json):
        handler = _JsonHandler()
        jp = JsonParser(handler)
        jp.parse(json, 65536)
        return handler.getValue()

    @staticmethod
# JAVA TO PYTHON CONVERTER WARNING: Method 'throws' clauses are not available in Python:
# ORIGINAL LINE: public static void main(String[] args) throws Throwable
    def main(args):

        handler = _JsonHandler()

        jp = JsonParser(handler)

        jp.parse("{\"a\":false}")

        print(handler.getValue())
