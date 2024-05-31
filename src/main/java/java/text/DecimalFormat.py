import copy
import math

#
# * Copyright (c) 1996, 2024, Oracle and/or its affiliates. All rights reserved.
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



from sun.util.locale.provider import LocaleProviderAdapter
from sun.util.locale.provider import ResourceBundleBasedAdapter

#*
# * {@code DecimalFormat} is a concrete subclass of
# * {@code NumberFormat} that formats decimal numbers in a localized manner.
# * It has a variety of features designed to make it possible to parse and format
# * numbers in any locale, including support for Western, Arabic, and Indic digits.
# * It also supports different kinds of numbers, including integers (123), fixed-point
# * numbers (123.4), scientific notation (1.23E4), percentages (12%), and
# * currency amounts ($123).
# *
# * <h2>Getting a DecimalFormat</h2>
# *
# * To obtain a standard decimal format for a specific locale, including the default locale,
# * it is recommended to call one of the {@code NumberFormat}
# * {@link NumberFormat##factory_methods factory methods}, such as {@link NumberFormat#getInstance()}.
# * These factory methods may not always return a {@code DecimalFormat}
# * depending on the locale-service provider implementation
# * installed. Thus, to use an instance method defined by {@code DecimalFormat},
# * the {@code NumberFormat} returned by the factory method should be
# * type checked before converted to {@code DecimalFormat}. If the installed locale-sensitive
# * service implementation does not support the given {@code Locale}, the parent
# * locale chain will be looked up, and a {@code Locale} used that is supported.
# *
# * <p>If the factory methods are not desired, use one of the constructors such
# * as {@link #DecimalFormat(String) DecimalFormat(String pattern)}. See the {@link
# * ##patterns Pattern} section for more information on the {@code pattern} parameter.
# *
# * <h2>Using DecimalFormat</h2>
# * The following is an example of formatting and parsing,
# * {@snippet lang=java :
# * NumberFormat nFmt = NumberFormat.getCurrencyInstance(Locale.US)
# * if (nFmt instanceof DecimalFormat dFmt) {
# *     // pattern match to DecimalFormat to use setPositiveSuffix(String)
# *     dFmt.setPositiveSuffix(" dollars")
# *     dFmt.format(100000); // returns "$100,000.00 dollars"
# *     dFmt.parse("$100,000.00 dollars"); // returns 100000
# * }
# * }
# *
# *
# * <h2 id="formatting">Formatting and Parsing</h2>
# * <h3 id="rounding">Rounding</h3>
# *
# * When formatting, {@code DecimalFormat} can adjust its rounding using {@link
# * #setRoundingMode(RoundingMode)}. By default, it uses
# * {@link java.math.RoundingMode#HALF_EVEN RoundingMode.HALF_EVEN}.
# *
# * <h3>Digits</h3>
# *
# * When formatting, {@code DecimalFormat} uses the ten consecutive
# * characters starting with the localized zero digit defined in the
# * {@code DecimalFormatSymbols} object as digits.
# * <p>When parsing, these digits as well as all Unicode decimal digits, as
# * defined by {@link Character#digit Character.digit}, are recognized.
# *
# * <h3 id="digit_limits"> Integer and Fraction Digit Limits </h3>
# * @implSpec
# * When formatting a {@code Number} other than {@code BigInteger} and
# * {@code BigDecimal}, {@code 309} is used as the upper limit for integer digits,
# * and {@code 340} as the upper limit for fraction digits. This occurs, even if
# * one of the {@code DecimalFormat} getter methods, for example, {@link #getMinimumFractionDigits()}
# * returns a numerically greater value.
# *
# * <h3>Special Values</h3>
# * <ul>
# * <li><p><b>Not a Number</b> ({@code NaN}) is formatted as a string,
# * which is typically given as "NaN". This string is determined by {@link
# * DecimalFormatSymbols#getNaN()}. This is the only value for which the prefixes
# * and suffixes are not attached.
# *
# * <li><p><b>Infinity</b> is formatted as a string, which is typically given as
# * "&#8734;" ({@code U+221E}), with the positive or negative prefixes and suffixes
# * attached. This string is determined by {@link DecimalFormatSymbols#getInfinity()}.
# *
# * <li><p><b>Negative zero</b> ({@code "-0"}) parses to
# * <ul>
# * <li>{@code BigDecimal(0)} if {@code isParseBigDecimal()} is
# * true
# * <li>{@code Long(0)} if {@code isParseBigDecimal()} is false
# *     and {@code isParseIntegerOnly()} is true
# * <li>{@code Double(-0.0)} if both {@code isParseBigDecimal()}
# * and {@code isParseIntegerOnly()} are false
# * </ul>
# * </ul>
# *
# * <h2><a id="synchronization">Synchronization</a></h2>
# *
# * <p>
# * Decimal formats are generally not synchronized.
# * It is recommended to create separate format instances for each thread.
# * If multiple threads access a format concurrently, it must be synchronized
# * externally.
# *
# * <h2 id="patterns">DecimalFormat Pattern</h2>
# *
# * A {@code DecimalFormat} comprises a <em>pattern</em> and a set of
# * <em>symbols</em>. The pattern may be set directly using {@code applyPattern()},
# * or indirectly using the various API methods. The symbols are stored in a {@code
# * DecimalFormatSymbols} object. When using the {@code NumberFormat} factory
# * methods, the pattern and symbols are created from the locale-sensitive service
# * implementation installed.
# *
# * <p> {@code DecimalFormat} patterns have the following syntax:
# * <blockquote><pre>
# * <i>Pattern:</i>
# *         <i>PositivePattern</i>
# *         <i>PositivePattern</i> ; <i>NegativePattern</i>
# * <i>PositivePattern:</i>
# *         <i>Prefix<sub>opt</sub></i> <i>Number</i> <i>Suffix<sub>opt</sub></i>
# * <i>NegativePattern:</i>
# *         <i>Prefix<sub>opt</sub></i> <i>Number</i> <i>Suffix<sub>opt</sub></i>
# * <i>Prefix:</i>
# *         Any characters except the {@linkplain ##special_pattern_character
# *         special pattern characters}
# * <i>Suffix:</i>
# *         Any characters except the {@linkplain ##special_pattern_character
# *         special pattern characters}
# * <i>Number:</i>
# *         <i>Integer</i> <i>Exponent<sub>opt</sub></i>
# *         <i>Integer</i> . <i>Fraction</i> <i>Exponent<sub>opt</sub></i>
# * <i>Integer:</i>
# *         <i>MinimumInteger</i>
# *         #
# *         # <i>Integer</i>
# *         # , <i>Integer</i>
# * <i>MinimumInteger:</i>
# *         0
# *         0 <i>MinimumInteger</i>
# *         0 , <i>MinimumInteger</i>
# * <i>Fraction:</i>
# *         <i>MinimumFraction<sub>opt</sub></i> <i>OptionalFraction<sub>opt</sub></i>
# * <i>MinimumFraction:</i>
# *         0 <i>MinimumFraction<sub>opt</sub></i>
# * <i>OptionalFraction:</i>
# *         # <i>OptionalFraction<sub>opt</sub></i>
# * <i>Exponent:</i>
# *         E <i>MinimumExponent</i>
# * <i>MinimumExponent:</i>
# *         0 <i>MinimumExponent<sub>opt</sub></i>
# * </pre></blockquote>
# *
# * <h3><a id="special_pattern_character">Special Pattern Characters</a></h3>
# *
# * <p>The special characters in the table below are interpreted syntactically when
# * used in the DecimalFormat pattern.
# * They must be quoted, unless noted otherwise, if they are to appear in the
# * prefix or suffix as literals.
# *
# * <p> The characters in the {@code Symbol} column are used in non-localized
# * patterns. The corresponding characters in the {@code Localized Symbol} column are used
# * in localized patterns, with the characters in {@code Symbol} losing their
# * syntactical meaning. Two exceptions are the currency sign ({@code U+00A4}) and
# * quote ({@code U+0027}), which are not localized.
# * <p>
# * Non-localized patterns should be used when calling {@link #applyPattern(String)}.
# * Localized patterns should be used when calling {@link #applyLocalizedPattern(String)}.
# *
# * <blockquote>
# * <table class="striped">
# * <caption style="display:none">Chart showing symbol, location, localized, and meaning.</caption>
# * <thead>
# *     <tr>
# *          <th scope="col" style="text-align:left">Symbol
# *          <th scope="col" style="text-align:left">Localized Symbol
# *          <th scope="col" style="text-align:left">Location
# *          <th scope="col" style="text-align:left;width:50%">Meaning
# * </thead>
# * <tbody>
# *     <tr>
# *          <th scope="row">{@code 0}
# *          <td>{@link DecimalFormatSymbols#getZeroDigit()}
# *          <td>Number
# *          <td>Digit
# *     <tr>
# *          <th scope="row">{@code #}
# *          <td>{@link DecimalFormatSymbols#getDigit()}
# *          <td>Number
# *          <td>Digit, zero shows as absent
# *     <tr>
# *          <th scope="row">{@code .}
# *          <td>{@link DecimalFormatSymbols#getDecimalSeparator()}
# *          <td>Number
# *          <td>Decimal separator or monetary decimal separator
# *     <tr>
# *          <th scope="row">{@code - (U+002D)}
# *          <td>{@link DecimalFormatSymbols#getMinusSign()}
# *          <td>Number
# *          <td>Minus sign
# *     <tr>
# *          <th scope="row">{@code ,}
# *          <td>{@link DecimalFormatSymbols#getGroupingSeparator()}
# *          <td>Number
# *          <td>Grouping separator or monetary grouping separator
# *     <tr>
# *          <th scope="row">{@code E}
# *          <td>{@link DecimalFormatSymbols#getExponentSeparator()}
# *          <td>Number
# *          <td>Separates mantissa and exponent in scientific notation. This value
# *              is case sensistive. <em>Need not be quoted in prefix or suffix.</em>
# *     <tr>
# *          <th scope="row">{@code ;}
# *          <td>{@link DecimalFormatSymbols#getPatternSeparator()}
# *          <td>Subpattern boundary
# *          <td>Separates positive and negative subpatterns
# *     <tr>
# *          <th scope="row">{@code %}
# *          <td>{@link DecimalFormatSymbols#getPercent()}
# *          <td>Prefix or suffix
# *          <td>Multiply by 100 and show as percentage
# *     <tr>
# *          <th scope="row">&permil; ({@code U+2030})
# *          <td>{@link DecimalFormatSymbols#getPerMill()}
# *          <td>Prefix or suffix
# *          <td>Multiply by 1000 and show as per mille value
# *     <tr>
# *          <th scope="row">&#164; ({@code U+00A4})
# *          <td> n/a (not localized)
# *          <td>Prefix or suffix
# *          <td>Currency sign, replaced by currency symbol.  If
# *              doubled, replaced by international currency symbol.
# *              If present in a pattern, the monetary decimal/grouping separators
# *              are used instead of the decimal/grouping separators.
# *     <tr>
# *          <th scope="row">{@code ' (U+0027)}
# *          <td> n/a (not localized)
# *          <td>Prefix or suffix
# *          <td>Used to quote special characters in a prefix or suffix,
# *              for example, {@code "'#'#"} formats 123 to
# *              {@code "#123"}.  To create a single quote
# *              itself, use two in a row: {@code "# o''clock"}.
# * </tbody>
# * </table>
# * </blockquote>
# *
# * <h3>Maximum Digits Derivation</h3>
# * For any given {@code DecimalFormat} pattern, if the pattern is not
# * in scientific notation, the maximum number of integer digits will not be
# * derived from the pattern, and instead set to {@link Integer#MAX_VALUE}.
# * Otherwise, if the pattern is in scientific notation, the maximum number of
# * integer digits will be derived from the pattern. This derivation is detailed
# * in the {@link ##scientific_notation Scientific Notation} section. {@link
# * #setMaximumIntegerDigits(int)} can be used to manually adjust the maximum
# * integer digits.
# *
# * <h3>Negative Subpatterns</h3>
# * A {@code DecimalFormat} pattern contains a positive and negative
# * subpattern, for example, {@code "#,##0.00;(#,##0.00)"}.  Each
# * subpattern has a prefix, numeric part, and suffix. The negative subpattern
# * is optional; if absent, then the positive subpattern prefixed with the
# * minus sign {@code '-' (U+002D HYPHEN-MINUS)} is used as the
# * negative subpattern. That is, {@code "0.00"} alone is equivalent to
# * {@code "0.00;-0.00"}.  If there is an explicit negative subpattern, it
# * serves only to specify the negative prefix and suffix; the number of digits,
# * minimal digits, and other characteristics are all the same as the positive
# * pattern. That means that {@code "#,##0.0#;(#)"} produces precisely
# * the same behavior as {@code "#,##0.0#;(#,##0.0#)"}.
# *
# * <p>The prefixes, suffixes, and various symbols used for infinity, digits,
# * grouping separators, decimal separators, etc. may be set to arbitrary
# * values, and they will appear properly during formatting.  However, care must
# * be taken that the symbols and strings do not conflict, or parsing will be
# * unreliable.  For example, either the positive and negative prefixes or the
# * suffixes must be distinct for {@code DecimalFormat.parse()} to be able
# * to distinguish positive from negative values.  (If they are identical, then
# * {@code DecimalFormat} will behave as if no negative subpattern was
# * specified.)  Another example is that the decimal separator and grouping
# * separator should be distinct characters, or parsing will be impossible.
# *
# * <h3>Grouping Separator</h3>
# * <p>The grouping separator is commonly used for thousands, but in some
# * locales it separates ten-thousands. The grouping size is a constant number
# * of digits between the grouping characters, such as 3 for 100,000,000 or 4 for
# * 1,0000,0000. If you supply a pattern with multiple grouping characters, the
# * interval between the last one and the end of the integer is the one that is
# * used. For example, {@code "#,##,###,####"} == {@code "######,####"} ==
# * {@code "##,####,####"}.
# *
# * <h3 id="scientific_notation">Scientific Notation</h3>
# *
# * <p>Numbers in scientific notation are expressed as the product of a mantissa
# * and a power of ten, for example, 1234 can be expressed as 1.234 x 10^3.  The
# * mantissa is often in the range 1.0 &le; x {@literal <} 10.0, but it need not
# * be.
# * {@code DecimalFormat} can be instructed to format and parse scientific
# * notation <em>only via a pattern</em>; there is currently no factory method
# * that creates a scientific notation format.  In a pattern, the exponent
# * character immediately followed by one or more digit characters indicates
# * scientific notation.  Example: {@code "0.###E0"} formats the number
# * 1234 as {@code "1.234E3"}.
# *
# * <ul>
# * <li>The number of digit characters after the exponent character gives the
# * minimum exponent digit count.  There is no maximum.  Negative exponents are
# * formatted using the localized minus sign, <em>not</em> the prefix and suffix
# * from the pattern.  This allows patterns such as {@code "0.###E0 m/s"}.
# *
# * <li>The <em>maximum integer</em> digits is the sum of '0's and '#'s
# * prior to the decimal point. The <em>minimum integer</em> digits is the
# * sum of the '0's prior to the decimal point. The <em>maximum fraction</em>
# * and <em>minimum fraction</em> digits follow the same rules, but apply to the
# * digits after the decimal point but before the exponent. For example, the
# * following pattern: {@code "#00.0####E0"} would have a minimum number of
# * integer digits = 2("00") and a maximum number of integer digits = 3("#00"). It
# * would have a minimum number of fraction digits = 1("0") and a maximum number of fraction
# * digits= 5("0####").
# *
# * <li>The minimum and maximum number of integer digits are interpreted
# * together:
# *
# * <ul>
# * <li>If the maximum number of integer digits is greater than their minimum number
# * and greater than 1, it forces the exponent to be a multiple of the maximum
# * number of integer digits, and the minimum number of integer digits to be
# * interpreted as 1.  The most common use of this is to generate
# * <em>engineering notation</em>, in which the exponent is a multiple of three,
# * e.g., {@code "##0.#####E0"}. Using this pattern, the number 12345
# * formats to {@code "12.345E3"}, and 123456 formats to
# * {@code "123.456E3"}.
# *
# * <li>Otherwise, the minimum number of integer digits is achieved by adjusting the
# * exponent.  Example: 0.00123 formatted with {@code "00.###E0"} yields
# * {@code "12.3E-4"}.
# * </ul>
# *
# * <li>For a given number, the amount of significant digits in
# * the mantissa can be calculated as such
# *
# * <blockquote><pre>
# * <i>Mantissa Digits:</i>
# *         min(max(Minimum Pattern Digits, Original Number Digits), Maximum Pattern Digits)
# * <i>Minimum pattern Digits:</i>
# *         <i>Minimum Integer Digits</i> + <i>Minimum Fraction Digits</i>
# * <i>Maximum pattern Digits:</i>
# *         <i>Maximum Integer Digits</i> + <i>Maximum Fraction Digits</i>
# * <i>Original Number Digits:</i>
# *         The amount of significant digits in the number to be formatted
# * </pre></blockquote>
# *
# * This means that generally, a mantissa will have up to the combined maximum integer
# * and fraction digits, if the original number itself has enough significant digits. However,
# * if there are more minimum pattern digits than significant digits in the original number,
# * the mantissa will have significant digits that equals the combined
# * minimum integer and fraction digits. The number of significant digits
# * does not affect parsing.
# *
# * <p>It should be noted, that the integer portion of the mantissa will give
# * any excess digits to the fraction portion, whether it be for precision or
# * for satisfying the total amount of combined minimum digits.
# *
# * <p>This behavior can be observed in the following example,
# * {@snippet lang=java :
# *     DecimalFormat df = new DecimalFormat("#000.000##E0")
# *     df.format(12); // returns "12.0000E0"
# *     df.format(123456789) // returns "1.23456789E8"
# * }
# *
# * <li>Exponential patterns may not contain grouping separators.
# * </ul>
# *
# * @spec         https://www.unicode.org/reports/tr35
# *               Unicode Locale Data Markup Language (LDML)
# * @see          <a href="http://docs.oracle.com/javase/tutorial/i18n/format/decimalFormat.html">Java Tutorial</a>
# * @see          NumberFormat
# * @see          DecimalFormatSymbols
# * @see          ParsePosition
# * @see          Locale
# * @author       Mark Davis
# * @author       Alan Liu
# * @since 1.1
# 
class DecimalFormat(NumberFormat):

    def _initialize_instance_fields(self):
        # instance fields found by Java to Python Converter:
        self._bigIntegerMultiplier = None
        self._bigDecimalMultiplier = None
        self._digitList = DigitList()
        self._positivePrefix = ""
        self._positiveSuffix = ""
        self._negativePrefix = "-"
        self._negativeSuffix = ""
        self._posPrefixPattern = None
        self._posSuffixPattern = None
        self._negPrefixPattern = None
        self._negSuffixPattern = None
        self._multiplier = 1
        self._groupingSize = 3
        self._decimalSeparatorAlwaysShown = False
        self._parseBigDecimal = False
        self._isCurrencyFormat = False
        self._symbols = None
        self._useExponentialNotation = False
        self._parseStrict = False
        self._positivePrefixFieldPositions = None
        self._positiveSuffixFieldPositions = None
        self._negativePrefixFieldPositions = None
        self._negativeSuffixFieldPositions = None
        self._minExponentDigits = 0
        self._maximumIntegerDigits = super().getMaximumIntegerDigits()
        self._minimumIntegerDigits = super().getMinimumIntegerDigits()
        self._maximumFractionDigits = super().getMaximumFractionDigits()
        self._minimumFractionDigits = super().getMinimumFractionDigits()
        self._roundingMode = java.math.RoundingMode.HALF_EVEN
        self._isFastPath = False
        self._fastPathCheckNeeded = True
        self._fastPathData = None
        self._serialVersionOnStream = java.text.DecimalFormat.CURRENT_SERIAL_VERSION


    #    *
    #     * Creates a DecimalFormat using the default pattern and symbols
    #     * for the default {@link java.util.Locale.Category#FORMAT FORMAT} locale.
    #     * This is a convenient way to obtain a
    #     * DecimalFormat when internationalization is not the main concern.
    #     * <p>
    #     * To obtain standard formats for a given locale, use the factory methods
    #     * on NumberFormat such as getNumberInstance. These factories will
    #     * return the most appropriate sub-class of NumberFormat for a given
    #     * locale.
    #     *
    #     * @see java.text.NumberFormat#getInstance
    #     * @see java.text.NumberFormat#getNumberInstance
    #     * @see java.text.NumberFormat#getCurrencyInstance
    #     * @see java.text.NumberFormat#getPercentInstance
    #     
# JAVA TO PYTHON CONVERTER TASK: Java annotations have no direct Python equivalent:
# ORIGINAL LINE: @SuppressWarnings("this-escape") public DecimalFormat()
# JAVA TO PYTHON CONVERTER TASK: There is no Python equivalent to multiple constructors:
    def __init__(self):
        self._initialize_instance_fields()

        # Get the pattern for the default locale.
        def_ = java.util.Locale.getDefault(java.util.Locale.Category.FORMAT)
        adapter = sun.util.locale.provider.LocaleProviderAdapter.getAdapter(java.text.spi.NumberFormatProvider.class, def_)
        if not(isinstance(adapter, sun.util.locale.provider.ResourceBundleBasedAdapter)):
            adapter = sun.util.locale.provider.LocaleProviderAdapter.getResourceBundleBased()
        all = adapter.getLocaleResources(def_).getNumberPatterns()

        # Always applyPattern after the symbols are set
        self._symbols = DecimalFormatSymbols.getInstance(def_)
        self._applyPattern(all[0], False)


    #    *
    #     * Creates a DecimalFormat using the given pattern and the symbols
    #     * for the default {@link java.util.Locale.Category#FORMAT FORMAT} locale.
    #     * This is a convenient way to obtain a
    #     * DecimalFormat when internationalization is not the main concern.
    #     * The number of maximum integer digits is usually not derived from the pattern.
    #     * See the note in the {@link ##patterns Patterns} section for more detail.
    #     * <p>
    #     * To obtain standard formats for a given locale, use the factory methods
    #     * on NumberFormat such as getNumberInstance. These factories will
    #     * return the most appropriate sub-class of NumberFormat for a given
    #     * locale.
    #     *
    #     * @param pattern a non-localized pattern string.
    #     * @throws    NullPointerException if {@code pattern} is null
    #     * @throws    IllegalArgumentException if the given pattern is invalid.
    #     * @see java.text.NumberFormat#getInstance
    #     * @see java.text.NumberFormat#getNumberInstance
    #     * @see java.text.NumberFormat#getCurrencyInstance
    #     * @see java.text.NumberFormat#getPercentInstance
    #     
