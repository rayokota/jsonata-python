import random
import math

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

# JAVA TO PYTHON CONVERTER TASK: Java 'import static' statements are not converted by Java to Python Converter:
#import static com.dashjoin.jsonata.Jsonata.jsonata
from com.dashjoin.jsonata import Jsonata.JFunction
from com.dashjoin.jsonata import Parser.Symbol
import com.dashjoin.jsonata.Utils
from com.dashjoin.jsonata.json import Json
from com.dashjoin.jsonata.utils import Constants
from com.dashjoin.jsonata.utils import DateTimeUtils

# JAVA TO PYTHON CONVERTER TASK: Java annotations have no direct Python equivalent:
# ORIGINAL LINE: @SuppressWarnings({"rawtypes", "unchecked"}) public class Functions
class Functions:

    #    *
    #     * Sum function
    #     * @param {Object} args - Arguments
    #     * @returns {number} Total value of arguments
    #     
    @staticmethod
    def sum(args):
        # undefined inputs always return undefined
        if args is None:
            return None

        total = args.stream().mapToDouble(Number::doubleValue).sum()
        return total

    #    *
    #     * Count function
    #     * @param {Object} args - Arguments
    #     * @returns {number} Number of elements in the array
    #     
    @staticmethod
    def count(args):
        # undefined inputs always return undefined
        if args is None:
            return 0

        return len(args)

    #    *
    #     * Max function
    #     * @param {Object} args - Arguments
    #     * @returns {number} Max element in the array
    #     
    @staticmethod
    def max(args):
        # undefined inputs always return undefined
        if args is None or len(args) == 0:
            return None

        res = args.stream().mapToDouble(Number::doubleValue).max()
        if res.isPresent():
            return res.getAsDouble()
        else:
            return None

    #    *
    #     * Min function
    #     * @param {Object} args - Arguments
    #     * @returns {number} Min element in the array
    #     
    @staticmethod
    def min(args):
        # undefined inputs always return undefined
        if args is None or len(args) == 0:
            return None

        res = args.stream().mapToDouble(Number::doubleValue).min()
        if res.isPresent():
            return res.getAsDouble()
        else:
            return None

    #    *
    #     * Average function
    #     * @param {Object} args - Arguments
    #     * @returns {number} Average element in the array
    #     
    @staticmethod
    def average(args):
        # undefined inputs always return undefined
        if args is None or len(args) == 0:
            return None

        res = args.stream().mapToDouble(Number::doubleValue).average()
        if res.isPresent():
            return res.getAsDouble()
        else:
            return None

    #    *
    #     * Stringify arguments
    #     * @param {Object} arg - Arguments
    #     * @param {boolean} [prettify] - Pretty print the result
    #     * @returns {String} String from arguments
    #     
    @staticmethod
# JAVA TO PYTHON CONVERTER TASK: Python does not allow method overloads:
    def string(arg, prettify):

        if isinstance(arg, com.dashjoin.jsonata.Utils.JList):
            if (arg).outerWrapper:
                arg = (arg).get(0)

        if arg is None:
            return None

        # see https://docs.jsonata.org/string-functions#string: Strings are unchanged
        if isinstance(arg, String):
            return str(arg)

        sb = StringBuilder()
        com.dashjoin.jsonata.Functions.string(sb, arg, prettify is not None and prettify, "")
        return str(sb)

    #    *
    #     * Internal recursive string function based on StringBuilder.
    #     * Avoids creation of intermediate String objects
    #         
    @staticmethod
# JAVA TO PYTHON CONVERTER TASK: Python does not allow method overloads:
    def string(b, arg, prettify, indent):
        # if (arg == null)
        #   return null

        if arg is None or arg is Jsonata.NULL_VALUE:
            b.append("null")
            return

        if isinstance(arg, com.dashjoin.jsonata.Jsonata.JFunction):
            return

        if isinstance(arg, com.dashjoin.jsonata.Parser.Symbol):
            return

        if isinstance(arg, Double):
            # TODO: this really should be in the jackson serializer
            bd = java.math.BigDecimal(float(arg), java.math.MathContext(15))
            res = str(bd.stripTrailingZeros())

            if res.find("E+") > 0:
                res = res.replace("E+", "e+")
            if res.find("E-") > 0:
                res = res.replace("E-", "e-")

            b.append(res)
            return

        if isinstance(arg, Number) or isinstance(arg, Boolean):
            b.append(arg)
            return

        if isinstance(arg, String):
            # quotes within strings must be escaped
            Utils.quote(str(arg), b)
            return

        if isinstance(arg, java.util.Map):
            b.append('{')
            if prettify:
                b.append('\n')
            for e in (arg).entrySet():
                if prettify:
                    b.append(indent)
                    b.append("  ")
                b.append('"')
                b.append(e.getKey())
                b.append('"')
                b.append(':')
                if prettify:
                    b.append(' ')
