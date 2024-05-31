import math

#
# * Copyright (c) 1996, 2023, Oracle and/or its affiliates. All rights reserved.
# * DO NOT ALTER OR REMOVE COPYRIGHT NOTICES OR THIS FILE HEADER.
# *
# * This code is free software; you can redistribute it and/or modify it
# * under the terms of the GNU General Public License version 2 only, as
# * published by the Free Software Foundation.  Oracle designates this
# * particular file as subject to the "Classpath" exception as provided
# * by Oracle in the LICENSE file that accompanied this code.
# *
# * This code is distributed in the hope that it will be useful, but WITHOUT
# * ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# * FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# * version 2 for more details (a copy is included in the LICENSE file that
# * accompanied this code).
# *
# * You should have received a copy of the GNU General Public License version
# * 2 along with this work; if not, write to the Free Software Foundation,
# * Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA.
# *
# * Please contact Oracle, 500 Oracle Parkway, Redwood Shores, CA 94065 USA
# * or visit www.oracle.com if you need additional information or have any
# * questions.
# 

#
# * (C) Copyright Taligent, Inc. 1996, 1997 - All Rights Reserved
# * (C) Copyright IBM Corp. 1996 - 1998 - All Rights Reserved
# *
# *   The original version of this source code and documentation is copyrighted
# * and owned by Taligent, Inc., a wholly-owned subsidiary of IBM. These
# * materials are provided under terms of a License Agreement between Taligent
# * and Sun. This technology is protected by multiple US and International
# * patents. This notice and attribution to Taligent may not be removed.
# *   Taligent is a registered trademark of Taligent, Inc.
# *
# 


from jdk.internal.math import FloatingDecimal

#*
# * Digit List. Private to DecimalFormat.
# * Handles the transcoding
# * between numeric values and strings of characters.  Only handles
# * non-negative numbers.  The division of labor between DigitList and
# * DecimalFormat is that DigitList handles the radix 10 representation
# * issues; DecimalFormat handles the locale-specific issues such as
# * positive/negative, grouping, decimal point, currency, and so on.
# *
# * A DigitList is really a representation of a floating point value.
# * It may be an integer value; we assume that a double has sufficient
# * precision to represent all digits of a long.
# *
# * The DigitList representation consists of a string of characters,
# * which are the digits radix 10, from '0' to '9'.  It also has a radix
# * 10 exponent associated with it.  The value represented by a DigitList
# * object can be computed by mulitplying the fraction f, where 0 <= f < 1,
# * derived by placing all the digits of the list to the right of the
# * decimal point, by 10^exponent.
# *
# * @see  Locale
# * @see  Format
# * @see  NumberFormat
# * @see  DecimalFormat
# * @see  ChoiceFormat
# * @see  MessageFormat
# * @author       Mark Davis, Alan Liu
# 
class DigitList(Cloneable):

    def __init__(self):
        # instance fields found by Java to Python Converter:
        self.decimalAt = 0
        self.count = 0
        self.digits = ['\0' for _ in range(java.text.DigitList.MAX_COUNT)]
        self._data = None
        self._roundingMode = java.math.RoundingMode.HALF_EVEN
        self._isNegative = False
        self._tempBuilder = None

    #    *
    #     * The maximum number of significant digits in an IEEE 754 double, that
    #     * is, in a Java double.  This must not be increased, or garbage digits
    #     * will be generated, and should not be decreased, or accuracy will be lost.
    #     
    MAX_COUNT = 19 # == Long.toString(Long.MAX_VALUE).length()

    #    *
    #     * These data members are intentionally public and can be set directly.
    #     *
    #     * The value represented is given by placing the decimal point before
    #     * digits[decimalAt].  If decimalAt is < 0, then leading zeros between
    #     * the decimal point and the first nonzero digit are implied.  If decimalAt
    #     * is > count, then trailing zeros between the digits[count-1] and the
    #     * decimal point are implied.
    #     *
    #     * Equivalently, the represented value is given by f * 10^decimalAt.  Here
    #     * f is a value 0.1 <= f < 1 arrived at by placing the digits in Digits to
    #     * the right of the decimal.
    #     *
    #     * DigitList is normalized, so if it is non-zero, digits[0] is non-zero.  We
    #     * don't allow denormalized numbers because our exponent is effectively of
    #     * unlimited magnitude.  The count value contains the number of significant
    #     * digits present in digits[].
    #     *
    #     * Zero is represented by any DigitList with count == 0 or with each digits[i]
    #     * for all i <= count == '0'.
    #     


    #    *
    #     * Return true if the represented number is zero.
    #     
    def isZero(self):
        return not self._nonZeroAfterIndex(0)


    #    *
    #     * Return true if there exists a non-zero digit in the digit list
    #     * from the given index until the end.
    #     
    def _nonZeroAfterIndex(self, index):
        i = index
        while i < self.count:
            if self.digits[i] != '0':
                return True
            i += 1
        return False

    #    *
    #     * Set the rounding mode
    #     
    def setRoundingMode(self, r):
        self._roundingMode = r

    #    *
    #     * Clears out the digits.
    #     * Use before appending them.
    #     * Typically, you set a series of digits with append, then at the point
    #     * you hit the decimal point, you set myDigitList.decimalAt = myDigitList.count
    #     * then go on appending digits.
    #     
    def clear(self):
        self.decimalAt = 0
        self.count = 0

    #    *
    #     * Appends a digit to the list, extending the list when necessary.
    #     
    def append(self, digit):
        if self.count == len(self.digits):
            data = ['\0' for _ in range(self.count + 100)]
            System.arraycopy(self.digits, 0, data, 0, self.count)
            self.digits = data