# JAVA TO PYTHON CONVERTER TASK: Java annotations have no direct Python equivalent:
# ORIGINAL LINE: @SuppressWarnings("this-escape") public DecimalFormat(String pattern)
# JAVA TO PYTHON CONVERTER TASK: There is no Python equivalent to multiple constructors:
    def __init__(self, pattern):
        self._initialize_instance_fields()

        # Always applyPattern after the symbols are set
        self._symbols = DecimalFormatSymbols.getInstance(java.util.Locale.getDefault(java.util.Locale.Category.FORMAT))
        self._applyPattern(pattern, False)


    #    *
    #     * Creates a DecimalFormat using the given pattern and symbols.
    #     * Use this constructor when you need to completely customize the
    #     * behavior of the format.
    #     * The number of maximum integer digits is usually not derived from the pattern.
    #     * See the note in the {@link ##patterns Patterns} section for more detail.
    #     * <p>
    #     * To obtain standard formats for a given
    #     * locale, use the factory methods on NumberFormat such as
    #     * getInstance or getCurrencyInstance. If you need only minor adjustments
    #     * to a standard format, you can modify the format returned by
    #     * a NumberFormat factory method.
    #     *
    #     * @param pattern a non-localized pattern string
    #     * @param symbols the set of symbols to be used
    #     * @throws    NullPointerException if any of the given arguments is null
    #     * @throws    IllegalArgumentException if the given pattern is invalid
    #     * @see java.text.NumberFormat#getInstance
    #     * @see java.text.NumberFormat#getNumberInstance
    #     * @see java.text.NumberFormat#getCurrencyInstance
    #     * @see java.text.NumberFormat#getPercentInstance
    #     * @see java.text.DecimalFormatSymbols
    #     
# JAVA TO PYTHON CONVERTER TASK: Java annotations have no direct Python equivalent:
# ORIGINAL LINE: @SuppressWarnings("this-escape") public DecimalFormat(String pattern, DecimalFormatSymbols symbols)
# JAVA TO PYTHON CONVERTER TASK: There is no Python equivalent to multiple constructors:
    def __init__(self, pattern, symbols):
        self._initialize_instance_fields()

        # Always applyPattern after the symbols are set
        self._symbols = symbols.clone()
        self._applyPattern(pattern, False)


    # Overrides
    #    *
    #     * Formats a number and appends the resulting text to the given string
    #     * buffer.
    #     * The number can be of any subclass of {@link java.lang.Number}.
    #     * <p>
    #     * This implementation uses the maximum precision permitted.
    #     * @param number     the number to format
    #     * @param toAppendTo the {@code StringBuffer} to which the formatted
    #     *                   text is to be appended
    #     * @param pos        keeps track on the position of the field within the
    #     *                   returned string. For example, for formatting a number
    #     *                   {@code 1234567.89} in {@code Locale.US} locale,
    #     *                   if the given {@code fieldPosition} is
    #     *                   {@link NumberFormat#INTEGER_FIELD}, the begin index
    #     *                   and end index of {@code fieldPosition} will be set
    #     *                   to 0 and 9, respectively for the output string
    #     *                   {@code 1,234,567.89}.
    #     * @return           the value passed in as {@code toAppendTo}
    #     * @throws           IllegalArgumentException if {@code number} is
    #     *                   null or not an instance of {@code Number}.
    #     * @throws           NullPointerException if {@code toAppendTo} or
    #     *                   {@code pos} is null
    #     * @throws           ArithmeticException if rounding is needed with rounding
    #     *                   mode being set to RoundingMode.UNNECESSARY
    #     * @see              java.text.FieldPosition
    #     
# JAVA TO PYTHON CONVERTER TASK: Python does not allow method overloads:
    def format(self, number, toAppendTo, pos):
        if isinstance(number, Long) or isinstance(number, Integer) or isinstance(number, Short) or isinstance(number, Byte) or isinstance(number, java.util.concurrent.atomic.AtomicInteger) or isinstance(number, java.util.concurrent.atomic.AtomicLong) or (isinstance(number, java.math.BigInteger) and (number).bitLength() < 64):
            return self.format((number).longValue(), toAppendTo, pos)
        elif isinstance(number, java.math.BigDecimal):
            return self._format(number, toAppendTo, pos)
        elif isinstance(number, java.math.BigInteger):
            return self._format(number, toAppendTo, pos)
        elif isinstance(number, Number):
            return self.format((number).doubleValue(), toAppendTo, pos)
        else:
            raise IllegalArgumentException("Cannot format given Object as a Number")

    #    *
    #     * Formats a double to produce a string.
    #     * @param number    The double to format
    #     * @param result    where the text is to be appended
    #     * @param fieldPosition    keeps track on the position of the field within
    #     *                         the returned string. For example, for formatting
    #     *                         a number {@code 1234567.89} in {@code Locale.US}
    #     *                         locale, if the given {@code fieldPosition} is
    #     *                         {@link NumberFormat#INTEGER_FIELD}, the begin index
    #     *                         and end index of {@code fieldPosition} will be set
    #     *                         to 0 and 9, respectively for the output string
    #     *                         {@code 1,234,567.89}.
    #     * @throws    NullPointerException if {@code result} or
    #     *            {@code fieldPosition} is {@code null}
    #     * @throws    ArithmeticException if rounding is needed with rounding
    #     *            mode being set to RoundingMode.UNNECESSARY
    #     * @return The formatted number string
    #     * @see java.text.FieldPosition
    #     
# JAVA TO PYTHON CONVERTER TASK: Python does not allow method overloads:
    def format(self, number, result, fieldPosition):
        # If fieldPosition is a DontCareFieldPosition instance we can
        # try to go to fast-path code.
        tryFastPath = False
        if fieldPosition is DontCareFieldPosition.INSTANCE:
            tryFastPath = True
        else:
            fieldPosition.setBeginIndex(0)
            fieldPosition.setEndIndex(0)

        if tryFastPath:
            tempResult = self.fastFormat(number)
            if tempResult is not None:
                result.append(tempResult)
                return result

        # if fast-path could not work, we fallback to standard code.
        return format(number, result, fieldPosition.getFieldDelegate())

    #    *
    #     * Formats a double to produce a string.
    #     * @param number    The double to format
    #     * @param result    where the text is to be appended
    #     * @param delegate notified of locations of sub fields
    #     * @throws          ArithmeticException if rounding is needed with rounding
    #     *                  mode being set to RoundingMode.UNNECESSARY
    #     * @return The formatted number string
    #     
# JAVA TO PYTHON CONVERTER TASK: Python does not allow method overloads:
    def format(self, number, result, delegate):

        nanOrInfinity = self.handleNaN(number, result, delegate)
        if nanOrInfinity:
            return result

        #         Detecting whether a double is negative is easy with the exception of
        #         * the value -0.0.  This is a double which has a zero mantissa (and
        #         * exponent), but a negative sign bit.  It is semantically distinct from
        #         * a zero with a positive sign bit, and this distinction is important
        #         * to certain kinds of computations.  However, it's a little tricky to
        #         * detect, since (-0.0 == 0.0) and !(-0.0 < 0.0).  How then, you may
        #         * ask, does it behave distinctly from +0.0?  Well, 1/(-0.0) ==
        #         * -Infinity.  Proper detection of -0.0 is needed to deal with the
        #         * issues raised by bugs 4106658, 4106667, and 4147706.  Liu 7/6/98.
        #         
        isNegative = ((number < 0.0) or (number == 0.0 and 1 / number < 0.0)) ^ (self._multiplier < 0)

        if self._multiplier != 1:
            number *= self._multiplier

        nanOrInfinity = self.handleInfinity(number, result, delegate, isNegative)
        if nanOrInfinity:
            return result

        if isNegative:
            number = -number

        # at this point we are guaranteed a nonnegative finite number.
        assert (number >= 0 and (not Double.isInfinite(number)))
        return self.doubleSubformat(number, result, delegate, isNegative)

    #    *
    #     * Checks if the given {@code number} is {@code Double.NaN}. if yes
    #     * appends the NaN symbol to the result string. The NaN string is
    #     * determined by the DecimalFormatSymbols object.
    #     * @param number the double number to format
    #     * @param result where the text is to be appended
    #     * @param delegate notified of locations of sub fields
    #     * @return true, if number is a NaN; false otherwise
    #     
    def handleNaN(self, number, result, delegate):
        if Double.isNaN(number) or (Double.isInfinite(number) and self._multiplier == 0):
            iFieldStart = result.length()
            result.append(self._symbols.getNaN())
            delegate.formatted(java.text.DecimalFormat.INTEGER_FIELD, Field.INTEGER, Field.INTEGER, iFieldStart, result.length(), result)
            return True
        return False

    #    *
    #     * Checks if the given {@code number} is {@code Double.NEGATIVE_INFINITY}
    #     * or {@code Double.POSITIVE_INFINITY}. if yes
    #     * appends the infinity string to the result string. The infinity string is
    #     * determined by the DecimalFormatSymbols object.
    #     * @param number the double number to format
    #     * @param result where the text is to be appended
    #     * @param delegate notified of locations of sub fields
    #     * @param isNegative whether the given {@code number} is negative
    #     * @return true, if number is a {@code Double.NEGATIVE_INFINITY} or
    #     *         {@code Double.POSITIVE_INFINITY}; false otherwise
    #     
    def handleInfinity(self, number, result, delegate, isNegative):
        if Double.isInfinite(number):
            if isNegative:
                self._append(result, self._negativePrefix, delegate, self._getNegativePrefixFieldPositions(), Field.SIGN)
            else:
                self._append(result, self._positivePrefix, delegate, self._getPositivePrefixFieldPositions(), Field.SIGN)

            iFieldStart = result.length()
            result.append(self._symbols.getInfinity())
            delegate.formatted(java.text.DecimalFormat.INTEGER_FIELD, Field.INTEGER, Field.INTEGER, iFieldStart, result.length(), result)

            if isNegative:
                self._append(result, self._negativeSuffix, delegate, self._getNegativeSuffixFieldPositions(), Field.SIGN)
            else:
                self._append(result, self._positiveSuffix, delegate, self._getPositiveSuffixFieldPositions(), Field.SIGN)

            return True
        return False

    def doubleSubformat(self, number, result, delegate, isNegative):
# JAVA TO PYTHON CONVERTER TASK: Synchronized blocks are not converted by Java to Python Converter:
        synchronized(self._digitList)
            maxIntDigits = super().getMaximumIntegerDigits()
            minIntDigits = super().getMinimumIntegerDigits()
            maxFraDigits = super().getMaximumFractionDigits()
            minFraDigits = super().getMinimumFractionDigits()

            self._digitList.set(isNegative, number,maxIntDigits + maxFraDigits if self._useExponentialNotation else maxFraDigits, (not self._useExponentialNotation))
            return self._subformat(result, delegate, isNegative, False, maxIntDigits, minIntDigits, maxFraDigits, minFraDigits)

    #    *
    #     * Format a long to produce a string.
    #     * @param number    The long to format
    #     * @param result    where the text is to be appended
    #     * @param fieldPosition    keeps track on the position of the field within
    #     *                         the returned string. For example, for formatting
    #     *                         a number {@code 123456789} in {@code Locale.US}
    #     *                         locale, if the given {@code fieldPosition} is
    #     *                         {@link NumberFormat#INTEGER_FIELD}, the begin index
    #     *                         and end index of {@code fieldPosition} will be set
    #     *                         to 0 and 11, respectively for the output string
    #     *                         {@code 123,456,789}.
    #     * @throws          NullPointerException if {@code result} or
    #     *                  {@code fieldPosition} is {@code null}
    #     * @throws          ArithmeticException if rounding is needed with rounding
    #     *                  mode being set to RoundingMode.UNNECESSARY
    #     * @return The formatted number string
    #     * @see java.text.FieldPosition
    #     
# JAVA TO PYTHON CONVERTER TASK: Python does not allow method overloads:
    def format(self, number, result, fieldPosition):
        fieldPosition.setBeginIndex(0)
        fieldPosition.setEndIndex(0)

        return format(number, result, fieldPosition.getFieldDelegate())

    #    *
    #     * Format a long to produce a string.
    #     * @param number    The long to format
    #     * @param result    where the text is to be appended
    #     * @param delegate notified of locations of sub fields
    #     * @return The formatted number string
    #     * @throws           ArithmeticException if rounding is needed with rounding
    #     *                   mode being set to RoundingMode.UNNECESSARY
    #     * @see java.text.FieldPosition
    #     
# JAVA TO PYTHON CONVERTER TASK: Python does not allow method overloads:
    def format(self, number, result, delegate):
        isNegative = (number < 0)
        if isNegative:
            number = -number

        # In general, long values always represent real finite numbers, so
        # we don't have to check for +/- Infinity or NaN.  However, there
        # is one case we have to be careful of:  The multiplier can push
        # a number near MIN_VALUE or MAX_VALUE outside the legal range.  We
        # check for this before multiplying, and if it happens we use
        # BigInteger instead.
        useBigInteger = False
        if number < 0:
            if self._multiplier != 0:
                useBigInteger = True
        elif self._multiplier != 1 and self._multiplier != 0:
# JAVA TO PYTHON CONVERTER TASK: Java to Python Converter cannot determine whether both operands of this division are integer types - if they are then you should change 'lhs / rhs' to 'math.trunc(lhs / float(rhs))':
            cutoff = Long.MAX_VALUE / self._multiplier
            if cutoff < 0:
                cutoff = -cutoff
            useBigInteger = (number > cutoff)

        if useBigInteger:
            if isNegative:
                number = -number
            bigIntegerValue = java.math.BigInteger.valueOf(number)
            return self.format(bigIntegerValue, result, delegate, True)

        number *= self._multiplier
        if number == 0:
            isNegative = False
        else:
            if self._multiplier < 0:
                number = -number
                isNegative = not isNegative

# JAVA TO PYTHON CONVERTER TASK: Synchronized blocks are not converted by Java to Python Converter:
        synchronized(self._digitList)
            maxIntDigits = super().getMaximumIntegerDigits()
            minIntDigits = super().getMinimumIntegerDigits()
            maxFraDigits = super().getMaximumFractionDigits()
            minFraDigits = super().getMinimumFractionDigits()

            self._digitList.set(isNegative, number,maxIntDigits + maxFraDigits if self._useExponentialNotation else 0)

            return self._subformat(result, delegate, isNegative, True, maxIntDigits, minIntDigits, maxFraDigits, minFraDigits)

    #    *
    #     * Formats a BigDecimal to produce a string.
    #     * @param number    The BigDecimal to format
    #     * @param result    where the text is to be appended
    #     * @param fieldPosition    keeps track on the position of the field within
    #     *                         the returned string. For example, for formatting
    #     *                         a number {@code 1234567.89} in {@code Locale.US}
    #     *                         locale, if the given {@code fieldPosition} is
    #     *                         {@link NumberFormat#INTEGER_FIELD}, the begin index
    #     *                         and end index of {@code fieldPosition} will be set
    #     *                         to 0 and 9, respectively for the output string
    #     *                         {@code 1,234,567.89}.
    #     * @return The formatted number string
    #     * @throws           ArithmeticException if rounding is needed with rounding
    #     *                   mode being set to RoundingMode.UNNECESSARY
    #     * @see java.text.FieldPosition
    #     
# JAVA TO PYTHON CONVERTER TASK: Python does not allow method overloads:
    def _format(self, number, result, fieldPosition):
        fieldPosition.setBeginIndex(0)
        fieldPosition.setEndIndex(0)
        return format(number, result, fieldPosition.getFieldDelegate())

    #    *
    #     * Formats a BigDecimal to produce a string.
    #     * @param number    The BigDecimal to format
    #     * @param result    where the text is to be appended
    #     * @param delegate notified of locations of sub fields
    #     * @throws           ArithmeticException if rounding is needed with rounding
    #     *                   mode being set to RoundingMode.UNNECESSARY
    #     * @return The formatted number string
    #     
# JAVA TO PYTHON CONVERTER TASK: Python does not allow method overloads:
    def format(self, number, result, delegate):
        if self._multiplier != 1:
            number = number.multiply(self._getBigDecimalMultiplier())
        isNegative = number.signum() == -1
        if isNegative:
            number = number.negate()

# JAVA TO PYTHON CONVERTER TASK: Synchronized blocks are not converted by Java to Python Converter:
        synchronized(self._digitList)
            maxIntDigits = self.getMaximumIntegerDigits()
            minIntDigits = self.getMinimumIntegerDigits()
            maxFraDigits = self.getMaximumFractionDigits()
            minFraDigits = self.getMinimumFractionDigits()
            maximumDigits = maxIntDigits + maxFraDigits

            self._digitList.set(isNegative, number,(Integer.MAX_VALUE if (maximumDigits < 0) else maximumDigits) if self._useExponentialNotation else maxFraDigits, (not self._useExponentialNotation))

            return self._subformat(result, delegate, isNegative, False, maxIntDigits, minIntDigits, maxFraDigits, minFraDigits)

    #    *
    #     * Format a BigInteger to produce a string.
    #     * @param number    The BigInteger to format
    #     * @param result    where the text is to be appended
    #     * @param fieldPosition    keeps track on the position of the field within
    #     *                         the returned string. For example, for formatting
    #     *                         a number {@code 123456789} in {@code Locale.US}
    #     *                         locale, if the given {@code fieldPosition} is
    #     *                         {@link NumberFormat#INTEGER_FIELD}, the begin index
    #     *                         and end index of {@code fieldPosition} will be set
    #     *                         to 0 and 11, respectively for the output string
    #     *                         {@code 123,456,789}.
    #     * @return The formatted number string
    #     * @throws           ArithmeticException if rounding is needed with rounding
    #     *                   mode being set to RoundingMode.UNNECESSARY
    #     * @see java.text.FieldPosition
    #     
# JAVA TO PYTHON CONVERTER TASK: Python does not allow method overloads:
    def _format(self, number, result, fieldPosition):
        fieldPosition.setBeginIndex(0)
        fieldPosition.setEndIndex(0)

        return self.format(number, result, fieldPosition.getFieldDelegate(), False)

    #    *
    #     * Format a BigInteger to produce a string.
    #     * @param number    The BigInteger to format
    #     * @param result    where the text is to be appended
    #     * @param delegate notified of locations of sub fields
    #     * @return The formatted number string
    #     * @throws           ArithmeticException if rounding is needed with rounding
    #     *                   mode being set to RoundingMode.UNNECESSARY
    #     * @see java.text.FieldPosition
    #     
# JAVA TO PYTHON CONVERTER TASK: Python does not allow method overloads:
    def format(self, number, result, delegate, formatLong):
        if self._multiplier != 1:
            number = number.multiply(self._getBigIntegerMultiplier())
        isNegative = number.signum() == -1
        if isNegative:
            number = number.negate()