# JAVA TO PYTHON CONVERTER WARNING: The original Java variable was marked 'final':
# ORIGINAL LINE: final Object v = e.getValue();
                v = e.getValue()
                if isinstance(v, String) or isinstance(v, com.dashjoin.jsonata.Parser.Symbol) or isinstance(v, com.dashjoin.jsonata.Jsonata.JFunction):
                    b.append('"')
                    com.dashjoin.jsonata.Functions.string(b, v, prettify, indent + "  ")
                    b.append('"')
                else:
                    com.dashjoin.jsonata.Functions.string(b, v, prettify, indent + "  ")
                b.append(',')
                if prettify:
                    b.append('\n')
            if len((arg)) > 0:
                b.deleteCharAt(b.length() - (2 if prettify else 1))
            if prettify:
                b.append(indent)
            b.append('}')
            return

        if (isinstance(arg, java.util.List)):
            if len((arg)) == 0:
                b.append("[]")
                return
            b.append('[')
            if prettify:
                b.append('\n')
            for v in arg:
                if prettify:
                    b.append(indent)
                    b.append("  ")
                if isinstance(v, String) or isinstance(v, com.dashjoin.jsonata.Parser.Symbol) or isinstance(v, com.dashjoin.jsonata.Jsonata.JFunction):
                    b.append('"')
                    com.dashjoin.jsonata.Functions.string(b, v, prettify, indent + "  ")
                    b.append('"')
                else:
                    com.dashjoin.jsonata.Functions.string(b, v, prettify, indent + "  ")
                b.append(',')
                if prettify:
                    b.append('\n')
            if len((arg)) > 0:
                b.deleteCharAt(b.length() - (2 if prettify else 1))
            if prettify:
                b.append(indent)
            b.append(']')
            return

        # Throw error for unknown types
        raise IllegalArgumentException("Only JSON types (values, Map, List) can be stringified. Unsupported type: " + type(arg).getName())


    #    *
    #     * Validate input data types.
    #     * This will make sure that all input data can be processed.
    #     * 
    #     * @param arg
    #     * @return
    #     
    @staticmethod
    def validateInput(arg):
        # if (arg == null)
        #   return null

        if arg is None or arg is Jsonata.NULL_VALUE:
            return

        if isinstance(arg, com.dashjoin.jsonata.Jsonata.JFunction):
            return

        if isinstance(arg, com.dashjoin.jsonata.Parser.Symbol):
            return

        if isinstance(arg, Double):
            return

        if isinstance(arg, Number) or isinstance(arg, Boolean):
            return

        if isinstance(arg, String):
            return

        if isinstance(arg, java.util.Map):
            for e in (arg).entrySet():
                com.dashjoin.jsonata.Functions.validateInput(e.getKey())
                com.dashjoin.jsonata.Functions.validateInput(e.getValue())
            return

        if (isinstance(arg, java.util.List)):
            for v in arg:
                com.dashjoin.jsonata.Functions.validateInput(v)
            return

        # Throw error for unknown types
        raise IllegalArgumentException("Only JSON types (values, Map, List) are allowed as input. Unsupported type: " + type(arg).getCanonicalName())

    #    *
    #     * Create substring based on character number and length
    #     * @param {String} str - String to evaluate
    #     * @param {Integer} start - Character number to start substring
    #     * @param {Integer} [length] - Number of characters in substring
    #     * @returns {string|*} Substring
    #     
    @staticmethod
    def substring(str, _start, _length):
        # undefined inputs always return undefined
        if str is None:
            return None

        start = _start.intValue() if _start is not None else None
        length = _length.intValue() if _length is not None else None

        # not used: var strArray = stringToArray(str)
        strLength = len(str)

        if strLength + start < 0:
            start = 0

        if length is not None:
            if length <= 0:
                return ""
            return com.dashjoin.jsonata.Functions.substr(str, start, length)

        return com.dashjoin.jsonata.Functions.substr(str, start, strLength)


    #    *
    #     * Source = Jsonata4Java JSONataUtils.substr
    #     * @param str
    #     * @param start  Location at which to begin extracting characters. If a negative
    #     *               number is given, it is treated as strLength - start where
    #     *               strLength is the length of the string. For example,
    #     *               str.substr(-3) is treated as str.substr(str.length - 3)
    #     * @param length The number of characters to extract. If this argument is null,
    #     *               all the characters from start to the end of the string are
    #     *               extracted.
    #     * @return A new string containing the extracted section of the given string. If
    #     *         length is 0 or a negative number, an empty string is returned.
    #     
    @staticmethod
    def substr(str, start, length):

        # below has to convert start and length for emojis and unicode
        origLen = len(str)

        strData = java.util.Objects.requireNonNull(str).intern()
        strLen = strData.codePointCount(0, len(strData))
        if start >= strLen:
            return ""
        # If start is negative, substr() uses it as a character index from the
        # end of the string; the index of the last character is -1.
        start = strData.offsetByCodePoints(0,start if start >= 0 else (0 if (strLen + start) < 0 else strLen + start))
        if start < 0:
            start = 0 # If start is negative and abs(start) is larger than the length of the
        # string, substr() uses 0 as the start index.
        # If length is omitted, substr() extracts characters to the end of the
        # string.
        if length is None:
            length = len(strData)
        elif length < 0:
            # If length is 0 or negative, substr() returns an empty string.
            return ""
        elif length > len(strData):
            length = len(strData)

        length = strData.offsetByCodePoints(0, length)

        if start >= 0:
            # If start is positive and is greater than or equal to the length of
            # the string, substr() returns an empty string.
            if start >= origLen:
                return ""

        # collect length characters (unless it reaches the end of the string
        # first, in which case it will return fewer)
        end = start + length
        if end > origLen:
            end = origLen

        return strData[start:end]

    #    *
    #     * Create substring up until a character
    #     * @param {String} str - String to evaluate
    #     * @param {String} chars - Character to define substring boundary
    #     * @returns {*} Substring
    #     
    @staticmethod
    def substringBefore(str, chars):
        # undefined inputs always return undefined
        if str is None:
            return None

        if chars is None:
            return str

        pos = str.find(chars)
        if pos > -1:
            return str[0:pos]
        else:
            return str

    #    *
    #     * Create substring after a character
    #     * @param {String} str - String to evaluate
    #     * @param {String} chars - Character to define substring boundary
    #     * @returns {*} Substring
    #     
    @staticmethod
    def substringAfter(str, chars):
        # undefined inputs always return undefined
        if str is None:
            return None

        pos = str.find(chars)
        if pos > -1:
            return str[pos + len(chars):]
        else:
            return str

    #    *
    #     * Lowercase a string
    #     * @param {String} str - String to evaluate
    #     * @returns {string} Lowercase string
    #     
    @staticmethod
    def lowercase(str):
        # undefined inputs always return undefined
        if str is None:
            return None

        return str.casefold()

    #    *
    #     * Uppercase a string
    #     * @param {String} str - String to evaluate
    #     * @returns {string} Uppercase string
    #     
    @staticmethod
    def uppercase(str):
        # undefined inputs always return undefined
        if str is None:
            return None

        return str.upper()

    #    *
    #     * length of a string
    #     * @param {String} str - string
    #     * @returns {Number} The number of characters in the string
    #     
    @staticmethod
    def length(str):
        # undefined inputs always return undefined
        if str is None:
            return None

        return str.codePointCount(0, len(str))

    #    *
    #     * Normalize and trim whitespace within a string
    #     * @param {string} str - string to be trimmed
    #     * @returns {string} - trimmed string
    #     
    @staticmethod
    def trim(str):
        # undefined inputs always return undefined
        if str is None:
            return None

        if len(str) == 0:
            return ""

        # normalize whitespace
        result = str.replaceAll("[ \t\n\r]+", " ")
        if result.charAt(0) == ' ':
            # strip leading space
            result = result.substring(1)

        if result.isEmpty():
            return ""

        if result.charAt(result.length() - 1) == ' ':
            # strip trailing space
            result = result.substring(0, result.length() - 1)
        return result

    #    *
    #     * Pad a string to a minimum width by adding characters to the start or end
    #     * @param {string} str - string to be padded
    #     * @param {number} width - the minimum width; +ve pads to the right, -ve pads to the left
    #     * @param {string} [char] - the pad character(s); defaults to ' '
    #     * @returns {string} - padded string
    #     
    @staticmethod
    def pad(str, width, _char):
        # undefined inputs always return undefined
        if str is None:
            return None

        if _char is None or len(_char) == 0:
            _char = " "

        result = None

        if width < 0:
            result = com.dashjoin.jsonata.Functions.leftPad(str, -width, _char)
        else:
            result = com.dashjoin.jsonata.Functions.rightPad(str, width, _char)
        return result

    # Source: Jsonata4Java PadFunction
    @staticmethod
# JAVA TO PYTHON CONVERTER TASK: There is no Python equivalent to Java's 'final' parameters:
# ORIGINAL LINE: public static String leftPad(final String str, final int size, String padStr)
    def leftPad(str, size, padStr):
        if str is None:
            return None
        if padStr is None:
            padStr = " "

        strData = java.util.Objects.requireNonNull(str).intern()
        strLen = strData.codePointCount(0, len(strData))

        padData = java.util.Objects.requireNonNull(padStr).intern()
        padLen = padData.codePointCount(0, len(padData))

        if padLen == 0:
            padStr = " "
# JAVA TO PYTHON CONVERTER WARNING: The original Java variable was marked 'final':
# ORIGINAL LINE: final int pads = size - strLen;
        pads = size - strLen
        if pads <= 0:
            return str
        padding = ""
        i = 0
        while i < pads + 1:
            padding += padStr
            i += 1
        return com.dashjoin.jsonata.Functions.substr(padding, 0, pads).concat(str)

    # Source: Jsonata4Java PadFunction
    @staticmethod
# JAVA TO PYTHON CONVERTER TASK: There is no Python equivalent to Java's 'final' parameters:
# ORIGINAL LINE: public static String rightPad(final String str, final int size, String padStr)
    def rightPad(str, size, padStr):
        if str is None:
            return None
        if padStr is None:
            padStr = " "

        strData = java.util.Objects.requireNonNull(str).intern()
        strLen = strData.codePointCount(0, len(strData))

        padData = java.util.Objects.requireNonNull(padStr).intern()
        padLen = padData.codePointCount(0, len(padData))

        if padLen == 0:
            padStr = " "