# JAVA TO PYTHON CONVERTER WARNING: An assignment within expression was extracted from the following statement:
# ORIGINAL LINE: digits[count++] = digit;
        self.digits[self.count] = digit
        self.count += 1

    #    *
    #     * Utility routine to get the value of the digit list
    #     * If (count == 0) this returns 0.0,
    #     * unlike Double.parseDouble("") which throws NumberFormatException.
    #     
    def getDouble(self):
        if self.count == 0:
            return 0.0

        return float(str(self._getStringBuilder().append('.').append(self.digits, 0, self.count).append('E').append(self.decimalAt)))

    #    *
    #     * Utility routine to get the value of the digit list.
    #     * If (count == 0) this returns 0,
    #     * unlike Long.parseLong("") which throws NumberFormatException.
    #     
    def getLong(self):
        # for now, simple implementation; later, do proper IEEE native stuff

        if self.count == 0:
            return 0

        # We have to check for this, because this is the one NEGATIVE value
        # we represent.  If we tried to just pass the digits off to parseLong,
        # we'd get a parse failure.
        if self._isLongMIN_VALUE():
            return Long.MIN_VALUE

        temp = self._getStringBuilder()
        temp.append(self.digits, 0, self.count)
        temp.append("0".repeat(max(0, self.decimalAt - self.count)))
        return int(str(temp))

    #    *
    #     * Utility routine to get the value of the digit list.
    #     * If (count == 0) this does not throw a NumberFormatException,
    #     * unlike BigDecimal("").
    #     
    def getBigDecimal(self):
        if self.count == 0:
            if self.decimalAt == 0:
                return java.math.BigDecimal.ZERO
            else:
                return java.math.BigDecimal("0E" + str(self.decimalAt))

        if self.decimalAt == self.count:
            return java.math.BigDecimal(self.digits, 0, self.count)
        else:
            return (java.math.BigDecimal(self.digits, 0, self.count)).scaleByPowerOfTen(self.decimalAt - self.count)

    #    *
    #     * Return true if the number represented by this object can fit into
    #     * a long.
    #     * @param isPositive true if this number should be regarded as positive
    #     * @param ignoreNegativeZero true if -0 should be regarded as identical to
    #     * +0; otherwise they are considered distinct
    #     * @return true if this number fits into a Java long
    #     
    def fitsIntoLong(self, isPositive, ignoreNegativeZero):
        # Figure out if the result will fit in a long.  We have to
        # first look for nonzero digits after the decimal point
        # then check the size.  If the digit count is 18 or less, then
        # the value can definitely be represented as a long.  If it is 19
        # then it may be too large.

        # Trim trailing zeros.  This does not change the represented value.
        while self.count > 0 and self.digits[self.count - 1] == '0':
            self.count -= 1

        if self.count == 0:
            # Positive zero fits into a long, but negative zero can only
            # be represented as a double. - bug 4162852
            return isPositive or ignoreNegativeZero

        if self.decimalAt < self.count or self.decimalAt > java.text.DigitList.MAX_COUNT:
            return False

        if self.decimalAt < java.text.DigitList.MAX_COUNT:
            return True

        # At this point we have decimalAt == count, and count == MAX_COUNT.
        # The number will overflow if it is larger than 9223372036854775807
        # or smaller than -9223372036854775808.
        i = 0
        while i < self.count:
            dig = self.digits[i]
            max = java.text.DigitList.LONG_MIN_REP[i]
            if dig > max:
                return False
            if dig < max:
                return True
            i += 1

        # At this point the first count digits match.  If decimalAt is less
        # than count, then the remaining digits are zero, and we return true.
        if self.count < self.decimalAt:
            return True

        # Now we have a representation of Long.MIN_VALUE, without the leading
        # negative sign.  If this represents a positive value, then it does
        # not fit; otherwise it fits.
        return not isPositive

    #    *
    #     * Set the digit list to a representation of the given double value.
    #     * This method supports fixed-point notation.
    #     * @param isNegative Boolean value indicating whether the number is negative.
    #     * @param source Value to be converted; must not be Inf, -Inf, Nan,
    #     * or a value <= 0.
    #     * @param maximumFractionDigits The most fractional digits which should
    #     * be converted.
    #     