# JAVA TO PYTHON CONVERTER TASK: Synchronized blocks are not converted by Java to Python Converter:
        synchronized(self._digitList)
            maxIntDigits = 0
            minIntDigits = 0
            maxFraDigits = 0
            minFraDigits = 0
            maximumDigits = 0
            if formatLong:
                maxIntDigits = super().getMaximumIntegerDigits()
                minIntDigits = super().getMinimumIntegerDigits()
                maxFraDigits = super().getMaximumFractionDigits()
                minFraDigits = super().getMinimumFractionDigits()
                maximumDigits = maxIntDigits + maxFraDigits
            else:
                maxIntDigits = self.getMaximumIntegerDigits()
                minIntDigits = self.getMinimumIntegerDigits()
                maxFraDigits = self.getMaximumFractionDigits()
                minFraDigits = self.getMinimumFractionDigits()
                maximumDigits = maxIntDigits + maxFraDigits
                if maximumDigits < 0:
                    maximumDigits = Integer.MAX_VALUE

            self._digitList.set(isNegative, number,maximumDigits if self._useExponentialNotation else 0)

            return self._subformat(result, delegate, isNegative, True, maxIntDigits, minIntDigits, maxFraDigits, minFraDigits)

    #    *
    #     * Formats an Object producing an {@code AttributedCharacterIterator}.
    #     * You can use the returned {@code AttributedCharacterIterator}
    #     * to build the resulting String, as well as to determine information
    #     * about the resulting String.
    #     * <p>
    #     * Each attribute key of the AttributedCharacterIterator will be of type
    #     * {@code NumberFormat.Field}, with the attribute value being the
    #     * same as the attribute key.
    #     *
    #     * @throws    NullPointerException if obj is null.
    #     * @throws    IllegalArgumentException when the Format cannot format the
    #     *            given object.
    #     * @throws           ArithmeticException if rounding is needed with rounding
    #     *                   mode being set to RoundingMode.UNNECESSARY
    #     * @param obj The object to format
    #     * @return AttributedCharacterIterator describing the formatted value.
    #     * @since 1.4
    #     
    def formatToCharacterIterator(self, obj):
        delegate = CharacterIteratorFieldDelegate()
        sb = StringBuffer()

        if isinstance(obj, Double) or isinstance(obj, Float):
            format((obj).doubleValue(), sb, delegate)
        elif isinstance(obj, Long) or isinstance(obj, Integer) or isinstance(obj, Short) or isinstance(obj, Byte) or isinstance(obj, java.util.concurrent.atomic.AtomicInteger) or isinstance(obj, java.util.concurrent.atomic.AtomicLong):
            format((obj).longValue(), sb, delegate)
        elif isinstance(obj, java.math.BigDecimal):
            format(obj, sb, delegate)
        elif isinstance(obj, java.math.BigInteger):
            self.format(obj, sb, delegate, False)
        elif obj is None:
            raise NullPointerException("formatToCharacterIterator must be passed non-null object")
        else:
            raise IllegalArgumentException("Cannot format given Object as a Number")
        return delegate.getIterator(str(sb))

    # ==== Begin fast-path formatting logic for double =========================

    #     Fast-path formatting will be used for format(double ...) methods iff a
    #     * number of conditions are met (see checkAndSetFastPathStatus()):
    #     * - Only if instance properties meet the right predefined conditions.
    #     * - The abs value of the double to format is <= Integer.MAX_VALUE.
    #     *
    #     * The basic approach is to split the binary to decimal conversion of a
    #     * double value into two phases:
    #     * * The conversion of the integer portion of the double.
    #     * * The conversion of the fractional portion of the double
    #     *   (limited to two or three digits).
    #     *
    #     * The isolation and conversion of the integer portion of the double is
    #     * straightforward. The conversion of the fraction is more subtle and relies
    #     * on some rounding properties of double to the decimal precisions in
    #     * question.  Using the terminology of BigDecimal, this fast-path algorithm
    #     * is applied when a double value has a magnitude less than Integer.MAX_VALUE
    #     * and rounding is to nearest even and the destination format has two or
    #     * three digits of *scale* (digits after the decimal point).
    #     *
    #     * Under a rounding to nearest even policy, the returned result is a digit
    #     * string of a number in the (in this case decimal) destination format
    #     * closest to the exact numerical value of the (in this case binary) input
    #     * value.  If two destination format numbers are equally distant, the one
    #     * with the last digit even is returned.  To compute such a correctly rounded
    #     * value, some information about digits beyond the smallest returned digit
    #     * position needs to be consulted.
    #     *
    #     * In general, a guard digit, a round digit, and a sticky *bit* are needed
    #     * beyond the returned digit position.  If the discarded portion of the input
    #     * is sufficiently large, the returned digit string is incremented.  In round
    #     * to nearest even, this threshold to increment occurs near the half-way
    #     * point between digits.  The sticky bit records if there are any remaining
    #     * trailing digits of the exact input value in the new format; the sticky bit
    #     * is consulted only in close to half-way rounding cases.
    #     *
    #     * Given the computation of the digit and bit values, rounding is then
    #     * reduced to a table lookup problem.  For decimal, the even/odd cases look
    #     * like this:
    #     *
    #     * Last   Round   Sticky
    #     * 6      5       0      => 6   // exactly halfway, return even digit.
    #     * 6      5       1      => 7   // a little bit more than halfway, round up.
    #     * 7      5       0      => 8   // exactly halfway, round up to even.
    #     * 7      5       1      => 8   // a little bit more than halfway, round up.
    #     * With analogous entries for other even and odd last-returned digits.
    #     *
    #     * However, decimal negative powers of 5 smaller than 0.5 are *not* exactly
    #     * representable as binary fraction.  In particular, 0.005 (the round limit
    #     * for a two-digit scale) and 0.0005 (the round limit for a three-digit
    #     * scale) are not representable. Therefore, for input values near these cases
    #     * the sticky bit is known to be set which reduces the rounding logic to:
    #     *
    #     * Last   Round   Sticky
    #     * 6      5       1      => 7   // a little bit more than halfway, round up.
    #     * 7      5       1      => 8   // a little bit more than halfway, round up.
    #     *
    #     * In other words, if the round digit is 5, the sticky bit is known to be
    #     * set.  If the round digit is something other than 5, the sticky bit is not
    #     * relevant.  Therefore, some of the logic about whether or not to increment
    #     * the destination *decimal* value can occur based on tests of *binary*
    #     * computations of the binary input number.
    #     

    #    *
    #     * Check validity of using fast-path for this instance. If fast-path is valid
    #     * for this instance, sets fast-path state as true and initializes fast-path
    #     * utility fields as needed.
    #     *
    #     * This method is supposed to be called rarely, otherwise that will break the
    #     * fast-path performance. That means avoiding frequent changes of the
    #     * properties of the instance, since for most properties, each time a change
    #     * happens, a call to this method is needed at the next format call.
    #     *
    #     * FAST-PATH RULES:
    #     *  Similar to the default DecimalFormat instantiation case.
    #     *  More precisely:
    #     *  - HALF_EVEN rounding mode,
    #     *  - isGroupingUsed() is true,
    #     *  - groupingSize of 3,
    #     *  - multiplier is 1,
    #     *  - Decimal separator not mandatory,
    #     *  - No use of exponential notation,
    #     *  - minimumIntegerDigits is exactly 1 and maximumIntegerDigits at least 10
    #     *  - For number of fractional digits, the exact values found in the default case:
    #     *     Currency : min = max = 2.
    #     *     Decimal  : min = 0. max = 3.
    #     *
    #     
    def _checkAndSetFastPathStatus(self):

        fastPathWasOn = self._isFastPath

        if (self._roundingMode is java.math.RoundingMode.HALF_EVEN) and (self.isGroupingUsed()) and (self._groupingSize == 3) and (self._multiplier == 1) and (not self._decimalSeparatorAlwaysShown) and (not self._useExponentialNotation):

            # The fast-path algorithm is semi-hardcoded against
            #  minimumIntegerDigits and maximumIntegerDigits.
            self._isFastPath = ((self._minimumIntegerDigits == 1) and (self._maximumIntegerDigits >= 10))

            # The fast-path algorithm is hardcoded against
            #  minimumFractionDigits and maximumFractionDigits.
            if self._isFastPath:
                if self._isCurrencyFormat:
                    if (self._minimumFractionDigits != 2) or (self._maximumFractionDigits != 2):
                        self._isFastPath = False
                elif (self._minimumFractionDigits != 0) or (self._maximumFractionDigits != 3):
                    self._isFastPath = False
        else:
            self._isFastPath = False

        self._resetFastPathData(fastPathWasOn)
        self._fastPathCheckNeeded = False

        #        
        #         * Returns true after successfully checking the fast path condition and
        #         * setting the fast path data. The return value is used by the
        #         * fastFormat() method to decide whether to call the resetFastPathData
        #         * method to reinitialize fast path data or is it already initialized
        #         * in this method.
        #         
        return True

    def _resetFastPathData(self, fastPathWasOn):
        # Since some instance properties may have changed while still falling
        # in the fast-path case, we need to reinitialize fastPathData anyway.
        if self._isFastPath:
            # We need to instantiate fastPathData if not already done.
            if self._fastPathData is None:
                self._fastPathData = FastPathData()

            # Sets up the locale specific constants used when formatting.
            # '0' is our default representation of zero.
            self._fastPathData.zeroDelta = self._symbols.getZeroDigit() - '0'
            self._fastPathData.groupingChar = self._symbols.getMonetaryGroupingSeparator() if self._isCurrencyFormat else self._symbols.getGroupingSeparator()

            # Sets up fractional constants related to currency/decimal pattern.
            self._fastPathData.fractionalMaxIntBound = 99 if (self._isCurrencyFormat) else 999
            self._fastPathData.fractionalScaleFactor = 100.0 if (self._isCurrencyFormat) else 1000.0

            # Records the need for adding prefix or suffix
            self._fastPathData.positiveAffixesRequired = (not len(self._positivePrefix)) > 0 or (not len(self._positiveSuffix)) > 0
            self._fastPathData.negativeAffixesRequired = (not len(self._negativePrefix)) > 0 or (not len(self._negativeSuffix)) > 0

            # Creates a cached char container for result, with max possible size.
            maxNbIntegralDigits = 10
            maxNbGroups = 3
            containerSize = max(len(self._positivePrefix), len(self._negativePrefix)) + maxNbIntegralDigits + maxNbGroups + 1 + self._maximumFractionDigits + max(len(self._positiveSuffix), len(self._negativeSuffix))

            self._fastPathData.fastPathContainer = ['\0' for _ in range(containerSize)]

            # Sets up prefix and suffix char arrays constants.
            self._fastPathData.charsPositiveSuffix = self._positiveSuffix.toCharArray()
            self._fastPathData.charsNegativeSuffix = self._negativeSuffix.toCharArray()
            self._fastPathData.charsPositivePrefix = self._positivePrefix.toCharArray()
            self._fastPathData.charsNegativePrefix = self._negativePrefix.toCharArray()

            # Sets up fixed index positions for integral and fractional digits.
            # Sets up decimal point in cached result container.
            longestPrefixLength = max(len(self._positivePrefix), len(self._negativePrefix))
            decimalPointIndex = maxNbIntegralDigits + maxNbGroups + longestPrefixLength

            self._fastPathData.integralLastIndex = decimalPointIndex - 1
            self._fastPathData.fractionalFirstIndex = decimalPointIndex + 1
            self._fastPathData.fastPathContainer[decimalPointIndex] = self._symbols.getMonetaryDecimalSeparator() if self._isCurrencyFormat else self._symbols.getDecimalSeparator()

        elif fastPathWasOn:
            # Previous state was fast-path and is no more.
            # Resets cached array constants.
            self._fastPathData.fastPathContainer = None
            self._fastPathData.charsPositiveSuffix = None
            self._fastPathData.charsNegativeSuffix = None
            self._fastPathData.charsPositivePrefix = None
            self._fastPathData.charsNegativePrefix = None

    #    *
    #     * Returns true if rounding-up must be done on {@code scaledFractionalPartAsInt},
    #     * false otherwise.
    #     *
    #     * This is a utility method that takes correct half-even rounding decision on
    #     * passed fractional value at the scaled decimal point (2 digits for currency
    #     * case and 3 for decimal case), when the approximated fractional part after
    #     * scaled decimal point is exactly 0.5d.  This is done by means of exact
    #     * calculations on the {@code fractionalPart} floating-point value.
    #     *
    #     * This method is supposed to be called by private {@code fastDoubleFormat}
    #     * method only.
    #     *
    #     * The algorithms used for the exact calculations are :
    #     *
    #     * The <b><i>FastTwoSum</i></b> algorithm, from T.J.Dekker, described in the
    #     * papers  "<i>A  Floating-Point   Technique  for  Extending  the  Available
    #     * Precision</i>"  by Dekker, and  in "<i>Adaptive  Precision Floating-Point
    #     * Arithmetic and Fast Robust Geometric Predicates</i>" from J.Shewchuk.
    #     *
    #     * A modified version of <b><i>Sum2S</i></b> cascaded summation described in
    #     * "<i>Accurate Sum and Dot Product</i>" from Takeshi Ogita and All.  As
    #     * Ogita says in this paper this is an equivalent of the Kahan-Babuska's
    #     * summation algorithm because we order the terms by magnitude before summing
    #     * them. For this reason we can use the <i>FastTwoSum</i> algorithm rather
    #     * than the more expensive Knuth's <i>TwoSum</i>.
    #     *
    #     * We do this to avoid a more expensive exact "<i>TwoProduct</i>" algorithm,
    #     * like those described in Shewchuk's paper above. See comments in the code
    #     * below.
    #     *
    #     * @param  fractionalPart The  fractional value  on which  we  take rounding
    #     * decision.
    #     * @param scaledFractionalPartAsInt The integral part of the scaled
    #     * fractional value.
    #     *
    #     * @return the decision that must be taken regarding half-even rounding.
    #     
    def _exactRoundUp(self, fractionalPart, scaledFractionalPartAsInt):

        #         exactRoundUp() method is called by fastDoubleFormat() only.
        #         * The precondition expected to be verified by the passed parameters is :
        #         * scaledFractionalPartAsInt ==
        #         *     (int) (fractionalPart * fastPathData.fractionalScaleFactor).
        #         * This is ensured by fastDoubleFormat() code.
        #         

        #         We first calculate roundoff error made by fastDoubleFormat() on
        #         * the scaled fractional part. We do this with exact calculation on the
        #         * passed fractionalPart. Rounding decision will then be taken from roundoff.
        #         

        #         ---- TwoProduct(fractionalPart, scale factor (i.e. 1000.0d or 100.0d)).
        #         *
        #         * The below is an optimized exact "TwoProduct" calculation of passed
        #         * fractional part with scale factor, using Ogita's Sum2S cascaded
        #         * summation adapted as Kahan-Babuska equivalent by using FastTwoSum
        #         * (much faster) rather than Knuth's TwoSum.
        #         *
        #         * We can do this because we order the summation from smallest to
        #         * greatest, so that FastTwoSum can be used without any additional error.
        #         *
        #         * The "TwoProduct" exact calculation needs 17 flops. We replace this by
        #         * a cascaded summation of FastTwoSum calculations, each involving an
        #         * exact multiply by a power of 2.
        #         *
        #         * Doing so saves overall 4 multiplications and 1 addition compared to
        #         * using traditional "TwoProduct".
        #         *
        #         * The scale factor is either 100 (currency case) or 1000 (decimal case).
        #         * - when 1000, we replace it by (1024 - 16 - 8) = 1000.
        #         * - when 100,  we replace it by (128  - 32 + 4) =  100.
        #         * Every multiplication by a power of 2 (1024, 128, 32, 16, 8, 4) is exact.
        #         *
        #         
        approxMax = 0 # Will always be positive.
        approxMedium = 0 # Will always be negative.
        approxMin = 0

        fastTwoSumApproximation = 0.0
        fastTwoSumRoundOff = 0.0
        bVirtual = 0.0

        if self._isCurrencyFormat:
            # Scale is 100 = 128 - 32 + 4.
            # Multiply by 2**n is a shift. No roundoff. No error.
            approxMax = fractionalPart * 128.00
            approxMedium = - (fractionalPart * 32.00)
            approxMin = fractionalPart * 4.00
        else:
            # Scale is 1000 = 1024 - 16 - 8.
            # Multiply by 2**n is a shift. No roundoff. No error.
            approxMax = fractionalPart * 1024.00
            approxMedium = - (fractionalPart * 16.00)
            approxMin = - (fractionalPart * 8.00)

        # Shewchuk/Dekker's FastTwoSum(approxMedium, approxMin).
        assert(-approxMedium >= abs(approxMin))
        fastTwoSumApproximation = approxMedium + approxMin
        bVirtual = fastTwoSumApproximation - approxMedium
        fastTwoSumRoundOff = approxMin - bVirtual
        approxS1 = fastTwoSumApproximation
        roundoffS1 = fastTwoSumRoundOff

        # Shewchuk/Dekker's FastTwoSum(approxMax, approxS1)
        assert(approxMax >= abs(approxS1))
        fastTwoSumApproximation = approxMax + approxS1
        bVirtual = fastTwoSumApproximation - approxMax
        fastTwoSumRoundOff = approxS1 - bVirtual
        roundoff1000 = fastTwoSumRoundOff
        approx1000 = fastTwoSumApproximation
        roundoffTotal = roundoffS1 + roundoff1000

        # Shewchuk/Dekker's FastTwoSum(approx1000, roundoffTotal)
        assert(approx1000 >= abs(roundoffTotal))
        fastTwoSumApproximation = approx1000 + roundoffTotal
        bVirtual = fastTwoSumApproximation - approx1000

        # Now we have got the roundoff for the scaled fractional
        scaledFractionalRoundoff = roundoffTotal - bVirtual

        # ---- TwoProduct(fractionalPart, scale (i.e. 1000.0d or 100.0d)) end.

        #         ---- Taking the rounding decision
        #         *
        #         * We take rounding decision based on roundoff and half-even rounding
        #         * rule.
        #         *
        #         * The above TwoProduct gives us the exact roundoff on the approximated
        #         * scaled fractional, and we know that this approximation is exactly
        #         * 0.5d, since that has already been tested by the caller
        #         * (fastDoubleFormat).
        #         *
        #         * Decision comes first from the sign of the calculated exact roundoff.
        #         * - Since being exact roundoff, it cannot be positive with a scaled
        #         *   fractional less than 0.5d, as well as negative with a scaled
        #         *   fractional greater than 0.5d. That leaves us with following 3 cases.
        #         * - positive, thus scaled fractional == 0.500....0fff ==> round-up.
        #         * - negative, thus scaled fractional == 0.499....9fff ==> don't round-up.
        #         * - is zero,  thus scaled fractioanl == 0.5 ==> half-even rounding applies :
        #         *    we round-up only if the integral part of the scaled fractional is odd.
        #         *
        #         
        if scaledFractionalRoundoff > 0.0:
            return True
        elif scaledFractionalRoundoff < 0.0:
            return False
        elif (scaledFractionalPartAsInt & 1) != 0:
            return True

        return False

        # ---- Taking the rounding decision end

    #    *
    #     * Collects integral digits from passed {@code number}, while setting
    #     * grouping chars as needed. Updates {@code firstUsedIndex} accordingly.
    #     *
    #     * Loops downward starting from {@code backwardIndex} position (inclusive).
    #     *
    #     * @param number  The int value from which we collect digits.
    #     * @param digitsBuffer The char array container where digits and grouping chars
    #     *  are stored.
    #     * @param backwardIndex the position from which we start storing digits in
    #     *  digitsBuffer.
    #     *
    #     
    def _collectIntegralDigits(self, number, digitsBuffer, backwardIndex):
        index = backwardIndex
        q = 0
        r = 0
        while number > 999:
            # Generates 3 digits per iteration.
            q = math.trunc(number / float(1000))
            r = number - (q << 10) + (q << 4) + (q << 3) # -1024 +16 +8 = 1000.
            number = q

# JAVA TO PYTHON CONVERTER WARNING: An assignment within expression was extracted from the following statement:
# ORIGINAL LINE: digitsBuffer[index--] = DigitArrays.DigitOnes1000[r];
            digitsBuffer[index] = DigitArrays.DIGIT_ONES1000[r]
            index -= 1
# JAVA TO PYTHON CONVERTER WARNING: An assignment within expression was extracted from the following statement:
# ORIGINAL LINE: digitsBuffer[index--] = DigitArrays.DigitTens1000[r];
            digitsBuffer[index] = DigitArrays.DIGIT_TENS1000[r]
            index -= 1
# JAVA TO PYTHON CONVERTER WARNING: An assignment within expression was extracted from the following statement:
# ORIGINAL LINE: digitsBuffer[index--] = DigitArrays.DigitHundreds1000[r];
            digitsBuffer[index] = DigitArrays.DIGIT_HUNDREDS1000[r]
            index -= 1
# JAVA TO PYTHON CONVERTER WARNING: An assignment within expression was extracted from the following statement:
# ORIGINAL LINE: digitsBuffer[index--] = fastPathData.groupingChar;
            digitsBuffer[index] = self._fastPathData.groupingChar
            index -= 1

        # Collects last 3 or less digits.
        digitsBuffer[index] = DigitArrays.DIGIT_ONES1000[number]
        if number > 9:
            index -= 1
# JAVA TO PYTHON CONVERTER WARNING: An assignment within expression was extracted from the following statement:
# ORIGINAL LINE: digitsBuffer[--index] = DigitArrays.DigitTens1000[number];
            digitsBuffer[index] = DigitArrays.DIGIT_TENS1000[number]
            if number > 99:
                index -= 1
# JAVA TO PYTHON CONVERTER WARNING: An assignment within expression was extracted from the following statement:
# ORIGINAL LINE: digitsBuffer[--index] = DigitArrays.DigitHundreds1000[number];
                digitsBuffer[index] = DigitArrays.DIGIT_HUNDREDS1000[number]

        self._fastPathData.firstUsedIndex = index

    #    *
    #     * Collects the 2 (currency) or 3 (decimal) fractional digits from passed
    #     * {@code number}, starting at {@code startIndex} position
    #     * inclusive.  There is no punctuation to set here (no grouping chars).
    #     * Updates {@code fastPathData.lastFreeIndex} accordingly.
    #     *
    #     *
    #     * @param number  The int value from which we collect digits.
    #     * @param digitsBuffer The char array container where digits are stored.
    #     * @param startIndex the position from which we start storing digits in
    #     *  digitsBuffer.
    #     *
    #     
    def _collectFractionalDigits(self, number, digitsBuffer, startIndex):
        index = startIndex

        digitOnes = DigitArrays.DIGIT_ONES1000[number]
        digitTens = DigitArrays.DIGIT_TENS1000[number]

        if self._isCurrencyFormat:
            # Currency case. Always collects fractional digits.
# JAVA TO PYTHON CONVERTER WARNING: An assignment within expression was extracted from the following statement:
# ORIGINAL LINE: digitsBuffer[index++] = digitTens;
            digitsBuffer[index] = digitTens
            index += 1
# JAVA TO PYTHON CONVERTER WARNING: An assignment within expression was extracted from the following statement:
# ORIGINAL LINE: digitsBuffer[index++] = digitOnes;
            digitsBuffer[index] = digitOnes
            index += 1
        elif number != 0:
            # Decimal case. Hundreds will always be collected
# JAVA TO PYTHON CONVERTER WARNING: An assignment within expression was extracted from the following statement:
# ORIGINAL LINE: digitsBuffer[index++] = DigitArrays.DigitHundreds1000[number];
            digitsBuffer[index] = DigitArrays.DIGIT_HUNDREDS1000[number]
            index += 1

            # Ending zeros won't be collected.
            if digitOnes != '0':
# JAVA TO PYTHON CONVERTER WARNING: An assignment within expression was extracted from the following statement:
# ORIGINAL LINE: digitsBuffer[index++] = digitTens;
                digitsBuffer[index] = digitTens
                index += 1
# JAVA TO PYTHON CONVERTER WARNING: An assignment within expression was extracted from the following statement:
# ORIGINAL LINE: digitsBuffer[index++] = digitOnes;
                digitsBuffer[index] = digitOnes
                index += 1
            elif digitTens != '0':
# JAVA TO PYTHON CONVERTER WARNING: An assignment within expression was extracted from the following statement:
# ORIGINAL LINE: digitsBuffer[index++] = digitTens;
                digitsBuffer[index] = digitTens
                index += 1

        else:
            # This is decimal pattern and fractional part is zero.
            # We must remove decimal point from result.
            index -= 1

        self._fastPathData.lastFreeIndex = index

    #    *
    #     * Internal utility.
    #     * Adds the passed {@code prefix} and {@code suffix} to {@code container}.
    #     *
    #     * @param container  Char array container which to prepend/append the
    #     *  prefix/suffix.
    #     * @param prefix     Char sequence to prepend as a prefix.
    #     * @param suffix     Char sequence to append as a suffix.
    #     *
    #     
    #    private void addAffixes(boolean isNegative, char[] container) {
    def _addAffixes(self, container, prefix, suffix):

        # We add affixes only if needed (affix length > 0).
        pl = len(prefix)
        sl = len(suffix)
        if pl != 0:
            self._prependPrefix(prefix, pl, container)
        if sl != 0:
            self._appendSuffix(suffix, sl, container)


    #    *
    #     * Prepends the passed {@code prefix} chars to given result
    #     * {@code container}.  Updates {@code fastPathData.firstUsedIndex}
    #     * accordingly.
    #     *
    #     * @param prefix The prefix characters to prepend to result.
    #     * @param len The number of chars to prepend.
    #     * @param container Char array container which to prepend the prefix
    #     
    def _prependPrefix(self, prefix, len, container):

        self._fastPathData.firstUsedIndex -= len
        startIndex = self._fastPathData.firstUsedIndex

        # If prefix to prepend is only 1 char long, just assigns this char.
        # If prefix is less or equal 4, we use a dedicated algorithm that
        #  has shown to run faster than System.arraycopy.
        # If more than 4, we use System.arraycopy.
        if len == 1:
            container[startIndex] = prefix[0]
        elif len <= 4:
            dstLower = startIndex
            dstUpper = dstLower + len - 1
            srcUpper = len - 1
            container[dstLower] = prefix[0]
            container[dstUpper] = prefix[srcUpper]

            if len > 2:
                dstLower += 1
# JAVA TO PYTHON CONVERTER WARNING: An assignment within expression was extracted from the following statement:
# ORIGINAL LINE: container[++dstLower] = prefix[1];
                container[dstLower] = prefix[1]
            if len == 4:
                dstUpper -= 1