# JAVA TO PYTHON CONVERTER WARNING: The original Java variable was marked 'final':
# ORIGINAL LINE: final int pads = size - strLen;
        pads = size - strLen
        if pads <= 0:
            return str
        padding = ""
        i = 0
        while i < pads + 1:
            padding += padStr
            i += 1
        return str.concat(com.dashjoin.jsonata.Functions.substr(padding, 0, pads))

    class RegexpMatch:

        def __init__(self):
            # instance fields found by Java to Python Converter:
            self.match_ = None
            self.index = 0
            self.groups = None

        def toString(self):
            return "regexpMatch " + self.match_ + " idx=" + str(self.index) + " groups=" + self.groups
    #    *
    #     * Evaluate the matcher function against the str arg
    #     *
    #     * @param {*} matcher - matching function (native or lambda)
    #     * @param {string} str - the string to match against
    #     * @returns {object} - structure that represents the match(es)
    #     
    @staticmethod
    def evaluateMatcher(matcher, str):
        res = []
        m = matcher.matcher(str)
        while m.find():
            rm = RegexpMatch()

            #System.out.println("grc="+m.groupCount()+" "+m.group(1))

            rm.index = m.start()
            rm.match_ = m.group()

            groups = []
            # Collect the groups
            g = 1
            while g <= m.groupCount():
                groups.append(m.group(g))
                g += 1

            rm.groups = groups
            res.append(rm)
        return res

    #    *
    #     * Tests if the str contains the token
    #     * @param {String} str - string to test
    #     * @param {String} token - substring or regex to find
    #     * @returns {Boolean} - true if str contains token
    #     
    @staticmethod
    def contains(str, token):
        # undefined inputs always return undefined
        if str is None:
            return None

        result = False

        if isinstance(token, String):
            result = (str.find(str(token)) is not - 1)
        elif isinstance(token, java.util.regex.Pattern):
            matches = com.dashjoin.jsonata.Functions.evaluateMatcher(token, str)
            #if (dbg) System.out.println("match = "+matches)
            #result = (typeof matches !== 'undefined')
            #throw new Error("regexp not impl"); //result = false
            result = len(matches) > 0
        else:
            raise Error("unknown type to match: " + token)

        return result

    #    *
    #     * Match a string with a regex returning an array of object containing details of each match
    #     * @param {String} str - string
    #     * @param {String} regex - the regex applied to the string
    #     * @param {Integer} [limit] - max number of matches to return
    #     * @returns {Array} The array of match objects
    #     
    @staticmethod
    def match_(str, regex, limit):
        # undefined inputs always return undefined
        if str is None:
            return None

        # limit, if specified, must be a non-negative number
        if limit is not None and limit < 0:
            raise JException("D3040", -1, limit)

        result = Utils.createSequence()
        matches = com.dashjoin.jsonata.Functions.evaluateMatcher(regex, str)
        max = Integer.MAX_VALUE
        if limit is not None:
            max = limit

        for i, _ in enumerate(matches):
            m = java.util.LinkedHashMap()
            rm = matches[i]
            # Convert to JSON map:
            m["match"] = rm.match_
            m["index"] = rm.index
            m["groups"] = rm.groups
            result.append(m)
            if i >= max:
                break
        return result

    #    *
    #     * Join an array of strings
    #     * @param {Array} strs - array of string
    #     * @param {String} [separator] - the token that splits the string
    #     * @returns {String} The concatenated string
    #     
    @staticmethod
    def join(strs, separator):
        # undefined inputs always return undefined
        if strs is None:
            return None

        # if separator is not specified, default to empty string
        if separator is None:
            separator = ""

        return String.join(separator, strs)

    @staticmethod
    def safeReplacement(in_):
        # In JSONata and in Java the $ in the replacement test usually starts the insertion of a capturing group
        # In order to replace a simple $ in Java you have to escape the $ with "\$"
        # in JSONata you do this with a '$$'
        # "\$" followed any character besides '<' and and digit into $ + this character  
        return in_.replaceAll("\\$\\$", "\\\\\\$").replaceAll("([^\\\\]|^)\\$([^0-9^<])", "$1\\\\\\$$2").replaceAll("\\$$", "\\\\\\$") # allow $ at end

    #    *
    #     * Safe replaceAll
    #     * 
    #     * In Java, non-existing groups cause an exception.
    #     * Ignore these non-existing groups (replace with "")
    #     * 
    #     * @param s
    #     * @param pattern
    #     * @param replacement
    #     * @return
    #     
    @staticmethod
    def safeReplaceAll(s, pattern, _replacement):

        if not(isinstance(_replacement, String)):
            return com.dashjoin.jsonata.Functions.safeReplaceAllFn(s, pattern, _replacement)

        replacement = str(_replacement)

        replacement = com.dashjoin.jsonata.Functions.safeReplacement(replacement)
        m = pattern.matcher(s)
        r = None
        for i in range(0, 10):
            try:
                r = m.replaceAll(replacement)
                break
            except IndexOutOfBoundsException as e:
                msg = e.getMessage()

                # Message we understand needs to be:
                # No group X
                if (not "No group") in msg:
                    raise e

                # Adjust replacement to remove the non-existing group
                g = "" + msg[len(msg) - 1]

                replacement = replacement.replace("$" + g, "")
        return r

    #    *
    #     * Converts Java MatchResult to the Jsonata object format
    #     * @param mr
    #     * @return
    #     
    @staticmethod
    def toJsonataMatch(mr):
        obj = java.util.LinkedHashMap()
        obj["match"] = mr.group()

        groups = []
        i = 0
        while i <= mr.groupCount():
            groups.append(mr.group(i))
            i += 1

        obj["groups"] = groups

        return obj

    #    *
    #     * Regexp Replace with replacer function
    #     * @param s
    #     * @param pattern
    #     * @param fn
    #     * @return
    #     
    @staticmethod
    def safeReplaceAllFn(s, pattern, fn):
        m = pattern.matcher(s)
        r = None