# JAVA TO PYTHON CONVERTER TASK: Python does not allow method overloads:
    def set(self, isNegative, source, maximumFractionDigits):
        self.set(isNegative, source, maximumFractionDigits, True)

    #    *
    #     * Set the digit list to a representation of the given double value.
    #     * This method supports both fixed-point and exponential notation.
    #     * @param isNegative Boolean value indicating whether the number is negative.
    #     * @param source Value to be converted; must not be Inf, -Inf, Nan,
    #     * or a value <= 0.
    #     * @param maximumDigits The most fractional or total digits which should
    #     * be converted.
    #     * @param fixedPoint If true, then maximumDigits is the maximum
    #     * fractional digits to be converted.  If false, total digits.
    #     
# JAVA TO PYTHON CONVERTER TASK: Python does not allow method overloads:
    def set(self, isNegative, source, maximumDigits, fixedPoint):

        fdConverter = jdk.internal.math.FloatingDecimal.getBinaryToASCIIConverter(source)
        hasBeenRoundedUp = fdConverter.digitsRoundedUp()
        valueExactAsDecimal = fdConverter.decimalDigitsExact()
        assert not fdConverter.isExceptional()
        digitsString = fdConverter.toJavaFormatString()

        self._set(isNegative, digitsString, hasBeenRoundedUp, valueExactAsDecimal, maximumDigits, fixedPoint)

    #    *
    #     * Generate a representation of the form DDDDD, DDDDD.DDDDD, or
    #     * DDDDDE+/-DDDDD.
    #     * @param roundedUp whether or not rounding up has already happened.
    #     * @param valueExactAsDecimal whether or not collected digits provide
    #     * an exact decimal representation of the value.
    #     
# JAVA TO PYTHON CONVERTER TASK: Python does not allow method overloads:
    def _set(self, isNegative, s, roundedUp, valueExactAsDecimal, maximumDigits, fixedPoint):

        self._isNegative = isNegative
        len = len(s)
        source = self._getDataChars(len)
        s.getChars(0, len, source, 0)

        self.decimalAt = -1
        self.count = 0
        exponent = 0
        # Number of zeros between decimal point and first non-zero digit after
        # decimal point, for numbers < 1.
        leadingZerosAfterDecimal = 0
        nonZeroDigitSeen = False

        i = 0
        while i < len:
# JAVA TO PYTHON CONVERTER WARNING: An assignment within expression was extracted from the following statement:
# ORIGINAL LINE: char c = source[i++];
            c = source[i]
            i += 1
            if c == '.':
                self.decimalAt = self.count
            elif c == 'e' or c == 'E':
                exponent = java.text.DigitList._parseInt(source, i, len)
                break
            else:
                if not nonZeroDigitSeen:
                    nonZeroDigitSeen = (c != '0')
                    if not nonZeroDigitSeen and self.decimalAt != -1:
                        leadingZerosAfterDecimal += 1
                if nonZeroDigitSeen:
# JAVA TO PYTHON CONVERTER WARNING: An assignment within expression was extracted from the following statement:
# ORIGINAL LINE: digits[count++] = c;
                    self.digits[self.count] = c
                    self.count += 1
        if self.decimalAt == -1:
            self.decimalAt = self.count
        if nonZeroDigitSeen:
            self.decimalAt += exponent - leadingZerosAfterDecimal

        if fixedPoint:
            # The negative of the exponent represents the number of leading
            # zeros between the decimal and the first non-zero digit, for
            # a value < 0.1 (e.g., for 0.00123, -decimalAt == 2).  If this
            # is more than the maximum fraction digits, then we have an underflow
            # for the printed representation.
            if - self.decimalAt > maximumDigits:
                # Handle an underflow to zero when we round something like
                # 0.0009 to 2 fractional digits.
                self.count = 0
                return
            elif - self.decimalAt == maximumDigits:
                # If we round 0.0009 to 3 fractional digits, then we have to
                # create a new one digit in the least significant location.
                if self._shouldRoundUp(0, roundedUp, valueExactAsDecimal):
                    self.count = 1
                    self.decimalAt += 1
                    self.digits[0] = '1'
                else:
                    self.count = 0
                return
            # else fall through

        # Eliminate trailing zeros.
        while self.count > 1 and self.digits[self.count - 1] == '0':
            self.count -= 1

        # Eliminate digits beyond maximum digits to be displayed.
        # Round up if appropriate.
        self._round((maximumDigits + self.decimalAt) if fixedPoint else maximumDigits, roundedUp, valueExactAsDecimal)


    #    *
    #     * Round the representation to the given number of digits.
    #     * @param maximumDigits The maximum number of digits to be shown.
    #     *
    #     * Upon return, count will be less than or equal to maximumDigits.
    #     
    def _roundInt(self, maximumDigits):
        # Integers do not need to worry about double rounding
        self._round(maximumDigits, False, True)

    #    *
    #     * Round the representation to the given number of digits.
    #     * @param maximumDigits The maximum number of digits to be shown.
    #     * @param alreadyRounded whether or not rounding up has already happened.
    #     * @param valueExactAsDecimal whether or not collected digits provide
    #     * an exact decimal representation of the value.
    #     *
    #     * Upon return, count will be less than or equal to maximumDigits.
    #     
    def _round(self, maximumDigits, alreadyRounded, valueExactAsDecimal):
        # Eliminate digits beyond maximum digits to be displayed.
        # Round up if appropriate.
        if maximumDigits >= 0 and maximumDigits < self.count:
            if self._shouldRoundUp(maximumDigits, alreadyRounded, valueExactAsDecimal):
                # Rounding can adjust the max digits
                maximumDigits = self._roundUp(maximumDigits)
            self.count = maximumDigits

            # Eliminate trailing zeros.
            while self.count > 1 and self.digits[self.count - 1] == '0':
                self.count -= 1


    #    *
    #     * Return true if truncating the representation to the given number
    #     * of digits will result in an increment to the last digit.  This
    #     * method implements the rounding modes defined in the
    #     * java.math.RoundingMode class.
    #     * [bnf]
    #     * @param maximumDigits the number of digits to keep, from 0 to
    #     * {@code count-1}.  If 0, then all digits are rounded away, and
    #     * this method returns true if a one should be generated (e.g., formatting
    #     * 0.09 with "#.#").
    #     * @param alreadyRounded whether or not rounding up has already happened.
    #     * @param valueExactAsDecimal whether or not collected digits provide
    #     * an exact decimal representation of the value.
    #     * @throws    ArithmeticException if rounding is needed with rounding
    #     *            mode being set to RoundingMode.UNNECESSARY
    #     * @return true if digit {@code maximumDigits-1} should be
    #     * incremented
    #     
    def _shouldRoundUp(self, maximumDigits, alreadyRounded, valueExactAsDecimal):
        if maximumDigits < self.count:
            #            
            #             * To avoid erroneous double-rounding or truncation when converting
            #             * a binary double value to text, information about the exactness
            #             * of the conversion result in FloatingDecimal, as well as any
            #             * rounding done, is needed in this class.
            #             *
            #             * - For the  HALF_DOWN, HALF_EVEN, HALF_UP rounding rules below:
            #             *   In the case of formatting float or double, We must take into
            #             *   account what FloatingDecimal has done in the binary to decimal
            #             *   conversion.
            #             *
            #             *   Considering the tie cases, FloatingDecimal may round up the
            #             *   value (returning decimal digits equal to tie when it is below),
            #             *   or "truncate" the value to the tie while value is above it,
            #             *   or provide the exact decimal digits when the binary value can be
            #             *   converted exactly to its decimal representation given formatting
            #             *   rules of FloatingDecimal ( we have thus an exact decimal
            #             *   representation of the binary value).
            #             *
            #             *   - If the double binary value was converted exactly as a decimal
            #             *     value, then DigitList code must apply the expected rounding
            #             *     rule.
            #             *
            #             *   - If FloatingDecimal already rounded up the decimal value,
            #             *     DigitList should neither round up the value again in any of
            #             *     the three rounding modes above.
            #             *
            #             *   - If FloatingDecimal has truncated the decimal value to
            #             *     an ending '5' digit, DigitList should round up the value in
            #             *     all of the three rounding modes above.
            #             *
            #             *
            #             *   This has to be considered only if digit at maximumDigits index
            #             *   is exactly the last one in the set of digits, otherwise there are
            #             *   remaining digits after that position and we don't have to consider
            #             *   what FloatingDecimal did.
            #             *
            #             * - Other rounding modes are not impacted by these tie cases.
            #             *
            #             * - For other numbers that are always converted to exact digits
            #             *   (like BigInteger, Long, ...), the passed alreadyRounded boolean
            #             *   have to be  set to false, and valueExactAsDecimal has to be set to
            #             *   true in the upper DigitList call stack, providing the right state
            #             *   for those situations..
            #             

            match self._roundingMode:
                case UP:
                    return self._nonZeroAfterIndex(maximumDigits)
                case DOWN:
                    pass
                case CEILING:
                    return self._nonZeroAfterIndex(maximumDigits) and not self._isNegative
                case FLOOR:
                    return self._nonZeroAfterIndex(maximumDigits) and self._isNegative
                case HALF_UP | HALF_DOWN | HALF_EVEN:
                    # Above tie, round up for all cases
                    if self.digits[maximumDigits] > '5':
                        return True
                        # At tie, consider UP, DOWN, and EVEN logic
                    elif self.digits[maximumDigits] == '5':
                        # Rounding position is the last index, there are 3 Cases.
                        if maximumDigits == (self.count - 1):
                            # When exact, consider specific contract logic
                            if valueExactAsDecimal:
                                return (self._roundingMode is java.math.RoundingMode.HALF_UP) or (self._roundingMode is java.math.RoundingMode.HALF_EVEN and (maximumDigits > 0) and (int(math.fmod(self.digits[maximumDigits - 1], 2)) != 0))
                                # If already rounded, do not round again, otherwise round up
                            else:
                                return not alreadyRounded
                            # Rounding position is not the last index
                            # If any further digits have a non-zero value, round up
                        else:
                            return self._nonZeroAfterIndex(maximumDigits + 1)
                    # Below tie, do not round up for all cases
                case UNNECESSARY:
                    if self._nonZeroAfterIndex(maximumDigits):
                        raise ArithmeticException("Rounding needed with the rounding mode being set to RoundingMode.UNNECESSARY")
                case other:
                    assert False
        return False

    #    *
    #     * Round the digit list up numerically.
    #     * This involves incrementing digits from the LSD to the MSD.
    #     * @param maximumDigits The maximum number of digits to be shown.
    #     * @return The new maximum digits after rounding.
    #     
    def _roundUp(self, maximumDigits):
        loop_condition = True
        while loop_condition:
            maximumDigits -= 1
            #            
            #             * We have exhausted the max digits while attempting to round up
            #             * from the LSD to the MSD. This implies a value of all 9's. As such,
            #             * adjust representation to a single digit of one and increment the exponent.
            #             
            if maximumDigits < 0:
                self.digits[0] = '1'
                self.decimalAt += 1
                maximumDigits = 0 # Adjust the count
                break
            self.digits[maximumDigits] += chr(1)
            loop_condition = self.digits[maximumDigits] > '9'

        maximumDigits += 1