# JAVA TO PYTHON CONVERTER WARNING: An assignment within expression was extracted from the following statement:
# ORIGINAL LINE: container[--dstUpper] = prefix[2];
                container[dstUpper] = prefix[2]
        else:
            System.arraycopy(prefix, 0, container, startIndex, len)

    #    *
    #     * Appends the passed {@code suffix} chars to given result
    #     * {@code container}.  Updates {@code fastPathData.lastFreeIndex}
    #     * accordingly.
    #     *
    #     * @param suffix The suffix characters to append to result.
    #     * @param len The number of chars to append.
    #     * @param container Char array container which to append the suffix
    #     
    def _appendSuffix(self, suffix, len, container):

        startIndex = self._fastPathData.lastFreeIndex

        # If suffix to append is only 1 char long, just assigns this char.
        # If suffix is less or equal 4, we use a dedicated algorithm that
        #  has shown to run faster than System.arraycopy.
        # If more than 4, we use System.arraycopy.
        if len == 1:
            container[startIndex] = suffix[0]
        elif len <= 4:
            dstLower = startIndex
            dstUpper = dstLower + len - 1
            srcUpper = len - 1
            container[dstLower] = suffix[0]
            container[dstUpper] = suffix[srcUpper]

            if len > 2:
                dstLower += 1
# JAVA TO PYTHON CONVERTER WARNING: An assignment within expression was extracted from the following statement:
# ORIGINAL LINE: container[++dstLower] = suffix[1];
                container[dstLower] = suffix[1]
            if len == 4:
                dstUpper -= 1
# JAVA TO PYTHON CONVERTER WARNING: An assignment within expression was extracted from the following statement:
# ORIGINAL LINE: container[--dstUpper] = suffix[2];
                container[dstUpper] = suffix[2]
        else:
            System.arraycopy(suffix, 0, container, startIndex, len)

        self._fastPathData.lastFreeIndex += len

    #    *
    #     * Converts digit chars from {@code digitsBuffer} to current locale.
    #     *
    #     * Must be called before adding affixes since we refer to
    #     * {@code fastPathData.firstUsedIndex} and {@code fastPathData.lastFreeIndex},
    #     * and do not support affixes (for speed reason).
    #     *
    #     * We loop backward starting from last used index in {@code fastPathData}.
    #     *
    #     * @param digitsBuffer The char array container where the digits are stored.
    #     
    def _localizeDigits(self, digitsBuffer):

        # We will localize only the digits, using the groupingSize,
        # and taking into account fractional part.

        # First take into account fractional part.
        digitsCounter = self._fastPathData.lastFreeIndex - self._fastPathData.fractionalFirstIndex

        # The case when there is no fractional digits.
        if digitsCounter < 0:
            digitsCounter = self._groupingSize

        # Only the digits remains to localize.
        cursor = fastPathData.lastFreeIndex - 1
        while cursor >= self._fastPathData.firstUsedIndex:
            if digitsCounter != 0:
                # This is a digit char, we must localize it.
                digitsBuffer[cursor] += chr(self._fastPathData.zeroDelta)
                digitsCounter -= 1
            else:
                # Decimal separator or grouping char. Reinit counter only.
                digitsCounter = self._groupingSize
            cursor -= 1

    #    *
    #     * This is the main entry point for the fast-path format algorithm.
    #     *
    #     * At this point we are sure to be in the expected conditions to run it.
    #     * This algorithm builds the formatted result and puts it in the dedicated
    #     * {@code fastPathData.fastPathContainer}.
    #     *
    #     * @param d the double value to be formatted.
    #     * @param negative Flag precising if {@code d} is negative.
    #     
    def _fastDoubleFormat(self, d, negative):

        container = self._fastPathData.fastPathContainer

        #        
        #         * The principle of the algorithm is to :
        #         * - Break the passed double into its integral and fractional parts
        #         *    converted into integers.
        #         * - Then decide if rounding up must be applied or not by following
        #         *    the half-even rounding rule, first using approximated scaled
        #         *    fractional part.
        #         * - For the difficult cases (approximated scaled fractional part
        #         *    being exactly 0.5d), we refine the rounding decision by calling
        #         *    exactRoundUp utility method that both calculates the exact roundoff
        #         *    on the approximation and takes correct rounding decision.
        #         * - We round-up the fractional part if needed, possibly propagating the
        #         *    rounding to integral part if we meet a "all-nine" case for the
        #         *    scaled fractional part.
        #         * - We then collect digits from the resulting integral and fractional
        #         *   parts, also setting the required grouping chars on the fly.
        #         * - Then we localize the collected digits if needed, and
        #         * - Finally prepend/append prefix/suffix if any is needed.
        #         

        # Exact integral part of d.
        integralPartAsInt = int(d)

        # Exact fractional part of d (since we subtract it's integral part).
        exactFractionalPart = d - float(integralPartAsInt)

        # Approximated scaled fractional part of d (due to multiplication).
        scaledFractional = exactFractionalPart * self._fastPathData.fractionalScaleFactor

        # Exact integral part of scaled fractional above.
        fractionalPartAsInt = int(scaledFractional)

        # Exact fractional part of scaled fractional above.
        scaledFractional = scaledFractional - float(fractionalPartAsInt)

        # Only when scaledFractional is exactly 0.5d do we have to do exact
        # calculations and take fine-grained rounding decision, since
        # approximated results above may lead to incorrect decision.
        # Otherwise comparing against 0.5d (strictly greater or less) is ok.
        roundItUp = False
        if scaledFractional >= 0.5:
            if scaledFractional == 0.5:
                # Rounding need fine-grained decision.
                roundItUp = self._exactRoundUp(exactFractionalPart, fractionalPartAsInt)
            else:
                roundItUp = True

            if roundItUp:
                # Rounds up both fractional part (and also integral if needed).
                if fractionalPartAsInt < self._fastPathData.fractionalMaxIntBound:
                    fractionalPartAsInt += 1
                else:
                    # Propagates rounding to integral part since "all nines" case.
                    fractionalPartAsInt = 0
                    integralPartAsInt += 1

        # Collecting digits.
        self._collectFractionalDigits(fractionalPartAsInt, container, self._fastPathData.fractionalFirstIndex)
        self._collectIntegralDigits(integralPartAsInt, container, self._fastPathData.integralLastIndex)

        # Localizing digits.
        if self._fastPathData.zeroDelta != 0:
            self._localizeDigits(container)

        # Adding prefix and suffix.
        if negative:
            if self._fastPathData.negativeAffixesRequired:
                self._addAffixes(container, self._fastPathData.charsNegativePrefix, self._fastPathData.charsNegativeSuffix)
        elif self._fastPathData.positiveAffixesRequired:
            self._addAffixes(container, self._fastPathData.charsPositivePrefix, self._fastPathData.charsPositiveSuffix)

    #    *
    #     * A fast-path shortcut of format(double) to be called by NumberFormat, or by
    #     * format(double, ...) public methods.
    #     *
    #     * If instance can be applied fast-path and passed double is not NaN or
    #     * Infinity, is in the integer range, we call {@code fastDoubleFormat}
    #     * after changing {@code d} to its positive value if necessary.
    #     *
    #     * Otherwise returns null by convention since fast-path can't be exercized.
    #     *
    #     * @param d The double value to be formatted
    #     *
    #     * @return the formatted result for {@code d} as a string.
    #     
    def fastFormat(self, d):
        isDataSet = False
        # (Re-)Evaluates fast-path status if needed.
        if self._fastPathCheckNeeded:
            isDataSet = self._checkAndSetFastPathStatus()

        if not self._isFastPath:
            # DecimalFormat instance is not in a fast-path state.
            return None

        if not Double.isFinite(d):
            # Should not use fast-path for Infinity and NaN.
            return None

        # Extracts and records sign of double value, possibly changing it
        # to a positive one, before calling fastDoubleFormat().
        negative = False
        if d < 0.0:
            negative = True
            d = -d
        elif d == 0.0:
            negative = (math.copysign(1.0, d) == -1.0)
            d = +0.0

        if d > java.text.DecimalFormat.MAX_INT_AS_DOUBLE:
            # Filters out values that are outside expected fast-path range
            return None
        else:
            if not isDataSet:
                #                
                #                 * If the fast path data is not set through
                #                 * checkAndSetFastPathStatus() and fulfil the
                #                 * fast path conditions then reset the data
                #                 * directly through resetFastPathData()
                #                 
                self._resetFastPathData(self._isFastPath)
            self._fastDoubleFormat(d, negative)



        # Returns a new string from updated fastPathContainer.
        return str(self._fastPathData.fastPathContainer, self._fastPathData.firstUsedIndex, self._fastPathData.lastFreeIndex - self._fastPathData.firstUsedIndex)


    #    *
    #     * Sets the {@code DigitList} used by this {@code DecimalFormat}
    #     * instance.
    #     * @param number the number to format
    #     * @param isNegative true, if the number is negative; false otherwise
    #     * @param maxDigits the max digits
    #     
    def setDigitList(self, number, isNegative, maxDigits):

        if isinstance(number, Double):
            self._digitList.set(isNegative, float(number), maxDigits, True)
        elif isinstance(number, java.math.BigDecimal):
            self._digitList.set(isNegative, number, maxDigits, True)
        elif isinstance(number, Long):
            self._digitList.set(isNegative, int(number), maxDigits)
        elif isinstance(number, java.math.BigInteger):
            self._digitList.set(isNegative, number, maxDigits)

    # ======== End fast-path formatting logic for double =========================

    #    *
    #     * Complete the formatting of a finite number.  On entry, the digitList must
    #     * be filled in with the correct digits.
    #     
    def _subformat(self, result, delegate, isNegative, isInteger, maxIntDigits, minIntDigits, maxFraDigits, minFraDigits):

        # Process prefix
        if isNegative:
            self._append(result, self._negativePrefix, delegate, self._getNegativePrefixFieldPositions(), Field.SIGN)
        else:
            self._append(result, self._positivePrefix, delegate, self._getPositivePrefixFieldPositions(), Field.SIGN)

        # Process number
        self.subformatNumber(result, delegate, isNegative, isInteger, maxIntDigits, minIntDigits, maxFraDigits, minFraDigits)

        # Process suffix
        if isNegative:
            self._append(result, self._negativeSuffix, delegate, self._getNegativeSuffixFieldPositions(), Field.SIGN)
        else:
            self._append(result, self._positiveSuffix, delegate, self._getPositiveSuffixFieldPositions(), Field.SIGN)

        return result

    #    *
    #     * Subformats number part using the {@code DigitList} of this
    #     * {@code DecimalFormat} instance.
    #     * @param result where the text is to be appended
    #     * @param delegate notified of the location of sub fields
    #     * @param isNegative true, if the number is negative; false otherwise
    #     * @param isInteger true, if the number is an integer; false otherwise
    #     * @param maxIntDigits maximum integer digits
    #     * @param minIntDigits minimum integer digits
    #     * @param maxFraDigits maximum fraction digits
    #     * @param minFraDigits minimum fraction digits
    #     
    def subformatNumber(self, result, delegate, isNegative, isInteger, maxIntDigits, minIntDigits, maxFraDigits, minFraDigits):

        grouping = self._symbols.getMonetaryGroupingSeparator() if self._isCurrencyFormat else self._symbols.getGroupingSeparator()
        zero = self._symbols.getZeroDigit()
        zeroDelta = zero - '0' # '0' is the DigitList representation of zero

        decimal = self._symbols.getMonetaryDecimalSeparator() if self._isCurrencyFormat else self._symbols.getDecimalSeparator()

        #         Per bug 4147706, DecimalFormat must respect the sign of numbers which
        #         * format as zero.  This allows sensible computations and preserves
        #         * relations such as signum(1/x) = signum(x), where x is +Infinity or
        #         * -Infinity.  Prior to this fix, we always formatted zero values as if
        #         * they were positive.  Liu 7/6/98.
        #         
        if self._digitList.isZero():
            self._digitList.decimalAt = 0 # Normalize

        if self._useExponentialNotation:
            iFieldStart = result.length()
            iFieldEnd = -1
            fFieldStart = -1

            # Minimum integer digits are handled in exponential format by
            # adjusting the exponent.  For example, 0.01234 with 3 minimum
            # integer digits is "123.4E-4".
            # Maximum integer digits are interpreted as indicating the
            # repeating range.  This is useful for engineering notation, in
            # which the exponent is restricted to a multiple of 3.  For
            # example, 0.01234 with 3 maximum integer digits is "12.34e-3".
            # If maximum integer digits are > 1 and are larger than
            # minimum integer digits, then minimum integer digits are
            # ignored.
            exponent = self._digitList.decimalAt
            repeat = maxIntDigits
            minimumIntegerDigits = minIntDigits
            if repeat > 1 and repeat > minIntDigits:
                # A repeating range is defined; adjust to it as follows.
                # If repeat == 3, we have 6,5,4=>3; 3,2,1=>0; 0,-1,-2=>-3
                # -3,-4,-5=>-6, etc. This takes into account that the
                # exponent we have here is off by one from what we expect
                # it is for the format 0.MMMMMx10^n.
                if exponent >= 1:
                    exponent = (math.trunc((exponent - 1) / float(repeat))) * repeat
                else:
                    # integer division rounds towards 0
                    exponent = (math.trunc((exponent - repeat) / float(repeat))) * repeat
                minimumIntegerDigits = 1
            else:
                # No repeating range is defined; use minimum integer digits.
                exponent -= minimumIntegerDigits

            # We now output a minimum number of digits, and more if there
            # are more digits, up to the maximum number of digits.  We
            # place the decimal point after the "integer" digits, which
            # are the first (decimalAt - exponent) digits.
            minimumDigits = minIntDigits + minFraDigits
            if minimumDigits < 0:
                minimumDigits = Integer.MAX_VALUE

            # The number of integer digits is handled specially if the number
            # is zero, since then there may be no digits.
            integerDigits = minimumIntegerDigits if self._digitList.isZero() else self._digitList.decimalAt - exponent
            if minimumDigits < integerDigits:
                minimumDigits = integerDigits
            totalDigits = self._digitList.count
            if minimumDigits > totalDigits:
                totalDigits = minimumDigits
            addedDecimalSeparator = False

            for i in range(0, totalDigits):
                if i == integerDigits:
                    # Record field information for caller.
                    iFieldEnd = result.length()

                    result.append(decimal)
                    addedDecimalSeparator = True

                    # Record field information for caller.
                    fFieldStart = result.length()
                result.append(chr((self._digitList.digits[i] + zeroDelta)) if (i < self._digitList.count) else zero)

            if self._decimalSeparatorAlwaysShown and totalDigits == integerDigits:
                # Record field information for caller.
                iFieldEnd = result.length()

                result.append(decimal)
                addedDecimalSeparator = True

                # Record field information for caller.
                fFieldStart = result.length()

            # Record field information
            if iFieldEnd == -1:
                iFieldEnd = result.length()
            delegate.formatted(java.text.DecimalFormat.INTEGER_FIELD, Field.INTEGER, Field.INTEGER, iFieldStart, iFieldEnd, result)
            if addedDecimalSeparator:
                delegate.formatted(Field.DECIMAL_SEPARATOR, Field.DECIMAL_SEPARATOR, iFieldEnd, fFieldStart, result)
            if fFieldStart == -1:
                fFieldStart = result.length()
            delegate.formatted(java.text.DecimalFormat.FRACTION_FIELD, Field.FRACTION, Field.FRACTION, fFieldStart, result.length(), result)

            # The exponent is output using the pattern-specified minimum
            # exponent digits.  There is no maximum limit to the exponent
            # digits, since truncating the exponent would result in an
            # unacceptable inaccuracy.
            fieldStart = result.length()

            result.append(self._symbols.getExponentSeparator())

            delegate.formatted(Field.EXPONENT_SYMBOL, Field.EXPONENT_SYMBOL, fieldStart, result.length(), result)

            # For zero values, we force the exponent to zero.  We
            # must do this here, and not earlier, because the value
            # is used to determine integer digit count above.
            if self._digitList.isZero():
                exponent = 0

            negativeExponent = exponent < 0
            if negativeExponent:
                exponent = -exponent
                fieldStart = result.length()
                result.append(self._symbols.getMinusSignText())
                delegate.formatted(Field.EXPONENT_SIGN, Field.EXPONENT_SIGN, fieldStart, result.length(), result)
            self._digitList.set(negativeExponent, exponent)

            eFieldStart = result.length()

            i = digitList.decimalAt
            while i < self._minExponentDigits:
                result.append(zero)
                i += 1
            i = 0
            while i < self._digitList.decimalAt:
                result.append(chr((self._digitList.digits[i] + zeroDelta)) if (i < self._digitList.count) else zero)
                i += 1
            delegate.formatted(Field.EXPONENT, Field.EXPONENT, eFieldStart, result.length(), result)
        else:
            iFieldStart = result.length()

            # Output the integer portion.  Here 'count' is the total
            # number of integer digits we will display, including both
            # leading zeros required to satisfy getMinimumIntegerDigits,
            # and actual digits present in the number.
            count = minIntDigits
            digitIndex = 0 # Index into digitList.fDigits[]
            if self._digitList.decimalAt > 0 and count < self._digitList.decimalAt:
                count = self._digitList.decimalAt

            # Handle the case where getMaximumIntegerDigits() is smaller
            # than the real number of integer digits.  If this is so, we
            # output the least significant max integer digits.  For example,
            # the value 1997 printed with 2 max integer digits is just "97".
            if count > maxIntDigits:
                count = maxIntDigits
                digitIndex = self._digitList.decimalAt - count

            sizeBeforeIntegerPart = result.length()
            for i in range(count - 1, -1, -1):
                if i < self._digitList.decimalAt and digitIndex < self._digitList.count:
                    # Output a real digit
# JAVA TO PYTHON CONVERTER WARNING: An assignment within expression was extracted from the following statement:
# ORIGINAL LINE: result.append((char)(digitList.digits[digitIndex++] + zeroDelta));
                    result.append(chr((self._digitList.digits[digitIndex] + zeroDelta)))
                    digitIndex += 1
                else:
                    # Output a leading zero
                    result.append(zero)

                # Output grouping separator if necessary.  Don't output a
                # grouping separator if i==0 though; that's at the end of
                # the integer part.
                if self.isGroupingUsed() and i > 0 and (self._groupingSize != 0) and (int(math.fmod(i, self._groupingSize)) == 0):
                    gStart = result.length()
                    result.append(grouping)
                    delegate.formatted(Field.GROUPING_SEPARATOR, Field.GROUPING_SEPARATOR, gStart, result.length(), result)

            # Determine whether or not there are any printable fractional
            # digits.  If we've used up the digits we know there aren't.
            fractionPresent = (minFraDigits > 0) or (not isInteger and digitIndex < self._digitList.count)

            # If there is no fraction present, and we haven't printed any
            # integer digits, then print a zero.  Otherwise we won't print
            # _any_ digits, and we won't be able to parse this string.
            if not fractionPresent and result.length() == sizeBeforeIntegerPart:
                result.append(zero)

            delegate.formatted(java.text.DecimalFormat.INTEGER_FIELD, Field.INTEGER, Field.INTEGER, iFieldStart, result.length(), result)

            # Output the decimal separator if we always do so.
            sStart = result.length()
            if self._decimalSeparatorAlwaysShown or fractionPresent:
                result.append(decimal)

            if sStart != result.length():
                delegate.formatted(Field.DECIMAL_SEPARATOR, Field.DECIMAL_SEPARATOR, sStart, result.length(), result)
            fFieldStart = result.length()

            for i in range(0, maxFraDigits):
                # Here is where we escape from the loop.  We escape if we've
                # output the maximum fraction digits (specified in the for
                # expression above).
                # We also stop when we've output the minimum digits and either:
                # we have an integer, so there is no fractional stuff to
                # display, or we're out of significant digits.
                if i >= minFraDigits and (isInteger or digitIndex >= self._digitList.count):
                    break

                # Output leading fractional zeros. These are zeros that come
                # after the decimal but before any significant digits. These
                # are only output if abs(number being formatted) < 1.0.
                if - 1 - i > (self._digitList.decimalAt - 1):
                    result.append(zero)
                    continue

                # Output a digit, if we have any precision left, or a
                # zero if we don't.  We don't want to output noise digits.
                if not isInteger and digitIndex < self._digitList.count:
# JAVA TO PYTHON CONVERTER WARNING: An assignment within expression was extracted from the following statement:
# ORIGINAL LINE: result.append((char)(digitList.digits[digitIndex++] + zeroDelta));
                    result.append(chr((self._digitList.digits[digitIndex] + zeroDelta)))
                    digitIndex += 1
                else:
                    result.append(zero)

            # Record field information for caller.
            delegate.formatted(java.text.DecimalFormat.FRACTION_FIELD, Field.FRACTION, Field.FRACTION, fFieldStart, result.length(), result)

    #    *
    #     * Appends the String {@code string} to {@code result}.
    #     * {@code delegate} is notified of all  the
    #     * {@code FieldPosition}s in {@code positions}.
    #     * <p>
    #     * If one of the {@code FieldPosition}s in {@code positions}
    #     * identifies a {@code SIGN} attribute, it is mapped to
    #     * {@code signAttribute}. This is used
    #     * to map the {@code SIGN} attribute to the {@code EXPONENT}
    #     * attribute as necessary.
    #     * <p>
    #     * This is used by {@code subformat} to add the prefix/suffix.
    #     
    def _append(self, result, string, delegate, positions, signAttribute):
        start = result.length()

        if (not len(string)) > 0:
            result.append(string)
            counter = 0
            max = positions.length
            while counter < max:
                fp = positions[counter]
                attribute = fp.getFieldAttribute()

                if attribute is Field.SIGN:
                    attribute = signAttribute
                delegate.formatted(attribute, attribute, start + fp.getBeginIndex(), start + fp.getEndIndex(), result)
                counter += 1

    #    *
    #     * {@inheritDoc NumberFormat}
    #     * <p>
    #     * Parsing can be done in either a strict or lenient manner, by default it is lenient.
    #     * <p>
    #     * Parsing fails when <b>lenient</b>, if the prefix and/or suffix are non-empty
    #     * and cannot be found due to parsing ending early, or the first character
    #     * after the prefix cannot be parsed.
    #     * <p>
    #     * Parsing fails when <b>strict</b>, if in {@code text},
    #     * <ul>
    #     *   <li> The prefix is not found. For example, a {@code Locale.US} currency
    #     *   format prefix: "{@code $}"
    #     *   <li> The suffix is not found. For example, a {@code Locale.US} percent
    #     *   format suffix: "{@code %}"
    #     *   <li> {@link #isGroupingUsed()} returns {@code true}, and {@link
    #     *   #getGroupingSize()} is not adhered to
    #     *   <li> {@link #isGroupingUsed()} returns {@code false}, and the grouping
    #     *   symbol is found
    #     *   <li> {@link #isParseIntegerOnly()} returns {@code true}, and the decimal
    #     *   separator is found
    #     *   <li> {@link #isGroupingUsed()} returns {@code true} and {@link
    #     *   #isParseIntegerOnly()} returns {@code false}, and the grouping
    #     *   symbol occurs after the decimal separator
    #     *   <li> Any other characters are found, that are not the expected symbols,
    #     *   and are not digits that occur within the numerical portion
    #     * </ul>
    #     * <p>
    #     * The subclass returned depends on the value of {@link #isParseBigDecimal}
    #     * as well as on the string being parsed.
    #     * <ul>
    #     *   <li>If {@code isParseBigDecimal()} is false (the default),
    #     *       most integer values are returned as {@code Long}
    #     *       objects, no matter how they are written: {@code "17"} and
    #     *       {@code "17.000"} both parse to {@code Long(17)}.
    #     *       Values that cannot fit into a {@code Long} are returned as
    #     *       {@code Double}s. This includes values with a fractional part,
    #     *       infinite values, {@code NaN}, and the value -0.0.
    #     *       {@code DecimalFormat} does <em>not</em> decide whether to
    #     *       return a {@code Double} or a {@code Long} based on the
    #     *       presence of a decimal separator in the source string. Doing so
    #     *       would prevent integers that overflow the mantissa of a double,
    #     *       such as {@code "-9,223,372,036,854,775,808.00"}, from being
    #     *       parsed accurately.
    #     *       <p>
    #     *       Callers may use the {@code Number} methods
    #     *       {@code doubleValue}, {@code longValue}, etc., to obtain
    #     *       the type they want.
    #     *   <li>If {@code isParseBigDecimal()} is true, values are returned
    #     *       as {@code BigDecimal} objects. The values are the ones
    #     *       constructed by {@link java.math.BigDecimal#BigDecimal(String)}
    #     *       for corresponding strings in locale-independent format. The
    #     *       special cases negative and positive infinity and NaN are returned
    #     *       as {@code Double} instances holding the values of the
    #     *       corresponding {@code Double} constants.
    #     * </ul>
    #     * <p>
    #     * {@code DecimalFormat} parses all Unicode characters that represent
    #     * decimal digits, as defined by {@code Character.digit()}. In
    #     * addition, {@code DecimalFormat} also recognizes as digits the ten
    #     * consecutive characters starting with the localized zero digit defined in
    #     * the {@code DecimalFormatSymbols} object.
    #     *
    #     * @param text the string to be parsed
    #     * @param pos  A {@code ParsePosition} object with index and error
    #     *             index information as described above.
    #     * @return     the parsed value, or {@code null} if the parse fails
    #     * @throws     NullPointerException if {@code text} or
    #     *             {@code pos} is null.
    #     
# JAVA TO PYTHON CONVERTER TASK: Python does not allow method overloads:
    def parse(self, text, pos):
        # special case NaN
        if text.regionMatches(pos.index, self._symbols.getNaN(), 0, len(self._symbols.getNaN())):
            pos.index = pos.index + len(self._symbols.getNaN())
            return float(math.nan)

        status = [False for _ in range(java.text.DecimalFormat.STATUS_LENGTH)]
        if not self._subparse(text, pos, self._positivePrefix, self._negativePrefix, self._digitList, False, status):
            return None

        # special case INFINITY
        if status[java.text.DecimalFormat.STATUS_INFINITE]:
            if status[java.text.DecimalFormat.STATUS_POSITIVE] == (self._multiplier >= 0):
                return float(Double.POSITIVE_INFINITY)
            else:
                return float(Double.NEGATIVE_INFINITY)

        if self._multiplier == 0:
            if self._digitList.isZero():
                return float(math.nan)
            elif status[java.text.DecimalFormat.STATUS_POSITIVE]:
                return float(Double.POSITIVE_INFINITY)
            else:
                return float(Double.NEGATIVE_INFINITY)

        if self.isParseBigDecimal():
            bigDecimalResult = self._digitList.getBigDecimal()

            if self._multiplier != 1:
                try:
                    bigDecimalResult = bigDecimalResult.divide(self._getBigDecimalMultiplier())
                except ArithmeticException as e:
                    bigDecimalResult = bigDecimalResult.divide(self._getBigDecimalMultiplier(), self._roundingMode)

            if not status[java.text.DecimalFormat.STATUS_POSITIVE]:
                bigDecimalResult = bigDecimalResult.negate()
            return bigDecimalResult
        else:
            gotDouble = True
            gotLongMinimum = False
            doubleResult = 0.0
            longResult = 0

            # Finally, have DigitList parse the digits into a value.
            if self._digitList.fitsIntoLong(status[java.text.DecimalFormat.STATUS_POSITIVE], self.isParseIntegerOnly()):
                gotDouble = False
                longResult = self._digitList.getLong()
                if longResult < 0:
                    gotLongMinimum = True
            else:
                doubleResult = self._digitList.getDouble()

            # Divide by multiplier. We have to be careful here not to do
            # unneeded conversions between double and long.
            if self._multiplier != 1:
                if gotDouble:
                    doubleResult /= self._multiplier
                else:
                    # Avoid converting to double if we can
                    if int(math.fmod(longResult, self._multiplier)) == 0:
                        longResult = math.trunc(longResult / float(self._multiplier))
                    else:
                        doubleResult = (float(longResult)) / self._multiplier
                        gotDouble = True

            if not status[java.text.DecimalFormat.STATUS_POSITIVE] and not gotLongMinimum:
                doubleResult = -doubleResult
                longResult = -longResult

            # At this point, if we divided the result by the multiplier, the
            # result may fit into a long.  We check for this case and return
            # a long if possible.
            # We must do this AFTER applying the negative (if appropriate)
            # in order to handle the case of LONG_MIN; otherwise, if we do
            # this with a positive value -LONG_MIN, the double is > 0, but
            # the long is < 0. We also must retain a double in the case of
            # -0.0, which will compare as == to a long 0 cast to a double
            # (bug 4162852).
            if self._multiplier != 1 and gotDouble:
                longResult = int(doubleResult)
                gotDouble = ((doubleResult != float(longResult)) or (doubleResult == 0.0 and 1 / doubleResult < 0.0)) and not self.isParseIntegerOnly()

            # cast inside of ?: because of binary numeric promotion, JLS 15.25
            return doubleResult if gotDouble else longResult

    #    *
    #     * Return a BigInteger multiplier.
    #     
    def _getBigIntegerMultiplier(self):
        if self._bigIntegerMultiplier is None:
            self._bigIntegerMultiplier = java.math.BigInteger.valueOf(self._multiplier)
        return self._bigIntegerMultiplier

    #    *
    #     * Return a BigDecimal multiplier.
    #     
    def _getBigDecimalMultiplier(self):
        if self._bigDecimalMultiplier is None:
            self._bigDecimalMultiplier = java.math.BigDecimal(self._multiplier)
        return self._bigDecimalMultiplier

    STATUS_INFINITE = 0
    STATUS_POSITIVE = 1
    STATUS_LENGTH = 2

    #    *
    #     * Parse the given text into a number.  The text is parsed beginning at
    #     * parsePosition, until an unparseable character is seen.
    #     * @param text The string to parse.
    #     * @param parsePosition The position at which to being parsing.  Upon
    #     * return, the first unparseable character.
    #     * @param digits The DigitList to set to the parsed value.
    #     * @param isExponent If true, parse an exponent.  This means no
    #     * infinite values and integer only.
    #     * @param status Upon return contains boolean status flags indicating
    #     * whether the value was infinite and whether it was positive.
    #     
    def _subparse(self, text, parsePosition, positivePrefix, negativePrefix, digits, isExponent, status):
        position = parsePosition.index
        oldStart = parsePosition.index
        gotPositive = False
        gotNegative = False

        # check for positivePrefix; take longest
        gotPositive = text.regionMatches(position, positivePrefix, 0, len(positivePrefix))
        gotNegative = text.regionMatches(position, negativePrefix, 0, len(negativePrefix))

        if gotPositive and gotNegative:
            if len(positivePrefix) > len(negativePrefix):
                gotNegative = False
            elif len(positivePrefix) < len(negativePrefix):
                gotPositive = False

        if gotPositive:
            position += len(positivePrefix)
        elif gotNegative:
            position += len(negativePrefix)
        else:
            parsePosition.errorIndex = position
            return False

        # position will serve as new index when success, otherwise it will
        # serve as errorIndex when failure
        position = self.subparseNumber(text, position, digits, True, isExponent, status)

        # First character after the prefix was un-parseable, should
        # fail regardless if lenient or strict.
        if position == -1:
            parsePosition.index = oldStart
            parsePosition.errorIndex = oldStart
            return False

        # When strict, text should end with the suffix.
        # When lenient, text only needs to contain the suffix.
        if not isExponent:
            if gotPositive:
                containsPosSuffix = text.regionMatches(position, self._positiveSuffix, 0, len(self._positiveSuffix))
                endsWithPosSuffix = containsPosSuffix and len(text) == position + len(self._positiveSuffix)
                gotPositive = endsWithPosSuffix if self._parseStrict else containsPosSuffix
            if gotNegative:
                containsNegSuffix = text.regionMatches(position, self._negativeSuffix, 0, len(self._negativeSuffix))
                endsWithNegSuffix = containsNegSuffix and len(text) == position + len(self._negativeSuffix)
                gotNegative = endsWithNegSuffix if self._parseStrict else containsNegSuffix

            # If both match, take longest
            if gotPositive and gotNegative:
                if len(self._positiveSuffix) > len(self._negativeSuffix):
                    gotNegative = False
                elif len(self._positiveSuffix) < len(self._negativeSuffix):
                    gotPositive = False

            # Fail if neither or both
            if gotPositive == gotNegative:
                parsePosition.errorIndex = position
                return False

            # No failures, thus increment the index by the suffix
            parsePosition.index = position + (len(self._positiveSuffix) if gotPositive else len(self._negativeSuffix))
        else:
            parsePosition.index = position

        status[java.text.DecimalFormat.STATUS_POSITIVE] = gotPositive
        if parsePosition.index == oldStart:
            parsePosition.errorIndex = position
            return False
        return True

    #    *
    #     * Parses a number from the given {@code text}. The text is parsed
    #     * beginning at {@code position}, until an unparseable character is seen.
    #     *
    #     * @param text the string to parse
    #     * @param position the position at which parsing begins
    #     * @param digits the DigitList to set to the parsed value
    #     * @param checkExponent whether to check for exponential number
    #     * @param isExponent if the exponential part is encountered
    #     * @param status upon return contains boolean status flags indicating
    #     *               whether the value is infinite and whether it is
    #     *               positive
    #     * @return returns the position of the first unparseable character or
    #     *         -1 in case of no valid number parsed
    #     
    def subparseNumber(self, text, position, digits, checkExponent, isExponent, status):
        # process digits or Inf, find decimal position
        status[java.text.DecimalFormat.STATUS_INFINITE] = False
        if not isExponent and text.regionMatches(position, self._symbols.getInfinity(), 0, len(self._symbols.getInfinity())):
            position += len(self._symbols.getInfinity())
            status[java.text.DecimalFormat.STATUS_INFINITE] = True
        else:
            # We now have a string of digits, possibly with grouping symbols,
            # and decimal points.  We want to process these into a DigitList.
            # We don't want to put a bunch of leading zeros into the DigitList
            # though, so we keep track of the location of the decimal point,
            # put only significant digits into the DigitList, and adjust the
            # exponent as needed.

            digits.decimalAt = digits.count = 0
            zero = self._symbols.getZeroDigit()
            decimal = self._symbols.getMonetaryDecimalSeparator() if self._isCurrencyFormat else self._symbols.getDecimalSeparator()
            grouping = self._symbols.getMonetaryGroupingSeparator() if self._isCurrencyFormat else self._symbols.getGroupingSeparator()
            exponentString = self._symbols.getExponentSeparator()
            sawDecimal = False
            sawDigit = False
            # Storing as long allows us to maintain accuracy of exponent
            # when the exponent value as well as the decimalAt nears
            # Integer.MAX/MIN value. However, the final expressed value is an int
            exponent = 0
            expStat = [False for _ in range(java.text.DecimalFormat.STATUS_LENGTH)]

            # We have to track digitCount ourselves, because digits.count will
            # pin when the maximum allowable digits is reached.
            digitCount = 0
            prevSeparatorIndex = -self._groupingSize
            startPos = position # Rely on startPos as index after prefix

            backup = -1
            while position < len(text):
                ch = text[position]

                #                 We recognize all digit ranges, not only the Latin digit range
                #                 * '0'..'9'.  We do so by using the Character.digit() method,
                #                 * which converts a valid Unicode digit to the range 0..9.
                #                 *
                #                 * The character 'ch' may be a digit.  If so, place its value
                #                 * from 0 to 9 in 'digit'.  First try using the locale digit,
                #                 * which may or MAY NOT be a standard Unicode digit range.  If
                #                 * this fails, try using the standard Unicode digit ranges by
                #                 * calling Character.digit().  If this also fails, digit will
                #                 * have a value outside the range 0..9.
                #                 
                digit = ch - zero
                if digit < 0 or digit > 9:
                    digit = Character.digit(ch, 10)

                # Enforce the grouping size on the first group
                if self._parseStrict and self.isGroupingUsed() and position == startPos + self._groupingSize and prevSeparatorIndex == -self._groupingSize and not sawDecimal and digit >= 0 and digit <= 9:
                    return position

                if digit == 0:
                    # Cancel out backup setting (see grouping handler below)
                    backup = -1 # Do this BEFORE continue statement below!!!
                    sawDigit = True

                    # Handle leading zeros
                    if digits.count == 0:
                        # Ignore leading zeros in integer part of number.
                        if not sawDecimal:
                            position += 1
                            continue

                        # If we have seen the decimal, but no significant
                        # digits yet, then we account for leading zeros by
                        # decrementing the digits.decimalAt into negative
                        # values.
                        digits.decimalAt -= 1
                    else:
                        digitCount += 1
                        digits.append(chr((digit + '0')))
                elif digit > 0 and digit <= 9:
                    sawDigit = True
                    digitCount += 1
                    digits.append(chr((digit + '0')))

                    # Cancel out backup setting (see grouping handler below)
                    backup = -1
                elif not isExponent and ch == decimal:
                    # Check grouping size on decimal separator
                    if self._parseStrict and self._isGroupingViolation(position, prevSeparatorIndex):
                        return self._groupingViolationIndex(position, prevSeparatorIndex)
                    # If we're only parsing integers, or if we ALREADY saw the
                    # decimal, then don't parse this one.
                    if self.isParseIntegerOnly() or sawDecimal:
                        break
                    digits.decimalAt = digitCount # Not digits.count!
                    sawDecimal = True
                elif not isExponent and ch == grouping and self.isGroupingUsed():
                    if self._parseStrict:
                        # text should not start with grouping when strict
                        if position == startPos:
                            return startPos
                        # when strict, fail if grouping occurs after decimal OR
                        # current group violates grouping size
                        if sawDecimal or (self._isGroupingViolation(position, prevSeparatorIndex)):
                            return self._groupingViolationIndex(position, prevSeparatorIndex)
                        prevSeparatorIndex = position # track previous
                    else:
                        # when lenient, only exit if grouping occurs after decimal
                        # subsequent grouping symbols are allowed when lenient
                        if sawDecimal:
                            break
                    # Ignore grouping characters, if we are using them, but
                    # require that they be followed by a digit.  Otherwise
                    # we backup and reprocess them.
                    backup = position
                elif checkExponent and not isExponent and text.regionMatches(position, exponentString, 0, len(exponentString)):
                    # Process the exponent by recursively calling this method.
                    pos = ParsePosition(position + len(exponentString))
                    exponentDigits = DigitList()

                    if self._subparse(text, pos, "", self._symbols.getMinusSignText(), exponentDigits, True, expStat):
                        # We parse the exponent with isExponent == true, thus fitsIntoLong()
                        # only returns false here if the exponent DigitList value exceeds
                        # Long.MAX_VALUE. We do not need to worry about false being
                        # returned for faulty values as they are ignored by DigitList.
                        if exponentDigits.fitsIntoLong(expStat[java.text.DecimalFormat.STATUS_POSITIVE], True):
                            exponent = exponentDigits.getLong()
                            if not expStat[java.text.DecimalFormat.STATUS_POSITIVE]:
                                exponent = -exponent
                        else:
                            exponent = Long.MAX_VALUE if expStat[java.text.DecimalFormat.STATUS_POSITIVE] else Long.MIN_VALUE
                        position = pos.index # Advance past the exponent
                    break # Whether we fail or succeed, we exit this loop
                else:
                    break
                position += 1

            # (When strict), within the loop we enforce grouping when encountering
            # decimal/grouping symbols. Once outside loop, we need to check
            # the final grouping, ex: "1,234". Only check the final grouping
            # if we have not seen a decimal separator, to prevent a non needed check,
            # for ex: "1,234.", "1,234.12"
            if self._parseStrict:
                if not sawDecimal and self._isGroupingViolation(position, prevSeparatorIndex):
                    # -1, since position is incremented by one too many when loop is finished
                    # "1,234%" and "1,234" both end with pos = 5, since '%' breaks
                    # the loop before incrementing position. In both cases, check
                    # should be done at pos = 4
                    return self._groupingViolationIndex(position - 1, prevSeparatorIndex)

            # If a grouping symbol is not followed by a digit, it must be
            # backed up to either exit early or fail depending on leniency
            if backup != -1:
                position = backup

            # If there was no decimal point we have an integer
            if not sawDecimal:
                digits.decimalAt = digitCount # Not digits.count!

            # Adjust for exponent, if any
            if exponent != 0:
                digits.decimalAt = self._shiftDecimalAt(digits.decimalAt, exponent)

            # If none of the text string was recognized.  For example, parse
            # "x" with pattern "#0.00" (return index and error index both 0)
            # parse "$" with pattern "$#0.00". (return index 0 and error
            # index 1).
            if not sawDigit and digitCount == 0:
                return -1
        return position

    # Calculate the final decimal position based off the exponent value
    # and the existing decimalAt position. If overflow/underflow, the value
    # should be set as either Integer.MAX/MIN
    def _shiftDecimalAt(self, decimalAt, exponent):
        try:
            exponent = Math.addExact(decimalAt, exponent)
        except ArithmeticException as ex:
            # If we under/overflow a Long do not bother with the decimalAt
            # As it can only shift up to Integer.MAX/MIN which has no affect
            if exponent > 0 and decimalAt > 0:
                return Integer.MAX_VALUE
            else:
                return Integer.MIN_VALUE
        try:
            decimalAt = Math.toIntExact(exponent)
        except ArithmeticException as ex:
            decimalAt = Integer.MAX_VALUE if exponent > 0 else Integer.MIN_VALUE
        return decimalAt

    # Checks to make sure grouping size is not violated. Used when strict.
    def _isGroupingViolation(self, pos, prevGroupingPos):
        assert self._parseStrict, "Grouping violations should only occur when strict"
        return self.isGroupingUsed() and prevGroupingPos != -self._groupingSize and pos - 1 != prevGroupingPos + self._groupingSize

    # Calculates the index that violated the grouping size
    # Violation can be over or under the grouping size
    # under - Current group has a grouping size of less than the expected
    # over - Current group has a grouping size of more than the expected
    def _groupingViolationIndex(self, pos, prevGroupingPos):
        # Both examples assume grouping size of 3 and 0 indexed
        # under ex: "1,23,4". (4) OR "1,,2". (2) When under, violating char is grouping symbol
        # over ex: "1,2345,6. (5) When over, violating char is the excess digit
        # This method is only evaluated when a grouping symbol is found, thus
        # we can take the minimum of either the current pos, or where we expect
        # the current group to have ended
        return min(pos, prevGroupingPos + self._groupingSize + 1)

    #    *
    #     * Returns a copy of the decimal format symbols, which is generally not
    #     * changed by the programmer or user.
    #     * @return a copy of the desired DecimalFormatSymbols
    #     * @see java.text.DecimalFormatSymbols
    #     
    def getDecimalFormatSymbols(self):
        try:
            # don't allow multiple references
            return self._symbols.clone()
        except Exception as foo:
            return None # should never happen


    #    *
    #     * Sets the decimal format symbols, which is generally not changed
    #     * by the programmer or user.
    #     * @param newSymbols desired DecimalFormatSymbols
    #     * @see java.text.DecimalFormatSymbols
    #     
    def setDecimalFormatSymbols(self, newSymbols):
        try:
            # don't allow multiple references
            self._symbols = newSymbols.clone()
            self._expandAffixes()
            self._fastPathCheckNeeded = True
        except Exception as foo:
            # should never happen
            pass

    #    *
    #     * Get the positive prefix.
    #     * <P>Examples: +123, $123, sFr123
    #     *
    #     * @return the positive prefix
    #     
    def getPositivePrefix(self):
        return self._positivePrefix

    #    *
    #     * Set the positive prefix.
    #     * <P>Examples: +123, $123, sFr123
    #     *
    #     * @param newValue the new positive prefix
    #     
    def setPositivePrefix(self, newValue):
        self._positivePrefix = newValue
        self._posPrefixPattern = None
        self._positivePrefixFieldPositions = None
        self._fastPathCheckNeeded = True

    #    *
    #     * Returns the FieldPositions of the fields in the prefix used for
    #     * positive numbers. This is not used if the user has explicitly set
    #     * a positive prefix via {@code setPositivePrefix}. This is
    #     * lazily created.
    #     *
    #     * @return FieldPositions in positive prefix
    #     
    def _getPositivePrefixFieldPositions(self):
        if self._positivePrefixFieldPositions is None:
            if self._posPrefixPattern is not None:
                self._positivePrefixFieldPositions = self._expandAffix(self._posPrefixPattern)
            else:
                self._positivePrefixFieldPositions = java.text.DecimalFormat._EmptyFieldPositionArray
        return self._positivePrefixFieldPositions

    #    *
    #     * Get the negative prefix.
    #     * <P>Examples: -123, ($123) (with negative suffix), sFr-123
    #     *
    #     * @return the negative prefix
    #     
    def getNegativePrefix(self):
        return self._negativePrefix

    #    *
    #     * Set the negative prefix.
    #     * <P>Examples: -123, ($123) (with negative suffix), sFr-123
    #     *
    #     * @param newValue the new negative prefix
    #     
    def setNegativePrefix(self, newValue):
        self._negativePrefix = newValue
        self._negPrefixPattern = None
        self._fastPathCheckNeeded = True

    #    *
    #     * Returns the FieldPositions of the fields in the prefix used for
    #     * negative numbers. This is not used if the user has explicitly set
    #     * a negative prefix via {@code setNegativePrefix}. This is
    #     * lazily created.
    #     *
    #     * @return FieldPositions in positive prefix
    #     
    def _getNegativePrefixFieldPositions(self):
        if self._negativePrefixFieldPositions is None:
            if self._negPrefixPattern is not None:
                self._negativePrefixFieldPositions = self._expandAffix(self._negPrefixPattern)
            else:
                self._negativePrefixFieldPositions = java.text.DecimalFormat._EmptyFieldPositionArray
        return self._negativePrefixFieldPositions

    #    *
    #     * Get the positive suffix.
    #     * <P>Example: 123%
    #     *
    #     * @return the positive suffix
    #     
    def getPositiveSuffix(self):
        return self._positiveSuffix

    #    *
    #     * Set the positive suffix.
    #     * <P>Example: 123%
    #     *
    #     * @param newValue the new positive suffix
    #     
    def setPositiveSuffix(self, newValue):
        self._positiveSuffix = newValue
        self._posSuffixPattern = None
        self._fastPathCheckNeeded = True

    #    *
    #     * Returns the FieldPositions of the fields in the suffix used for
    #     * positive numbers. This is not used if the user has explicitly set
    #     * a positive suffix via {@code setPositiveSuffix}. This is
    #     * lazily created.
    #     *
    #     * @return FieldPositions in positive prefix
    #     
    def _getPositiveSuffixFieldPositions(self):
        if self._positiveSuffixFieldPositions is None:
            if self._posSuffixPattern is not None:
                self._positiveSuffixFieldPositions = self._expandAffix(self._posSuffixPattern)
            else:
                self._positiveSuffixFieldPositions = java.text.DecimalFormat._EmptyFieldPositionArray
        return self._positiveSuffixFieldPositions

    #    *
    #     * Get the negative suffix.
    #     * <P>Examples: -123%, ($123) (with positive suffixes)
    #     *
    #     * @return the negative suffix
    #     
    def getNegativeSuffix(self):
        return self._negativeSuffix

    #    *
    #     * Set the negative suffix.
    #     * <P>Examples: 123%
    #     *
    #     * @param newValue the new negative suffix
    #     
    def setNegativeSuffix(self, newValue):
        self._negativeSuffix = newValue
        self._negSuffixPattern = None
        self._fastPathCheckNeeded = True

    #    *
    #     * Returns the FieldPositions of the fields in the suffix used for
    #     * negative numbers. This is not used if the user has explicitly set
    #     * a negative suffix via {@code setNegativeSuffix}. This is
    #     * lazily created.
    #     *
    #     * @return FieldPositions in positive prefix
    #     
    def _getNegativeSuffixFieldPositions(self):
        if self._negativeSuffixFieldPositions is None:
            if self._negSuffixPattern is not None:
                self._negativeSuffixFieldPositions = self._expandAffix(self._negSuffixPattern)
            else:
                self._negativeSuffixFieldPositions = java.text.DecimalFormat._EmptyFieldPositionArray
        return self._negativeSuffixFieldPositions

    #    *
    #     * Gets the multiplier for use in percent, per mille, and similar
    #     * formats.
    #     *
    #     * @return the multiplier
    #     * @see #setMultiplier(int)
    #     
    def getMultiplier(self):
        return self._multiplier

    #    *
    #     * Sets the multiplier for use in percent, per mille, and similar
    #     * formats.
    #     * For a percent format, set the multiplier to 100 and the suffixes to
    #     * have '%' (for Arabic, use the Arabic percent sign).
    #     * For a per mille format, set the multiplier to 1000 and the suffixes to
    #     * have '{@code U+2030}'.
    #     *
    #     * <P>Example: with multiplier 100, 1.23 is formatted as "123", and
    #     * "123" is parsed into 1.23.
    #     *
    #     * @param newValue the new multiplier
    #     * @see #getMultiplier
    #     
    def setMultiplier(self, newValue):
        self._multiplier = newValue
        self._bigDecimalMultiplier = None
        self._bigIntegerMultiplier = None
        self._fastPathCheckNeeded = True

    #    *
    #     * {@inheritDoc}
    #     
    def setGroupingUsed(self, newValue):
        super().setGroupingUsed(newValue)
        self._fastPathCheckNeeded = True

    #    *
    #     * Return the grouping size. Grouping size is the number of digits between
    #     * grouping separators in the integer portion of a number.  For example,
    #     * in the number "123,456.78", the grouping size is 3. Grouping size of
    #     * zero designates that grouping is not used, which provides the same
    #     * formatting as if calling {@link #setGroupingUsed(boolean)
    #     * setGroupingUsed(false)}.
    #     *
    #     * @return the grouping size
    #     * @see #setGroupingSize
    #     * @see java.text.NumberFormat#isGroupingUsed
    #     * @see java.text.DecimalFormatSymbols#getGroupingSeparator
    #     
    def getGroupingSize(self):
        return self._groupingSize

    #    *
    #     * Set the grouping size. Grouping size is the number of digits between
    #     * grouping separators in the integer portion of a number.  For example,
    #     * in the number "123,456.78", the grouping size is 3. Grouping size of
    #     * zero designates that grouping is not used, which provides the same
    #     * formatting as if calling {@link #setGroupingUsed(boolean)
    #     * setGroupingUsed(false)}.
    #     * <p>
    #     * The value passed in is converted to a byte, which may lose information.
    #     * Values that are negative or greater than
    #     * {@link java.lang.Byte#MAX_VALUE Byte.MAX_VALUE}, will throw an
    #     * {@code IllegalArgumentException}.
    #     *
    #     * @param newValue the new grouping size
    #     * @see #getGroupingSize
    #     * @see java.text.NumberFormat#setGroupingUsed
    #     * @see java.text.DecimalFormatSymbols#setGroupingSeparator
    #     * @throws IllegalArgumentException if {@code newValue} is negative or
    #     *          greater than {@link java.lang.Byte#MAX_VALUE Byte.MAX_VALUE}
    #     
    def setGroupingSize(self, newValue):
        if newValue < 0 or newValue > Byte.MAX_VALUE:
            raise IllegalArgumentException("newValue is out of valid range. value: " + str(newValue))
        self._groupingSize = int(newValue)
        self._fastPathCheckNeeded = True

    #    *
    #     * Allows you to get the behavior of the decimal separator with integers.
    #     * (The decimal separator will always appear with decimals.)
    #     * <P>Example: Decimal ON: 12345 &rarr; 12345.; OFF: 12345 &rarr; 12345
    #     *
    #     * @return {@code true} if the decimal separator is always shown
    #     *         {@code false} otherwise
    #     
    def isDecimalSeparatorAlwaysShown(self):
        return self._decimalSeparatorAlwaysShown

    #    *
    #     * Allows you to set the behavior of the decimal separator with integers.
    #     * (The decimal separator will always appear with decimals.)
    #     * <P>Example: Decimal ON: 12345 &rarr; 12345.; OFF: 12345 &rarr; 12345
    #     *
    #     * @param newValue {@code true} if the decimal separator is always shown
    #     *                 {@code false} otherwise
    #     
    def setDecimalSeparatorAlwaysShown(self, newValue):
        self._decimalSeparatorAlwaysShown = newValue
        self._fastPathCheckNeeded = True

    #    *
    #     * {@inheritDoc NumberFormat}
    #     *
    #     * @see #setStrict(boolean)
    #     * @see #parse(String, ParsePosition)
    #     * @since 23
    #     
    def isStrict(self):
        return self._parseStrict

    #    *
    #     * {@inheritDoc NumberFormat}
    #     *
    #     * @see #isStrict()
    #     * @see #parse(String, ParsePosition)
    #     * @since 23
    #     
    def setStrict(self, strict):
        self._parseStrict = strict

    #    *
    #     * Returns whether the {@link #parse(java.lang.String, java.text.ParsePosition)}
    #     * method returns {@code BigDecimal}. The default value is false.
    #     *
    #     * @return {@code true} if the parse method returns BigDecimal
    #     *         {@code false} otherwise
    #     * @see #setParseBigDecimal
    #     * @since 1.5
    #     
    def isParseBigDecimal(self):
        return self._parseBigDecimal

    #    *
    #     * Sets whether the {@link #parse(java.lang.String, java.text.ParsePosition)}
    #     * method returns {@code BigDecimal}.
    #     *
    #     * @param newValue {@code true} if the parse method returns BigDecimal
    #     *                 {@code false} otherwise
    #     * @see #isParseBigDecimal
    #     * @since 1.5
    #     
    def setParseBigDecimal(self, newValue):
        self._parseBigDecimal = newValue

    #    *
    #     * Standard override; no change in semantics.
    #     
    def clone(self):
        other = super().clone()
        other._symbols = self._symbols.clone()
        other._digitList = copy.copy(self._digitList)

        # Fast-path is almost stateless algorithm. The only logical state is the
        # isFastPath flag. In addition fastPathCheckNeeded is a sentinel flag
        # that forces recalculation of all fast-path fields when set to true.
        #
        # There is thus no need to clone all the fast-path fields.
        # We just only need to set fastPathCheckNeeded to true when cloning,
        # and init fastPathData to null as if it were a truly new instance.
        # Every fast-path field will be recalculated (only once) at next usage of
        # fast-path algorithm.
        other._fastPathCheckNeeded = True
        other._isFastPath = False
        other._fastPathData = None

        return other

    #    *
    #     * Compares the specified object with this {@code DecimalFormat} for equality.
    #     * Returns true if the object is also a {@code DecimalFormat} and the
    #     * two formats would format any value the same.
    #     *
    #     * @implSpec This method performs an equality check with a notion of class
    #     * identity based on {@code getClass()}, rather than {@code instanceof}.
    #     * Therefore, in the equals methods in subclasses, no instance of this class
    #     * should compare as equal to an instance of a subclass.
    #     * @param  obj object to be compared for equality
    #     * @return {@code true} if the specified object is equal to this {@code DecimalFormat}
    #     * @see Object#equals(Object)
    #     
    def equals(self, obj):
        if self is obj:
            return True

        if not super().equals(obj):
            return False # super does null and class checks

        other = obj
        return ((self._posPrefixPattern is other._posPrefixPattern and self._positivePrefix == other._positivePrefix) or (self._posPrefixPattern is not None and self._posPrefixPattern == other._posPrefixPattern)) and ((self._posSuffixPattern is other._posSuffixPattern and self._positiveSuffix == other._positiveSuffix) or (self._posSuffixPattern is not None and self._posSuffixPattern == other._posSuffixPattern)) and ((self._negPrefixPattern is other._negPrefixPattern and self._negativePrefix == other._negativePrefix) or (self._negPrefixPattern is not None and self._negPrefixPattern == other._negPrefixPattern)) and ((self._negSuffixPattern is other._negSuffixPattern and self._negativeSuffix == other._negativeSuffix) or (self._negSuffixPattern is not None and self._negSuffixPattern == other._negSuffixPattern)) and self._multiplier == other._multiplier and self._groupingSize == other._groupingSize and self._decimalSeparatorAlwaysShown == other._decimalSeparatorAlwaysShown and self._parseBigDecimal == other._parseBigDecimal and self._useExponentialNotation == other._useExponentialNotation and (not self._useExponentialNotation or self._minExponentDigits == other._minExponentDigits) and self._maximumIntegerDigits == other._maximumIntegerDigits and self._minimumIntegerDigits == other._minimumIntegerDigits and self._maximumFractionDigits == other._maximumFractionDigits and self._minimumFractionDigits == other._minimumFractionDigits and self._roundingMode is other._roundingMode and self._symbols.equals(other._symbols) and self._parseStrict == other._parseStrict

    #    *
    #     * {@return the hash code for this {@code DecimalFormat}}
    #     *
    #     * @implSpec This method calculates the hash code value using the values returned from
    #     * {@link #getPositivePrefix()} and {@link NumberFormat#hashCode()}.
    #     * @see Object#hashCode()
    #     * @see NumberFormat#hashCode()
    #     
    def hashCode(self):
        return super().hashCode() * 37 + hash(self._positivePrefix)
        # just enough fields for a reasonable distribution

    #    *
    #     * {@return a string identifying this {@code DecimalFormat}, for debugging}
    #     
    def toString(self):
        return """DecimalFormat [locale: \"%s\", pattern: \"%s\"]
""".formatted(self._symbols.getLocale().getDisplayName(), self.toPattern())

    #    *
    #     * Synthesizes a pattern string that represents the current state
    #     * of this Format object.
    #     *
    #     * @return a pattern string
    #     * @see #applyPattern
    #     