# JAVA TO PYTHON CONVERTER TASK: Only expression lambdas are converted by Java to Python Converter:
        #        r = m.replaceAll(t ->
        #        {
        #            try
        #            {
        #                Object res = funcApply(fn, List.of(toJsonataMatch(t)))
        #                if (res instanceof String)
        #                    return (String)res
        #                else
        #                    return null
        #            }
        #            catch (Throwable e)
        #            {
        #                e.printStackTrace()
        #            }
        #            return null
        #        }
        #        )
        return r

    #    *
    #     * Safe replaceFirst
    #     * 
    #     * @param s
    #     * @param pattern
    #     * @param replacement
    #     * @return
    #     
    @staticmethod
    def safeReplaceFirst(s, pattern, replacement):
        replacement = com.dashjoin.jsonata.Functions.safeReplacement(replacement)
        m = pattern.matcher(s)
        r = None
        for i in range(0, 10):
            try:
                r = m.replaceFirst(replacement)
                break
            except IndexOutOfBoundsException as e:
                msg = e.getMessage()

                # Message we understand needs to be:
                # No group X
                if (not "No group") in msg:
                    raise e

                # Adjust replacement to remove the non-existing group
                g = "" + msg[len(msg) - 1]

                replacement = replacement.replace("$" + g, "")
        return r

    @staticmethod
    def replace(str, pattern, replacement, limit):
        if str is None:
            return None
        if isinstance(pattern, String):
            if len((str(pattern))) == 0:
                raise JException("Second argument of replace function cannot be an empty string", 0)
        if limit is None:
            if isinstance(pattern, String):
                return str.replace(str(pattern), str(replacement))
            else:
                return com.dashjoin.jsonata.Functions.safeReplaceAll(str, pattern, replacement)
        else:

            if limit < 0:
                raise JException("Fourth argument of replace function must evaluate to a positive number", 0)

            for i in range(0, limit):
                if isinstance(pattern, String):
                    str = str.replaceFirst(str(pattern), str(replacement))
                else:
                    str = com.dashjoin.jsonata.Functions.safeReplaceFirst(str, pattern, str(replacement))
            return str



    #    *
    #     * Base64 encode a string
    #     * @param {String} str - string
    #     * @returns {String} Base 64 encoding of the binary data
    #     
    @staticmethod
    def base64encode(str):
        # undefined inputs always return undefined
        if str is None:
            return None
        try:
            return java.util.Base64.getEncoder().encodeToString(str.getBytes("utf-8"))
        except java.io.UnsupportedEncodingException as e:
            # TODO Auto-generated catch block
            e.printStackTrace()
            return None

    #    *
    #     * Base64 decode a string
    #     * @param {String} str - string
    #     * @returns {String} Base 64 encoding of the binary data
    #     
    @staticmethod
    def base64decode(str):
        # undefined inputs always return undefined
        if str is None:
            return None
        try:
            return str(java.util.Base64.getDecoder().decode(str), "utf-8")
        except java.io.UnsupportedEncodingException as e:
            # TODO Auto-generated catch block
            e.printStackTrace()
            return None

    #    *
    #     * Encode a string into a component for a url
    #     * @param {String} str - String to encode
    #     * @returns {string} Encoded string
    #     
    @staticmethod
    def encodeUrlComponent(str):
        # undefined inputs always return undefined
        if str is None:
            return None

        Utils.checkUrl(str)

        return java.net.URLEncoder.encode(str, java.nio.charset.StandardCharsets.UTF_8).replaceAll("\\+", "%20").replaceAll("\\%21", "!").replaceAll("\\%27", "'").replaceAll("\\%28", "(").replaceAll("\\%29", ")").replaceAll("\\%7E", "~")

    #    *
    #     * Encode a string into a url
    #     * @param {String} str - String to encode
    #     * @returns {string} Encoded string
    #     
    @staticmethod
    def encodeUrl(str):
        # undefined inputs always return undefined
        if str is None:
            return None

        Utils.checkUrl(str)

        try:
            # only encode query part: https://docs.jsonata.org/string-functions#encodeurl
            url = java.net.URL(str)
            query = url.getQuery()
            if query is not None:
                offset = str.find(query)
                strResult = str[0:offset]
                return strResult + com.dashjoin.jsonata.Functions.encodeURI(query)
        except Exception as e:
            # ignore and return default
            pass
        return java.net.URLEncoder.encode(str, java.nio.charset.StandardCharsets.UTF_8)

    @staticmethod
    def encodeURI(uri):
        result = None
        if uri is not None:
            try:
                # https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/encodeURI
                # Not encoded: A-Z a-z 0-9 ; , / ? : @ & = + $ - _ . ! ~ * ' ( ) #
                result = java.net.URLEncoder.encode(uri, "UTF-8").replaceAll("\\+", "%20").replaceAll("%20", " ").replaceAll("\\%21", "!").replaceAll("\\%23", "#").replaceAll("\\%24", "$").replaceAll("\\%26", "&").replaceAll("\\%27", "'").replaceAll("\\%28", "(").replaceAll("\\%29", ")").replaceAll("\\%2A", "*").replaceAll("\\%2B", "+").replaceAll("\\%2C", ",").replaceAll("\\%2D", "-").replaceAll("\\%2E", ".").replaceAll("\\%2F", "/").replaceAll("\\%3A", ":").replaceAll("\\%3B", ";").replaceAll("\\%3D", "=").replaceAll("\\%3F", "?").replaceAll("\\%40", "@").replaceAll("\\%5F", "_").replaceAll("\\%7E", "~")
            except java.io.UnsupportedEncodingException as e:
                e.printStackTrace()
        return result

    #    *
    #     * Decode a string from a component for a url
    #     * @param {String} str - String to decode
    #     * @returns {string} Decoded string
    #     
    @staticmethod
    def decodeUrlComponent(str):
        # undefined inputs always return undefined
        if str is None:
            return None

        return java.net.URLDecoder.decode(str, java.nio.charset.StandardCharsets.UTF_8)

    #    *
    #     * Decode a string from a url
    #     * @param {String} str - String to decode
    #     * @returns {string} Decoded string
    #     
    @staticmethod
    def decodeUrl(str):
        # undefined inputs always return undefined
        if str is None:
            return None

        return java.net.URLDecoder.decode(str, java.nio.charset.StandardCharsets.UTF_8)

    @staticmethod
    def split(str, pattern, limit):
        if str is None:
            return None

        if limit is not None and limit.intValue() < 0:
            raise JException("D3020", -1, str)

        result = []
        if limit is not None and limit.intValue() == 0:
            return result

        if isinstance(pattern, String):
            sep = str(pattern)
            if len(sep) == 0:
                # $split("str", ""): Split string into characters
                l = limit.intValue() if limit is not None else Integer.MAX_VALUE
                i = 0
                while i < len(str) and i < l:
                    result.append("" + str[i])
                    i += 1
            else:
                # Quote separator string + preserve trailing empty strings (-1)
                result = [str.split(java.util.regex.Pattern.quote(sep), -1)]
        else:
            result = [(pattern).split(str, -1)]
        if limit is not None and limit.intValue() < len(result):
            result = result.subList(0, limit.intValue())
        return result

    #    *
    #     * Formats a number into a decimal string representation using XPath 3.1 F&O fn:format-number spec
    #     * @param {number} value - number to format
    #     * @param {String} picture - picture string definition
    #     * @param {Object} [options] - override locale defaults
    #     * @returns {String} The formatted string
    #     
    @staticmethod
    def formatNumber(value, picture, options):
        # undefined inputs always return undefined
        if value is None:
            return None

        if picture is not None:
            if ",," in picture:
                raise RuntimeException("The sub-picture must not contain two adjacent instances of the 'grouping-separator' character")
            if picture.find('%') >= 0:
                if picture.find('e') >= 0:
                    raise RuntimeException("A sub-picture that contains a 'percent' or 'per-mille' character must not contain a character treated as an 'exponent-separator")

        symbols = java.text.DecimalFormatSymbols(java.util.Locale.US) if options is None else com.dashjoin.jsonata.Functions._processOptionsArg(options)

        # Create the formatter and format the number
        formatter = java.text.DecimalFormat()
        formatter.setDecimalFormatSymbols(symbols)
        fixedPicture = picture #picture.replaceAll("9", "0");
        for c in range('1', '9' + 1):
            fixedPicture = fixedPicture.replace(c, '0')

        littleE = False
        if "e" in fixedPicture:
            fixedPicture = fixedPicture.replace("e", "E")
            littleE = True
        #System.out.println("picture "+fixedPicture)
        formatter.applyLocalizedPattern(fixedPicture)
        result = formatter.format(value)

        if littleE:
            result = result.replace("E", "e")


        return result

    # From JSONata4Java FormatNumberFunction
    @staticmethod
    def _processOptionsArg(argOptions):
        # Create the variable return
        symbols = java.text.DecimalFormatSymbols(java.util.Locale.US) # (DecimalFormatSymbols) Constants.DEFAULT_DECIMAL_FORMAT_SYMBOLS.clone();

        # Iterate over the formatting character overrides
        fieldNames = argOptions.keys().iterator()
        while fieldNames.hasNext():
            fieldName = fieldNames.next()
            valueNode = str(argOptions[fieldName])
            # String value = getFormattingCharacter(valueNode)
            if fieldName is com.dashjoin.jsonata.utils.Constants.SYMBOL_DECIMAL_SEPARATOR:
                    value = com.dashjoin.jsonata.Functions._getFormattingCharacter(valueNode, com.dashjoin.jsonata.utils.Constants.SYMBOL_DECIMAL_SEPARATOR, True)
                    symbols.setDecimalSeparator(value[0])

            elif fieldName is com.dashjoin.jsonata.utils.Constants.SYMBOL_GROUPING_SEPARATOR:
                    value = com.dashjoin.jsonata.Functions._getFormattingCharacter(valueNode, com.dashjoin.jsonata.utils.Constants.SYMBOL_GROUPING_SEPARATOR, True)
                    symbols.setGroupingSeparator(value[0])

            elif fieldName is com.dashjoin.jsonata.utils.Constants.SYMBOL_INFINITY:
                    value = com.dashjoin.jsonata.Functions._getFormattingCharacter(valueNode, com.dashjoin.jsonata.utils.Constants.SYMBOL_INFINITY, False)
                    symbols.setInfinity(value)

            elif fieldName is com.dashjoin.jsonata.utils.Constants.SYMBOL_MINUS_SIGN:
                    value = com.dashjoin.jsonata.Functions._getFormattingCharacter(valueNode, com.dashjoin.jsonata.utils.Constants.SYMBOL_MINUS_SIGN, True)
                    symbols.setMinusSign(value[0])

            elif fieldName is com.dashjoin.jsonata.utils.Constants.SYMBOL_NAN:
                    value = com.dashjoin.jsonata.Functions._getFormattingCharacter(valueNode, com.dashjoin.jsonata.utils.Constants.SYMBOL_NAN, False)
                    symbols.setNaN(value)

            elif fieldName is com.dashjoin.jsonata.utils.Constants.SYMBOL_PERCENT:
                    value = com.dashjoin.jsonata.Functions._getFormattingCharacter(valueNode, com.dashjoin.jsonata.utils.Constants.SYMBOL_PERCENT, True)
                    symbols.setPercent(value[0])

            elif fieldName is com.dashjoin.jsonata.utils.Constants.SYMBOL_PER_MILLE:
                    value = com.dashjoin.jsonata.Functions._getFormattingCharacter(valueNode, com.dashjoin.jsonata.utils.Constants.SYMBOL_PER_MILLE, False)
                    symbols.setPerMill(value[0])

            elif fieldName is com.dashjoin.jsonata.utils.Constants.SYMBOL_ZERO_DIGIT:
                    value = com.dashjoin.jsonata.Functions._getFormattingCharacter(valueNode, com.dashjoin.jsonata.utils.Constants.SYMBOL_ZERO_DIGIT, True)
                    symbols.setZeroDigit(value[0])

            elif fieldName is com.dashjoin.jsonata.utils.Constants.SYMBOL_DIGIT:
                    value = com.dashjoin.jsonata.Functions._getFormattingCharacter(valueNode, com.dashjoin.jsonata.utils.Constants.SYMBOL_DIGIT, True)
                    symbols.setDigit(value[0])

            elif fieldName is com.dashjoin.jsonata.utils.Constants.SYMBOL_PATTERN_SEPARATOR:
                    value = com.dashjoin.jsonata.Functions._getFormattingCharacter(valueNode, com.dashjoin.jsonata.utils.Constants.SYMBOL_PATTERN_SEPARATOR, True)
                    symbols.setPatternSeparator(value[0])

            else:
                    #final String msg = String.format(Constants.ERR_MSG_INVALID_OPTIONS_UNKNOWN_PROPERTY,
                    #    Constants.FUNCTION_FORMAT_NUMBER, fieldName)
                    raise RuntimeException("Error parsing formatNumber format string") # SWITCH // WHILE

        return symbols

    # From JSONata4Java FormatNumberFunction
    @staticmethod
    def _getFormattingCharacter(value, propertyName, isChar):
        # Create the variable to return
        formattingChar = None

        # Make sure that we have a valid node and that its content is textual
        #if (valueNode != null && valueNode.isTextual()) {
        # Read the value
        #String value = valueNode.textValue()
        if value is not None and (not len(value)) > 0:

            # If the target property requires a single char, check the length
            if isChar:
                if len(value) == 1:
                    formattingChar = value
                else:
                    #final String msg = String.format(Constants.ERR_MSG_INVALID_OPTIONS_SINGLE_CHAR,
                    #    Constants.FUNCTION_FORMAT_NUMBER, propertyName)
                    raise RuntimeException()
            else:
                formattingChar = value
        else:
# JAVA TO PYTHON CONVERTER WARNING: The original Java variable was marked 'final':
# ORIGINAL LINE: final String msgTemplate;
            msgTemplate = None
            if isChar:
                msgTemplate = com.dashjoin.jsonata.utils.Constants.ERR_MSG_INVALID_OPTIONS_SINGLE_CHAR
            else:
                msgTemplate = com.dashjoin.jsonata.utils.Constants.ERR_MSG_INVALID_OPTIONS_STRING
            #final String msg = String.format(msgTemplate, Constants.FUNCTION_FORMAT_NUMBER, propertyName)
            raise RuntimeException(msgTemplate)
        #} 

        return formattingChar

    #    *
    #     * Converts a number to a string using a specified number base
    #     * @param {number} value - the number to convert
    #     * @param {number} [radix] - the number base; must be between 2 and 36. Defaults to 10
    #     * @returns {string} - the converted string
    #     
    @staticmethod
    def formatBase(value, _radix):
        # undefined inputs always return undefined
        if value is None:
            return None

        value = com.dashjoin.jsonata.Functions.round(value, 0)

        radix = 0
        if _radix is None:
            radix = 10
        else:
            radix = _radix.intValue()

        if radix < 2 or radix > 36:
            raise JException("D3100", radix)


        result = Long.toString(value.longValue(), radix)

        return result

    #    *
    #     * Cast argument to number
    #     * @param {Object} arg - Argument
    #     * @throws NumberFormatException
    #     * @returns {Number} numeric value of argument
    #     
    @staticmethod
# JAVA TO PYTHON CONVERTER WARNING: Method 'throws' clauses are not available in Python:
# ORIGINAL LINE: public static Number number(Object arg) throws NumberFormatException, JException
    def number(arg):
        result = None

        # undefined inputs always return undefined
        if arg is None:
            return None

        if arg is Jsonata.NULL_VALUE:
            raise JException("T0410", -1)

        if isinstance(arg, Number):
            result = arg
        elif isinstance(arg, String):
            s = str(arg)
            if s.startswith("0x"):
                result = Long.parseLong(s[2:], 16)
            elif s.startswith("0B"):
                result = Long.parseLong(s[2:], 2)
            elif s.startswith("0O"):
                result = Long.parseLong(s[2:], 8)
            else:
                result = float(str(arg))
        elif isinstance(arg, Boolean):
            result = 1 if (bool(arg)) else 0
        return result

    #    *
    #     * Absolute value of a number
    #     * @param {Number} arg - Argument
    #     * @returns {Number} absolute value of argument
    #     
    @staticmethod
    def abs(arg):

        # undefined inputs always return undefined
        if arg is None:
            return None

        return abs(arg.doubleValue()) if isinstance(arg, Double) else abs(arg.longValue())

    #    *
    #     * Rounds a number down to integer
    #     * @param {Number} arg - Argument
    #     * @returns {Number} rounded integer
    #     
    @staticmethod
    def floor(arg):

        # undefined inputs always return undefined
        if arg is None:
            return None

        return math.floor(arg.doubleValue())

    #    *
    #     * Rounds a number up to integer
    #     * @param {Number} arg - Argument
    #     * @returns {Number} rounded integer
    #     
    @staticmethod
    def ceil(arg):

        # undefined inputs always return undefined
        if arg is None:
            return None

        return math.ceil(arg.doubleValue())

    #    *
    #     * Round to half even
    #     * @param {Number} arg - Argument
    #     * @param {Number} [precision] - number of decimal places
    #     * @returns {Number} rounded integer
    #     
    @staticmethod
    def round(arg, precision):

        # undefined inputs always return undefined
        if arg is None:
            return None

        b = java.math.BigDecimal(arg + "")
        if precision is None:
            precision = 0
        b = b.setScale(precision.intValue(), java.math.RoundingMode.HALF_EVEN)

        return b.doubleValue()

    #    *
    #     * Square root of number
    #     * @param {Number} arg - Argument
    #     * @returns {Number} square root
    #     
    @staticmethod
    def sqrt(arg):

        # undefined inputs always return undefined
        if arg is None:
            return None

        if arg.doubleValue() < 0:
            raise JException("D3060", 1, arg)

        return math.sqrt(arg.doubleValue())

    #    *
    #     * Raises number to the power of the second number
    #     * @param {Number} arg - the base
    #     * @param {Number} exp - the exponent
    #     * @returns {Number} rounded integer
    #     
    @staticmethod
    def power(arg, exp):

        # undefined inputs always return undefined
        if arg is None:
            return None

        result = arg.doubleValue() ** exp.doubleValue()

        if not Double.isFinite(result):
            raise JException("D3061", 1, arg, exp)

        return result

    #    *
    #     * Returns a random number 0 <= n < 1
    #     * @returns {number} random number
    #     
    @staticmethod
    def random():
        return random.random()

    #    *
    #     * Evaluate an input and return a boolean
    #     * @param {*} arg - Arguments
    #     * @returns {boolean} Boolean
    #     
    @staticmethod
    def toBoolean(arg):
        # cast arg to its effective boolean value
        # boolean: unchanged
        # string: zero-length -> false; otherwise -> true
        # number: 0 -> false; otherwise -> true
        # null -> false
        # array: empty -> false; length > 1 -> true
        # object: empty -> false; non-empty -> true
        # function -> false

        # undefined inputs always return undefined
        if arg is None:
            return None # Uli: Null would need to be handled as false anyway

        result = False
        if isinstance(arg, java.util.List):
            l = arg
            if len(l) == 1:
                result = com.dashjoin.jsonata.Functions.toBoolean(l[0])
            elif len(l) > 1:
                truesLength = l.stream().filter(lambda e : Jsonata.boolize(e)).count()
                result = truesLength > 0
        elif isinstance(arg, String):
            s = str(arg)
            if len(s) > 0:
                result = True
        elif isinstance(arg, Number):
            if (arg).doubleValue() != 0:
                result = True
        elif isinstance(arg, java.util.Map):
            if len((arg)) > 0:
                result = True
        elif isinstance(arg, Boolean):
            result = bool(arg)
        return result

    #    *
    #     * returns the Boolean NOT of the arg
    #     * @param {*} arg - argument
    #     * @returns {boolean} - NOT arg
    #     
    @staticmethod
    def not_(arg):
        # undefined inputs always return undefined
        if arg is None:
            return None

        return not com.dashjoin.jsonata.Functions.toBoolean(arg)


    @staticmethod
    def getFunctionArity(func):
        if isinstance(func, com.dashjoin.jsonata.Jsonata.JFunction):
            return (func).signature.getMinNumberOfArgs()
        else:
            # Lambda
            return len((func).arguments)

    #    *
    #     * Helper function to build the arguments to be supplied to the function arg of the
    #     * HOFs map, filter, each, sift and single
    #     * @param {function} func - the function to be invoked
    #     * @param {*} arg1 - the first (required) arg - the value
    #     * @param {*} arg2 - the second (optional) arg - the position (index or key)
    #     * @param {*} arg3 - the third (optional) arg - the whole structure (array or object)
    #     * @returns {*[]} the argument list
    #     
    @staticmethod
    def hofFuncArgs(func, arg1, arg2, arg3):
        func_args = []
        func_args.append(arg1) # the first arg (the value) is required
        # the other two are optional - only supply it if the function can take it
        length = com.dashjoin.jsonata.Functions.getFunctionArity(func)
        if length >= 2:
            func_args.append(arg2)
        if length >= 3:
            func_args.append(arg3)
        return func_args

    #    *
    #     * Call helper for Java
    #     * 
    #     * @param func
    #     * @param funcArgs
    #     * @return
    #     * @throws Throwable
    #     
    @staticmethod
# JAVA TO PYTHON CONVERTER WARNING: Method 'throws' clauses are not available in Python:
# ORIGINAL LINE: public static Object funcApply(Object func, java.util.List funcArgs) throws Throwable
    def funcApply(func, funcArgs):
        res = None
        if com.dashjoin.jsonata.Functions.isLambda(func):
            res = Jsonata.CURRENT.get().apply(func, funcArgs, None, Jsonata.CURRENT.get().environment)
        else:
            res = (func).call(None, funcArgs)
        return res

    #    *
    #     * Create a map from an array of arguments
    #     * @param {Array} [arr] - array to map over
    #     * @param {Function} func - function to apply
    #     * @returns {Array} Map array
    #     
    @staticmethod