# JAVA TO PYTHON CONVERTER WARNING: An assignment within expression was extracted from the following statement:
# ORIGINAL LINE: return ++maximumDigits;
        return maximumDigits # Increment for use as count

    #    *
    #     * Utility routine to set the value of the digit list from a long
    #     
# JAVA TO PYTHON CONVERTER TASK: Python does not allow method overloads:
    def set(self, isNegative, source):
        self.set(isNegative, source, 0)

    #    *
    #     * Set the digit list to a representation of the given long value.
    #     * @param isNegative Boolean value indicating whether the number is negative.
    #     * @param source Value to be converted; must be >= 0 or ==
    #     * Long.MIN_VALUE.
    #     * @param maximumDigits The most digits which should be converted.
    #     * If maximumDigits is lower than the number of significant digits
    #     * in source, the representation will be rounded.  Ignored if <= 0.
    #     
# JAVA TO PYTHON CONVERTER TASK: Python does not allow method overloads:
    def set(self, isNegative, source, maximumDigits):
        self._isNegative = isNegative

        # This method does not expect a negative number. However,
        # "source" can be a Long.MIN_VALUE (-9223372036854775808),
        # if the number being formatted is a Long.MIN_VALUE.  In that
        # case, it will be formatted as -Long.MIN_VALUE, a number
        # which is outside the legal range of a long, but which can
        # be represented by DigitList.
        if source <= 0:
            if source == Long.MIN_VALUE:
                self.decimalAt = self.count = java.text.DigitList.MAX_COUNT
                System.arraycopy(java.text.DigitList.LONG_MIN_REP, 0, self.digits, 0, self.count)
            else:
                self.decimalAt = self.count = 0 # Values <= 0 format as zero
        else:
            # Rewritten to improve performance.  I used to call
            # Long.toString(), which was about 4x slower than this code.
            left = java.text.DigitList.MAX_COUNT
            right = 0
            while source > 0:
                left -= 1