# JAVA TO PYTHON CONVERTER TASK: Python does not allow method overloads:
    def toPattern(self):
        return self._toPattern(False)

    #    *
    #     * Synthesizes a localized pattern string that represents the current
    #     * state of this Format object.
    #     *
    #     * @return a localized pattern string
    #     * @see #applyPattern
    #     
    def toLocalizedPattern(self):
        return self._toPattern(True)

    #    *
    #     * Expand the affix pattern strings into the expanded affix strings.  If any
    #     * affix pattern string is null, do not expand it.  This method should be
    #     * called any time the symbols or the affix patterns change in order to keep
    #     * the expanded affix strings up to date.
    #     
    def _expandAffixes(self):
        # Reuse one StringBuilder for better performance
        buffer = StringBuilder()
        if self._posPrefixPattern is not None:
            self._positivePrefix = self._expandAffix(self._posPrefixPattern, buffer)
            self._positivePrefixFieldPositions = None
        if self._posSuffixPattern is not None:
            self._positiveSuffix = self._expandAffix(self._posSuffixPattern, buffer)
            self._positiveSuffixFieldPositions = None
        if self._negPrefixPattern is not None:
            self._negativePrefix = self._expandAffix(self._negPrefixPattern, buffer)
            self._negativePrefixFieldPositions = None
        if self._negSuffixPattern is not None:
            self._negativeSuffix = self._expandAffix(self._negSuffixPattern, buffer)
            self._negativeSuffixFieldPositions = None

    #    *
    #     * Expand an affix pattern into an affix string.  All characters in the
    #     * pattern are literal unless prefixed by QUOTE.  The following characters
    #     * after QUOTE are recognized: PATTERN_PERCENT, PATTERN_PER_MILLE,
    #     * PATTERN_MINUS, and CURRENCY_SIGN.  If CURRENCY_SIGN is doubled (QUOTE +
    #     * CURRENCY_SIGN + CURRENCY_SIGN), it is interpreted as an ISO 4217
    #     * currency code.  Any other character after a QUOTE represents itself.
    #     * QUOTE must be followed by another character; QUOTE may not occur by
    #     * itself at the end of the pattern.
    #     *
    #     * @param pattern the non-null, possibly empty pattern
    #     * @param buffer a scratch StringBuilder; its contents will be lost
    #     * @return the expanded equivalent of pattern
    #     
# JAVA TO PYTHON CONVERTER TASK: Python does not allow method overloads:
    def _expandAffix(self, pattern, buffer):
        buffer.setLength(0)
        i = 0
        while i < len(pattern):
# JAVA TO PYTHON CONVERTER WARNING: An assignment within expression was extracted from the following statement:
# ORIGINAL LINE: char c = pattern.charAt(i++);
            c = pattern[i]
            i += 1
            if c == java.text.DecimalFormat.QUOTE:
# JAVA TO PYTHON CONVERTER WARNING: An assignment within expression was extracted from the following statement:
# ORIGINAL LINE: c = pattern.charAt(i++);
                c = pattern[i]
                i += 1
                match c:
                    case java.text.DecimalFormat.CURRENCY_SIGN:
                        if i < len(pattern) and pattern[i] == java.text.DecimalFormat.CURRENCY_SIGN:
                            i += 1
                            buffer.append(self._symbols.getInternationalCurrencySymbol())
                        else:
                            buffer.append(self._symbols.getCurrencySymbol())
                        continue
                    case java.text.DecimalFormat.CURRENCY_SIGN | java.text.DecimalFormat.PATTERN_PERCENT:
                        buffer.append(self._symbols.getPercentText())
                        continue
                    case java.text.DecimalFormat.CURRENCY_SIGN | java.text.DecimalFormat.PATTERN_PERCENT | java.text.DecimalFormat.PATTERN_PER_MILLE:
                        buffer.append(self._symbols.getPerMillText())
                        continue
                    case java.text.DecimalFormat.CURRENCY_SIGN | java.text.DecimalFormat.PATTERN_PERCENT | java.text.DecimalFormat.PATTERN_PER_MILLE | java.text.DecimalFormat.PATTERN_MINUS:
                        buffer.append(self._symbols.getMinusSignText())
                        continue
            buffer.append(c)
        return str(buffer)

    #    *
    #     * Expand an affix pattern into an array of FieldPositions describing
    #     * how the pattern would be expanded.
    #     * All characters in the
    #     * pattern are literal unless prefixed by QUOTE.  The following characters
    #     * after QUOTE are recognized: PATTERN_PERCENT, PATTERN_PER_MILLE,
    #     * PATTERN_MINUS, and CURRENCY_SIGN.  If CURRENCY_SIGN is doubled (QUOTE +
    #     * CURRENCY_SIGN + CURRENCY_SIGN), it is interpreted as an ISO 4217
    #     * currency code.  Any other character after a QUOTE represents itself.
    #     * QUOTE must be followed by another character; QUOTE may not occur by
    #     * itself at the end of the pattern.
    #     *
    #     * @param pattern the non-null, possibly empty pattern
    #     * @return FieldPosition array of the resulting fields.
    #     
# JAVA TO PYTHON CONVERTER TASK: Python does not allow method overloads:
    def _expandAffix(self, pattern):
        positions = None
        stringIndex = 0
        i = 0
        while i < len(pattern):
# JAVA TO PYTHON CONVERTER WARNING: An assignment within expression was extracted from the following statement:
# ORIGINAL LINE: char c = pattern.charAt(i++);
            c = pattern[i]
            i += 1
            if c == java.text.DecimalFormat.QUOTE:
                fieldID = None
                string = None
# JAVA TO PYTHON CONVERTER WARNING: An assignment within expression was extracted from the following statement:
# ORIGINAL LINE: c = pattern.charAt(i++);
                c = pattern[i]
                i += 1
                match c:
                    case java.text.DecimalFormat.CURRENCY_SIGN:
                        if i < len(pattern) and pattern[i] == java.text.DecimalFormat.CURRENCY_SIGN:
                            i += 1
                            string = self._symbols.getInternationalCurrencySymbol()
                        else:
                            string = self._symbols.getCurrencySymbol()
                        fieldID = Field.CURRENCY
                    case java.text.DecimalFormat.PATTERN_PERCENT:
                        string = self._symbols.getPercentText()
                        fieldID = Field.PERCENT
                    case java.text.DecimalFormat.PATTERN_PER_MILLE:
                        string = self._symbols.getPerMillText()
                        fieldID = Field.PERMILLE
                    case java.text.DecimalFormat.PATTERN_MINUS:
                        string = self._symbols.getMinusSignText()
                        fieldID = Field.SIGN

                if fieldID is not None and (not len(string)) > 0:
                    if positions is None:
                        positions = list(2)
                    fp = FieldPosition(fieldID)
                    fp.setBeginIndex(stringIndex)
                    fp.setEndIndex(stringIndex + len(string))
                    positions.append(fp)
                    stringIndex += len(string)
                    continue
            stringIndex += 1
        if positions is not None:
            return positions.toArray(java.text.DecimalFormat._EmptyFieldPositionArray)
        return java.text.DecimalFormat._EmptyFieldPositionArray

    #    *
    #     * Appends an affix pattern to the given StringBuilder, quoting special
    #     * characters as needed.  Uses the internal affix pattern, if that exists,
    #     * or the literal affix, if the internal affix pattern is null.  The
    #     * appended string will generate the same affix pattern (or literal affix)
    #     * when passed to toPattern().
    #     *
    #     * @param buffer the affix string is appended to this
    #     * @param affixPattern a pattern such as posPrefixPattern; may be null
    #     * @param expAffix a corresponding expanded affix, such as positivePrefix.
    #     * Ignored unless affixPattern is null.  If affixPattern is null, then
    #     * expAffix is appended as a literal affix.
    #     * @param localized true if the appended pattern should contain localized
    #     * pattern characters; otherwise, non-localized pattern chars are appended
    #     
# JAVA TO PYTHON CONVERTER TASK: Python does not allow method overloads:
    def _appendAffix(self, buffer, affixPattern, expAffix, localized):
        if affixPattern is None:
            self._appendAffix(buffer, expAffix, localized)
        else:
            i = 0
            pos = 0
            while pos < len(affixPattern):
                i = affixPattern.find(java.text.DecimalFormat.QUOTE, pos)
                if i < 0:
                    self._appendAffix(buffer, affixPattern[pos:], localized)
                    break
                if i > pos:
                    self._appendAffix(buffer, affixPattern[pos:i], localized)
                i += 1
# JAVA TO PYTHON CONVERTER WARNING: An assignment within expression was extracted from the following statement:
# ORIGINAL LINE: char c = affixPattern.charAt(++i);
                c = affixPattern[i]
                i += 1
                if c == java.text.DecimalFormat.QUOTE:
                    buffer.append(c)
                    # Fall through and append another QUOTE below
                elif c == java.text.DecimalFormat.CURRENCY_SIGN and i < len(affixPattern) and affixPattern[i] == java.text.DecimalFormat.CURRENCY_SIGN:
                    i += 1
                    buffer.append(c)
                    # Fall through and append another CURRENCY_SIGN below
                elif localized:
                    match c:
                        case java.text.DecimalFormat.PATTERN_PERCENT:
                            buffer.append(self._symbols.getPercentText())
                            pos = i
                            continue
                        case java.text.DecimalFormat.PATTERN_PERCENT | java.text.DecimalFormat.PATTERN_PER_MILLE:
                            buffer.append(self._symbols.getPerMillText())
                            pos = i
                            continue
                        case java.text.DecimalFormat.PATTERN_PERCENT | java.text.DecimalFormat.PATTERN_PER_MILLE | java.text.DecimalFormat.PATTERN_MINUS:
                            buffer.append(self._symbols.getMinusSignText())
                            pos = i
                            continue
                buffer.append(c)
                pos = i

    #    *
    #     * Append an affix to the given StringBuilder, using quotes if
    #     * there are special characters.  Single quotes themselves must be
    #     * escaped in either case.
    #     