# JAVA TO PYTHON CONVERTER WARNING: Method 'throws' clauses are not available in Python:
# ORIGINAL LINE: public static java.util.List map(java.util.List arr, Object func) throws Throwable
    def map(arr, func):

        # undefined inputs always return undefined
        if arr is None:
            return None

        result = Utils.createSequence()
        # do the map - iterate over the arrays, and invoke func
        for i, _ in enumerate(arr):
            arg = arr[i]
            funcArgs = com.dashjoin.jsonata.Functions.hofFuncArgs(func, arg, i, arr)

            res = com.dashjoin.jsonata.Functions.funcApply(func, funcArgs)
            if res is not None:
                result.append(res)
        return result

    #    *
    #     * Create a map from an array of arguments
    #     * @param {Array} [arr] - array to filter
    #     * @param {Function} func - predicate function
    #     * @returns {Array} Map array
    #     
    @staticmethod
# JAVA TO PYTHON CONVERTER WARNING: Method 'throws' clauses are not available in Python:
# ORIGINAL LINE: public static java.util.List filter(java.util.List arr, Object func) throws Throwable
    def filter(arr, func):
        # undefined inputs always return undefined
        if arr is None:
            return None

        result = Utils.createSequence()

        for i, _ in enumerate(arr):
            entry = arr[i]
            func_args = com.dashjoin.jsonata.Functions.hofFuncArgs(func, entry, i, arr)
            # invoke func
            res = com.dashjoin.jsonata.Functions.funcApply(func, func_args)
            if com.dashjoin.jsonata.Functions.toBoolean(res):
                result.append(entry)

        return result

    #    *
    #     * Given an array, find the single element matching a specified condition
    #     * Throws an exception if the number of matching elements is not exactly one
    #     * @param {Array} [arr] - array to filter
    #     * @param {Function} [func] - predicate function
    #     * @returns {*} Matching element
    #     
    @staticmethod
# JAVA TO PYTHON CONVERTER WARNING: Method 'throws' clauses are not available in Python:
# ORIGINAL LINE: public static Object single(java.util.List arr, Object func) throws Throwable
    def single(arr, func):
        # undefined inputs always return undefined
        if arr is None:
            return None

        hasFoundMatch = False
        result = None

        for i, _ in enumerate(arr):
            entry = arr[i]
            positiveResult = True
            if func is not None:
                func_args = com.dashjoin.jsonata.Functions.hofFuncArgs(func, entry, i, arr)
                # invoke func
                res = com.dashjoin.jsonata.Functions.funcApply(func, func_args)
                positiveResult = com.dashjoin.jsonata.Functions.toBoolean(res)
            if positiveResult:
                if not hasFoundMatch:
                    result = entry
                    hasFoundMatch = True
                else:
                    raise JException("D3138", i)

        if not hasFoundMatch:
            raise JException("D3139", -1)

        return result

    #    *
    #     * Convolves (zips) each value from a set of arrays
    #     * @param {Array} [args] - arrays to zip
    #     * @returns {Array} Zipped array
    #     
    @staticmethod
    def zip(args):
        result = []
        # length of the shortest array
        length = Integer.MAX_VALUE
        nargs = 0
        # nargs : the real size of args!=null
        while nargs < len(args):
            if args[nargs] is None:
                length = 0
                break

            length = min(length, args[nargs].size())
            nargs += 1

        for i in range(0, length):
            tuple = []
            for k in range(0, nargs):
                tuple.append(args[k].get(i))
            result.append(tuple)
        return result

    #    *
    #     * Fold left function
    #     * @param {Array} sequence - Sequence
    #     * @param {Function} func - Function
    #     * @param {Object} init - Initial value
    #     * @returns {*} Result
    #     
    @staticmethod
# JAVA TO PYTHON CONVERTER WARNING: Method 'throws' clauses are not available in Python:
# ORIGINAL LINE: public static Object foldLeft(java.util.List sequence, Object func, Object init) throws Throwable
    def foldLeft(sequence, func, init):
        # undefined inputs always return undefined
        if sequence is None:
            return None
        result = None

        arity = com.dashjoin.jsonata.Functions.getFunctionArity(func)
        if arity < 2:
            raise JException("D3050", 1)

        index = 0
        if init is None and len(sequence) > 0:
            result = sequence[0]
            index = 1
        else:
            result = init
            index = 0

        while index < len(sequence):
            args = []
            args.append(result)
            args.append(sequence[index])
            if arity >= 3:
                args.append(index)
            if arity >= 4:
                args.append(sequence)
            result = com.dashjoin.jsonata.Functions.funcApply(func, args)
            index += 1

        return result

    #    *
    #     * Return keys for an object
    #     * @param {Object} arg - Object
    #     * @returns {Array} Array of keys
    #     
    @staticmethod
    def keys(arg):
        result = Utils.createSequence()

        if isinstance(arg, java.util.List):
            keys = java.util.LinkedHashSet()
            # merge the keys of all of the items in the array
            for el in (arg):
                keys.addAll(com.dashjoin.jsonata.Functions.keys(el))

            result.extend(keys)
        elif isinstance(arg, java.util.Map):
            result.extend((arg).keys())
        return result

    # here: append, lookup

    #    *
    #     * Determines if the argument is undefined
    #     * @param {*} arg - argument
    #     * @returns {boolean} False if argument undefined, otherwise true
    #     
    @staticmethod
    def exists(arg):
        if arg is None:
            return False
        else:
            return True

    #    *
    #     * Splits an object into an array of object with one property each
    #     * @param {*} arg - the object to split
    #     * @returns {*} - the array
    #     
    @staticmethod
    def spread(arg):
        result = Utils.createSequence()

        if isinstance(arg, java.util.List):
            # spread all of the items in the array
            for item in (arg):
                result = com.dashjoin.jsonata.Functions.append(result, com.dashjoin.jsonata.Functions.spread(item))
        elif isinstance(arg, java.util.Map):
            for entry in (arg).entrySet():
                obj = java.util.LinkedHashMap()
                obj.put(entry.getKey(), entry.getValue())
                (result).append(obj)
        else:
            return arg # result = arg;
        return result

    #    *
    #     * Merges an array of objects into a single object.  Duplicate properties are
    #     * overridden by entries later in the array
    #     * @param {*} arg - the objects to merge
    #     * @returns {*} - the object
    #     
    @staticmethod
    def merge(arg):
        # undefined inputs always return undefined
        if arg is None:
            return None

        result = java.util.LinkedHashMap()

        for obj in arg:
            for entry in (obj).entrySet():
                result.put(entry.getKey(), entry.getValue())
        return result

    #    *
    #     * Reverses the order of items in an array
    #     * @param {Array} arr - the array to reverse
    #     * @returns {Array} - the reversed array
    #     
    @staticmethod
    def reverse(arr):
        # undefined inputs always return undefined
        if arr is None:
            return None

        if len(arr) <= 1:
            return arr

        result = list(arr)
        result.reverse()
        return result

    #    *
    #     *
    #     * @param {*} obj - the input object to iterate over
    #     * @param {*} func - the function to apply to each key/value pair
    #     * @throws Throwable
    #     * @returns {Array} - the resultant array
    #     
    @staticmethod
# JAVA TO PYTHON CONVERTER WARNING: Method 'throws' clauses are not available in Python:
# ORIGINAL LINE: public static java.util.List each(java.util.Map obj, Object func) throws Throwable
    def each(obj, func):
        if obj is None:
            return None

        result = Utils.createSequence()

# JAVA TO PYTHON CONVERTER TASK: The following line could not be converted:
        for (var key : obj.keySet())
# JAVA TO PYTHON CONVERTER TASK: The following line could not be converted:
            var func_args = hofFuncArgs(func, obj.get(key), key, obj);
            # invoke func
            val = com.dashjoin.jsonata.Functions.funcApply(func, func_args)
            if val is not None:
                result.append(val)

        return result

    #    *
    #     *
    #     * @param {string} [message] - the message to attach to the error
    #     * @throws custom error with code 'D3137'
    #     
    @staticmethod
# JAVA TO PYTHON CONVERTER WARNING: Method 'throws' clauses are not available in Python:
# ORIGINAL LINE: public static void error(String message) throws Throwable
    def error(message):
        raise JException("D3137", -1,message if message is not None else "$error() function evaluated")

    #    *
    #     *
    #     * @param {boolean} condition - the condition to evaluate
    #     * @param {string} [message] - the message to attach to the error
    #     * @throws custom error with code 'D3137'
    #     * @returns {undefined}
    #     
    @staticmethod