# JAVA TO PYTHON CONVERTER WARNING: An assignment within expression was extracted from the following statement:
# ORIGINAL LINE: digits[--left] = (char)('0' + (source % 10));
                self.digits[left] = chr(('0' + (int(math.fmod(source, 10)))))
                source = math.trunc(source / float(10))
            self.decimalAt = java.text.DigitList.MAX_COUNT - left
            # Don't copy trailing zeros.  We are guaranteed that there is at
            # least one non-zero digit, so we don't have to check lower bounds.
            right = java.text.DigitList.MAX_COUNT - 1
            while self.digits[right] == '0':
                right -= 1
            self.count = right - left + 1
            System.arraycopy(self.digits, left, self.digits, 0, self.count)
        if maximumDigits > 0:
            self._roundInt(maximumDigits)

    #    *
    #     * Set the digit list to a representation of the given BigDecimal value.
    #     * This method supports both fixed-point and exponential notation.
    #     * @param isNegative Boolean value indicating whether the number is negative.
    #     * @param source Value to be converted; must not be a value <= 0.
    #     * @param maximumDigits The most fractional or total digits which should
    #     * be converted.
    #     * @param fixedPoint If true, then maximumDigits is the maximum
    #     * fractional digits to be converted.  If false, total digits.
    #     
