#
# jsonata-java is the JSONata Java reference port
# 
# Copyright Dashjoin GmbH. https://dashjoin.com
# 
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# 

import base64
import datetime
import decimal
import functools
import inspect
import json
import math
import random
import re
import sys
import unicodedata
import urllib.parse
from dataclasses import dataclass
from typing import Any, AnyStr, Mapping, NoReturn, Sequence, Callable, Type

from jsonata import datetimeutils, jexception, parser, utils


class Functions:

    #
    # Sum function
    # @param {Object} args - Arguments
    # @returns {number} Total value of arguments
    #     
    @staticmethod
    def sum(args: Sequence[float] | None) -> float | None:
        # undefined inputs always return undefined
        if args is None:
            return None

        return sum(args)

    #
    # Count function
    # @param {Object} args - Arguments
    # @returns {number} Number of elements in the array
    #     
    @staticmethod
    def count(args: Sequence[Any] | None) -> float:
        # undefined inputs always return undefined
        if args is None:
            return 0

        return len(args)

    #
    # Max function
    # @param {Object} args - Arguments
    # @returns {number} Max element in the array
    #     
    @staticmethod
    def max(args: Sequence[float] | None) -> float | None:
        # undefined inputs always return undefined
        if args is None or len(args) == 0:
            return None

        return max(args)

    #
    # Min function
    # @param {Object} args - Arguments
    # @returns {number} Min element in the array
    #     
    @staticmethod
    def min(args: Sequence[float] | None) -> float | None:
        # undefined inputs always return undefined
        if args is None or len(args) == 0:
            return None

        return min(args)

    #
    # Average function
    # @param {Object} args - Arguments
    # @returns {number} Average element in the array
    #     
    @staticmethod
    def average(args: Sequence[float] | None) -> float | None:
        # undefined inputs always return undefined
        if args is None or len(args) == 0:
            return None

        return sum(args) / len(args)

    #
    # Stringify arguments
    # @param {Object} arg - Arguments
    # @param {boolean} [prettify] - Pretty print the result
    # @returns {String} String from arguments
    #     
    @staticmethod
    def string(arg: Any | None, prettify: bool | None) -> str | None:

        if isinstance(arg, utils.Utils.JList):
            if arg.outer_wrapper:
                arg = arg[0]

        if arg is None:
            return None

        # see https://docs.jsonata.org/string-functions#string: Strings are unchanged
        if isinstance(arg, str):
            return str(arg)

        return Functions._string(arg, prettify is not None and prettify)

    @staticmethod
    def _string(arg: Any, prettify: bool) -> str:
        from jsonata import jsonata

        if isinstance(arg, (jsonata.Jsonata.JFunction, parser.Parser.Symbol)):
            return ""

        if prettify:
            return json.dumps(arg, cls=Functions.Encoder, indent="  ")
        else:
            return json.dumps(arg, cls=Functions.Encoder, separators=(',', ':'))

    class Encoder(json.JSONEncoder):
        def encode(self, arg):
            if not isinstance(arg, bool) and isinstance(arg, (int, float)):
                d = decimal.Decimal(arg)
                res = Functions.remove_exponent(d, decimal.Context(prec=15))
                return str(res).lower()

            return super().encode(arg)

        def default(self, arg):
            from jsonata import jsonata

            if arg is utils.Utils.NULL_VALUE:
                return None

            if isinstance(arg, (jsonata.Jsonata.JFunction, parser.Parser.Symbol)):
                return ""

            return super().default(arg)

    @staticmethod
    def remove_exponent(d: decimal.Decimal, ctx: decimal.Context) -> decimal.Decimal:
        # Adapted from https://docs.python.org/3/library/decimal.html#decimal-faq
        if d == d.to_integral():
            try:
                return d.quantize(decimal.Decimal(1), context=ctx)
            except decimal.InvalidOperation:
                pass
        return d.normalize(ctx)

    #
    # Validate input data types.
    # This will make sure that all input data can be processed.
    # 
    # @param arg
    # @return
    #     
    @staticmethod
    def validate_input(arg: Any | None) -> None:
        from jsonata import jsonata

        if arg is None or arg is utils.Utils.NULL_VALUE:
            return

        if isinstance(arg, (jsonata.Jsonata.JFunction, parser.Parser.Symbol)):
            return

        if isinstance(arg, bool):
            return

        if isinstance(arg, (int, float)):
            return

        if isinstance(arg, str):
            return

        if isinstance(arg, dict):
            for k, v in arg.items():
                Functions.validate_input(k)
                Functions.validate_input(v)
            return

        if isinstance(arg, list):
            for v in arg:
                Functions.validate_input(v)
            return

        # Throw error for unknown types
        raise ValueError(
            "Only JSON types (values, Map, List) are allowed as input. Unsupported type: " + str(type(arg)))

    #
    # Create substring based on character number and length
    # @param {String} str - String to evaluate
    # @param {Integer} start - Character number to start substring
    # @param {Integer} [length] - Number of characters in substring
    # @returns {string|*} Substring
    #     
    @staticmethod
    def substring(string: str | None, _start: float | None, _length: float | None) -> str | None:
        # undefined inputs always return undefined
        if string is None:
            return None

        start = int(_start) if _start is not None else None
        length = int(_length) if _length is not None else None

        # not used: var strArray = stringToArray(string)
        str_length = len(string)

        if str_length + start < 0:
            start = 0

        if length is not None:
            if length <= 0:
                return ""
            return Functions.substr(string, start, length)

        return Functions.substr(string, start, str_length)

    #
    # Source = Jsonata4Java JSONataUtils.substr
    # @param str
    # @param start  Location at which to begin extracting characters. If a negative
    #               number is given, it is treated as strLength - start where
    #               strLength is the length of the string. For example,
    #               str.substr(-3) is treated as str.substr(str.length - 3)
    # @param length The number of characters to extract. If this argument is null,
    #               all the characters from start to the end of the string are
    #               extracted.
    # @return A new string containing the extracted section of the given string. If
    #         length is 0 or a negative number, an empty string is returned.
    #     
    @staticmethod
    def substr(string: str | None, start: int | None, length: int | None) -> str:

        # below has to convert start and length for emojis and unicode
        orig_len = len(string)

        str_data = string
        str_len = len(str_data)
        if start >= str_len:
            return ""
        # If start is negative, substr() uses it as a character index from the
        # end of the string; the index of the last character is -1.
        start = start if start >= 0 else (0 if (str_len + start) < 0 else str_len + start)
        if start < 0:
            start = 0  # If start is negative and abs(start) is larger than the length of the
        # string, substr() uses 0 as the start index.
        # If length is omitted, substr() extracts characters to the end of the
        # string.
        if length is None:
            length = len(str_data)
        elif length < 0:
            # If length is 0 or negative, substr() returns an empty string.
            return ""
        elif length > len(str_data):
            length = len(str_data)

        if start >= 0:
            # If start is positive and is greater than or equal to the length of
            # the string, substr() returns an empty string.
            if start >= orig_len:
                return ""

        # collect length characters (unless it reaches the end of the string
        # first, in which case it will return fewer)
        end = start + length
        if end > orig_len:
            end = orig_len

        return str_data[start:end]

    #
    # Create substring up until a character
    # @param {String} str - String to evaluate
    # @param {String} chars - Character to define substring boundary
    # @returns {*} Substring
    #     
    @staticmethod
    def substring_before(string: str | None, chars: str | None) -> str | None:
        # undefined inputs always return undefined
        if string is None:
            return None

        if chars is None:
            return string

        pos = string.find(chars)
        if pos > -1:
            return string[0:pos]
        else:
            return string

    #
    # Create substring after a character
    # @param {String} str - String to evaluate
    # @param {String} chars - Character to define substring boundary
    # @returns {*} Substring
    #     
    @staticmethod
    def substring_after(string: str | None, chars: str | None) -> str | None:
        # undefined inputs always return undefined
        if string is None:
            return None

        pos = string.find(chars)
        if pos > -1:
            return string[pos + len(chars):]
        else:
            return string

    #
    # Lowercase a string
    # @param {String} str - String to evaluate
    # @returns {string} Lowercase string
    #     
    @staticmethod
    def lowercase(string: str | None) -> str | None:
        # undefined inputs always return undefined
        if string is None:
            return None

        return string.casefold()

    #
    # Uppercase a string
    # @param {String} str - String to evaluate
    # @returns {string} Uppercase string
    #     
    @staticmethod
    def uppercase(string: str | None) -> str | None:
        # undefined inputs always return undefined
        if string is None:
            return None

        return string.upper()

    #
    # length of a string
    # @param {String} str - string
    # @returns {Number} The number of characters in the string
    #     
    @staticmethod
    def length(string: str | None) -> int | None:
        # undefined inputs always return undefined
        if string is None:
            return None

        return len(string)

    #
    # Normalize and trim whitespace within a string
    # @param {string} str - string to be trimmed
    # @returns {string} - trimmed string
    #     
    @staticmethod
    def trim(string: str | None) -> str | None:
        # undefined inputs always return undefined
        if string is None:
            return None

        if len(string) == 0:
            return ""

        # normalize whitespace
        result = re.sub("[ \t\n\r]+", " ", string)
        if result[0] == ' ':
            # strip leading space
            result = result[1:]

        if result == "":
            return ""

        if result[len(result) - 1] == ' ':
            # strip trailing space
            result = result[0:len(result) - 1]
        return result

    #
    # Pad a string to a minimum width by adding characters to the start or end
    # @param {string} str - string to be padded
    # @param {number} width - the minimum width; +ve pads to the right, -ve pads to the left
    # @param {string} [char] - the pad character(s); defaults to ' '
    # @returns {string} - padded string
    #     
    @staticmethod
    def pad(string: str | None, width: int | None, _char: str | None) -> str | None:
        # undefined inputs always return undefined
        if string is None:
            return None

        if _char is None or len(_char) == 0:
            _char = " "

        result = None

        if width < 0:
            result = Functions.left_pad(string, -width, _char)
        else:
            result = Functions.right_pad(string, width, _char)
        return result

    # Source: Jsonata4Java PadFunction
    @staticmethod
    def left_pad(string: str | None, size: int | None, pad_str: str | None) -> str | None:
        if string is None:
            return None
        if pad_str is None:
            pad_str = " "

        str_data = string
        str_len = len(str_data)

        pad_data = pad_str
        pad_len = len(pad_data)

        if pad_len == 0:
            pad_str = " "
        pads = size - str_len
        if pads <= 0:
            return string
        padding = ""
        i = 0
        while i < pads + 1:
            padding += pad_str
            i += 1
        return Functions.substr(padding, 0, pads) + string

    # Source: Jsonata4Java PadFunction
    @staticmethod
    def right_pad(string: str | None, size: int | None, pad_str: str | None) -> str | None:
        if string is None:
            return None
        if pad_str is None:
            pad_str = " "

        str_data = string
        str_len = len(str_data)

        pad_data = pad_str
        pad_len = len(pad_data)

        if pad_len == 0:
            pad_str = " "
        pads = size - str_len
        if pads <= 0:
            return string
        padding = ""
        i = 0
        while i < pads + 1:
            padding += pad_str
            i += 1
        return string + Functions.substr(padding, 0, pads)

    @dataclass
    class RegexpMatch:
        match: str
        index: int
        groups: Sequence[AnyStr]

    #
    # Evaluate the matcher function against the str arg
    #
    # @param {*} matcher - matching function (native or lambda)
    # @param {string} str - the string to match against
    # @returns {object} - structure that represents the match(es)
    #     
    @staticmethod
    def evaluate_matcher(matcher: re.Pattern | None, string: str | None) -> list[RegexpMatch]:
        res = []
        matches = matcher.finditer(string)
        for m in matches:
            groups = []
            # Collect the groups
            g = 1
            while g <= len(m.groups()):
                groups.append(m.group(g))
                g += 1

            rm = Functions.RegexpMatch(m.group(), m.start(), groups)
            rm.groups = groups
            res.append(rm)
        return res

    #
    # Tests if the str contains the token
    # @param {String} str - string to test
    # @param {String} token - substring or regex to find
    # @returns {Boolean} - true if str contains token
    #     
    @staticmethod
    def contains(string: str | None, token: None | str | re.Pattern) -> bool | None:
        # undefined inputs always return undefined
        if string is None:
            return None

        result = False

        if isinstance(token, str):
            result = (string.find(str(token)) != - 1)
        elif isinstance(token, re.Pattern):
            matches = Functions.evaluate_matcher(token, string)
            # if (dbg) System.out.println("match = "+matches)
            # result = (typeof matches !== 'undefined')
            # throw new Error("regexp not impl"); //result = false
            result = len(matches) > 0
        else:
            raise RuntimeError("unknown type to match: " + str(token))

        return result

    #
    # Match a string with a regex returning an array of object containing details of each match
    # @param {String} str - string
    # @param {String} regex - the regex applied to the string
    # @param {Integer} [limit] - max number of matches to return
    # @returns {Array} The array of match objects
    #     
    @staticmethod
    def match_(string: str | None, regex: re.Pattern | None, limit: int | None) -> list[dict] | None:
        # undefined inputs always return undefined
        if string is None:
            return None

        # limit, if specified, must be a non-negative number
        if limit is not None and limit < 0:
            raise jexception.JException("D3040", -1, limit)

        result = utils.Utils.create_sequence()
        matches = Functions.evaluate_matcher(regex, string)
        max = sys.maxsize
        if limit is not None:
            max = limit

        for i, rm in enumerate(matches):
            m = {"match": rm.match, "index": rm.index, "groups": rm.groups}
            # Convert to JSON map:
            result.append(m)
            if i >= max:
                break
        return result

    #
    # Join an array of strings
    # @param {Array} strs - array of string
    # @param {String} [separator] - the token that splits the string
    # @returns {String} The concatenated string
    #     
    @staticmethod
    def join(strs: Sequence[str] | None, separator: str | None) -> str | None:
        # undefined inputs always return undefined
        if strs is None:
            return None

        # if separator is not specified, default to empty string
        if separator is None:
            separator = ""

        return separator.join(strs)

    @staticmethod
    def safe_replacement(in_: str) -> str:
        result = in_

        # Replace "$<num>" with "\<num>" for Python regex
        result = re.sub(r"\$(\d+)", r"\\g<\g<1>>", result)

        # Replace "$$" with "$"
        result = re.sub("\\$\\$", "$", result)

        return result

    #
    # Safe replaceAll
    # 
    # In Java, non-existing groups cause an exception.
    # Ignore these non-existing groups (replace with "")
    # 
    # @param s
    # @param pattern
    # @param replacement
    # @return
    #     
    @staticmethod
    def safe_replace_all(s: str | None, pattern: re.Pattern, _replacement: Any | None) -> str | None:

        if not (isinstance(_replacement, str)):
            return Functions.safe_replace_all_fn(s, pattern, _replacement)

        replacement = str(_replacement)

        replacement = Functions.safe_replacement(replacement)
        r = None
        for i in range(0, 10):
            try:
                r = re.sub(pattern, replacement, s)
                break
            except Exception as e:
                msg = str(e)

                # Message we understand needs to be:
                # invalid group reference <g> at position <p>
                m = re.match(r"invalid group reference (\d+) at position (\d+)", msg)

                if m is None:
                    raise e

                g = m.group(1)
                suffix = g[-1]
                prefix = g[:-1]
                # Try capturing a smaller numbered group, e.g. "\g<1>2" instead of "\g<12>"
                replace = "" if len(prefix) == 0 else r"\g<" + prefix + ">" + suffix

                # Adjust replacement to remove the non-existing group
                replacement = replacement.replace(r"\g<" + g + ">", replace)
        return r

    #
    # Converts Java MatchResult to the Jsonata object format
    # @param mr
    # @return
    #     
    @staticmethod
    def to_jsonata_match(mr: re.Match[str]) -> dict[str, str]:
        obj = {"match": mr.group()}

        groups = []
        i = 0
        while i <= len(mr.groups()):
            groups.append(mr.group(i))
            i += 1

        obj["groups"] = groups

        return obj

    #
    # Regexp Replace with replacer function
    # @param s
    # @param pattern
    # @param fn
    # @return
    #     
    @staticmethod
    def safe_replace_all_fn(s: str | None, pattern: re.Pattern, fn: Any | None) -> str:
        def replace_fn(t):
            res = Functions.func_apply(fn, [Functions.to_jsonata_match(t)])
            if isinstance(res, str):
                return res
            else:
                raise jexception.JException("D3012", -1)

        r = re.sub(pattern, replace_fn, s)
        return r

    #
    # Safe replaceFirst
    # 
    # @param s
    # @param pattern
    # @param replacement
    # @return
    #     
    @staticmethod
    def safe_replace_first(s: str | None, pattern: re.Pattern, replacement: str) -> str | None:
        replacement = Functions.safe_replacement(replacement)
        r = None
        for i in range(0, 10):
            try:
                r = re.sub(pattern, replacement, s, 1)
                break
            except Exception as e:
                msg = str(e)

                # Message we understand needs to be:
                # invalid group reference <g> at position <p>
                m = re.match(r"invalid group reference (\d+) at position (\d+)", msg)

                if m is None:
                    raise e

                g = m.group(1)
                suffix = g[-1]
                prefix = g[:-1]
                # Try capturing a smaller numbered group, e.g. "\g<1>2" instead of "\g<12>"
                replace = "" if len(prefix) == 0 else r"\g<" + prefix + ">" + suffix

                # Adjust replacement to remove the non-existing group
                replacement = replacement.replace(r"\g<" + g + ">", replace)
        return r

    @staticmethod
    def replace(string: str | None, pattern: str | re.Pattern, replacement: Any | None, limit: int | None) -> str | None:
        if string is None:
            return None
        if isinstance(pattern, str):
            if len((str(pattern))) == 0:
                raise jexception.JException("Second argument of replace function cannot be an empty string", 0)
        if limit is None:
            if isinstance(pattern, str):
                return re.sub(pattern, str(replacement), string)
            else:
                return Functions.safe_replace_all(string, pattern, replacement)
        else:

            if limit < 0:
                raise jexception.JException("Fourth argument of replace function must evaluate to a positive number", 0)

            for i in range(0, limit):
                if isinstance(pattern, str):
                    string = re.sub(pattern, str(replacement), string, 1)
                else:
                    string = Functions.safe_replace_first(string, pattern, str(replacement))
            return string

    #
    # Base64 encode a string
    # @param {String} str - string
    # @returns {String} Base 64 encoding of the binary data
    #     
    @staticmethod
    def base64encode(string: str | None) -> str | None:
        # undefined inputs always return undefined
        if string is None:
            return None
        try:
            return base64.b64encode(string.encode("utf-8")).decode("utf-8")
        except Exception as e:
            return None

    #
    # Base64 decode a string
    # @param {String} str - string
    # @returns {String} Base 64 encoding of the binary data
    #     
    @staticmethod
    def base64decode(string: str | None) -> str | None:
        # undefined inputs always return undefined
        if string is None:
            return None
        try:
            return base64.b64decode(string.encode("utf-8")).decode("utf-8")
        except Exception as e:
            return None

    #
    # Encode a string into a component for a url
    # @param {String} str - String to encode
    # @returns {string} Encoded string
    #     
    @staticmethod
    def encode_url_component(string: str | None) -> str | None:
        # undefined inputs always return undefined
        if string is None:
            return None

        # See https://stackoverflow.com/questions/946170/equivalent-javascript-functions-for-pythons-urllib-parse-quote-and-urllib-par
        return urllib.parse.quote(string, safe="~()*!.'")

    #
    # Encode a string into a url
    # @param {String} str - String to encode
    # @returns {string} Encoded string
    #     
    @staticmethod
    def encode_url(string: str | None) -> str | None:
        # undefined inputs always return undefined
        if string is None:
            return None

        # See https://stackoverflow.com/questions/946170/equivalent-javascript-functions-for-pythons-urllib-parse-quote-and-urllib-par
        return urllib.parse.quote(string, safe="~@#$&()*!+=:;,.?/'")

    #
    # Decode a string from a component for a url
    # @param {String} str - String to decode
    # @returns {string} Decoded string
    #     
    @staticmethod
    def decode_url_component(string: str | None) -> str | None:
        # undefined inputs always return undefined
        if string is None:
            return None

        # See https://stackoverflow.com/questions/946170/equivalent-javascript-functions-for-pythons-urllib-parse-quote-and-urllib-par
        return urllib.parse.unquote(string, errors="strict")

    #
    # Decode a string from a url
    # @param {String} str - String to decode
    # @returns {string} Decoded string
    #     
    @staticmethod
    def decode_url(string: str | None) -> str | None:
        # undefined inputs always return undefined
        if string is None:
            return None

        # See https://stackoverflow.com/questions/946170/equivalent-javascript-functions-for-pythons-urllib-parse-quote-and-urllib-par
        return urllib.parse.unquote(string, errors="strict")

    @staticmethod
    def split(string: str | None, pattern: str | re.Pattern | None, limit: float | None) -> list[str] | None:
        if string is None:
            return None

        if limit is not None and int(limit) < 0:
            raise jexception.JException("D3020", -1, string)

        result = []
        if limit is not None and int(limit) == 0:
            return result

        if isinstance(pattern, str):
            sep = str(pattern)
            if len(sep) == 0:
                # $split("str", ""): Split string into characters
                lim = int(limit) if limit is not None else sys.maxsize
                i = 0
                while i < len(string) and i < lim:
                    result.append(string[i])
                    i += 1
            else:
                # Quote separator string + preserve trailing empty strings (-1)
                result = list(filter(None, string.split(sep, -1)))
        else:
            result = list(filter(None, pattern.split(string)))
        if limit is not None and int(limit) < len(result):
            result = result[0:int(limit)]
        return result

    EXPONENT_PIC = re.compile(r'\d[eE]\d')

    #
    # Formats a number into a decimal string representation using XPath 3.1 F&O fn:format-number spec
    # @param {number} value - number to format
    # @param {String} picture - picture string definition
    # @param {Object} [options] - override locale defaults
    # @returns {String} The formatted string
    #     
    # Adapted from https://github.com/sissaschool/elementpath
    @staticmethod
    def format_number(value: float | None, picture: str | None, decimal_format: Mapping[str, str] | None) -> str | None:
        if decimal_format is None:
            decimal_format = {}
        pattern_separator = decimal_format.get('pattern-separator', ';')
        sub_pictures = picture.split(pattern_separator)
        if len(sub_pictures) > 2:
            raise jexception.JException('D3080', -1)

        decimal_separator = decimal_format.get('decimal-separator', '.')
        if any(p.count(decimal_separator) > 1 for p in sub_pictures):
            raise jexception.JException('D3081', -1)

        percent_sign = decimal_format.get('percent', '%')
        if any(p.count(percent_sign) > 1 for p in sub_pictures):
            raise jexception.JException('D3082', -1)

        per_mille_sign = decimal_format.get('per-mille', '‰')
        if any(p.count(per_mille_sign) > 1 for p in sub_pictures):
            raise jexception.JException('D3083', -1)
        if any(p.count(percent_sign) + p.count(per_mille_sign) > 1 for p in sub_pictures):
            raise jexception.JException('D3084')

        zero_digit = decimal_format.get('zero-digit', '0')
        optional_digit = decimal_format.get('digit', '#')
        digits_family = ''.join(chr(cp + ord(zero_digit)) for cp in range(10))
        if any(optional_digit not in p and all(x not in p for x in digits_family)
               for p in sub_pictures):
            raise jexception.JException('D3085', -1)

        grouping_separator = decimal_format.get('grouping-separator', ',')
        adjacent_pattern = re.compile(r'[\\%s\\%s]{2}' % (grouping_separator, decimal_separator))
        if any(adjacent_pattern.search(p) for p in sub_pictures):
            raise jexception.JException('D3087', -1)

        if any(x.endswith(grouping_separator)
               for s in sub_pictures for x in s.split(decimal_separator)):
            raise jexception.JException('D3088', -1)

        active_characters = digits_family + ''.join([
            decimal_separator, grouping_separator, pattern_separator, optional_digit
        ])

        exponent_pattern = None

        # Check optional exponent spec correctness in each sub-picture
        exponent_separator = decimal_format.get('exponent-separator', 'e')
        _pattern = re.compile(r'(?<=[{0}]){1}[{0}]'.format(
            re.escape(active_characters), exponent_separator
        ))
        for p in sub_pictures:
            for match in _pattern.finditer(p):
                if percent_sign in p or per_mille_sign in p:
                    raise jexception.JException('D3092', -1)
                elif any(c not in digits_family for c in p[match.span()[1] - 1:]):
                    # detailed check to consider suffix
                    has_suffix = False
                    for ch in p[match.span()[1] - 1:]:
                        if ch in digits_family:
                            if has_suffix:
                                raise jexception.JException('D3093', -1)
                        elif ch in active_characters:
                            raise jexception.JException('D3086', -1)
                        else:
                            has_suffix = True

                exponent_pattern = _pattern

        if value is None:
            return None
        elif math.isnan(value):
            return decimal_format.get('NaN', 'NaN')
        elif isinstance(value, float):
            value = decimal.Decimal.from_float(value)
        elif not isinstance(value, decimal.Decimal):
            value = decimal.Decimal(value)

        minus_sign = decimal_format.get('minus-sign', '-')

        prefix = ''
        if value >= 0:
            subpic = sub_pictures[0]
        else:
            subpic = sub_pictures[-1]
            if len(sub_pictures) == 1:
                prefix = minus_sign

        for k, ch in enumerate(subpic):
            if ch in active_characters:
                prefix += subpic[:k]
                subpic = subpic[k:]
                break
        else:
            prefix += subpic
            subpic = ''

        if not subpic:
            suffix = ''
        elif subpic.endswith(percent_sign):
            suffix = percent_sign
            subpic = subpic[:-len(percent_sign)]

            if value.as_tuple().exponent < 0:
                value *= 100
            else:
                value = decimal.Decimal(int(value) * 100)

        elif subpic.endswith(per_mille_sign):
            suffix = per_mille_sign
            subpic = subpic[:-len(per_mille_sign)]

            if value.as_tuple().exponent < 0:
                value *= 1000
            else:
                value = decimal.Decimal(int(value) * 1000)

        else:
            for k, ch in enumerate(reversed(subpic)):
                if ch in active_characters:
                    idx = len(subpic) - k
                    suffix = subpic[idx:]
                    subpic = subpic[:idx]
                    break
            else:
                suffix = subpic
                subpic = ''

        exp_fmt = None
        if exponent_pattern is not None:
            exp_match = exponent_pattern.search(subpic)
            if exp_match is not None:
                exp_fmt = subpic[exp_match.span()[0] + 1:]
                subpic = subpic[:exp_match.span()[0]]

        fmt_tokens = subpic.split(decimal_separator)
        if all(not fmt for fmt in fmt_tokens):
            raise jexception.JException('both integer and fractional parts are empty', -1)

        if math.isinf(value):
            return prefix + decimal_format.get('infinity', '∞') + suffix

        # Calculate the exponent value if it's in the sub-picture
        exp_value = 0
        if exp_fmt and value:
            num_digits = 0
            for ch in fmt_tokens[0]:
                if ch in digits_family:
                    num_digits += 1

            if abs(value) > 1:
                v = abs(value)
                while v > 10 ** num_digits:
                    exp_value += 1
                    v /= 10

                # modify empty fractional part to store a digit
                if not num_digits:
                    if len(fmt_tokens) == 1:
                        fmt_tokens.append(zero_digit)
                    elif not fmt_tokens[-1]:
                        fmt_tokens[-1] = zero_digit

            elif len(fmt_tokens) > 1 and fmt_tokens[-1] and value >= 0:
                v = abs(value) * 10
                while v < 10 ** num_digits:
                    exp_value -= 1
                    v *= 10
            else:
                v = abs(value) * 10
                while v < 10:
                    exp_value -= 1
                    v *= 10

            if exp_value:
                value = value * decimal.Decimal(10) ** -exp_value

        # round the value by fractional part
        if len(fmt_tokens) == 1 or not fmt_tokens[-1]:
            exp = decimal.Decimal('1')
        else:
            k = -1
            for ch in fmt_tokens[-1]:
                if ch in digits_family or ch == optional_digit:
                    k += 1
            exp = decimal.Decimal('.' + '0' * k + '1')

        try:
            if value > 0:
                value = value.quantize(exp, rounding='ROUND_HALF_UP')
            else:
                value = value.quantize(exp, rounding='ROUND_HALF_DOWN')
        except decimal.InvalidOperation:
            pass  # number too large, don't round ...

        chunks = Functions.decimal_to_string(value).lstrip('-').split('.')
        kwargs = {
            'digits_family': digits_family,
            'optional_digit': optional_digit,
            'grouping_separator': grouping_separator,
        }
        result = Functions.format_digits(chunks[0], fmt_tokens[0], **kwargs)

        if len(fmt_tokens) > 1 and fmt_tokens[0]:
            has_decimal_digit = False
            for ch in fmt_tokens[0]:
                if ch in digits_family:
                    has_decimal_digit = True
                elif ch == optional_digit and has_decimal_digit:
                    raise jexception.JException('D3090', -1)

        if len(fmt_tokens) > 1 and fmt_tokens[-1]:
            has_optional_digit = False
            for ch in fmt_tokens[-1]:
                if ch == optional_digit:
                    has_optional_digit = True
                elif ch in digits_family and has_optional_digit:
                    raise jexception.JException('D3091', -1)

            if len(chunks) == 1:
                chunks.append(zero_digit)

            decimal_part = Functions.format_digits(chunks[1], fmt_tokens[-1], **kwargs)

            for ch in reversed(fmt_tokens[-1]):
                if ch == optional_digit:
                    if decimal_part and decimal_part[-1] == zero_digit:
                        decimal_part = decimal_part[:-1]
                else:
                    if not decimal_part:
                        decimal_part = zero_digit
                    break

            if decimal_part:
                result += decimal_separator + decimal_part

                if not fmt_tokens[0] and result.startswith(zero_digit):
                    result = result.lstrip(zero_digit)

        if exp_fmt:
            exp_digits = Functions.format_digits(str(abs(exp_value)), exp_fmt, **kwargs)
            if exp_value >= 0:
                result += f'{exponent_separator}{exp_digits}'
            else:
                result += f'{exponent_separator}-{exp_digits}'

        return prefix + result + suffix

    @staticmethod
    def decimal_to_string(value: decimal.Decimal) -> str:
        """
        Convert a Decimal value to a string representation
        that not includes exponent and with its decimals.
        """
        sign, digits, exponent = value.as_tuple()

        if not exponent:
            result = ''.join(str(x) for x in digits)
        elif exponent > 0:
            result = ''.join(str(x) for x in digits) + '0' * exponent
        else:
            result = ''.join(str(x) for x in digits[:exponent])
            if not result:
                result = '0'
            result += '.'
            if len(digits) >= -exponent:
                result += ''.join(str(x) for x in digits[exponent:])
            else:
                result += '0' * (-exponent - len(digits))
                result += ''.join(str(x) for x in digits)

        return '-' + result if sign else result

    @staticmethod
    def format_digits(digits: str,
                      fmt: str,
                      digits_family: str = '0123456789',
                      optional_digit: str = '#',
                      grouping_separator: str | None = None) -> str:
        result = []
        iter_num_digits = reversed(digits)
        num_digit = next(iter_num_digits)

        for fmt_char in reversed(fmt):
            if fmt_char in digits_family or fmt_char == optional_digit:
                if num_digit:
                    result.append(digits_family[ord(num_digit) - 48])
                    num_digit = next(iter_num_digits, '')
                elif fmt_char != optional_digit:
                    result.append(digits_family[0])
            elif not result or not result[-1] in digits_family and grouping_separator \
                    and result[-1] != grouping_separator:
                raise jexception.JException("invalid grouping in picture argument", -1)
            else:
                result.append(fmt_char)

        if num_digit:
            separator = ''
            _separator = {x for x in fmt if x not in digits_family and x != optional_digit}
            if len(_separator) != 1:
                repeat = None
            else:
                separator = _separator.pop()
                chunks = fmt.split(separator)

                if len(chunks[0]) > len(chunks[-1]):
                    repeat = None
                elif all(len(item) == len(chunks[-1]) for item in chunks[1:-1]):
                    repeat = len(chunks[-1]) + 1
                else:
                    repeat = None

            if repeat is None:
                while num_digit:
                    result.append(digits_family[ord(num_digit) - 48])
                    num_digit = next(iter_num_digits, '')
            else:
                while num_digit:
                    if ((len(result) + 1) % repeat) == 0:
                        result.append(separator)
                    result.append(digits_family[ord(num_digit) - 48])
                    num_digit = next(iter_num_digits, '')

        if grouping_separator:
            return ''.join(reversed(result)).lstrip(grouping_separator)
        while result and \
                unicodedata.category(result[-1]) not in ('Nd', 'Nl', 'No', 'Lu', 'Ll', 'Lt', 'Lm', 'Lo'):
            result.pop()
        return ''.join(reversed(result))

    #
    # Converts a number to a string using a specified number base
    # @param {number} value - the number to convert
    # @param {number} [radix] - the number base; must be between 2 and 36. Defaults to 10
    # @returns {string} - the converted string
    #     
    @staticmethod
    def format_base(value: float | None, _radix: float | None) -> str | None:
        # undefined inputs always return undefined
        if value is None:
            return None

        value = Functions.round(value, 0)

        radix = 0
        if _radix is None:
            radix = 10
        else:
            radix = int(_radix)

        if radix < 2 or radix > 36:
            raise jexception.JException("D3100", radix)

        result = Functions.base_repr(int(value), radix).lower()

        return result

    @staticmethod
    def base_repr(number: int, base: int = 2, padding: int = 0) -> str:
        """
        Return a string representation of a number in the given base system.

        Parameters
        ----------
        number : int
            The value to convert. Positive and negative values are handled.
        base : int, optional
            Convert `number` to the `base` number system. The valid range is 2-36,
            the default value is 2.
        padding : int, optional
            Number of zeros padded on the left. Default is 0 (no padding).

        Returns
        -------
        out : str
            String representation of `number` in `base` system.

        """
        digits = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        if base > len(digits):
            raise ValueError("Bases greater than 36 not handled in base_repr.")
        elif base < 2:
            raise ValueError("Bases less than 2 not handled in base_repr.")

        num = abs(number)
        res = []
        while num:
            res.append(digits[num % base])
            num //= base
        if padding:
            res.append('0' * padding)
        if number < 0:
            res.append('-')
        return ''.join(reversed(res or '0'))

    #
    # Cast argument to number
    # @param {Object} arg - Argument
    # @throws NumberFormatException
    # @returns {Number} numeric value of argument
    #     
    @staticmethod
    def number(arg: Any | None) -> float | None:
        result = None

        # undefined inputs always return undefined
        if arg is None:
            return None

        if arg is utils.Utils.NULL_VALUE:
            raise jexception.JException("T0410", -1)

        if isinstance(arg, bool):
            result = 1 if (bool(arg)) else 0
        elif isinstance(arg, (int, float)):
            result = arg
        elif isinstance(arg, str):
            s = str(arg)
            if s.startswith("0x"):
                result = int(s[2:], 16)
            elif s.startswith("0B"):
                result = int(s[2:], 2)
            elif s.startswith("0O"):
                result = int(s[2:], 8)
            else:
                result = float(str(arg))
        return result

    #
    # Absolute value of a number
    # @param {Number} arg - Argument
    # @returns {Number} absolute value of argument
    #     
    @staticmethod
    def abs(arg: float | None) -> float | None:

        # undefined inputs always return undefined
        if arg is None:
            return None

        return abs(float(arg)) if isinstance(arg, float) else abs(int(arg))

    #
    # Rounds a number down to integer
    # @param {Number} arg - Argument
    # @returns {Number} rounded integer
    #     
    @staticmethod
    def floor(arg: float | None) -> float | None:

        # undefined inputs always return undefined
        if arg is None:
            return None

        return math.floor(float(arg))

    #
    # Rounds a number up to integer
    # @param {Number} arg - Argument
    # @returns {Number} rounded integer
    #     
    @staticmethod
    def ceil(arg: float | None) -> float | None:

        # undefined inputs always return undefined
        if arg is None:
            return None

        return math.ceil(float(arg))

    #
    # Round to half even
    # @param {Number} arg - Argument
    # @param {Number} [precision] - number of decimal places
    # @returns {Number} rounded integer
    #     
    @staticmethod
    def round(arg: float | None, precision: float | None) -> float | None:

        # undefined inputs always return undefined
        if arg is None:
            return None

        d = decimal.Decimal(str(arg))
        return float(round(d, precision))

    #
    # Square root of number
    # @param {Number} arg - Argument
    # @returns {Number} square root
    #     
    @staticmethod
    def sqrt(arg: float | None) -> float | None:

        # undefined inputs always return undefined
        if arg is None:
            return None

        if float(arg) < 0:
            raise jexception.JException("D3060", 1, arg)

        return math.sqrt(float(arg))

    #
    # Raises number to the power of the second number
    # @param {Number} arg - the base
    # @param {Number} exp - the exponent
    # @returns {Number} rounded integer
    #     
    @staticmethod
    def power(arg: float | None, exp: float | None) -> float | None:

        # undefined inputs always return undefined
        if arg is None:
            return None

        result = float(arg) ** float(exp)

        if not math.isfinite(result):
            raise jexception.JException("D3061", 1, arg, exp)

        return result

    #
    # Returns a random number 0 <= n < 1
    # @returns {number} random number
    #     
    @staticmethod
    def random() -> float:
        return random.random()

    #
    # Evaluate an input and return a boolean
    # @param {*} arg - Arguments
    # @returns {boolean} Boolean
    #     
    @staticmethod
    def to_boolean(arg: Any | None) -> bool | None:
        from jsonata import jsonata
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
            return None  # Uli: Null would need to be handled as false anyway

        result = False
        if isinstance(arg, list):
            el = arg
            if len(el) == 1:
                result = Functions.to_boolean(el[0])
            elif len(el) > 1:
                trues_length = len(list(filter(lambda e: jsonata.Jsonata.boolize(e), el)))
                result = trues_length > 0
        elif isinstance(arg, str):
            s = str(arg)
            if len(s) > 0:
                result = True
        elif isinstance(arg, bool):
            result = bool(arg)
        elif isinstance(arg, (int, float)):
            if float(arg) != 0:
                result = True
        elif isinstance(arg, dict):
            if len(arg) > 0:
                result = True
        return result

    #
    # returns the Boolean NOT of the arg
    # @param {*} arg - argument
    # @returns {boolean} - NOT arg
    #     
    @staticmethod
    def not_(arg: Any | None) -> bool | None:
        # undefined inputs always return undefined
        if arg is None:
            return None

        return not Functions.to_boolean(arg)

    @staticmethod
    def get_function_arity(func: Any | None) -> int:
        from jsonata import jsonata
        if isinstance(func, jsonata.Jsonata.JFunction):
            return func.signature.get_min_number_of_args()
        else:
            # Lambda
            return len(func.arguments)

    #
    # Helper function to build the arguments to be supplied to the function arg of the
    # HOFs map, filter, each, sift and single
    # @param {function} func - the function to be invoked
    # @param {*} arg1 - the first (required) arg - the value
    # @param {*} arg2 - the second (optional) arg - the position (index or key)
    # @param {*} arg3 - the third (optional) arg - the whole structure (array or object)
    # @returns {*[]} the argument list
    #     
    @staticmethod
    def hof_func_args(func: Any | None, arg1: Any | None, arg2: Any | None, arg3: Any | None) -> list:
        func_args = [arg1]
        # the other two are optional - only supply it if the function can take it
        length = Functions.get_function_arity(func)
        if length >= 2:
            func_args.append(arg2)
        if length >= 3:
            func_args.append(arg3)
        return func_args

    #
    # Call helper for Java
    # 
    # @param func
    # @param funcArgs
    # @return
    # @throws Throwable
    #     
    @staticmethod
    def func_apply(func: Any | None, func_args: Sequence | None) -> Any | None:
        from jsonata import jsonata
        res = None
        if Functions.is_lambda(func):
            res = jsonata.Jsonata.CURRENT.jsonata.apply(func, func_args, None,
                                                        jsonata.Jsonata.CURRENT.jsonata.environment)
        else:
            res = func.call(None, func_args)
        return res

    #
    # Create a map from an array of arguments
    # @param {Array} [arr] - array to map over
    # @param {Function} func - function to apply
    # @returns {Array} Map array
    #     
    @staticmethod
    def map(arr: Sequence | None, func: Any | None) -> list | None:

        # undefined inputs always return undefined
        if arr is None:
            return None

        result = utils.Utils.create_sequence()
        # do the map - iterate over the arrays, and invoke func
        for i, arg in enumerate(arr):
            func_args = Functions.hof_func_args(func, arg, i, arr)

            res = Functions.func_apply(func, func_args)
            if res is not None:
                result.append(res)
        return result

    #
    # Create a map from an array of arguments
    # @param {Array} [arr] - array to filter
    # @param {Function} func - predicate function
    # @returns {Array} Map array
    #     
    @staticmethod
    def filter(arr: Sequence | None, func: Any | None) -> list | None:
        # undefined inputs always return undefined
        if arr is None:
            return None

        result = utils.Utils.create_sequence()

        for i, entry in enumerate(arr):
            func_args = Functions.hof_func_args(func, entry, i, arr)
            # invoke func
            res = Functions.func_apply(func, func_args)
            if Functions.to_boolean(res):
                result.append(entry)

        return result

    #
    # Given an array, find the single element matching a specified condition
    # Throws an exception if the number of matching elements is not exactly one
    # @param {Array} [arr] - array to filter
    # @param {Function} [func] - predicate function
    # @returns {*} Matching element
    #     
    @staticmethod
    def single(arr: Sequence | None, func: Any | None) -> Any | None:
        # undefined inputs always return undefined
        if arr is None:
            return None

        has_found_match = False
        result = None

        for i, entry in enumerate(arr):
            positive_result = True
            if func is not None:
                func_args = Functions.hof_func_args(func, entry, i, arr)
                # invoke func
                res = Functions.func_apply(func, func_args)
                positive_result = Functions.to_boolean(res)
            if positive_result:
                if not has_found_match:
                    result = entry
                    has_found_match = True
                else:
                    raise jexception.JException("D3138", i)

        if not has_found_match:
            raise jexception.JException("D3139", -1)

        return result

    #
    # Convolves (zips) each value from a set of arrays
    # @param {Array} [args] - arrays to zip
    # @returns {Array} Zipped array
    #     
    @staticmethod
    def zip(*args: Sequence) -> list:
        result = []
        # length of the shortest array
        length = sys.maxsize
        nargs = 0
        # nargs : the real size of args!=null
        while nargs < len(args):
            if args[nargs] is None:
                length = 0
                break

            length = min(length, len(args[nargs]))
            nargs += 1

        for i in range(0, length):
            tuple = []
            for k in range(0, nargs):
                tuple.append(args[k][i])
            result.append(tuple)
        return result

    #
    # Fold left function
    # @param {Array} sequence - Sequence
    # @param {Function} func - Function
    # @param {Object} init - Initial value
    # @returns {*} Result
    #     
    @staticmethod
    def fold_left(sequence: Sequence | None, func: Any | None, init: Any | None) -> Any | None:
        # undefined inputs always return undefined
        if sequence is None:
            return None
        result = None

        arity = Functions.get_function_arity(func)
        if arity < 2:
            raise jexception.JException("D3050", 1)

        index = 0
        if init is None and len(sequence) > 0:
            result = sequence[0]
            index = 1
        else:
            result = init
            index = 0

        while index < len(sequence):
            args = [result, sequence[index]]
            if arity >= 3:
                args.append(index)
            if arity >= 4:
                args.append(sequence)
            result = Functions.func_apply(func, args)
            index += 1

        return result

    #
    # Return keys for an object
    # @param {Object} arg - Object
    # @returns {Array} Array of keys
    #     
    @staticmethod
    def keys(arg: Sequence | Mapping | None) -> list:
        result = utils.Utils.create_sequence()

        if isinstance(arg, list):
            # merge the keys of all of the items in the array
            keys = {}
            for el in arg:
                keys.update({k: '' for k in Functions.keys(el)})
            result.extend(keys.keys())
        elif isinstance(arg, dict):
            result.extend(arg.keys())
        return result

    # here: append, lookup

    #
    # Determines if the argument is undefined
    # @param {*} arg - argument
    # @returns {boolean} False if argument undefined, otherwise true
    #     
    @staticmethod
    def exists(arg: Any | None) -> bool:
        if arg is None:
            return False
        else:
            return True

    #
    # Splits an object into an array of object with one property each
    # @param {*} arg - the object to split
    # @returns {*} - the array
    #     
    @staticmethod
    def spread(arg: Any | None) -> Any | None:
        result = utils.Utils.create_sequence()

        if isinstance(arg, list):
            # spread all of the items in the array
            for item in arg:
                result = Functions.append(result, Functions.spread(item))
        elif isinstance(arg, dict):
            for k, v in arg.items():
                obj = {k: v}
                result.append(obj)
        else:
            return arg  # result = arg;
        return result

    #
    # Merges an array of objects into a single object.  Duplicate properties are
    # overridden by entries later in the array
    # @param {*} arg - the objects to merge
    # @returns {*} - the object
    #     
    @staticmethod
    def merge(arg: Sequence | None) -> dict | None:
        # undefined inputs always return undefined
        if arg is None:
            return None

        result = {}

        for obj in arg:
            for k, v in obj.items():
                result[k] = v
        return result

    #
    # Reverses the order of items in an array
    # @param {Array} arr - the array to reverse
    # @returns {Array} - the reversed array
    #     
    @staticmethod
    def reverse(arr: Sequence | None) -> Sequence | None:
        # undefined inputs always return undefined
        if arr is None:
            return None

        if len(arr) <= 1:
            return arr

        result = list(arr)
        result.reverse()
        return result

    #
    #
    # @param {*} obj - the input object to iterate over
    # @param {*} func - the function to apply to each key/value pair
    # @throws Throwable
    # @returns {Array} - the resultant array
    #     
    @staticmethod
    def each(obj: Mapping | None, func: Any | None) -> list | None:
        if obj is None:
            return None

        result = utils.Utils.create_sequence()

        for key in obj:
            func_args = Functions.hof_func_args(func, obj[key], key, obj)
            # invoke func
            val = Functions.func_apply(func, func_args)
            if val is not None:
                result.append(val)

        return result

    #
    #
    # @param {string} [message] - the message to attach to the error
    # @throws custom error with code 'D3137'
    #     
    @staticmethod
    def error(message: str | None) -> NoReturn:
        raise jexception.JException("D3137", -1, message if message is not None else "$error() function evaluated")

    #
    #
    # @param {boolean} condition - the condition to evaluate
    # @param {string} [message] - the message to attach to the error
    # @throws custom error with code 'D3137'
    # @returns {undefined}
    #     
    @staticmethod
    def assert_fn(condition: bool | None, message: str | None) -> None:
        if condition is utils.Utils.NULL_VALUE:
            raise jexception.JException("T0410", -1)

        if not condition:
            raise jexception.JException("D3141", -1, "$assert() statement failed")
            #                message: message || "$assert() statement failed"

    #
    #
    # @param {*} [value] - the input to which the type will be checked
    # @returns {string} - the type of the input
    #     
    @staticmethod
    def type(value: Any | None) -> str | None:
        if value is None:
            return None

        if value is utils.Utils.NULL_VALUE:
            return "null"

        if isinstance(value, bool):
            return "boolean"

        if isinstance(value, (int, float)):
            return "number"

        if isinstance(value, str):
            return "string"

        if isinstance(value, list):
            return "array"

        if utils.Utils.is_function(value) or Functions.is_lambda(value):
            return "function"

        return "object"

    #
    # Implements the merge sort (stable) with optional comparator function
    #
    # @param {Array} arr - the array to sort
    # @param {*} comparator - comparator function
    # @returns {Array} - sorted array
    #     
    @staticmethod
    def sort(arr: Sequence | None, comparator: Any | None) -> Sequence | None:
        # undefined inputs always return undefined
        if arr is None:
            return None

        if len(arr) <= 1:
            return arr

        result = list(arr)

        if comparator is not None:
            comp = Functions.Comparator(comparator).compare
            result = sorted(result, key=functools.cmp_to_key(comp))
        else:
            result = sorted(result)

        return result

    class Comparator:
        _comparator: Any | None

        def __init__(self, comparator):
            from jsonata import jsonata
            if isinstance(comparator, Callable):
                self._comparator = jsonata.Jsonata.JLambda(comparator)
            else:
                self._comparator = comparator

        def compare(self, o1, o2):
            res = Functions.func_apply(self._comparator, [o1, o2])
            if isinstance(res, bool):
                return 1 if res else -1
            return int(res)

    #
    # Randomly shuffles the contents of an array
    # @param {Array} arr - the input array
    # @returns {Array} the shuffled array
    #     
    @staticmethod
    def shuffle(arr: Sequence | None) -> Sequence | None:
        # undefined inputs always return undefined
        if arr is None:
            return None

        if len(arr) <= 1:
            return arr

        result = list(arr)
        random.shuffle(result)
        return result

    #
    # Returns the values that appear in a sequence, with duplicates eliminated.
    # @param {Array} arr - An array or sequence of values
    # @returns {Array} - sequence of distinct values
    #     
    @staticmethod
    def distinct(_arr: Any | None) -> Any | None:
        # undefined inputs always return undefined
        if _arr is None:
            return None

        if not (isinstance(_arr, list)) or len(_arr) <= 1:
            return _arr
        arr = _arr

        results = utils.Utils.create_sequence() if (isinstance(arr, utils.Utils.JList)) else []

        for el in arr:
            if el not in results:
                results.append(el)

        return results

    #
    # Applies a predicate function to each key/value pair in an object, and returns an object containing
    # only the key/value pairs that passed the predicate
    #
    # @param {object} arg - the object to be sifted
    # @param {object} func - the predicate function (lambda or native)
    # @throws Throwable
    # @returns {object} - sifted object
    #     
    @staticmethod
    def sift(arg: Mapping | None, func: Any | None) -> dict | None:
        from jsonata import jsonata
        if arg is None:
            return None

        result = {}

        for item, entry in arg.items():
            func_args = Functions.hof_func_args(func, entry, item, arg)
            # invoke func
            res = Functions.func_apply(func, func_args)
            if jsonata.Jsonata.boolize(res):
                result[item] = entry

        # empty objects should be changed to undefined
        if len(result) == 0:
            result = None

        return result

    # /////
    # /////
    # /////
    # /////

    #
    # Append second argument to first
    # @param {Array|Object} arg1 - First argument
    # @param {Array|Object} arg2 - Second argument
    # @returns {*} Appended arguments
    #     
    @staticmethod
    def append(arg1: Any | None, arg2: Any | None) -> Any | None:
        # disregard undefined args
        if arg1 is None:
            return arg2
        if arg2 is None:
            return arg1

        # if either argument is not an array, make it so
        if not (isinstance(arg1, list)):
            arg1 = utils.Utils.create_sequence(arg1)
        if not (isinstance(arg2, list)):
            arg2 = utils.Utils.JList([arg2])
        # else
        #     // Arg2 was a list: add it as a list element (don't flatten)
        #     ((List)arg1).add((List)arg2)

        arg1 = utils.Utils.JList(arg1)  # create a new copy!
        if isinstance(arg2, utils.Utils.JList) and arg2.cons:
            arg1.append(arg2)
        else:
            arg1.extend(arg2)
        return arg1

    @staticmethod
    def is_lambda(result: Any | None) -> bool:
        return isinstance(result, parser.Parser.Symbol) and result._jsonata_lambda

    #
    # Return value from an object for a given key
    # @param {Object} input - Object/Array
    # @param {String} key - Key in object
    # @returns {*} Value of key in object
    #     
    @staticmethod
    def lookup(input: Mapping | Sequence | None, key: str | None) -> Any | None:
        # lookup the 'name' item in the input
        result = None
        if isinstance(input, list):
            _input = input
            result = utils.Utils.create_sequence()
            for _, inp in enumerate(_input):
                res = Functions.lookup(inp, key)
                if res is not None:
                    if isinstance(res, list):
                        result.extend(res)
                    else:
                        result.append(res)
        elif isinstance(input, dict):
            result = input.get(key)
            # Detect the case where the value is null:
            if result is None and key in input:
                result = utils.Utils.NULL_VALUE
        return result

    @staticmethod
    def test(a: str | None, b: str | None) -> str:
        return a + b

    @staticmethod
    def get_function(clz: Type | None, name: str | None) -> Any | None:
        if name is None:
            return None
        return getattr(clz, name)

    @staticmethod
    def call(clz: Type | None, name: str | None, args: Sequence | None) -> Any | None:
        return Functions._call(Functions.get_function(clz, name), args)

    @staticmethod
    def _call(m: Callable, args: Sequence | None) -> Any | None:
        nargs = len(inspect.signature(m).parameters)

        call_args = list(args)
        while len(call_args) < nargs:
            # Add default arg null if not enough args were provided
            call_args.append(None)

        res = m(*call_args)
        if utils.Utils.is_numeric(res):
            res = utils.Utils.convert_number(res)
        return res

    #
    # DateTime
    #

    #
    # Converts an ISO 8601 timestamp to milliseconds since the epoch
    #
    # @param {string} timestamp - the timestamp to be converted
    # @param {string} [picture] - the picture string defining the format of the timestamp (defaults to ISO 8601)
    # @throws ParseException 
    # @returns {Number} - milliseconds since the epoch
    #     
    @staticmethod
    def datetime_to_millis(timestamp: str | None, picture: str | None) -> int | None:
        # undefined inputs always return undefined
        if timestamp is None:
            return None

        if picture is None:
            if Functions.is_numeric(timestamp):
                dt = datetime.datetime.strptime(timestamp, "%Y")
            else:
                dt = datetime.datetime.fromisoformat(timestamp)
            dt = dt.replace(tzinfo=datetime.timezone.utc)
            return int(dt.timestamp() * 1000)
            # try:
            #     size = len(timestamp)
            #     if size > 5:
            #         if timestamp[size - 5] == '+' or timestamp[size - 5] == '-':
            #             if (timestamp[size - 4]).isdigit() and (timestamp[size - 3]).isdigit() and (
            #             timestamp[size - 2]).isdigit() and (timestamp[size - 1]).isdigit():
            #                 timestamp = timestamp[0:size - 2] + ':' + timestamp[size - 2:size]
            #     return java.time.OffsetDateTime.parse(timestamp).toInstant().toEpochMilli()
            # except RuntimeError as e:
            #     ldt = java.time.LocalDate.parse(timestamp, java.time.format.DateTimeFormatter.ofPattern("yyyy-MM-dd"))
            #     return ldt.atStartOfDay().atZone(java.time.ZoneId.of("UTC")).toInstant().toEpochMilli()
        else:
            return datetimeutils.DateTimeUtils.parse_datetime(timestamp, picture)

    # Adapted from: org.apache.commons.lang3.StringUtils
    @staticmethod
    def is_numeric(cs: Sequence | None) -> bool:
        if cs is None or len(cs) == 0:
            return False
        sz = len(cs)
        for i in range(0, sz):
            if not cs[i].isdigit():
                return False
        return True

    #
    # Converts milliseconds since the epoch to an ISO 8601 timestamp
    # @param {Number} millis - milliseconds since the epoch to be converted
    # @param {string} [picture] - the picture string defining the format of the timestamp (defaults to ISO 8601)
    # @param {string} [timezone] - the timezone to format the timestamp in (defaults to UTC)
    # @returns {String} - the formatted timestamp
    #     
    @staticmethod
    def datetime_from_millis(millis: float | None, picture: str | None, timezone: str | None) -> str | None:
        # undefined inputs always return undefined
        if millis is None:
            return None

        return datetimeutils.DateTimeUtils.format_datetime(int(millis), picture, timezone)

    #
    # Formats an integer as specified by the XPath fn:format-integer function
    # See https://www.w3.org/TR/xpath-functions-31/#func-format-integer
    # @param {number} value - the number to be formatted
    # @param {string} picture - the picture string that specifies the format
    # @returns {string} - the formatted number
    #     
    @staticmethod
    def format_integer(value: float | None, picture: str | None) -> str | None:
        if value is None:
            return None
        return datetimeutils.DateTimeUtils.format_integer(int(value), picture)

    #
    # parse a string containing an integer as specified by the picture string
    # @param {string} value - the string to parse
    # @param {string} picture - the picture string
    # @throws ParseException
    # @returns {number} - the parsed number
    #     
    @staticmethod
    def parse_integer(value: str | None, picture: str | None) -> int | None:
        if value is None:
            return None
        return datetimeutils.DateTimeUtils.parse_integer(value, picture)

    #
    # Clones an object
    # @param {Object} arg - object to clone (deep copy)
    # @returns {*} - the cloned object
    #     
    @staticmethod
    def function_clone(arg: Any | None) -> Any | None:
        # undefined inputs always return undefined
        if arg is None:
            return None

        res = json.loads(Functions.string(arg, False))
        return res

    #
    # parses and evaluates the supplied expression
    # @param {string} expr - expression to evaluate
    # @returns {*} - result of evaluating the expression
    #     
    @staticmethod
    def function_eval(expr: str | None, focus: Any | None) -> Any | None:
        from jsonata import jsonata
        # undefined inputs always return undefined
        if expr is None:
            return None
        input = jsonata.Jsonata.CURRENT.jsonata.input  # =  this.input;
        if focus is not None:
            input = focus
            # if the input is a JSON array, then wrap it in a singleton sequence so it gets treated as a single input
            if (isinstance(input, list)) and not utils.Utils.is_sequence(input):
                input = utils.Utils.create_sequence(input)
                input.outer_wrapper = True

        ast = None
        try:
            ast = jsonata.Jsonata(expr)
        except Exception as err:
            # error parsing the expression passed to $eval
            # populateMessage(err)
            raise jexception.JException("D3120", -1)
        result = None
        try:
            result = ast.evaluate(input, jsonata.Jsonata.CURRENT.jsonata.environment)
        except Exception as err:
            # error evaluating the expression passed to $eval
            # populateMessage(err)
            raise jexception.JException("D3121", -1)

        return result

    #  environment.bind("now", defineFunction(function(picture, timezone) {
    #      return datetime.fromMillis(timestamp.getTime(), picture, timezone)
    #  }, "<s?s?:s>"))
    @staticmethod
    def now(picture: str | None, timezone: str | None) -> str | None:
        from jsonata import jsonata
        t = jsonata.Jsonata.CURRENT.jsonata.timestamp
        return Functions.datetime_from_millis(t, picture, timezone)

    #  environment.bind("millis", defineFunction(function() {
    #      return timestamp.getTime()
    #  }, "<:n>"))
    @staticmethod
    def millis() -> int:
        from jsonata import jsonata
        t = jsonata.Jsonata.CURRENT.jsonata.timestamp
        return t
