import datetime
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

# Derived from original JSONata4Java DateTimeUtils code under this license:
#
# * (c) Copyright 2018, 2019 IBM Corporation
# * 1 New Orchard Road, 
# * Armonk, New York, 10504-1722
# * United States
# * +1 914 499 1900
# * support: Nathaniel Mills wnm3@us.ibm.com
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
# *
# 
#package com.api.jsonata4java.expressions.utils

# import org.apache.commons.lang3.ArrayUtils
# import org.apache.commons.lang3.StringUtils
# import org.apache.commons.lang3.tuple.ImmutablePair
# import org.apache.commons.lang3.tuple.Pair

from com.dashjoin.jsonata import Functions

class DateTimeUtils:

    SERIAL_VERSION_UID = 365963860104380193

    _few = ["Zero", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen"]
    _ordinals = ["Zeroth", "First", "Second", "Third", "Fourth", "Fifth", "Sixth", "Seventh", "Eighth", "Ninth", "Tenth", "Eleventh", "Twelfth", "Thirteenth", "Fourteenth", "Fifteenth", "Sixteenth", "Seventeenth", "Eighteenth", "Nineteenth"]
    _decades = ["Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety", "Hundred"]
    _magnitudes = ["Thousand", "Million", "Billion", "Trillion"]

    @staticmethod
    def numberToWords(value, ordinal):
        return com.dashjoin.jsonata.utils.DateTimeUtils._lookup(value, False, ordinal)

    @staticmethod
    def _lookup(num, prev, ord):
        words = ""
        if num <= 19:
            words = (" and " if prev else "") + (com.dashjoin.jsonata.utils.DateTimeUtils._ordinals[int(num)] if ord else com.dashjoin.jsonata.utils.DateTimeUtils._few[int(num)])
        elif num < 100:
            tens = math.trunc(int(num) / float(10))
            remainder = int(math.fmod(int(num), 10))
            words = (" and " if prev else "") + com.dashjoin.jsonata.utils.DateTimeUtils._decades[tens - 2]
            if remainder > 0:
                words += "-" + com.dashjoin.jsonata.utils.DateTimeUtils._lookup(remainder, False, ord)
            elif ord:
                words = words[0:len(words) - 1] + "ieth"
        elif num < 1000:
            hundreds = math.trunc(int(num) / float(100))
            remainder = int(math.fmod(int(num), 100))
            words = (", " if prev else "") + com.dashjoin.jsonata.utils.DateTimeUtils._few[hundreds] + " Hundred"
            if remainder > 0:
                words += com.dashjoin.jsonata.utils.DateTimeUtils._lookup(remainder, True, ord)
            elif ord:
                words += "th"
        else:
# JAVA TO PYTHON CONVERTER TASK: Java to Python Converter cannot determine whether both operands of this division are integer types - if they are then you should change 'lhs / rhs' to 'math.trunc(lhs / float(rhs))':
            mag = int(math.floor(math.log10(num) / 3))
            if mag > len(com.dashjoin.jsonata.utils.DateTimeUtils._magnitudes):
                mag = len(com.dashjoin.jsonata.utils.DateTimeUtils._magnitudes) # the largest word
            factor = int(10 ** mag * 3)
            mant = int(math.floor(math.trunc(num / float(factor))))
            remainder = num - mant * factor
            words = (", " if prev else "") + com.dashjoin.jsonata.utils.DateTimeUtils._lookup(mant, False, False) + " " + com.dashjoin.jsonata.utils.DateTimeUtils._magnitudes[mag - 1]
            if remainder > 0:
                words += com.dashjoin.jsonata.utils.DateTimeUtils._lookup(remainder, True, ord)
            elif ord:
                words += "th"
        return words

    _wordValues = {}
    @staticmethod
    def _static_initializer():
        i = 0
        while i < len(com.dashjoin.jsonata.utils.DateTimeUtils._few):
            com.dashjoin.jsonata.utils.DateTimeUtils._wordValues[com.dashjoin.jsonata.utils.DateTimeUtils._few[i].casefold()] = i
            i += 1
        i = 0
        while i < len(com.dashjoin.jsonata.utils.DateTimeUtils._ordinals):
            com.dashjoin.jsonata.utils.DateTimeUtils._wordValues[com.dashjoin.jsonata.utils.DateTimeUtils._ordinals[i].casefold()] = i
            i += 1
        i = 0
        while i < len(com.dashjoin.jsonata.utils.DateTimeUtils._decades):
            lword = com.dashjoin.jsonata.utils.DateTimeUtils._decades[i].casefold()
            com.dashjoin.jsonata.utils.DateTimeUtils._wordValues[lword] = (i + 2) * 10
            com.dashjoin.jsonata.utils.DateTimeUtils._wordValues[lword[0:len(lword) - 1] + "ieth"] = com.dashjoin.jsonata.utils.DateTimeUtils._wordValues[lword]
            i += 1
        com.dashjoin.jsonata.utils.DateTimeUtils._wordValues["hundreth"] = 100
        i = 0
        while i < len(com.dashjoin.jsonata.utils.DateTimeUtils._magnitudes):
            lword = com.dashjoin.jsonata.utils.DateTimeUtils._magnitudes[i].casefold()
            val = int(10 ** (i + 1) * 3)
            com.dashjoin.jsonata.utils.DateTimeUtils._wordValues[lword] = val
            com.dashjoin.jsonata.utils.DateTimeUtils._wordValues[lword + "th"] = val
            i += 1
        i = 0
        while i < len(com.dashjoin.jsonata.utils.DateTimeUtils._few):
            com.dashjoin.jsonata.utils.DateTimeUtils._wordValuesLong[com.dashjoin.jsonata.utils.DateTimeUtils._few[i].casefold()] = int(i)
            i += 1
        i = 0
        while i < len(com.dashjoin.jsonata.utils.DateTimeUtils._ordinals):
            com.dashjoin.jsonata.utils.DateTimeUtils._wordValuesLong[com.dashjoin.jsonata.utils.DateTimeUtils._ordinals[i].casefold()] = int(i)
            i += 1
        i = 0
        while i < len(com.dashjoin.jsonata.utils.DateTimeUtils._decades):
            lword = com.dashjoin.jsonata.utils.DateTimeUtils._decades[i].casefold()
            com.dashjoin.jsonata.utils.DateTimeUtils._wordValuesLong[lword] = int((i + 2)) * 10
            com.dashjoin.jsonata.utils.DateTimeUtils._wordValuesLong[lword[0:len(lword) - 1] + "ieth"] = com.dashjoin.jsonata.utils.DateTimeUtils._wordValuesLong[lword]
            i += 1
        com.dashjoin.jsonata.utils.DateTimeUtils._wordValuesLong["hundredth"] = int(100)
        com.dashjoin.jsonata.utils.DateTimeUtils._wordValuesLong["hundreth"] = int(100)
        i = 0
        while i < len(com.dashjoin.jsonata.utils.DateTimeUtils._magnitudes):
            lword = com.dashjoin.jsonata.utils.DateTimeUtils._magnitudes[i].casefold()
            val = int(10 ** (i + 1) * 3)
            com.dashjoin.jsonata.utils.DateTimeUtils._wordValuesLong[lword] = val
            com.dashjoin.jsonata.utils.DateTimeUtils._wordValuesLong[lword + "th"] = val
            i += 1

    _static_initializer()

    _wordValuesLong = {}

    @staticmethod
    def wordsToNumber(text):
        parts = text.split(",\\s|\\sand\\s|[\\s\\-]")
        values = [0 for _ in range(len(parts))]
        i = 0
        while i < len(parts):
            values[i] = com.dashjoin.jsonata.utils.DateTimeUtils._wordValues[parts[i]]
            i += 1
        segs = java.util.Stack()
        segs.push(0)
        for value in values:
            if value < 100:
                top = segs.pop()
                if top >= 1000:
                    segs.push(top)
                    top = 0
                segs.push(top + value)
            else:
                segs.push(segs.pop() * value)
        return segs.stream().mapToInt(lambda i : i).sum()

    #    *
    #     * long version of above
    #     
    @staticmethod
    def wordsToLong(text):
        parts = text.split(",\\s|\\sand\\s|[\\s\\-]")
        values = [0 for _ in range(len(parts))]
        i = 0
        while i < len(parts):
            values[i] = com.dashjoin.jsonata.utils.DateTimeUtils._wordValuesLong[parts[i]]
            i += 1
        segs = java.util.Stack()
        segs.push(int(0))
        for value in values:
            if value < 100:
                top = segs.pop()
                if top >= 1000:
                    segs.push(top)
                    top = int(0)
                segs.push(top + value)
            else:
                segs.push(segs.pop() * value)
        return segs.stream().mapToLong(lambda i : i.longValue()).sum()

    class RomanNumeral:


        def __init__(self, value, letters):
            # instance fields found by Java to Python Converter:
            self._value = 0
            self._letters = None

            self._value = value
            self._letters = letters

        def getValue(self):
            return self._value

        def getLetters(self):
            return self._letters

    _romanNumerals = [RomanNumeral(1000, "m"), RomanNumeral(900, "cm"), RomanNumeral(500, "d"), RomanNumeral(400, "cd"), RomanNumeral(100, "c"), RomanNumeral(90, "xc"), RomanNumeral(50, "l"), RomanNumeral(40, "xl"), RomanNumeral(10, "x"), RomanNumeral(9, "ix"), RomanNumeral(5, "v"), RomanNumeral(4, "iv"), RomanNumeral(1, "i")]

    _romanValues = _createRomanValues()

    @staticmethod
    def _createRomanValues():
        values = {}
        values["M"] = 1000
        values["D"] = 500
        values["C"] = 100
        values["L"] = 50
        values["X"] = 10
        values["V"] = 5
        values["I"] = 1
        return values

    @staticmethod
    def _decimalToRoman(value):
        i = 0
        while i < len(com.dashjoin.jsonata.utils.DateTimeUtils._romanNumerals):
            numeral = com.dashjoin.jsonata.utils.DateTimeUtils._romanNumerals[i]
            if value >= numeral.getValue():
                return numeral.getLetters() + com.dashjoin.jsonata.utils.DateTimeUtils._decimalToRoman(value - numeral.getValue())
            i += 1
        return ""

    @staticmethod
    def romanToDecimal(roman):
        decimal = 0
        max = 1
        for i in range(len(roman) - 1, -1, -1):
            digit = roman[i]
            value = com.dashjoin.jsonata.utils.DateTimeUtils._romanValues[digit]
            if value < max:
                decimal -= value
            else:
                max = value
                decimal += value
        return decimal

    @staticmethod
    def _decimalToLetters(value, aChar):
        letters = []
        aCode = aChar[0]
        while value > 0:
            letters.insertElementAt(chr((int(math.fmod((value - 1), 26)) + aCode)), 0)
            value = math.trunc((value - 1) / float(26))
        return letters.stream().reduce("", lambda a, b : a + b)

    @staticmethod
# JAVA TO PYTHON CONVERTER TASK: Python does not allow method overloads:
    def formatInteger(value, picture):
        format = com.dashjoin.jsonata.utils.DateTimeUtils._analyseIntegerPicture(picture)
        return com.dashjoin.jsonata.utils.DateTimeUtils._formatInteger(value, format)

# JAVA TO PYTHON CONVERTER TASK: Complex Java enums are not converted by Java to Python Converter:
#    enum formats
    #    {
    #
    #            DECIMAL("decimal"),
    #            LETTERS("letters"),
    #            ROMAN("roman"),
    #            WORDS("words"),
    #            SEQUENCE("sequence")
    #
    #        public String value
    #
    #        private formats(String value)
    #        {
    #            this.value = value
    #        }
    #    }

# JAVA TO PYTHON CONVERTER TASK: Complex Java enums are not converted by Java to Python Converter:
#    enum tcase
    #    {
    #
    #            UPPER("upper"),
    #            LOWER("lower"),
    #            TITLE("title")
    #
    #        public String value
    #
    #        private tcase(String value)
    #        {
    #            this.value = value
    #        }
    #    }

    class Format:

        def __init__(self):
            # instance fields found by Java to Python Converter:
            self.type = "integer"
            self.primary = formats.DECIMAL
            self.case_type = tcase.LOWER
            self.ordinal = False
            self.zeroCode = 0
            self.mandatoryDigits = 0
            self.optionalDigits = 0
            self.regular = False
            self.groupingSeparators = []
            self.token = None



    class GroupingSeparator:


        def __init__(self, position, character):
            # instance fields found by Java to Python Converter:
            self.position = 0
            self.character = None

            self.position = position
            self.character = character

    _suffix123 = _createSuffixMap()

    @staticmethod
    def _createSuffixMap():
        suffix = {}
        suffix["1"] = "st"
        suffix["2"] = "nd"
        suffix["3"] = "rd"
        return suffix

    @staticmethod
# JAVA TO PYTHON CONVERTER TASK: Python does not allow method overloads:
    def _formatInteger(value, format):
        formattedInteger = ""
        negative = value < 0
        value = abs(value)
        match format.primary:
            case com.dashjoin.jsonata.utils.DateTimeUtils.formats.LETTERS:
                formattedInteger = com.dashjoin.jsonata.utils.DateTimeUtils._decimalToLetters(int(value),"A" if format.case_type == tcase.UPPER else "a")
            case com.dashjoin.jsonata.utils.DateTimeUtils.formats.ROMAN:
                formattedInteger = com.dashjoin.jsonata.utils.DateTimeUtils._decimalToRoman(int(value))
                if format.case_type == tcase.UPPER:
                    formattedInteger = formattedInteger.upper()
            case com.dashjoin.jsonata.utils.DateTimeUtils.formats.WORDS:
                formattedInteger = com.dashjoin.jsonata.utils.DateTimeUtils.numberToWords(value, format.ordinal)
                if format.case_type == tcase.UPPER:
                    formattedInteger = formattedInteger.upper()
                elif format.case_type == tcase.LOWER:
                    formattedInteger = formattedInteger.casefold()
            case com.dashjoin.jsonata.utils.DateTimeUtils.formats.DECIMAL:
                formattedInteger = "" + str(value)
                padLength = format.mandatoryDigits - len(formattedInteger)
                if padLength > 0:
                    formattedInteger = com.dashjoin.jsonata.Functions.leftPad(formattedInteger, format.mandatoryDigits, "0")
                if format.zeroCode != 0x30:
                    chars = formattedInteger.toCharArray()
                    i = 0
                    while i < len(chars):
                        chars[i] = chr((chars[i] + format.zeroCode - 0x30))
                        i += 1
                    formattedInteger = str(chars)
                if format.regular:
# JAVA TO PYTHON CONVERTER TASK: Java to Python Converter cannot determine whether both operands of this division are integer types - if they are then you should change 'lhs / rhs' to 'math.trunc(lhs / float(rhs))':
                    n = (len(formattedInteger) - 1) / format.groupingSeparators.elementAt(0).position
                    for i in range(n, 0, -1):
                        pos = len(formattedInteger) - i * format.groupingSeparators.elementAt(0).position
                        formattedInteger = formattedInteger[0:pos] + format.groupingSeparators.elementAt(0).character + formattedInteger[pos:]
                else:
                    format.groupingSeparators.reverse()
                    for separator in format.groupingSeparators:
                        pos = len(formattedInteger) - separator.position
                        formattedInteger = formattedInteger[0:pos] + separator.character + formattedInteger[pos:]

                if format.ordinal:
                    lastDigit = formattedInteger[len(formattedInteger) - 1:]
                    suffix = com.dashjoin.jsonata.utils.DateTimeUtils._suffix123[lastDigit]
                    if suffix is None or (len(formattedInteger) > 1 and formattedInteger[len(formattedInteger) - 2] == '1'):
                        suffix = "th"
                    formattedInteger += suffix
            case com.dashjoin.jsonata.utils.DateTimeUtils.formats.SEQUENCE:
                raise RuntimeException(String.format(Constants.ERR_MSG_SEQUENCE_UNSUPPORTED, format.token))
        if negative:
            formattedInteger = "-" + formattedInteger

        return formattedInteger

    _decimalGroups = [0x30, 0x0660, 0x06F0, 0x07C0, 0x0966, 0x09E6, 0x0A66, 0x0AE6, 0x0B66, 0x0BE6, 0x0C66, 0x0CE6, 0x0D66, 0x0DE6, 0x0E50, 0x0ED0, 0x0F20, 0x1040, 0x1090, 0x17E0, 0x1810, 0x1946, 0x19D0, 0x1A80, 0x1A90, 0x1B50, 0x1BB0, 0x1C40, 0x1C50, 0xA620, 0xA8D0, 0xA900, 0xA9D0, 0xA9F0, 0xAA50, 0xABF0, 0xFF10]

    @staticmethod
# JAVA TO PYTHON CONVERTER TASK: Java annotations have no direct Python equivalent:
# ORIGINAL LINE: @SuppressWarnings("unused") private static Format analyseIntegerPicture(String picture)
    def _analyseIntegerPicture(picture):
        format = Format()
        primaryFormat = None
        formatModifier = None
        semicolon = picture.rfind(";")
        if semicolon == -1:
            primaryFormat = picture
        else:
            primaryFormat = picture[0:semicolon]
            formatModifier = picture[semicolon + 1:]
            if formatModifier[0] == 'o':
                format.ordinal = True

        if primaryFormat == "A":
            format.case_type = tcase.UPPER
        if primaryFormat == "A" or primaryFormat == "a":
            format.primary = formats.LETTERS
        elif primaryFormat == "I":
            format.case_type = tcase.UPPER
        elif primaryFormat == "I" or primaryFormat == "i":
            format.primary = formats.ROMAN
        elif primaryFormat == "W":
            format.case_type = tcase.UPPER
            format.primary = formats.WORDS
        elif primaryFormat == "Ww":
            format.case_type = tcase.TITLE
            format.primary = formats.WORDS
        elif primaryFormat == "w":
            format.primary = formats.WORDS
        else:
                zeroCode = None
                mandatoryDigits = 0
                optionalDigits = 0
                groupingSeparators = []
                separatorPosition = 0
                formatCodepoints = primaryFormat.toCharArray()
                #ArrayUtils.reverse(formatCodepoints)
                for ix in range(len(formatCodepoints) - 1, -1, -1):
                    codePoint = formatCodepoints[ix]
                    digit = False
                    i = 0
                    while i < len(com.dashjoin.jsonata.utils.DateTimeUtils._decimalGroups):
                        group = com.dashjoin.jsonata.utils.DateTimeUtils._decimalGroups[i]
                        if codePoint >= chr(group) and codePoint <= chr(group + 9):
                            digit = True
                            mandatoryDigits += 1
                            separatorPosition += 1
                            if zeroCode is None:
                                zeroCode = group
                            elif group != zeroCode:
                                raise RuntimeException(Constants.ERR_MSG_DIFF_DECIMAL_GROUP)
                            break
                        i += 1
                    if not digit:
                        if codePoint == chr(0x23):
                            separatorPosition += 1
                            optionalDigits += 1
                        else:
                            groupingSeparators.append(GroupingSeparator(separatorPosition, codePoint))
                if mandatoryDigits > 0:
                    format.primary = formats.DECIMAL
                    format.zeroCode = zeroCode
                    format.mandatoryDigits = mandatoryDigits
                    format.optionalDigits = optionalDigits

                    regular = com.dashjoin.jsonata.utils.DateTimeUtils._getRegularRepeat(groupingSeparators)
                    if regular > 0:
                        format.regular = True
                        format.groupingSeparators.append(GroupingSeparator(regular, groupingSeparators.elementAt(0).character))
                    else:
                        format.regular = False
                        format.groupingSeparators = groupingSeparators
                else:
                    format.primary = formats.SEQUENCE
                    format.token = primaryFormat


        return format

    @staticmethod
    def _getRegularRepeat(separators):
        if len(separators) == 0:
            return 0

        sepChar = separators.elementAt(0).character
        for i in range(1, len(separators)):
            if separators.elementAt(i).character is not sepChar:
                return 0

        indexes = separators.stream().map(lambda seperator : seperator.position).collect(java.util.stream.Collectors.toList())
        factor = indexes.stream().reduce(lambda a, b : java.math.BigInteger.valueOf(a).gcd(java.math.BigInteger.valueOf(b)).intValue()).get()
        for index in range(1, len(indexes) + 1):
            if (indexes.index(index * factor) if index * factor in indexes else -1) == -1:
                return 0
        return factor

    _defaultPresentationModifiers = _createDefaultPresentationModifiers()

    @staticmethod
    def _createDefaultPresentationModifiers():
        map = {}
        map['Y'] = "1"
        map['M'] = "1"
        map['D'] = "1"
        map['d'] = "1"
        map['F'] = "n"
        map['W'] = "1"
        map['w'] = "1"
        map['X'] = "1"
        map['x'] = "1"
        map['H'] = "1"
        map['h'] = "1"
        map['P'] = "n"
        map['m'] = "01"
        map['s'] = "01"
        map['f'] = "1"
        map['Z'] = "01:01"
        map['z'] = "01:01"
        map['C'] = "n"
        map['E'] = "n"
        return map

    class PictureFormat:


        def __init__(self, type):
            # instance fields found by Java to Python Converter:
            self.type = None
            self.parts = []

            self.type = type

        def addLiteral(self, picture, start, end):
            if end > start:
                literal = picture[start:end]
                if literal == "]]":
                    # handle special case where picture ends with ]], split yields empty array
                    literal = "]"
                else:
                    literal = String.join("]", literal.split("]]"))
                self.parts.append(SpecPart("literal", literal))

    class Pair:
        def __init__(self, a, b):
            # instance fields found by Java to Python Converter:
            self._a = None
            self._b = None

            self._a = a
            self._b = b
        def getLeft(self):
            return self._a
        def getRight(self):
            return self._b

    class SpecPart:

        def _initialize_instance_fields(self):
            # instance fields found by Java to Python Converter:
            self.type = None
            self.value = None
            self.component = '\0'
            self.width = None
            self.presentation1 = None
            self.presentation2 = '\0'
            self.ordinal = False
            self.names = 0
            self.integerFormat = None
            self.n = 0



# JAVA TO PYTHON CONVERTER TASK: There is no Python equivalent to multiple constructors:
# ORIGINAL LINE: public SpecPart(String type, String value)
        def __init__(self, type, value):
            self._initialize_instance_fields()

            self.type = type
            self.value = value

# JAVA TO PYTHON CONVERTER TASK: There is no Python equivalent to multiple constructors:
# ORIGINAL LINE: public SpecPart(String type, char component)
        def __init__(self, type, component):
            self._initialize_instance_fields()

            self.type = type
            self.component = component

    @staticmethod
    def _analyseDateTimePicture(picture):
        format = PictureFormat("datetime")
        start = 0
        pos = 0
        while pos < len(picture):
            if picture[pos] == '[':
                #check it's not a doubled [[
                if picture[pos + 1] == '[':
                    #literal [
                    format.addLiteral(picture, start, pos)
                    format.parts.append(SpecPart("literal", "["))
                    pos += 2
                    start = pos
                    continue
                format.addLiteral(picture, start, pos)
                start = pos
                pos = picture.find("]", start)
                if pos == -1:
                    raise RuntimeException(Constants.ERR_MSG_NO_CLOSING_BRACKET)
                marker = picture[start + 1:pos]
                marker = String.join("", marker.split("\\s+"))
                def_ = SpecPart("marker", marker[0])
                comma = marker.rfind(",")
                presMod = None
                if comma != -1:
                    widthMod = marker[comma + 1:]
                    dash = widthMod.find("-")
                    min = None
                    max = None
                    if dash == -1:
                        min = widthMod
                    else:
                        min = widthMod[0:dash]
                        max = widthMod[dash + 1:]
                    def_.width = Pair(com.dashjoin.jsonata.utils.DateTimeUtils._parseWidth(min), com.dashjoin.jsonata.utils.DateTimeUtils._parseWidth(max))
                    presMod = marker[1:comma]
                else:
                    presMod = marker[1:]
                if len(presMod) == 1:
                    def_.presentation1 = presMod
                elif len(presMod) > 1:
                    lastChar = presMod[len(presMod) - 1]
                    if "atco".find(lastChar) != -1:
                        def_.presentation2 = lastChar
                        if lastChar == 'o':
                            def_.ordinal = True
                        def_.presentation1 = presMod[0:len(presMod) - 1]
                    else:
                        def_.presentation1 = presMod
                else:
                    def_.presentation1 = com.dashjoin.jsonata.utils.DateTimeUtils._defaultPresentationModifiers[def_.component]
                if def_.presentation1 is None:
                    raise RuntimeException(String.format(Constants.ERR_MSG_UNKNOWN_COMPONENT_SPECIFIER, def_.component))
                if def_.presentation1[0] == 'n':
                    def_.names = tcase.LOWER
                elif def_.presentation1[0] == 'N':
                    if len(def_.presentation1) > 1 and def_.presentation1[1] == 'n':
                        def_.names = tcase.TITLE
                    else:
                        def_.names = tcase.UPPER
                elif "YMDdFWwXxHhmsf".find(def_.component) != -1:
                    integerPattern = def_.presentation1
                    if def_.presentation2 is None:
                        integerPattern += ";" + def_.presentation2
                    def_.integerFormat = com.dashjoin.jsonata.utils.DateTimeUtils._analyseIntegerPicture(integerPattern)
                    def_.integerFormat.ordinal = def_.ordinal
                    if def_.width is not None and def_.width.getLeft() is not None:
                        if def_.integerFormat.mandatoryDigits < def_.width.getLeft():
                            def_.integerFormat.mandatoryDigits = def_.width.getLeft()
                    if def_.component == 'Y':
                        def_.n = -1
                        if def_.width is not None and def_.width.getRight() is not None:
                            def_.n = def_.width.getRight()
                            def_.integerFormat.mandatoryDigits = def_.n
                        else:
                            w = def_.integerFormat.mandatoryDigits + def_.integerFormat.optionalDigits
                            if w >= 2:
                                def_.n = w
                if def_.component == 'Z' or def_.component == 'z':
                    def_.integerFormat = com.dashjoin.jsonata.utils.DateTimeUtils._analyseIntegerPicture(def_.presentation1)
                    def_.integerFormat.ordinal = def_.ordinal
                format.parts.append(def_)
                start = pos + 1
            pos += 1
        format.addLiteral(picture, start, pos)
        return format

    @staticmethod
    def _parseWidth(wm):
        if wm is None or wm == "*":
            return None
        else:
            return int(wm)

    _days = ["", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    _months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

    _iso8601Spec = None

    @staticmethod
    def formatDateTime(millis, picture, timezone):
        offsetHours = 0
        offsetMinutes = 0

        if timezone is not None:
            offset = int(timezone)
            offsetHours = math.trunc(offset / float(100))
            offsetMinutes = int(math.fmod(offset, 100))
        formatSpec = None
        if picture is None:
            if com.dashjoin.jsonata.utils.DateTimeUtils._iso8601Spec is None:
                com.dashjoin.jsonata.utils.DateTimeUtils._iso8601Spec = com.dashjoin.jsonata.utils.DateTimeUtils._analyseDateTimePicture("[Y0001]-[M01]-[D01]T[H01]:[m01]:[s01].[f001][Z01:01t]")
            formatSpec = com.dashjoin.jsonata.utils.DateTimeUtils._iso8601Spec
        else:
            formatSpec = com.dashjoin.jsonata.utils.DateTimeUtils._analyseDateTimePicture(picture)

        offsetMillis = (60 * offsetHours + offsetMinutes) * 60 * 1000
        dateTime = java.time.LocalDateTime.ofInstant(java.time.Instant.ofEpochMilli(millis + offsetMillis), java.time.ZoneOffset.UTC)
        result = ""
        for part in formatSpec.parts:
            if part.type == "literal":
                result += part.value
            else:
                result += com.dashjoin.jsonata.utils.DateTimeUtils._formatComponent(dateTime, part, offsetHours, offsetMinutes)

        return result

    @staticmethod
    def _formatComponent(date, markerSpec, offsetHours, offsetMinutes):
        componentValue = com.dashjoin.jsonata.utils.DateTimeUtils._getDateTimeFragment(date, markerSpec.component)

        if "YMDdFWwXxHhms".find(markerSpec.component) != -1:
            if markerSpec.component == 'Y':
                if markerSpec.n != -1:
                    componentValue = "" + str(int((int(math.fmod(int(componentValue), 10 ** markerSpec.n)))))
            if markerSpec.names is not None:
                if markerSpec.component == 'M' or markerSpec.component == 'x':
                    componentValue = com.dashjoin.jsonata.utils.DateTimeUtils._months[int(componentValue) - 1]
                elif markerSpec.component == 'F':
                    componentValue = com.dashjoin.jsonata.utils.DateTimeUtils._days[int(componentValue)]
                else:
                    raise RuntimeException(String.format(Constants.ERR_MSG_INVALID_NAME_MODIFIER, markerSpec.component))
                if markerSpec.names == tcase.UPPER:
                    componentValue = componentValue.upper()
                elif markerSpec.names == tcase.LOWER:
                    componentValue = componentValue.casefold()
                if markerSpec.width is not None and len(componentValue) > markerSpec.width.getRight():
                    componentValue = componentValue[0:markerSpec.width.getRight()]
            else:
                componentValue = com.dashjoin.jsonata.utils.DateTimeUtils._formatInteger(int(componentValue), markerSpec.integerFormat)
        elif markerSpec.component == 'f':
            componentValue = com.dashjoin.jsonata.utils.DateTimeUtils._formatInteger(int(componentValue), markerSpec.integerFormat)
        elif markerSpec.component == 'Z' or markerSpec.component == 'z':
            offset = offsetHours * 100 + offsetMinutes
            if markerSpec.integerFormat.regular:
                componentValue = com.dashjoin.jsonata.utils.DateTimeUtils._formatInteger(offset, markerSpec.integerFormat)
            else:
                numDigits = markerSpec.integerFormat.mandatoryDigits
                if numDigits == 1 or numDigits == 2:
                    componentValue = com.dashjoin.jsonata.utils.DateTimeUtils._formatInteger(offsetHours, markerSpec.integerFormat)
                    if offsetMinutes != 0:
                        componentValue += ":" + com.dashjoin.jsonata.utils.DateTimeUtils.formatInteger(offsetMinutes, "00")
                elif numDigits == 3 or numDigits == 4:
                    componentValue = com.dashjoin.jsonata.utils.DateTimeUtils._formatInteger(offset, markerSpec.integerFormat)
                else:
                    raise RuntimeException(Constants.ERR_MSG_TIMEZONE_FORMAT)
            if offset >= 0:
                componentValue = "+" + componentValue
            if markerSpec.component == 'z':
                componentValue = "GMT" + componentValue
            if offset == 0 and markerSpec.presentation2 is not None and markerSpec.presentation2 == 't':
                componentValue = "Z"
        elif markerSpec.component == 'P':
            # §9.8.4.7 Formatting Other Components
            # Formatting P for am/pm
            # getDateTimeFragment() always returns am/pm lower case so check for UPPER here
            if markerSpec.names == tcase.UPPER:
                componentValue = componentValue.upper()
        return componentValue

    @staticmethod
    def _getDateTimeFragment(date, component):
        componentValue = ""
        match component:
            case 'Y': # year
                componentValue = "" + date.year
            case 'M': # month in year
                componentValue = "" + date.month
            case 'D': # day in month
                componentValue = "" + date.day
            case 'd': # day in year
                componentValue = "" + date.getDayOfYear()
            case 'F': # day of week
                componentValue = "" + date.getDayOfWeek().getValue()
            case 'W': # week in year
                componentValue = "" + date.get(java.time.temporal.IsoFields.WEEK_OF_WEEK_BASED_YEAR)
            case 'w': # week in month
                componentValue = "" + date.get(java.time.temporal.WeekFields.ISO.weekOfMonth())
            case 'X':
                #TODO work these out once others verified
                componentValue = "" + date.year
            case 'x':
                componentValue = "" + date.month
            case 'H': # hour in day (24 hours)
                componentValue = "" + date.hour
            case 'h': #hour in day (12 hours)
                hour = date.hour
                if hour > 12:
                    hour -= 12
                elif hour == 0:
                    hour = 12
                componentValue = "" + str(hour)
            case 'P':
                componentValue = "am" if date.hour < 12 else "pm"
            case 'm':
                componentValue = "" + date.minute
            case 's':
                componentValue = "" + date.second
            case 'f':
# JAVA TO PYTHON CONVERTER TASK: Java to Python Converter cannot determine whether both operands of this division are integer types - if they are then you should change 'lhs / rhs' to 'math.trunc(lhs / float(rhs))':
                componentValue = "" + (date.getNano() / 1000000)
            case 'Z' | 'z':
                pass
            case 'C':
                componentValue = "ISO"
            case 'E':
                componentValue = "ISO"
        return componentValue

    @staticmethod
    def parseDateTime(timestamp, picture):
        formatSpec = com.dashjoin.jsonata.utils.DateTimeUtils._analyseDateTimePicture(picture)
        matchSpec = com.dashjoin.jsonata.utils.DateTimeUtils._generateRegex(formatSpec)
        fullRegex = "^"
        for part in matchSpec.parts:
            fullRegex += "(" + part.regex + ")"
        fullRegex += "$"
        pattern = java.util.regex.Pattern.compile(fullRegex, java.util.regex.Pattern.CASE_INSENSITIVE)
        matcher = pattern.matcher(timestamp)
        if matcher.find():
            dmA = 161
            dmB = 130
            dmC = 84
            dmD = 72
            tmA = 23
            tmB = 47

            components = {}
            i = 1
            while i <= matcher.groupCount():
                mpart = matchSpec.parts[i - 1]
                try:
                    components[mpart.component] = mpart.parse(matcher.group(i))
                except UnsupportedOperationException as e:
                    #do nothing
                    pass
                i += 1

            if len(components) == 0:
                # nothing specified
                return None

            mask = 0

            for part in "YXMxWwdD".toCharArray():
                mask <<= 1
                if components[part] is not None:
                    mask += 1
            dateA = com.dashjoin.jsonata.utils.DateTimeUtils._isType(dmA, mask)
            dateB = not dateA and com.dashjoin.jsonata.utils.DateTimeUtils._isType(dmB, mask)
            dateC = com.dashjoin.jsonata.utils.DateTimeUtils._isType(dmC, mask)
            dateD = not dateC and com.dashjoin.jsonata.utils.DateTimeUtils._isType(dmD, mask)

            mask = 0
            for part in "PHhmsf".toCharArray():
                mask <<= 1
                if components[part] is not None:
                    mask += 1
                pass

            timeA = com.dashjoin.jsonata.utils.DateTimeUtils._isType(tmA, mask)
            timeB = not timeA and com.dashjoin.jsonata.utils.DateTimeUtils._isType(tmB, mask)

            dateComps = "YB" if dateB else "XxwF" if dateC else "XWF" if dateD else "YMD"
            timeComps = "Phmsf" if timeB else "Hmsf"
            comps = dateComps + timeComps

            now = java.time.LocalDateTime.now(java.time.ZoneOffset.UTC)

            startSpecified = False
            endSpecified = False
            for part in comps.toCharArray():
                if components[part] is None:
                    if startSpecified:
                        components[part] = 1 if "MDd".find(part) != -1 else 0
                        endSpecified = True
                    else:
                        components[part] = int(com.dashjoin.jsonata.utils.DateTimeUtils._getDateTimeFragment(now, part))
                else:
                    startSpecified = True
                    if endSpecified:
                        raise RuntimeException(Constants.ERR_MSG_MISSING_FORMAT)
            if components['M'] is not None and components['M'] > 0:
                components['M'] = components['M'] - 1
            else:
                components['M'] = 0
            if dateB:
                firstJan = datetime.datetime(components['Y'], 1, 1, 0, 0)
                firstJan = firstJan.withDayOfYear(components['d'])
                components['M'] = firstJan.month - 1
                components['D'] = firstJan.day
            if dateC:
                #TODO implement this
                #parsing this format not currently supported
                raise RuntimeException(Constants.ERR_MSG_MISSING_FORMAT)
            if dateD:
                #TODO implement this
                # parsing this format (ISO week date) not currently supported
                raise RuntimeException(Constants.ERR_MSG_MISSING_FORMAT)
            if timeB:
                components['H'] = 0 if components['h'] == 12 else components['h']
                if components['P'] == 1:
                    components['H'] = components['H'] + 12
            cal = LocalDateTime.of(components['Y'], components['M'] + 1, components['D'], components['H'], components['m'], components['s'], components['f'] * 1000000)
            millis = cal.toInstant(java.time.ZoneOffset.UTC).toEpochMilli()
            if components['Z'] is not None:
                millis -= components['Z'] * 60 * 1000
            elif components['z'] is not None:
                millis -= components['z'] * 60 * 1000
            return millis
        return None

    @staticmethod
    def _isType(type, mask):
        return ((~type & mask) == 0) and (type & mask) != 0

    @staticmethod
# JAVA TO PYTHON CONVERTER TASK: Python does not allow method overloads:
    def _generateRegex(formatSpec):
        matcher = PictureMatcher()
        for part in formatSpec.parts:
            res = None
            if part.type == "literal":
                p = java.util.regex.Pattern.compile("[.*+?^${}()|\\[\\]\\\\]")
                m = p.matcher(part.value)

                regex = m.replaceAll("\\\\$0")
                res = MatcherPartAnonymousInnerClass(regex)
            elif part.component == 'Z' or part.component == 'z':
# JAVA TO PYTHON CONVERTER WARNING: The original Java variable was marked 'final':
# ORIGINAL LINE: final boolean separator = part.integerFormat.groupingSeparators.size() == 1 && part.integerFormat.regular;
                separator = len(part.integerFormat.groupingSeparators) == 1 and part.integerFormat.regular
                regex = ""
                if part.component == 'z':
                    regex = "GMT"
                regex += "[-+][0-9]+"
                if separator:
                    regex += part.integerFormat.groupingSeparators[0].character + "[0-9]+"
                res = MatcherPartAnonymousInnerClass2(regex, part, separator)
            elif part.integerFormat is not None:
                res = com.dashjoin.jsonata.utils.DateTimeUtils._generateRegex(part.component,part.integerFormat)
            else:
                regex = "[a-zA-Z]+"
# JAVA TO PYTHON CONVERTER WARNING: The original Java variable was marked 'final':
# ORIGINAL LINE: final java.util.Map<String, Integer> lookup = new java.util.HashMap<>();
                lookup = {}
                if part.component == 'M' or part.component == 'x':
                    i = 0
                    while i < len(com.dashjoin.jsonata.utils.DateTimeUtils._months):
                        if part.width is not None and part.width.getRight() is not None:
                            lookup[com.dashjoin.jsonata.utils.DateTimeUtils._months[i][0:part.width.getRight()]] = i + 1
                        else:
                            lookup[com.dashjoin.jsonata.utils.DateTimeUtils._months[i]] = i + 1
                        i += 1
                elif part.component == 'F':
                    i = 1
                    while i < len(com.dashjoin.jsonata.utils.DateTimeUtils._days):
                        if part.width is not None and part.width.getRight() is not None:
                            lookup[com.dashjoin.jsonata.utils.DateTimeUtils._days[i][0:part.width.getRight()]] = i
                        else:
                            lookup[com.dashjoin.jsonata.utils.DateTimeUtils._days[i]] = i
                        i += 1
                elif part.component == 'P':
                    lookup["am"] = 0
                    lookup["AM"] = 0
                    lookup["pm"] = 1
                    lookup["PM"] = 1
                else:
                    raise RuntimeException(String.format(Constants.ERR_MSG_INVALID_NAME_MODIFIER, part.component))
                res = MatcherPartAnonymousInnerClass3(regex, lookup)
            res.component = part.component
            matcher.parts.append(res)
        return matcher

    class MatcherPartAnonymousInnerClass(MatcherPart):
        def __init__(self, regex):
            super().__init__(regex)


        def parse(self, value):
            raise UnsupportedOperationException()

    class MatcherPartAnonymousInnerClass2(MatcherPart):

        def __init__(self, regex, part, separator):
            super().__init__(regex)
            self._part = part
            self._separator = separator


        def parse(self, value):
            if self._part.component == 'z':
                value = value[3:]
            offsetHours = 0
            offsetMinutes = 0
            if self._separator:
                offsetHours = int(value[0:value.find(self._part.integerFormat.groupingSeparators[0].character)])
                offsetMinutes = int(value[value.find(self._part.integerFormat.groupingSeparators[0].character) + 1:])
            else:
                numdigits = len(value) - 1
                if numdigits <= 2:
                    offsetHours = int(value)
                else:
                    offsetHours = int(value[0:3])
                    offsetMinutes = int(value[3:])
            return offsetHours * 60 + offsetMinutes

    class MatcherPartAnonymousInnerClass3(MatcherPart):

        def __init__(self, regex, lookup):
            super().__init__(regex)
            self._lookup = lookup


        def parse(self, value):
            return self._lookup[value]

    @staticmethod
# JAVA TO PYTHON CONVERTER TASK: Python does not allow method overloads:
    def _generateRegex(component, formatSpec):
        matcher = None
# JAVA TO PYTHON CONVERTER WARNING: The original Java variable was marked 'final':
# ORIGINAL LINE: final boolean isUpper = formatSpec.case_type == tcase.UPPER;
        isUpper = formatSpec.case_type == tcase.UPPER
        match formatSpec.primary:
            case com.dashjoin.jsonata.utils.DateTimeUtils.formats.LETTERS:
                    regex = "[A-Z]+" if isUpper else "[a-z]+"
                    matcher = MatcherPartAnonymousInnerClass4(regex, isUpper)
            case com.dashjoin.jsonata.utils.DateTimeUtils.formats.ROMAN:
                    regex = "[MDCLXVI]+" if isUpper else "[mdclxvi]+"
                    matcher = MatcherPartAnonymousInnerClass5(regex, isUpper)
            case com.dashjoin.jsonata.utils.DateTimeUtils.formats.WORDS:
                    words = java.util.HashSet()
                    words.addAll(com.dashjoin.jsonata.utils.DateTimeUtils._wordValues.keys())
                    words.add("and")
                    words.add("[\\-, ]")
                    regex = "(?:" + String.join("|", words.toArray([None for _ in range(words.size())])) + ")+"
                    matcher = MatcherPartAnonymousInnerClass6(regex)
            case com.dashjoin.jsonata.utils.DateTimeUtils.formats.DECIMAL:
                    regex = "[0-9]+"
                    match component:
                        case 'Y':
                                regex = "[0-9]{2,4}"
                        case 'M' | 'D' | 'H' | 'h' | 'm' | 's':
                                regex = "[0-9]{1,2}"
                        case other:

                    if formatSpec.ordinal:
                        regex += "(?:th|st|nd|rd)"
                    matcher = MatcherPartAnonymousInnerClass7(regex, formatSpec)
            case other:
                    raise RuntimeException(Constants.ERR_MSG_SEQUENCE_UNSUPPORTED)
        return matcher

    class MatcherPartAnonymousInnerClass4(MatcherPart):

        def __init__(self, regex, isUpper):
            super().__init__(regex)
            self._isUpper = isUpper


        def parse(self, value):
            return com.dashjoin.jsonata.utils.DateTimeUtils.lettersToDecimal(value,'A' if self._isUpper else 'a')

    class MatcherPartAnonymousInnerClass5(MatcherPart):

        def __init__(self, regex, isUpper):
            super().__init__(regex)
            self._isUpper = isUpper


        def parse(self, value):
            return com.dashjoin.jsonata.utils.DateTimeUtils.romanToDecimal(value if self._isUpper else value.upper())

    class MatcherPartAnonymousInnerClass6(MatcherPart):
        def __init__(self, regex):
            super().__init__(regex)


        def parse(self, value):
            return com.dashjoin.jsonata.utils.DateTimeUtils.wordsToNumber(value.casefold())

    class MatcherPartAnonymousInnerClass7(MatcherPart):

        def __init__(self, regex, formatSpec):
            super().__init__(regex)
            self._formatSpec = formatSpec


        def parse(self, value):
            digits = value
            if self._formatSpec.ordinal:
                digits = value[0:len(value) - 2]
            if self._formatSpec.regular:
                digits = String.join("", digits.split(","))
            else:
                for sep in self._formatSpec.groupingSeparators:
                    digits = String.join("", digits.split(sep.character))
            if self._formatSpec.zeroCode != 0x30:
                chars = digits.toCharArray()
                i = 0
                while i < len(chars):
                    chars[i] = chr((chars[i] - self._formatSpec.zeroCode + 0x30))
                    i += 1
                digits = str(chars)
            return int(digits)

    @staticmethod
    def lettersToDecimal(letters, aChar):
        decimal = 0
        chars = letters.toCharArray()
        i = 0
        while i < len(chars):
            decimal += (chars[len(chars) - i - 1] - aChar + 1) * 26 ** i
            i += 1
        return decimal

    class PictureMatcher:

        def __init__(self):
            # instance fields found by Java to Python Converter:
            self.parts = []



    class MatcherPart:


        def parse(self, value):
            pass

        def __init__(self, regex):
            # instance fields found by Java to Python Converter:
            self.regex = None
            self.component = '\0'

            self.regex = regex