# JAVA TO PYTHON CONVERTER TASK: Python does not allow method overloads:
    def set(self, isNegative, source, maximumDigits, fixedPoint):
        s = str(source)
        self._extendDigits(len(s))

        self._set(isNegative, s, False, True, maximumDigits, fixedPoint)

    #    *
    #     * Set the digit list to a representation of the given BigInteger value.
    #     * @param isNegative Boolean value indicating whether the number is negative.
    #     * @param source Value to be converted; must be >= 0.
    #     * @param maximumDigits The most digits which should be converted.
    #     * If maximumDigits is lower than the number of significant digits
    #     * in source, the representation will be rounded.  Ignored if <= 0.
    #     
# JAVA TO PYTHON CONVERTER TASK: Python does not allow method overloads:
    def set(self, isNegative, source, maximumDigits):
        self._isNegative = isNegative
        s = str(source)
        len = len(s)
        self._extendDigits(len)
        s.getChars(0, len, self.digits, 0)

        self.decimalAt = len
        right = len - 1
        while right >= 0 and self.digits[right] == '0':
            right -= 1
        self.count = right + 1

        if maximumDigits > 0:
            self._roundInt(maximumDigits)

    #    *
    #     * equality test between two digit lists.
    #     
    def equals(self, obj):
        if self is obj: # quick check
            return True
        temp_var = isinstance(obj, DigitList)
        other = obj if temp_var else None
        if not(temp_var): # (1) same object?
            return False
        if self.count != other.count or self.decimalAt != other.decimalAt:
            return False
        i = 0
        while i < self.count:
            if self.digits[i] != other.digits[i]:
                return False
            i += 1
        return True

    #    *
    #     * Generates the hash code for the digit list.
    #     
    def hashCode(self):
        hashcode = self.decimalAt

        i = 0
        while i < self.count:
            hashcode = hashcode * 37 + self.digits[i]
            i += 1

        return hashcode

    #    *
    #     * Creates a copy of this object.
    #     * @return a clone of this instance.
    #     
    def clone(self):
        try:
            other = super().clone()
            newDigits = ['\0' for _ in range(len(self.digits))]
            newDigits = self.digits.copy()
            other.digits = newDigits
            other._tempBuilder = None
            return other
        except CloneNotSupportedException as e:
            raise InternalError(e)

    #    *
    #     * Returns true if this DigitList represents Long.MIN_VALUE
    #     * false, otherwise.  This is required so that getLong() works.
    #     
    def _isLongMIN_VALUE(self):
        if self.decimalAt != self.count or self.count != java.text.DigitList.MAX_COUNT:
            return False

        i = 0
        while i < self.count:
            if self.digits[i] != java.text.DigitList.LONG_MIN_REP[i]:
                return False
            i += 1

        return True

    @staticmethod
    def _parseInt(str, offset, strLen):
        c = '\0'
        positive = True
        if (c := str[offset]) == '-':
            positive = False
            offset += 1
        elif c == '+':
            offset += 1

        value = 0
        while offset < strLen:
# JAVA TO PYTHON CONVERTER WARNING: An assignment within expression was extracted from the following statement:
# ORIGINAL LINE: c = str[offset++];
            c = str[offset]
            offset += 1
            if c >= '0' and c <= '9':
                value = value * 10 + (c - '0')
            else:
                break
        return value if positive else - value

    # The digit part of -9223372036854775808L
    LONG_MIN_REP = "9223372036854775808".toCharArray()

    def toString(self):
        if self.isZero():
            return "0"

        return str(self._getStringBuilder().append("0.").append(self.digits, 0, self.count).append("x10^").append(self.decimalAt))


    def _getStringBuilder(self):
        if self._tempBuilder is None:
            self._tempBuilder = StringBuilder(java.text.DigitList.MAX_COUNT)
        else:
            self._tempBuilder.setLength(0)
        return self._tempBuilder

    def _extendDigits(self, len):
        if len > len(self.digits):
            self.digits = ['\0' for _ in range(len)]

    def _getDataChars(self, length):
        if self._data is None or len(self._data) < length:
            self._data = ['\0' for _ in range(length)]
        return self._data