# JAVA TO PYTHON CONVERTER TASK: Python does not allow method overloads:
    def _appendAffix(self, buffer, affix, localized):
        needQuote = False
        if localized:
            needQuote = affix.find(self._symbols.getZeroDigit()) >= 0 or affix.find(self._symbols.getGroupingSeparator()) >= 0 or affix.find(self._symbols.getDecimalSeparator()) >= 0 or affix.find(self._symbols.getPercentText()) >= 0 or affix.find(self._symbols.getPerMillText()) >= 0 or affix.find(self._symbols.getDigit()) >= 0 or affix.find(self._symbols.getPatternSeparator()) >= 0 or affix.find(self._symbols.getMinusSignText()) >= 0 or affix.find(java.text.DecimalFormat.CURRENCY_SIGN) >= 0
        else:
            needQuote = affix.find(java.text.DecimalFormat.PATTERN_ZERO_DIGIT) >= 0 or affix.find(java.text.DecimalFormat.PATTERN_GROUPING_SEPARATOR) >= 0 or affix.find(java.text.DecimalFormat.PATTERN_DECIMAL_SEPARATOR) >= 0 or affix.find(java.text.DecimalFormat.PATTERN_PERCENT) >= 0 or affix.find(java.text.DecimalFormat.PATTERN_PER_MILLE) >= 0 or affix.find(java.text.DecimalFormat.PATTERN_DIGIT) >= 0 or affix.find(java.text.DecimalFormat.PATTERN_SEPARATOR) >= 0 or affix.find(java.text.DecimalFormat.PATTERN_MINUS) >= 0 or affix.find(java.text.DecimalFormat.CURRENCY_SIGN) >= 0
        if needQuote:
            buffer.append('\'')
        if affix.find('\'') < 0:
            buffer.append(affix)
        else:
            j = 0
            while j < len(affix):
                c = affix[j]
                buffer.append(c)
                if c == '\'':
                    buffer.append(c)
                j += 1
        if needQuote:
            buffer.append('\'')

    #    *
    #     * Implementation of producing a pattern. This method returns a positive and
    #     * negative (if needed), pattern string in the form of : Prefix (optional)
    #     * Number Suffix (optional). A NegativePattern is only produced if the
    #     * prefix or suffix patterns differs.
    #     
# JAVA TO PYTHON CONVERTER TASK: Python does not allow method overloads:
    def _toPattern(self, localized):
        # Determine symbol values; use DFS if localized
        zeroSymbol = self._symbols.getZeroDigit() if localized else java.text.DecimalFormat.PATTERN_ZERO_DIGIT
        digitSymbol = self._symbols.getDigit() if localized else java.text.DecimalFormat.PATTERN_DIGIT
        groupingSymbol = (self._symbols.getMonetaryGroupingSeparator() if self._isCurrencyFormat else self._symbols.getGroupingSeparator()) if localized else java.text.DecimalFormat.PATTERN_GROUPING_SEPARATOR
        decimalSymbol = (self._symbols.getMonetaryDecimalSeparator() if self._isCurrencyFormat else self._symbols.getDecimalSeparator()) if localized else java.text.DecimalFormat.PATTERN_DECIMAL_SEPARATOR
        exponentSymbol = self._symbols.getExponentSeparator() if localized else java.text.DecimalFormat.PATTERN_EXPONENT
        patternSeparator = self._symbols.getPatternSeparator() if localized else java.text.DecimalFormat.PATTERN_SEPARATOR

        result = StringBuilder()
        # j == 1 denotes PositivePattern, j == 0 denotes NegativePattern
        for j in range(1, -1, -1):
            if j == 1:
                # Append positive and negative (if needed) prefix pattern
                self._appendAffix(result, self._posPrefixPattern, self._positivePrefix, localized)
            else:
                self._appendAffix(result, self._negPrefixPattern, self._negativePrefix, localized)
            # Append integer digits
            digitCount = self.getMaximumIntegerDigits() if self._useExponentialNotation else max(self._groupingSize, self.getMinimumIntegerDigits()) + 1
            for i in range(digitCount, 0, -1):
                if i != digitCount and self.isGroupingUsed() and self._groupingSize != 0 and int(math.fmod(i, self._groupingSize)) == 0:
                    result.append(groupingSymbol)
                result.append(zeroSymbol if i <= self.getMinimumIntegerDigits() else digitSymbol)
            # Append decimal symbol
            if self.getMaximumFractionDigits() > 0 or self._decimalSeparatorAlwaysShown:
                result.append(decimalSymbol)
            # Append fraction digits
            result.repeat(zeroSymbol, self.getMinimumFractionDigits())
            result.repeat(digitSymbol, self.getMaximumFractionDigits() - self.getMinimumFractionDigits())
            # Append exponent symbol and digits
            if self._useExponentialNotation:
                result.append(exponentSymbol)
                result.repeat(zeroSymbol, self._minExponentDigits)
            if j == 1:
                # Append positive suffix pattern
                self._appendAffix(result, self._posSuffixPattern, self._positiveSuffix, localized)
                if self._posEqualsNegPattern():
                    # Negative pattern not needed if suffix/prefix are equivalent
                    break
                result.append(patternSeparator)
            else:
                self._appendAffix(result, self._negSuffixPattern, self._negativeSuffix, localized)
        return str(result)

    #    *
    #     * This method returns true if the positive and negative prefix/suffix
    #     * values are equivalent. This is used to determine if an explicit NegativePattern
    #     * is required.
    #     
    def _posEqualsNegPattern(self):
        # Check suffix
        return ((self._negSuffixPattern is self._posSuffixPattern and self._negativeSuffix == self._positiveSuffix) or (self._negSuffixPattern is not None and self._negSuffixPattern == self._posSuffixPattern)) and ((self._negPrefixPattern is not None and self._posPrefixPattern is not None and self._negPrefixPattern == "'-" + self._posPrefixPattern) or (self._negPrefixPattern is self._posPrefixPattern and self._negativePrefix == self._symbols.getMinusSignText() + self._positivePrefix))

    #    *
    #     * Apply the given pattern to this Format object.  A pattern is a
    #     * short-hand specification for the various formatting properties.
    #     * These properties can also be changed individually through the
    #     * various setter methods.
    #     * <p>
    #     * The number of maximum integer digits is usually not derived from the pattern.
    #     * See the note in the {@link ##patterns Patterns} section for more detail.
    #     * For negative numbers, use a second pattern, separated by a semicolon
    #     * <P>Example {@code "#,#00.0#"} &rarr; 1,234.56
    #     * <P>This means a minimum of 2 integer digits, 1 fraction digit, and
    #     * a maximum of 2 fraction digits.
    #     * <p>Example: {@code "#,#00.0#;(#,#00.0#)"} for negatives in
    #     * parentheses.
    #     * <p>In negative patterns, the minimum and maximum counts are ignored
    #     * these are presumed to be set in the positive pattern.
    #     *
    #     * @param pattern a new pattern
    #     * @throws    NullPointerException if {@code pattern} is null
    #     * @throws    IllegalArgumentException if the given pattern is invalid.
    #     
# JAVA TO PYTHON CONVERTER TASK: Python does not allow method overloads:
    def applyPattern(self, pattern):
        self._applyPattern(pattern, False)

    #    *
    #     * Apply the given pattern to this Format object.  The pattern
    #     * is assumed to be in a localized notation. A pattern is a
    #     * short-hand specification for the various formatting properties.
    #     * These properties can also be changed individually through the
    #     * various setter methods.
    #     * <p>
    #     * The number of maximum integer digits is usually not derived from the pattern.
    #     * See the note in the {@link ##patterns Patterns} section for more detail.
    #     * For negative numbers, use a second pattern, separated by a semicolon
    #     * <P>Example {@code "#,#00.0#"} &rarr; 1,234.56
    #     * <P>This means a minimum of 2 integer digits, 1 fraction digit, and
    #     * a maximum of 2 fraction digits.
    #     * <p>Example: {@code "#,#00.0#;(#,#00.0#)"} for negatives in
    #     * parentheses.
    #     * <p>In negative patterns, the minimum and maximum counts are ignored
    #     * these are presumed to be set in the positive pattern.
    #     *
    #     * @param pattern a new pattern
    #     * @throws    NullPointerException if {@code pattern} is null
    #     * @throws    IllegalArgumentException if the given pattern is invalid.
    #     
    def applyLocalizedPattern(self, pattern):
        self._applyPattern(pattern, True)

    #    *
    #     * Does the real work of applying a pattern.
    #     
# JAVA TO PYTHON CONVERTER TASK: Python does not allow method overloads:
    def _applyPattern(self, pattern, localized):
        zeroDigit = java.text.DecimalFormat.PATTERN_ZERO_DIGIT
        groupingSeparator = java.text.DecimalFormat.PATTERN_GROUPING_SEPARATOR
        decimalSeparator = java.text.DecimalFormat.PATTERN_DECIMAL_SEPARATOR
        percent = java.text.DecimalFormat.PATTERN_PERCENT
        perMill = java.text.DecimalFormat.PATTERN_PER_MILLE
        digit = java.text.DecimalFormat.PATTERN_DIGIT
        separator = java.text.DecimalFormat.PATTERN_SEPARATOR
        exponent = java.text.DecimalFormat.PATTERN_EXPONENT
        minus = java.text.DecimalFormat.PATTERN_MINUS
        if localized:
            zeroDigit = self._symbols.getZeroDigit()
            groupingSeparator = self._symbols.getGroupingSeparator()
            decimalSeparator = self._symbols.getDecimalSeparator()
            percent = self._symbols.getPercent()
            perMill = self._symbols.getPerMill()
            digit = self._symbols.getDigit()
            separator = self._symbols.getPatternSeparator()
            exponent = self._symbols.getExponentSeparator()
            minus = self._symbols.getMinusSign()
        gotNegative = False
        self._decimalSeparatorAlwaysShown = False
        self._isCurrencyFormat = False
        self._useExponentialNotation = False

        start = 0
        j = 1
        while j >= 0 and start < len(pattern):
            inQuote = False
            prefix = StringBuilder()
            suffix = StringBuilder()
            decimalPos = -1
            multiplier = 1
            digitLeftCount = 0
            zeroDigitCount = 0
            digitRightCount = 0
            groupingCount = -1

            # The phase ranges from 0 to 2.  Phase 0 is the prefix.  Phase 1 is
            # the section of the pattern with digits, decimal separator,
            # grouping characters.  Phase 2 is the suffix.  In phases 0 and 2,
            # percent, per mille, and currency symbols are recognized and
            # translated.  The separation of the characters into phases is
            # strictly enforced; if phase 1 characters are to appear in the
            # suffix, for example, they must be quoted.
            phase = 0

            # The affix is either the prefix or the suffix.
            affix = prefix

            pos = start
            while pos < len(pattern):
                ch = pattern[pos]
                match phase:
                    case 0 | 2:
                        # Process the prefix / suffix characters
                        if inQuote:
                            # A quote within quotes indicates either the closing
                            # quote or two quotes, which is a quote literal. That
                            # is, we have the second quote in 'do' or 'don''t'.
                            if ch == java.text.DecimalFormat.QUOTE:
                                if (pos + 1) < len(pattern) and pattern[pos + 1] == java.text.DecimalFormat.QUOTE:
                                    pos += 1
                                    affix.append("''") # 'don''t'
                                else:
                                    inQuote = False # 'do'
                                pos += 1
                                continue
                        else:
                            # Process unquoted characters seen in prefix or suffix
                            # phase.
                            if ch == digit or ch == zeroDigit or ch == groupingSeparator or ch == decimalSeparator:
                                phase = 1
                                pos -= 1 # Reprocess this character
                                pos += 1
                                continue
                            elif ch == java.text.DecimalFormat.CURRENCY_SIGN:
                                # Use lookahead to determine if the currency sign
                                # is doubled or not.
                                doubled = (pos + 1) < len(pattern) and pattern[pos + 1] == java.text.DecimalFormat.CURRENCY_SIGN
                                if doubled:
                                    pos += 1
                                self._isCurrencyFormat = True
                                affix.append("'\u00A4\u00A4" if doubled else "'\u00A4")
                                pos += 1
                                continue
                            elif ch == java.text.DecimalFormat.QUOTE:
                                # A quote outside quotes indicates either the
                                # opening quote or two quotes, which is a quote
                                # literal. That is, we have the first quote in 'do'
                                # or o''clock.
                                if (pos + 1) < len(pattern) and pattern[pos + 1] == java.text.DecimalFormat.QUOTE:
                                    pos += 1
                                    affix.append("''") # o''clock
                                else:
                                    inQuote = True # 'do'
                                pos += 1
                                continue
                            elif ch == separator:
                                # Don't allow separators before we see digit
                                # characters of phase 1, and don't allow separators
                                # in the second pattern (j == 0).
                                if phase == 0 or j == 0:
                                    raise IllegalArgumentException("Unquoted special character '" + ch + "' in pattern \"" + pattern + '"')
                                start = pos + 1
                                pos = len(pattern)
                                pos += 1
                                continue

                            # Next handle characters which are appended directly.
                            elif ch == percent:
                                if multiplier != 1:
                                    raise IllegalArgumentException("Too many percent/per mille characters in pattern \"" + pattern + '"')
                                multiplier = 100
                                affix.append("'%")
                                pos += 1
                                continue
                            elif ch == perMill:
                                if multiplier != 1:
                                    raise IllegalArgumentException("Too many percent/per mille characters in pattern \"" + pattern + '"')
                                multiplier = 1000
                                affix.append("'\u2030")
                                pos += 1
                                continue
                            elif ch == minus:
                                affix.append("'-")
                                pos += 1
                                continue
                        # Note that if we are within quotes, or if this is an
                        # unquoted, non-special character, then we usually fall
                        # through to here.
                        affix.append(ch)

                    case 1:
                        # The negative subpattern (j = 0) serves only to specify the
                        # negative prefix and suffix, so all the phase 1 characters
                        # e.g. digits, zeroDigit, groupingSeparator,
                        # decimalSeparator, exponent are ignored
                        if j == 0:
                            while pos < len(pattern):
                                negPatternChar = pattern[pos]
                                if negPatternChar == digit or negPatternChar == zeroDigit or negPatternChar == groupingSeparator or negPatternChar == decimalSeparator:
                                    pos += 1
                                elif pattern.regionMatches(pos, exponent, 0, len(exponent)):
                                    pos = pos + len(exponent)
                                else:
                                    # Not a phase 1 character, consider it as
                                    # suffix and parse it in phase 2
                                    pos -= 1 #process it again in outer loop
                                    phase = 2
                                    affix = suffix
                                    break
                            pos += 1
                            continue

                        # Process the digits, decimal, and grouping characters. We
                        # record five pieces of information. We expect the digits
                        # to occur in the pattern ####0000.####, and we record the
                        # number of left digits, zero (central) digits, and right
                        # digits. The position of the last grouping character is
                        # recorded (should be somewhere within the first two blocks
                        # of characters), as is the position of the decimal point,
                        # if any (should be in the zero digits). If there is no
                        # decimal point, then there should be no right digits.
                        if ch == digit:
                            if zeroDigitCount > 0:
                                digitRightCount += 1
                            else:
                                digitLeftCount += 1
                            if groupingCount >= 0 and decimalPos < 0:
                                groupingCount += 1
                        elif ch == zeroDigit:
                            if digitRightCount > 0:
                                raise IllegalArgumentException("Unexpected '0' in pattern \"" + pattern + '"')
                            zeroDigitCount += 1
                            if groupingCount >= 0 and decimalPos < 0:
                                groupingCount += 1
                        elif ch == groupingSeparator:
                            groupingCount = 0
                        elif ch == decimalSeparator:
                            if decimalPos >= 0:
                                raise IllegalArgumentException("Multiple decimal separators in pattern \"" + pattern + '"')
                            decimalPos = digitLeftCount + zeroDigitCount + digitRightCount
                        elif pattern.regionMatches(pos, exponent, 0, len(exponent)):
                            if self._useExponentialNotation:
                                raise IllegalArgumentException("Multiple exponential " + "symbols in pattern \"" + pattern + '"')
                            self._useExponentialNotation = True
                            self._minExponentDigits = 0

                            # Use lookahead to parse out the exponential part
                            # of the pattern, then jump into phase 2.
                            pos = pos + len(exponent)
                            while pos < len(pattern) and pattern[pos] == zeroDigit:
                                self._minExponentDigits += 1
                                pos += 1

                            if (digitLeftCount + zeroDigitCount) < 1 or self._minExponentDigits < 1:
                                raise IllegalArgumentException("Malformed exponential " + "pattern \"" + pattern + '"')

                            # Transition to phase 2
                            phase = 2
                            affix = suffix
                            pos -= 1
                            pos += 1
                            continue
                        else:
                            phase = 2
                            affix = suffix
                            pos -= 1
                            pos += 1
                            continue
                pos += 1

            # Handle patterns with no '0' pattern character. These patterns
            # are legal, but must be interpreted.  "##.###" -> "#0.###".
            # ".###" -> ".0##".
            #             We allow patterns of the form "####" to produce a zeroDigitCount
            #             * of zero (got that?); although this seems like it might make it
            #             * possible for format() to produce empty strings, format() checks
            #             * for this condition and outputs a zero digit in this situation.
            #             * Having a zeroDigitCount of zero yields a minimum integer digits
            #             * of zero, which allows proper round-trip patterns.  That is, we
            #             * don't want "#" to become "#0" when toPattern() is called (even
            #             * though that's what it really is, semantically).
            #             
            if zeroDigitCount == 0 and digitLeftCount > 0 and decimalPos >= 0:
                # Handle "###.###" and "###." and ".###"
                n = decimalPos
                if n == 0:
                    n += 1
                digitRightCount = digitLeftCount - n
                digitLeftCount = n - 1
                zeroDigitCount = 1

            # Do syntax checking on the digits.
            if (decimalPos < 0 and digitRightCount > 0) or (decimalPos >= 0 and (decimalPos  (digitLeftCount + zeroDigitCount))) or groupingCount == 0 or inQuote:
                raise IllegalArgumentException("Malformed pattern \"" + pattern + '"')

            if j == 1:
                self._posPrefixPattern = str(prefix)
                self._posSuffixPattern = str(suffix)
                self._negPrefixPattern = self._posPrefixPattern # assume these for now
                self._negSuffixPattern = self._posSuffixPattern
                digitTotalCount = digitLeftCount + zeroDigitCount + digitRightCount
                #                 The effectiveDecimalPos is the position the decimal is at or
                #                 * would be at if there is no decimal. Note that if decimalPos<0,
                #                 * then digitTotalCount == digitLeftCount + zeroDigitCount.
                #                 
                effectiveDecimalPos = decimalPos if decimalPos >= 0 else digitTotalCount
                self.setMinimumIntegerDigits(effectiveDecimalPos - digitLeftCount)
                self.setMaximumIntegerDigits(digitLeftCount + self.getMinimumIntegerDigits() if self._useExponentialNotation else java.text.DecimalFormat.MAXIMUM_INTEGER_DIGITS)
                self.setMaximumFractionDigits((digitTotalCount - decimalPos) if decimalPos >= 0 else 0)
                self.setMinimumFractionDigits((digitLeftCount + zeroDigitCount - decimalPos) if decimalPos >= 0 else 0)
                self.setGroupingUsed(groupingCount > 0)
                self._groupingSize = groupingCount if (groupingCount > 0) else 0
                self._multiplier = multiplier
                self.setDecimalSeparatorAlwaysShown(decimalPos == 0 or decimalPos == digitTotalCount)
            else:
                self._negPrefixPattern = str(prefix)
                self._negSuffixPattern = str(suffix)
                gotNegative = True
            j -= 1

        if len(pattern) == 0:
            self._posPrefixPattern = self._posSuffixPattern = ""
            self.setMinimumIntegerDigits(0)
            self.setMaximumIntegerDigits(java.text.DecimalFormat.MAXIMUM_INTEGER_DIGITS)
            self.setMinimumFractionDigits(0)
            # As maxFracDigits are fully displayed unlike maxIntDigits
            # Prevent OOME by setting to a much more reasonable value.
            self.setMaximumFractionDigits(java.text.DecimalFormat.DOUBLE_FRACTION_DIGITS)

        # If there was no negative pattern, or if the negative pattern is
        # identical to the positive pattern, then prepend the minus sign to
        # the positive pattern to form the negative pattern.
        if not gotNegative or (self._negPrefixPattern == self._posPrefixPattern and self._negSuffixPattern == self._posSuffixPattern):
            self._negSuffixPattern = self._posSuffixPattern
            self._negPrefixPattern = "'-" + self._posPrefixPattern

        self._expandAffixes()

    #    *
    #     * Sets the maximum number of digits allowed in the integer portion of a
    #     * number. Negative input values are replaced with 0.
    #     * @see NumberFormat#setMaximumIntegerDigits
    #     * @see ##digit_limits Integer and Fraction Digit Limits
    #     
    def setMaximumIntegerDigits(self, newValue):
        self._maximumIntegerDigits = Math.clamp(newValue, 0, java.text.DecimalFormat.MAXIMUM_INTEGER_DIGITS)
        super().setMaximumIntegerDigits(min(self._maximumIntegerDigits, java.text.DecimalFormat.DOUBLE_INTEGER_DIGITS))
        if self._minimumIntegerDigits > self._maximumIntegerDigits:
            self._minimumIntegerDigits = self._maximumIntegerDigits
            super().setMinimumIntegerDigits(min(self._minimumIntegerDigits, java.text.DecimalFormat.DOUBLE_INTEGER_DIGITS))
        self._fastPathCheckNeeded = True

    #    *
    #     * Sets the minimum number of digits allowed in the integer portion of a
    #     * number. Negative input values are replaced with 0.
    #     * @see NumberFormat#setMinimumIntegerDigits
    #     * @see ##digit_limits Integer and Fraction Digit Limits
    #     
    def setMinimumIntegerDigits(self, newValue):
        self._minimumIntegerDigits = Math.clamp(newValue, 0, java.text.DecimalFormat.MAXIMUM_INTEGER_DIGITS)
        super().setMinimumIntegerDigits(min(self._minimumIntegerDigits, java.text.DecimalFormat.DOUBLE_INTEGER_DIGITS))
        if self._minimumIntegerDigits > self._maximumIntegerDigits:
            self._maximumIntegerDigits = self._minimumIntegerDigits
            super().setMaximumIntegerDigits(min(self._maximumIntegerDigits, java.text.DecimalFormat.DOUBLE_INTEGER_DIGITS))
        self._fastPathCheckNeeded = True

    #    *
    #     * Sets the maximum number of digits allowed in the fraction portion of a
    #     * number. Negative input values are replaced with 0.
    #     * @see NumberFormat#setMaximumFractionDigits
    #     * @see ##digit_limits Integer and Fraction Digit Limits
    #     
    def setMaximumFractionDigits(self, newValue):
        self._maximumFractionDigits = Math.clamp(newValue, 0, java.text.DecimalFormat.MAXIMUM_FRACTION_DIGITS)
        super().setMaximumFractionDigits(min(self._maximumFractionDigits, java.text.DecimalFormat.DOUBLE_FRACTION_DIGITS))
        if self._minimumFractionDigits > self._maximumFractionDigits:
            self._minimumFractionDigits = self._maximumFractionDigits
            super().setMinimumFractionDigits(min(self._minimumFractionDigits, java.text.DecimalFormat.DOUBLE_FRACTION_DIGITS))
        self._fastPathCheckNeeded = True

    #    *
    #     * Sets the minimum number of digits allowed in the fraction portion of a
    #     * number. Negative input values are replaced with 0.
    #     * @see NumberFormat#setMinimumFractionDigits
    #     * @see ##digit_limits Integer and Fraction Digit Limits
    #     
    def setMinimumFractionDigits(self, newValue):
        self._minimumFractionDigits = Math.clamp(newValue, 0, java.text.DecimalFormat.MAXIMUM_FRACTION_DIGITS)
        super().setMinimumFractionDigits(min(self._minimumFractionDigits, java.text.DecimalFormat.DOUBLE_FRACTION_DIGITS))
        if self._minimumFractionDigits > self._maximumFractionDigits:
            self._maximumFractionDigits = self._minimumFractionDigits
            super().setMaximumFractionDigits(min(self._maximumFractionDigits, java.text.DecimalFormat.DOUBLE_FRACTION_DIGITS))
        self._fastPathCheckNeeded = True

    #    *
    #     * Gets the maximum number of digits allowed in the integer portion of a
    #     * number. The maximum number of integer digits can be set by either {@link #setMaximumIntegerDigits(int)}
    #     * or {@link #applyPattern(String)}. See the {@link ##patterns Pattern Section} for
    #     * comprehensive rules regarding maximum integer digits in patterns.
    #     * @see #setMaximumIntegerDigits
    #     * @see ##digit_limits Integer and Fraction Digit Limits
    #     
    def getMaximumIntegerDigits(self):
        return self._maximumIntegerDigits

    #    *
    #     * Gets the minimum number of digits allowed in the integer portion of a
    #     * number.
    #     * @see #setMinimumIntegerDigits
    #     * @see ##digit_limits Integer and Fraction Digit Limits
    #     
    def getMinimumIntegerDigits(self):
        return self._minimumIntegerDigits

    #    *
    #     * Gets the maximum number of digits allowed in the fraction portion of a
    #     * number.
    #     * @see #setMaximumFractionDigits
    #     * @see ##digit_limits Integer and Fraction Digit Limits
    #     
    def getMaximumFractionDigits(self):
        return self._maximumFractionDigits

    #    *
    #     * Gets the minimum number of digits allowed in the fraction portion of a
    #     * number.
    #     * @see #setMinimumFractionDigits
    #     * @see ##digit_limits Integer and Fraction Digit Limits
    #     
    def getMinimumFractionDigits(self):
        return self._minimumFractionDigits

    #    *
    #     * Gets the currency used by this decimal format when formatting
    #     * currency values.
    #     * The currency is obtained by calling
    #     * {@link DecimalFormatSymbols#getCurrency DecimalFormatSymbols.getCurrency}
    #     * on this number format's symbols.
    #     *
    #     * @return the currency used by this decimal format, or {@code null}
    #     * @since 1.4
    #     
    def getCurrency(self):
        return self._symbols.getCurrency()

    #    *
    #     * Sets the currency used by this number format when formatting
    #     * currency values. This does not update the minimum or maximum
    #     * number of fraction digits used by the number format.
    #     * The currency is set by calling
    #     * {@link DecimalFormatSymbols#setCurrency DecimalFormatSymbols.setCurrency}
    #     * on this number format's symbols.
    #     *
    #     * @param currency the new currency to be used by this decimal format
    #     * @throws    NullPointerException if {@code currency} is null
    #     * @since 1.4
    #     
    def setCurrency(self, currency):
        if currency is not self._symbols.getCurrency():
            self._symbols.setCurrency(currency)
            if self._isCurrencyFormat:
                self._expandAffixes()
        self._fastPathCheckNeeded = True

    #    *
    #     * Gets the {@link java.math.RoundingMode} used in this DecimalFormat.
    #     *
    #     * @return The {@code RoundingMode} used for this DecimalFormat.
    #     * @see #setRoundingMode(RoundingMode)
    #     * @since 1.6
    #     
    def getRoundingMode(self):
        return self._roundingMode

    #    *
    #     * Sets the {@link java.math.RoundingMode} used in this DecimalFormat.
    #     *
    #     * @param roundingMode The {@code RoundingMode} to be used
    #     * @see #getRoundingMode()
    #     * @throws    NullPointerException if {@code roundingMode} is null.
    #     * @since 1.6
    #     
    def setRoundingMode(self, roundingMode):
        if roundingMode is None:
            raise NullPointerException()

        self._roundingMode = roundingMode
        self._digitList.setRoundingMode(roundingMode)
        self._fastPathCheckNeeded = True

    #    *
    #     * Reads the default serializable fields from the stream and performs
    #     * validations and adjustments for older serialized versions. The
    #     * validations and adjustments are:
    #     * <ol>
    #     * <li>
    #     * Verify that the superclass's digit count fields correctly reflect
    #     * the limits imposed on formatting numbers other than
    #     * {@code BigInteger} and {@code BigDecimal} objects. These
    #     * limits are stored in the superclass for serialization compatibility
    #     * with older versions, while the limits for {@code BigInteger} and
    #     * {@code BigDecimal} objects are kept in this class.
    #     * If, in the superclass, the minimum or maximum integer digit count is
    #     * larger than {@code DOUBLE_INTEGER_DIGITS} or if the minimum or
    #     * maximum fraction digit count is larger than
    #     * {@code DOUBLE_FRACTION_DIGITS}, then the stream data is invalid
    #     * and this method throws an {@code InvalidObjectException}.
    #     * <li>
    #     * If {@code serialVersionOnStream} is less than 4, initialize
    #     * {@code roundingMode} to {@link java.math.RoundingMode#HALF_EVEN
    #     * RoundingMode.HALF_EVEN}.  This field is new with version 4.
    #     * <li>
    #     * If {@code serialVersionOnStream} is less than 3, then call
    #     * the setters for the minimum and maximum integer and fraction digits with
    #     * the values of the corresponding superclass getters to initialize the
    #     * fields in this class. The fields in this class are new with version 3.
    #     * <li>
    #     * If {@code serialVersionOnStream} is less than 1, indicating that
    #     * the stream was written by JDK 1.1, initialize
    #     * {@code useExponentialNotation}
    #     * to false, since it was not present in JDK 1.1.
    #     * <li>
    #     * Set {@code serialVersionOnStream} to the maximum allowed value so
    #     * that default serialization will work properly if this object is streamed
    #     * out again.
    #     * </ol>
    #     *
    #     * <p>Stream versions older than 2 will not have the affix pattern variables
    #     * {@code posPrefixPattern} etc.  As a result, they will be initialized
    #     * to {@code null}, which means the affix strings will be taken as
    #     * literal values.  This is exactly what we want, since that corresponds to
    #     * the pre-version-2 behavior.
    #     