# JAVA TO PYTHON CONVERTER WARNING: Method 'throws' clauses are not available in Python:
# ORIGINAL LINE: public static void assertFn(boolean condition, String message) throws Throwable
    def assertFn(condition, message):
        if not condition:
            raise JException("D3141", -1, "$assert() statement failed")
            #                message: message || "$assert() statement failed"

    #    *
    #     *
    #     * @param {*} [value] - the input to which the type will be checked
    #     * @returns {string} - the type of the input
    #     
    @staticmethod
    def type(value):
        if value is None:
            return None

        if value is Jsonata.NULL_VALUE:
            return "null"

        if isinstance(value, Number):
            return "number"

        if isinstance(value, String):
            return "string"

        if isinstance(value, Boolean):
            return "boolean"

        if isinstance(value, java.util.List):
            return "array"

        if Utils.isFunction(value) or com.dashjoin.jsonata.Functions.isLambda(value):
            return "function"

        return "object"

    #    *
    #     * Implements the merge sort (stable) with optional comparator function
    #     *
    #     * @param {Array} arr - the array to sort
    #     * @param {*} comparator - comparator function
    #     * @returns {Array} - sorted array
    #     
    @staticmethod
    def sort(arr, comparator):
        # undefined inputs always return undefined
        if arr is None:
            return None

        if len(arr) <= 1:
            return arr

        result = list(arr)

        if comparator is not None:
            comp = ComparatorAnonymousInnerClass(comparator)
            if isinstance(comparator, java.util.Comparator):
                result.sort(comparator)
            else:
                result.sort(comp)
        else:
            result.sort(None)

        return result

    class ComparatorAnonymousInnerClass(java.util.Comparator):

        def __init__(self, comparator):
            self._comparator = comparator


        def compare(self, o1, o2):
            try:
                swap = bool(com.dashjoin.jsonata.Functions.funcApply(self._comparator, [o1, o2]))
                if swap:
                    return 1
                else:
                    return -1
            except Throwable as e:
                # TODO Auto-generated catch block
                #e.printStackTrace()
                raise RuntimeException(e)


    #    *
    #     * Randomly shuffles the contents of an array
    #     * @param {Array} arr - the input array
    #     * @returns {Array} the shuffled array
    #     
    @staticmethod
    def shuffle(arr):
        # undefined inputs always return undefined
        if arr is None:
            return None

        if len(arr) <= 1:
            return arr

        result = list(arr)
        java.util.Collections.shuffle(result)
        return result

    #    *
    #     * Returns the values that appear in a sequence, with duplicates eliminated.
    #     * @param {Array} arr - An array or sequence of values
    #     * @returns {Array} - sequence of distinct values
    #     
    @staticmethod
    def distinct(_arr):
        # undefined inputs always return undefined
        if _arr is None:
            return None

        if not(isinstance(_arr, java.util.List)) or len((_arr)) <= 1:
            return _arr
        arr = _arr

        results = Utils.createSequence() if (isinstance(arr, com.dashjoin.jsonata.Utils.JList)) else []

        # Create distinct list of elements by adding all to a set,
        # and then adding the set to the result
        set = java.util.LinkedHashSet(len(arr))
        set.addAll(arr)
        results.extend(set)

        return results

    #    *
    #     * Applies a predicate function to each key/value pair in an object, and returns an object containing
    #     * only the key/value pairs that passed the predicate
    #     *
    #     * @param {object} arg - the object to be sifted
    #     * @param {object} func - the predicate function (lambda or native)
    #     * @throws Throwable
    #     * @returns {object} - sifted object
    #     
    @staticmethod
# JAVA TO PYTHON CONVERTER WARNING: Method 'throws' clauses are not available in Python:
# ORIGINAL LINE: public static Object sift(java.util.Map<Object,Object> arg, Object func) throws Throwable
    def sift(arg, func):
        if arg is None:
            return None

        result = java.util.LinkedHashMap()

        for item in arg.keys():
            entry = arg[item]
            func_args = com.dashjoin.jsonata.Functions.hofFuncArgs(func, entry, item, arg)
            # invoke func
            res = com.dashjoin.jsonata.Functions.funcApply(func, func_args)
            if Jsonata.boolize(res):
                result.put(item, entry)

        # empty objects should be changed to undefined
        if result.isEmpty():
            result = None

        return result

    #/////
    #/////
    #/////
    #/////

    #    *
    #     * Append second argument to first
    #     * @param {Array|Object} arg1 - First argument
    #     * @param {Array|Object} arg2 - Second argument
    #     * @returns {*} Appended arguments
    #     
    @staticmethod
    def append(arg1, arg2):
        # disregard undefined args
        if arg1 is None:
            return arg2
        if arg2 is None:
            return arg1

        # if either argument is not an array, make it so
        if not(isinstance(arg1, java.util.List)):
            arg1 = Utils.createSequence(arg1)
        if not(isinstance(arg2, java.util.List)):
            arg2 = com.dashjoin.jsonata.Utils.JList(java.util.Arrays.asList(arg2))
        # else
        #     // Arg2 was a list: add it as a list element (don't flatten)
        #     ((List)arg1).add((List)arg2)

        # Shortcut:
        if len((arg1)) == 0 and (isinstance(arg2, Utils.RangeList)):
            return arg2

        arg1 = com.dashjoin.jsonata.Utils.JList(arg1) # create a new copy!
        if isinstance(arg2, com.dashjoin.jsonata.Utils.JList) and (arg2).cons:
            (arg1).append(arg2)
        else:
            (arg1).extend(arg2)
        return arg1

    @staticmethod
    def isLambda(result):
        return (isinstance(result, com.dashjoin.jsonata.Parser.Symbol) and (result)._jsonata_lambda)

    #    *
    #     * Return value from an object for a given key
    #     * @param {Object} input - Object/Array
    #     * @param {String} key - Key in object
    #     * @returns {*} Value of key in object
    #     
    @staticmethod
    def lookup(input, key):
        # lookup the 'name' item in the input
        result = None
        if isinstance(input, java.util.List):
            _input = input
            result = Utils.createSequence()
            for ii, _ in enumerate(_input):
                res = com.dashjoin.jsonata.Functions.lookup(_input[ii], key)
                if res is not None:
                    if isinstance(res, java.util.List):
                        (result).extend(res)
                    else:
                        (result).append(res)
        elif isinstance(input, java.util.Map):
            result = (input)[key]
            # Detect the case where the value is null:
            if result is None and key in (input).keys():
                result = Jsonata.NULL_VALUE
        return result

    @staticmethod
    def test(a, b):
        return a + b

    @staticmethod
    def getFunction(clz, name):
        methods = Functions.class.getMethods()
        for m in methods:
            # if (m.getModifiers() == (Modifier.STATIC | Modifier.PUBLIC) ) {
            #     System.out.println(m.getName())
            #     System.out.println(m.getParameterTypes())
            # }
            if m.getName() is name:
                return m
        return None

    @staticmethod
# JAVA TO PYTHON CONVERTER WARNING: Method 'throws' clauses are not available in Python:
# ORIGINAL LINE: public static Object call(Class clz, Object instance, String name, java.util.List<Object> args) throws Throwable
# JAVA TO PYTHON CONVERTER TASK: Python does not allow method overloads:
    def call(clz, instance, name, args):
        return com.dashjoin.jsonata.Functions.call(instance, com.dashjoin.jsonata.Functions.getFunction(clz, name), args)

    @staticmethod
# JAVA TO PYTHON CONVERTER WARNING: Method 'throws' clauses are not available in Python:
# ORIGINAL LINE: public static Object call(Object instance, java.lang.reflect.Method m, java.util.List<Object> args) throws Throwable
# JAVA TO PYTHON CONVERTER TASK: Python does not allow method overloads:
    def call(instance, m, args):
        types = m.getParameterTypes()
        nargs = m.getParameterTypes().length

        callArgs = list(args)
        while len(callArgs) < nargs:
            # Add default arg null if not enough args were provided
            callArgs.append(None)

        # Special handling of one arg if function requires list:
        # Wrap the single arg (if != null) in a list with one element
        if nargs > 0 and java.util.List.class.isAssignableFrom(types[0]) and not(isinstance(callArgs[0], java.util.List)):
            arg1 = callArgs[0]
            if arg1 is not None:
                wrap = []
                wrap.append(arg1)
                callArgs[0] = wrap
                #System.err.println("wrapped "+arg1+" as "+wrap)

        # If the function receives the args as JList:
        # i.e. a varargs fn like zip can use this
        if nargs == 1 and types[0] is com.dashjoin.jsonata.Utils.JList.class:
            allArgs = com.dashjoin.jsonata.Utils.JList(args)
            callArgs = [allArgs]

        try:
            res = m.invoke(None, callArgs.toArray())
            if isinstance(res, Number):
                res = Utils.convertNumber(res)
            return res
        except IllegalAccessException as e:
            raise Exception("Access error calling function " + m.getName(), e)
        except IllegalArgumentException as e:
            raise Exception("Argument error calling function " + m.getName(), e)
        except java.lang.reflect.InvocationTargetException as e:
            #e.printStackTrace()
            raise e.getTargetException()


    #
    # DateTime
    #

    #    *
    #     * Converts an ISO 8601 timestamp to milliseconds since the epoch
    #     *
    #     * @param {string} timestamp - the timestamp to be converted
    #     * @param {string} [picture] - the picture string defining the format of the timestamp (defaults to ISO 8601)
    #     * @throws ParseException 
    #     * @returns {Number} - milliseconds since the epoch
    #     
    @staticmethod
