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


from com.dashjoin.jsonata import Jsonata.JFunction
from com.dashjoin.jsonata import Jsonata.JFunctionCallable

# JAVA TO PYTHON CONVERTER TASK: Java annotations have no direct Python equivalent:
# ORIGINAL LINE: @SuppressWarnings({"rawtypes"}) public class Utils
class Utils:
    @staticmethod
    def isNumeric(v):
        if isinstance(v, Long):
            return True
        isNum = False
        if isinstance(v, Number):
            d = (v).doubleValue()
            isNum = not Double.isNaN(d)
            if isNum and not Double.isFinite(d):
                raise JException("D1001", 0, v)
        return isNum

    @staticmethod
    def isArrayOfStrings(v):
        result = False
        if isinstance(v, java.util.Collection):
            for o in (v):
                if not(isinstance(o, String)):
                    return False
            return True
        return False
    @staticmethod
    def isArrayOfNumbers(v):
        result = False
        if isinstance(v, java.util.Collection):
            for o in (v):
                if not com.dashjoin.jsonata.Utils.isNumeric(o):
                    return False
            return True
        return False

    @staticmethod
    def isFunction(o):
        return isinstance(o, com.dashjoin.jsonata.Jsonata.JFunction) or isinstance(o, com.dashjoin.jsonata.Jsonata.JFunctionCallable)

    NONE = Object()

    #    *
    #     * Create an empty sequence to contain query results
    #     * @returns {Array} - empty sequence
    #     
    @staticmethod
# JAVA TO PYTHON CONVERTER TASK: Python does not allow method overloads:
    def createSequence():
        return com.dashjoin.jsonata.Utils.createSequence(com.dashjoin.jsonata.Utils.NONE)

    @staticmethod
# JAVA TO PYTHON CONVERTER TASK: Python does not allow method overloads:
    def createSequence(el):
        sequence = JList()
        sequence.sequence = True
        if el is not com.dashjoin.jsonata.Utils.NONE:
            if isinstance(el, java.util.List) and len((el)) == 1:
                sequence.append((el)[0])
            else:
                # This case does NOT exist in Javascript! Why?
                sequence.append(el)
        return sequence

    class JList(list):

        def _initialize_instance_fields(self):
            # instance fields found by Java to Python Converter:
            self.sequence = False
            self.outerWrapper = False
            self.tupleStream = False
            self.keepSingleton = False
            self.cons = False

# JAVA TO PYTHON CONVERTER TASK: There is no Python equivalent to multiple constructors:
# ORIGINAL LINE: public JList()
        def __init__(self):
            self._initialize_instance_fields()

            super().__init__()
# JAVA TO PYTHON CONVERTER TASK: There is no Python equivalent to multiple constructors:
# ORIGINAL LINE: public JList(int capacity)
        def __init__(self, capacity):
            self._initialize_instance_fields()

            super().__init__(capacity)
# JAVA TO PYTHON CONVERTER TASK: There is no Python equivalent to multiple constructors:
# ORIGINAL LINE: public JList(java.util.Collection<? extends E> c)
        def __init__(self, c):
            self._initialize_instance_fields()

            super().__init__(c)

        # Jsonata specific flags





    @staticmethod
    def isSequence(result):
        return isinstance(result, JList) and (result).sequence

    #    *
    #     * List representing an int range [a,b]
    #     * Both sides are included. Read-only + immutable.
    #     * 
    #     * Used for late materialization of ranges.
    #     
    class RangeList(java.util.AbstractList):


        def __init__(self, left, right):
            # instance fields found by Java to Python Converter:
            self.a = 0
            self.b = 0
            self.size = 0

            assert(left <= right)
            assert(right - left < Integer.MAX_VALUE)
            self.a = left
            self.b = right
            self.size = int((self.b - self.a + 1))

        def size(self):
            return self.size

        def addAll(self, c):
            raise UnsupportedOperationException("RangeList does not support 'addAll'")

        def get(self, index):
            if index < self.size:
                try:
                    return Utils.convertNumber(self.a + index)
                except JException as e:
                    # TODO Auto-generated catch block
                    e.printStackTrace()
            raise IndexOutOfBoundsException(index)

    @staticmethod
    def convertNumber(n):
        # Use long if the number is not fractional
        if not com.dashjoin.jsonata.Utils.isNumeric(n):
            return None
        if n.longValue() == n.doubleValue():
            l = n.longValue()
            if (int(l)) == l:
                return int(l)
            else:
                return l
        return n.doubleValue()

    @staticmethod
    def checkUrl(str):
        isHigh = False
        i = 0
        while i < len(str):
            wasHigh = isHigh
            isHigh = Character.isHighSurrogate(str[i])
            if wasHigh and isHigh:
                raise JException("Malformed URL", i)
            i += 1
        if isHigh:
            raise JException("Malformed URL", 0)

    @staticmethod
    def convertValue(val):
        return val if val is not Jsonata.NULL_VALUE else None

    @staticmethod
# JAVA TO PYTHON CONVERTER TASK: Python does not allow method overloads:
    def convertNulls(res):
        for e in res.entrySet():
            val = e.getValue()
            l = com.dashjoin.jsonata.Utils.convertValue(val)
            if l is not val:
                e.setValue(l)
            com.dashjoin.jsonata.Utils.recurse(val)

    @staticmethod
# JAVA TO PYTHON CONVERTER TASK: Python does not allow method overloads:
    def convertNulls(res):
        for i, _ in enumerate(res):
            val = res[i]
            l = com.dashjoin.jsonata.Utils.convertValue(val)
            if l is not val:
                res[i] = l
            com.dashjoin.jsonata.Utils.recurse(val)

    @staticmethod
    def recurse(val):
        if isinstance(val, java.util.Map):
            com.dashjoin.jsonata.Utils.convertNulls(val)
        if isinstance(val, java.util.List):
            com.dashjoin.jsonata.Utils.convertNulls(val)

    @staticmethod
# JAVA TO PYTHON CONVERTER TASK: Python does not allow method overloads:
    def convertNulls(res):
        com.dashjoin.jsonata.Utils.recurse(res)
        return com.dashjoin.jsonata.Utils.convertValue(res)

    #    *
    #     * adapted from org.json.JSONObject https://github.com/stleary/JSON-java
    #     
    @staticmethod
    def quote(string, w):
        b = '\0'
        c = chr(0)
        hhhh = None
        i = 0
        len = len(string)

        for i in range(0, len):
            b = c
            c = string[i]
            if (c == '\\') or (c == '"'):
                w.append('\\')
                w.append(c)
                #          
                #          case '/':
                #              if (b == '<') {
                #                  w.append('\\')
                #              }
                #              w.append(c)
                #              break
                #          
            elif c == '\b':
                w.append("\\b")
            elif c == '\t':
                w.append("\\t")
            elif c == '\n':
                w.append("\\n")
            elif c == '\f':
                w.append("\\f")
            elif c == '\r':
                w.append("\\r")
            else:
                if c < ' ' or (c >= '\u0080' and c < '\u00a0') or (c >= '\u2000' and c < '\u2100'):
                    w.append("\\u")
                    hhhh = Integer.toHexString(c)
                    w.append("0000", 0, 4 - len(hhhh))
                    w.append(hhhh)
                else:
                    w.append(c)