# JAVA TO PYTHON CONVERTER TASK: Java annotations have no direct Python equivalent:
# ORIGINAL LINE: @java.io.Serial private void readObject(java.io.ObjectInputStream stream) throws IOException, ClassNotFoundException
# JAVA TO PYTHON CONVERTER WARNING: Method 'throws' clauses are not available in Python:
    def _readObject(self, stream):
        stream.defaultReadObject()
        self._digitList = DigitList()

        # We force complete fast-path reinitialization when the instance is
        # deserialized. See clone() comment on fastPathCheckNeeded.
        self._fastPathCheckNeeded = True
        self._isFastPath = False
        self._fastPathData = None

        if self._serialVersionOnStream < 4:
            self.setRoundingMode(java.math.RoundingMode.HALF_EVEN)
        else:
            self.setRoundingMode(self.getRoundingMode())

        # We only need to check the maximum counts because NumberFormat
        # .readObject has already ensured that the maximum is greater than the
        # minimum count.
        if super().getMaximumIntegerDigits() > java.text.DecimalFormat.DOUBLE_INTEGER_DIGITS or super().getMaximumFractionDigits() > java.text.DecimalFormat.DOUBLE_FRACTION_DIGITS:
            raise java.io.InvalidObjectException("Digit count out of range")
        if self._serialVersionOnStream < 3:
            self.setMaximumIntegerDigits(super().getMaximumIntegerDigits())
            self.setMinimumIntegerDigits(super().getMinimumIntegerDigits())
            self.setMaximumFractionDigits(super().getMaximumFractionDigits())
            self.setMinimumFractionDigits(super().getMinimumFractionDigits())
        if self._serialVersionOnStream < 1:
            # Didn't have exponential fields
            self._useExponentialNotation = False

        # Restore the invariant value if groupingSize is invalid.
        if self._groupingSize < 0:
            self._groupingSize = 3

        self._serialVersionOnStream = java.text.DecimalFormat.CURRENT_SERIAL_VERSION

    #----------------------------------------------------------------------
    # INSTANCE VARIABLES
    #----------------------------------------------------------------------


    #    *
    #     * The symbol used as a prefix when formatting positive numbers, e.g. "+".
    #     *
    #     * @serial
    #     * @see #getPositivePrefix
    #     

    #    *
    #     * The symbol used as a suffix when formatting positive numbers.
    #     * This is often an empty string.
    #     *
    #     * @serial
    #     * @see #getPositiveSuffix
    #     

    #    *
    #     * The symbol used as a prefix when formatting negative numbers, e.g. "-".
    #     *
    #     * @serial
    #     * @see #getNegativePrefix
    #     

    #    *
    #     * The symbol used as a suffix when formatting negative numbers.
    #     * This is often an empty string.
    #     *
    #     * @serial
    #     * @see #getNegativeSuffix
    #     

    #    *
    #     * The prefix pattern for non-negative numbers.  This variable corresponds
    #     * to {@code positivePrefix}.
    #     *
    #     * <p>This pattern is expanded by the method {@code expandAffix()} to
    #     * {@code positivePrefix} to update the latter to reflect changes in
    #     * {@code symbols}.  If this variable is {@code null} then
    #     * {@code positivePrefix} is taken as a literal value that does not
    #     * change when {@code symbols} changes.  This variable is always
    #     * {@code null} for {@code DecimalFormat} objects older than
    #     * stream version 2 restored from stream.
    #     *
    #     * @serial
    #     * @since 1.3
    #     

    #    *
    #     * The suffix pattern for non-negative numbers.  This variable corresponds
    #     * to {@code positiveSuffix}.  This variable is analogous to
    #     * {@code posPrefixPattern}; see that variable for further
    #     * documentation.
    #     *
    #     * @serial
    #     * @since 1.3
    #     

    #    *
    #     * The prefix pattern for negative numbers.  This variable corresponds
    #     * to {@code negativePrefix}.  This variable is analogous to
    #     * {@code posPrefixPattern}; see that variable for further
    #     * documentation.
    #     *
    #     * @serial
    #     * @since 1.3
    #     

    #    *
    #     * The suffix pattern for negative numbers.  This variable corresponds
    #     * to {@code negativeSuffix}.  This variable is analogous to
    #     * {@code posPrefixPattern}; see that variable for further
    #     * documentation.
    #     *
    #     * @serial
    #     * @since 1.3
    #     

    #    *
    #     * The multiplier for use in percent, per mille, etc.
    #     *
    #     * @serial
    #     * @see #getMultiplier
    #     

    #    *
    #     * The number of digits between grouping separators in the integer
    #     * portion of a number.  Must be non-negative and less than or equal to
    #     * {@link java.lang.Byte#MAX_VALUE Byte.MAX_VALUE} if
    #     * {@code NumberFormat.groupingUsed} is true.
    #     *
    #     * @serial
    #     * @see #getGroupingSize
    #     * @see java.text.NumberFormat#isGroupingUsed
    #     

    #    *
    #     * If true, forces the decimal separator to always appear in a formatted
    #     * number, even if the fractional part of the number is zero.
    #     *
    #     * @serial
    #     * @see #isDecimalSeparatorAlwaysShown
    #     

    #    *
    #     * If true, parse returns BigDecimal wherever possible.
    #     *
    #     * @serial
    #     * @see #isParseBigDecimal
    #     * @since 1.5
    #     


    #    *
    #     * True if this object represents a currency format.  This determines
    #     * whether the monetary decimal/grouping separators are used instead of the normal ones.
    #     

    #    *
    #     * The {@code DecimalFormatSymbols} object used by this format.
    #     * It contains the symbols used to format numbers, e.g. the grouping separator,
    #     * decimal separator, and so on.
    #     *
    #     * @serial
    #     * @see #setDecimalFormatSymbols
    #     * @see java.text.DecimalFormatSymbols
    #     

    #    *
    #     * True to force the use of exponential (i.e. scientific) notation when formatting
    #     * numbers.
    #     *
    #     * @serial
    #     * @since 1.2
    #     

    #    *
    #     * True if this {@code DecimalFormat} will parse numbers with strict
    #     * leniency.
    #     *
    #     * @serial
    #     * @since 23
    #     

    #    *
    #     * FieldPositions describing the positive prefix String. This is
    #     * lazily created. Use {@code getPositivePrefixFieldPositions}
    #     * when needed.
    #     

    #    *
    #     * FieldPositions describing the positive suffix String. This is
    #     * lazily created. Use {@code getPositiveSuffixFieldPositions}
    #     * when needed.
    #     

    #    *
    #     * FieldPositions describing the negative prefix String. This is
    #     * lazily created. Use {@code getNegativePrefixFieldPositions}
    #     * when needed.
    #     

    #    *
    #     * FieldPositions describing the negative suffix String. This is
    #     * lazily created. Use {@code getNegativeSuffixFieldPositions}
    #     * when needed.
    #     

    #    *
    #     * The minimum number of digits used to display the exponent when a number is
    #     * formatted in exponential notation.  This field is ignored if
    #     * {@code useExponentialNotation} is not true.
    #     *
    #     * @serial
    #     * @since 1.2
    #     

    #    *
    #     * The maximum number of digits allowed in the integer portion of a
    #     * {@code BigInteger} or {@code BigDecimal} number.
    #     * {@code maximumIntegerDigits} must be greater than or equal to
    #     * {@code minimumIntegerDigits}.
    #     *
    #     * @serial
    #     * @see #getMaximumIntegerDigits
    #     * @since 1.5
    #     

    #    *
    #     * The minimum number of digits allowed in the integer portion of a
    #     * {@code BigInteger} or {@code BigDecimal} number.
    #     * {@code minimumIntegerDigits} must be less than or equal to
    #     * {@code maximumIntegerDigits}.
    #     *
    #     * @serial
    #     * @see #getMinimumIntegerDigits
    #     * @since 1.5
    #     

    #    *
    #     * The maximum number of digits allowed in the fractional portion of a
    #     * {@code BigInteger} or {@code BigDecimal} number.
    #     * {@code maximumFractionDigits} must be greater than or equal to
    #     * {@code minimumFractionDigits}.
    #     *
    #     * @serial
    #     * @see #getMaximumFractionDigits
    #     * @since 1.5
    #     

    #    *
    #     * The minimum number of digits allowed in the fractional portion of a
    #     * {@code BigInteger} or {@code BigDecimal} number.
    #     * {@code minimumFractionDigits} must be less than or equal to
    #     * {@code maximumFractionDigits}.
    #     *
    #     * @serial
    #     * @see #getMinimumFractionDigits
    #     * @since 1.5
    #     

    #    *
    #     * The {@link java.math.RoundingMode} used in this DecimalFormat.
    #     *
    #     * @serial
    #     * @since 1.6
    #     

    # ------ DecimalFormat fields for fast-path for double algorithm  ------

    #    *
    #     * Helper inner utility class for storing the data used in the fast-path
    #     * algorithm. Almost all fields related to fast-path are encapsulated in
    #     * this class.
    #     *
    #     * Any {@code DecimalFormat} instance has a {@code fastPathData}
    #     * reference field that is null unless both the properties of the instance
    #     * are such that the instance is in the "fast-path" state, and a format call
    #     * has been done at least once while in this state.
    #     *
    #     * Almost all fields are related to the "fast-path" state only and don't
    #     * change until one of the instance properties is changed.
    #     *
    #     * {@code firstUsedIndex} and {@code lastFreeIndex} are the only
    #     * two fields that are used and modified while inside a call to
    #     * {@code fastDoubleFormat}.
    #     *
    #     
    class FastPathData:

        def __init__(self):
            # instance fields found by Java to Python Converter:
            self.lastFreeIndex = 0
            self.firstUsedIndex = 0
            self.zeroDelta = 0
            self.groupingChar = '\0'
            self.integralLastIndex = 0
            self.fractionalFirstIndex = 0
            self.fractionalScaleFactor = 0
            self.fractionalMaxIntBound = 0
            self.fastPathContainer = None
            self.charsPositivePrefix = None
            self.charsNegativePrefix = None
            self.charsPositiveSuffix = None
            self.charsNegativeSuffix = None
            self.positiveAffixesRequired = True
            self.negativeAffixesRequired = True

        # --- Temporary fields used in fast-path, shared by several methods.

        #* The first unused index at the end of the formatted result. 

        #* The first used index at the beginning of the formatted result 

        # --- State fields related to fast-path status. Changes due to a
        #     property change only. Set by checkAndSetFastPathStatus() only.

        #* Difference between locale zero and default zero representation. 

        #* Locale char for grouping separator. 

        #*  Fixed index position of last integral digit of formatted result 

        #*  Fixed index position of first fractional digit of formatted result 

        #* Fractional constants depending on decimal|currency state 


        #* The char array buffer that will contain the formatted result 

        #* Suffixes recorded as char array for efficiency. 

    #* The format fast-path status of the instance. Logical state. 

    #* Flag stating need of check and reinit fast-path status on next format call. 

    #* DecimalFormat reference to its FastPathData 


    #----------------------------------------------------------------------

    CURRENT_SERIAL_VERSION = 4

    #    *
    #     * The internal serial version which says which version was written.
    #     * Possible values are:
    #     * <ul>
    #     * <li><b>0</b> (default): versions before the Java 2 platform v1.2
    #     * <li><b>1</b>: version for 1.2, which includes the two new fields
    #     *      {@code useExponentialNotation} and
    #     *      {@code minExponentDigits}.
    #     * <li><b>2</b>: version for 1.3 and later, which adds four new fields:
    #     *      {@code posPrefixPattern}, {@code posSuffixPattern},
    #     *      {@code negPrefixPattern}, and {@code negSuffixPattern}.
    #     * <li><b>3</b>: version for 1.5 and later, which adds five new fields:
    #     *      {@code maximumIntegerDigits},
    #     *      {@code minimumIntegerDigits},
    #     *      {@code maximumFractionDigits},
    #     *      {@code minimumFractionDigits}, and
    #     *      {@code parseBigDecimal}.
    #     * <li><b>4</b>: version for 1.6 and later, which adds one new field:
    #     *      {@code roundingMode}.
    #     * </ul>
    #     * @since 1.2
    #     * @serial
    #     

    #----------------------------------------------------------------------
    # CONSTANTS
    #----------------------------------------------------------------------

    # ------ Fast-Path for double Constants ------

    #* Maximum valid integer value for applying fast-path algorithm 
    MAX_INT_AS_DOUBLE = float(Integer.MAX_VALUE)

    #    *
    #     * The digit arrays used in the fast-path methods for collecting digits.
    #     * Using 3 constants arrays of chars ensures a very fast collection of digits
    #     
    class DigitArrays:
        DIGIT_ONES1000 = ['\0' for _ in range(1000)]
        DIGIT_TENS1000 = ['\0' for _ in range(1000)]
        DIGIT_HUNDREDS1000 = ['\0' for _ in range(1000)]

        # initialize on demand holder class idiom for arrays of digits
        @staticmethod
        def _static_initializer():
            tenIndex = 0
            hundredIndex = 0
            digitOne = '0'
            digitTen = '0'
            digitHundred = '0'
            for i in range(0, 1000):

                java.text.DecimalFormat.DigitArrays.DIGIT_ONES1000[i] = digitOne
                if digitOne == '9':
                    digitOne = '0'
                else:
                    digitOne += chr(1)

                java.text.DecimalFormat.DigitArrays.DIGIT_TENS1000[i] = digitTen
                if i == (tenIndex + 9):
                    tenIndex += 10
                    if digitTen == '9':
                        digitTen = '0'
                    else:
                        digitTen += chr(1)

                java.text.DecimalFormat.DigitArrays.DIGIT_HUNDREDS1000[i] = digitHundred
                if i == (hundredIndex + 99):
                    digitHundred += chr(1)
                    hundredIndex += 100

        _static_initializer()
    # ------ Fast-Path for double Constants end ------

    # Constants for characters used in programmatic (unlocalized) patterns.
    PATTERN_ZERO_DIGIT = '0'
    PATTERN_GROUPING_SEPARATOR = ','
    PATTERN_DECIMAL_SEPARATOR = '.'
    PATTERN_PER_MILLE = '\u2030'
    PATTERN_PERCENT = '%'
    PATTERN_DIGIT = '#'
    PATTERN_SEPARATOR = ';'
    PATTERN_EXPONENT = "E"
    PATTERN_MINUS = '-'

    #    *
    #     * The CURRENCY_SIGN is the standard Unicode symbol for currency.  It
    #     * is used in patterns and substituted with either the currency symbol,
    #     * or if it is doubled, with the international currency symbol.  If the
    #     * CURRENCY_SIGN is seen in a pattern, then the decimal/grouping separators
    #     * are replaced with the monetary decimal/grouping separators.
    #     *
    #     * The CURRENCY_SIGN is not localized.
    #     
    CURRENCY_SIGN = '\u00A4'

    QUOTE = '\''

    _EmptyFieldPositionArray = []

    # Upper limit on integer and fraction digits for a Java double
    DOUBLE_INTEGER_DIGITS = 309
    DOUBLE_FRACTION_DIGITS = 340

    # Upper limit on integer and fraction digits for BigDecimal and BigInteger
    MAXIMUM_INTEGER_DIGITS = Integer.MAX_VALUE
    MAXIMUM_FRACTION_DIGITS = Integer.MAX_VALUE

    # Proclaim JDK 1.1 serial compatibility.
# JAVA TO PYTHON CONVERTER TASK: Java annotations have no direct Python equivalent:
# ORIGINAL LINE: @java.io.Serial static final long serialVersionUID = 864413376551465018L;
    SERIAL_VERSION_UID = 864413376551465018