# JAVA TO PYTHON CONVERTER WARNING: Method 'throws' clauses are not available in Python:
# ORIGINAL LINE: public static Long dateTimeToMillis(String timestamp, String picture) throws java.text.ParseException
    def dateTimeToMillis(timestamp, picture):
        # undefined inputs always return undefined
        if timestamp is None:
            return None

        if picture is None:
            if com.dashjoin.jsonata.Functions.isNumeric(timestamp):
                sdf = java.text.SimpleDateFormat("yyyy")
                sdf.setTimeZone(java.util.TimeZone.getTimeZone("UTC"))
                return sdf.parse(timestamp).getTime()
            try:
                len = len(timestamp)
                if len > 5:
                    if timestamp[len - 5] == '+' or timestamp[len - 5] == '-':
                        if (timestamp[len - 4]).isdigit() and (timestamp[len - 3]).isdigit() and (timestamp[len - 2]).isdigit() and (timestamp[len - 1]).isdigit():
                            timestamp = timestamp[0:len - 2] + ':' + timestamp[len - 2:len]
                return java.time.OffsetDateTime.parse(timestamp).toInstant().toEpochMilli()
            except RuntimeException as e:
                ldt = java.time.LocalDate.parse(timestamp, java.time.format.DateTimeFormatter.ofPattern("yyyy-MM-dd"))
                return ldt.atStartOfDay().atZone(java.time.ZoneId.of("UTC")).toInstant().toEpochMilli()
        else:
            return com.dashjoin.jsonata.utils.DateTimeUtils.parseDateTime(timestamp, picture)
    # Adapted from: org.apache.commons.lang3.StringUtils
    @staticmethod
# JAVA TO PYTHON CONVERTER TASK: There is no Python equivalent to Java's 'final' parameters:
# ORIGINAL LINE: public static boolean isNumeric(final CharSequence cs)
    def isNumeric(cs):
        if cs is None or cs.length() == 0:
            return False
# JAVA TO PYTHON CONVERTER WARNING: The original Java variable was marked 'final':
# ORIGINAL LINE: final int sz = cs.length();
        sz = cs.length()
        for i in range(0, sz):
            if not (cs.charAt(i)).isdigit():
                return False
        return True

    #    *
    #     * Converts milliseconds since the epoch to an ISO 8601 timestamp
    #     * @param {Number} millis - milliseconds since the epoch to be converted
    #     * @param {string} [picture] - the picture string defining the format of the timestamp (defaults to ISO 8601)
    #     * @param {string} [timezone] - the timezone to format the timestamp in (defaults to UTC)
    #     * @returns {String} - the formatted timestamp
    #     
    @staticmethod
    def dateTimeFromMillis(millis, picture, timezone):
        # undefined inputs always return undefined
        if millis is None:
            return None

        return com.dashjoin.jsonata.utils.DateTimeUtils.formatDateTime(millis.longValue(), picture, timezone)

    #    *
    #     * Formats an integer as specified by the XPath fn:format-integer function
    #     * See https://www.w3.org/TR/xpath-functions-31/#func-format-integer
    #     * @param {number} value - the number to be formatted
    #     * @param {string} picture - the picture string that specifies the format
    #     * @returns {string} - the formatted number
    #     
    @staticmethod
    def formatInteger(value, picture):
        if value is None:
            return None
        return com.dashjoin.jsonata.utils.DateTimeUtils.formatInteger(value.longValue(), picture)

    #    *
    #     * parse a string containing an integer as specified by the picture string
    #     * @param {string} value - the string to parse
    #     * @param {string} picture - the picture string
    #     * @throws ParseException
    #     * @returns {number} - the parsed number
    #     
    @staticmethod
# JAVA TO PYTHON CONVERTER WARNING: Method 'throws' clauses are not available in Python:
# ORIGINAL LINE: public static Number parseInteger(String value, String picture) throws ParseException, JException
    def parseInteger(value, picture):
        if value is None:
            return None

        # const formatSpec = analyseIntegerPicture(picture)
        # const matchSpec = generateRegex(formatSpec)
        # //const fullRegex = '^' + matchSpec.regex + '$'
        # //const matcher = new RegExp(fullRegex)
        # // TODO validate input based on the matcher regex
        # const result = matchSpec.parse(value)
        # return result

        if picture is not None:
            if picture == "#":
                raise java.text.ParseException("Formatting or parsing an integer as a sequence starting with \"#\" is not supported by this implementation", 0)
            if picture.endswith(";o"):
                picture = picture[0:len(picture) - 2]
            if picture == "a":
                return com.dashjoin.jsonata.utils.DateTimeUtils.lettersToDecimal(value, 'a')
            if picture == "A":
                return com.dashjoin.jsonata.utils.DateTimeUtils.lettersToDecimal(value, 'A')
            if picture == "i":
                return com.dashjoin.jsonata.utils.DateTimeUtils.romanToDecimal(value.upper())
            if picture == "I":
                return com.dashjoin.jsonata.utils.DateTimeUtils.romanToDecimal(value)
            if picture == "w":
                return com.dashjoin.jsonata.utils.DateTimeUtils.wordsToLong(value)
            if picture == "W" or picture == "wW" or picture == "Ww":
                return com.dashjoin.jsonata.utils.DateTimeUtils.wordsToLong(value.casefold())
            if picture.find(':') >= 0:
                value = value.replace(':', ',')
                picture = picture.replace(':', ',')

        formatter = java.text.DecimalFormat(picture, java.text.DecimalFormatSymbols(java.util.Locale.US)) if picture is not None else java.text.DecimalFormat()
        return formatter.parse(value)
        #throw new RuntimeException("not implemented")

    #    *
    #     * Clones an object
    #     * @param {Object} arg - object to clone (deep copy)
    #     * @returns {*} - the cloned object
    #     
    @staticmethod
    def functionClone(arg):
        # undefined inputs always return undefined
        if arg is None:
            return None

        res = com.dashjoin.jsonata.json.Json.parseJson(com.dashjoin.jsonata.Functions.string(arg, False))
        return res

    #    *
    #     * parses and evaluates the supplied expression
    #     * @param {string} expr - expression to evaluate
    #     * @returns {*} - result of evaluating the expression
    #     
    @staticmethod
    def functionEval(expr, focus):
        # undefined inputs always return undefined
        if expr is None:
            return None
        input = Jsonata.CURRENT.get().input # =  this.input;
        if focus is not None:
            input = focus
            # if the input is a JSON array, then wrap it in a singleton sequence so it gets treated as a single input
            if (isinstance(input, java.util.List)) and not Utils.isSequence(input):
                input = Utils.createSequence(input)
                (input).outerWrapper = True

        ast = None
        try:
            ast = jsonata(expr)
        except Throwable as err:
            # error parsing the expression passed to $eval
            #populateMessage(err)
            raise JException("D3120", -1)
        result = None
        try:
            result = ast.evaluate(input, Jsonata.CURRENT.get().environment)
        except Throwable as err:
            # error evaluating the expression passed to $eval
            #populateMessage(err)
            raise JException("D3121", -1)

        return result

    #  environment.bind("now", defineFunction(function(picture, timezone) {
    #      return datetime.fromMillis(timestamp.getTime(), picture, timezone)
    #  }, "<s?s?:s>"))
    @staticmethod
    def now(picture, timezone):
        t = Jsonata.CURRENT.get().timestamp
        return com.dashjoin.jsonata.Functions.dateTimeFromMillis(t, picture, timezone)

    #  environment.bind("millis", defineFunction(function() {
    #      return timestamp.getTime()
    #  }, "<:n>"))
    @staticmethod
    def millis():
        t = Jsonata.CURRENT.get().timestamp
        return t
