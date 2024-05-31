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


from sun.util.locale.provider import CalendarDataUtility
from sun.util.locale.provider import LocaleProviderAdapter
from sun.util.locale.provider import LocaleServiceProviderPool
from sun.util.locale.provider import ResourceBundleBasedAdapter

#*
# * This class represents the set of symbols (such as the decimal separator,
# * the grouping separator, and so on) needed by {@code DecimalFormat}
# * to format numbers. {@code DecimalFormat} creates for itself an instance of
# * {@code DecimalFormatSymbols} from its locale data.  If you need to change any
# * of these symbols, you can get the {@code DecimalFormatSymbols} object from
# * your {@code DecimalFormat} and modify it.
# *
# * <p>If the locale contains "rg" (region override)
# * <a href="../util/Locale.html#def_locale_extension">Unicode extension</a>,
# * the symbols are overridden for the designated region.
# *
# * @see          java.util.Locale
# * @see          DecimalFormat
# * @author       Mark Davis
# * @author       Alan Liu
# * @since 1.1
# 

class DecimalFormatSymbols(Cloneable):

    def _initialize_instance_fields(self):
        # instance fields found by Java to Python Converter:
        self._zeroDigit = '\0'
        self._groupingSeparator = '\0'
        self._decimalSeparator = '\0'
        self._perMill = '\0'
        self._percent = '\0'
        self._digit = '\0'
        self._patternSeparator = '\0'
        self._infinity = None
        self._NaN = None
        self._minusSign = '\0'
        self._currencySymbol = None
        self._intlCurrencySymbol = None
        self._monetarySeparator = '\0'
        self._exponential = '\0'
        self._exponentialSeparator = None
        self._locale = None
        self._perMillText = None
        self._percentText = None
        self._minusSignText = None
        self._monetaryGroupingSeparator = '\0'
        self._currency = None
        self._currencyInitialized = False
        self._hashCode = 0
        self._serialVersionOnStream = java.text.DecimalFormatSymbols.CURRENT_SERIAL_VERSION


    #    *
    #     * Create a DecimalFormatSymbols object for the default
    #     * {@link java.util.Locale.Category#FORMAT FORMAT} locale.
    #     * This constructor can only construct instances for the locales
    #     * supported by the Java runtime environment, not for those
    #     * supported by installed
    #     * {@link java.text.spi.DecimalFormatSymbolsProvider DecimalFormatSymbolsProvider}
    #     * implementations. For full locale coverage, use the
    #     * {@link #getInstance(Locale) getInstance} method.
    #     * <p>This is equivalent to calling
    #     * {@link #DecimalFormatSymbols(Locale)
    #     *     DecimalFormatSymbols(Locale.getDefault(Locale.Category.FORMAT))}.
    #     * @see java.util.Locale#getDefault(java.util.Locale.Category)
    #     * @see java.util.Locale.Category#FORMAT
    #     
# JAVA TO PYTHON CONVERTER TASK: There is no Python equivalent to multiple constructors:
# ORIGINAL LINE: public DecimalFormatSymbols()
    def __init__(self):
        self._initialize_instance_fields()

        self._initialize(java.util.Locale.getDefault(java.util.Locale.Category.FORMAT))

    #    *
    #     * Create a DecimalFormatSymbols object for the given locale.
    #     * This constructor can only construct instances for the locales
    #     * supported by the Java runtime environment, not for those
    #     * supported by installed
    #     * {@link java.text.spi.DecimalFormatSymbolsProvider DecimalFormatSymbolsProvider}
    #     * implementations. For full locale coverage, use the
    #     * {@link #getInstance(Locale) getInstance} method.
    #     * If the specified locale contains the {@link java.util.Locale#UNICODE_LOCALE_EXTENSION}
    #     * for the numbering system, the instance is initialized with the specified numbering
    #     * system if the JRE implementation supports it. For example,
    #     * <pre>
    #     * NumberFormat.getNumberInstance(Locale.forLanguageTag("th-TH-u-nu-thai"))
    #     * </pre>
    #     * This may return a {@code NumberFormat} instance with the Thai numbering system,
    #     * instead of the Latin numbering system.
    #     *
    #     * @param locale the desired locale
    #     * @throws    NullPointerException if {@code locale} is null
    #     
# JAVA TO PYTHON CONVERTER TASK: There is no Python equivalent to multiple constructors:
# ORIGINAL LINE: public DecimalFormatSymbols(java.util.Locale locale)
    def __init__(self, locale):
        self._initialize_instance_fields()

        self._initialize(locale)

    #    *
    #     * Returns an array of all locales for which the
    #     * {@code getInstance} methods of this class can return
    #     * localized instances.
    #     * The returned array represents the union of locales supported by the Java
    #     * runtime and by installed
    #     * {@link java.text.spi.DecimalFormatSymbolsProvider DecimalFormatSymbolsProvider}
    #     * implementations. At a minimum, the returned array must contain a
    #     * {@code Locale} instance equal to {@link Locale#ROOT Locale.ROOT} and
    #     * a {@code Locale} instance equal to {@link Locale#US Locale.US}.
    #     *
    #     * @return an array of locales for which localized
    #     *         {@code DecimalFormatSymbols} instances are available.
    #     * @since 1.6
    #     
    @staticmethod
    def getAvailableLocales():
        pool = sun.util.locale.provider.LocaleServiceProviderPool.getPool(java.text.spi.DecimalFormatSymbolsProvider.class)
        return pool.getAvailableLocales()

    #    *
    #     * Gets the {@code DecimalFormatSymbols} instance for the default
    #     * locale.  This method provides access to {@code DecimalFormatSymbols}
    #     * instances for locales supported by the Java runtime itself as well
    #     * as for those supported by installed
    #     * {@link java.text.spi.DecimalFormatSymbolsProvider
    #     * DecimalFormatSymbolsProvider} implementations.
    #     * <p>This is equivalent to calling
    #     * {@link #getInstance(Locale)
    #     *     getInstance(Locale.getDefault(Locale.Category.FORMAT))}.
    #     * @see java.util.Locale#getDefault(java.util.Locale.Category)
    #     * @see java.util.Locale.Category#FORMAT
    #     * @return a {@code DecimalFormatSymbols} instance.
    #     * @since 1.6
    #     
    @staticmethod
# JAVA TO PYTHON CONVERTER TASK: Python does not allow method overloads:
    def getInstance():
        return java.text.DecimalFormatSymbols.getInstance(java.util.Locale.getDefault(java.util.Locale.Category.FORMAT))

    #    *
    #     * Gets the {@code DecimalFormatSymbols} instance for the specified
    #     * locale.  This method provides access to {@code DecimalFormatSymbols}
    #     * instances for locales supported by the Java runtime itself as well
    #     * as for those supported by installed
    #     * {@link java.text.spi.DecimalFormatSymbolsProvider
    #     * DecimalFormatSymbolsProvider} implementations.
    #     * If the specified locale contains the {@link java.util.Locale#UNICODE_LOCALE_EXTENSION}
    #     * for the numbering system, the instance is initialized with the specified numbering
    #     * system if the JRE implementation supports it. For example,
    #     * <pre>
    #     * NumberFormat.getNumberInstance(Locale.forLanguageTag("th-TH-u-nu-thai"))
    #     * </pre>
    #     * This may return a {@code NumberFormat} instance with the Thai numbering system,
    #     * instead of the Latin numbering system.
    #     *
    #     * @param locale the desired locale.
    #     * @return a {@code DecimalFormatSymbols} instance.
    #     * @throws    NullPointerException if {@code locale} is null
    #     * @since 1.6
    #     
    @staticmethod
# JAVA TO PYTHON CONVERTER TASK: Python does not allow method overloads:
    def getInstance(locale):
        adapter = None
        adapter = sun.util.locale.provider.LocaleProviderAdapter.getAdapter(java.text.spi.DecimalFormatSymbolsProvider.class, locale)
        provider = adapter.getDecimalFormatSymbolsProvider()
        dfsyms = provider.getInstance(locale)
        if dfsyms is None:
            provider = sun.util.locale.provider.LocaleProviderAdapter.forJRE().getDecimalFormatSymbolsProvider()
            dfsyms = provider.getInstance(locale)
        return dfsyms

    #    *
    #     * {@return locale used to create this instance}
    #     *
    #     * @since 19
    #     
    def getLocale(self):
        return self._locale

    #    *
    #     * Gets the character used for zero. Different for Arabic, etc.
    #     *
    #     * @return the character used for zero
    #     
    def getZeroDigit(self):
        return self._zeroDigit

    #    *
    #     * Sets the character used for zero. Different for Arabic, etc.
    #     *
    #     * @param zeroDigit the character used for zero
    #     
    def setZeroDigit(self, zeroDigit):
        self._hashCode = 0
        self._zeroDigit = zeroDigit

    #    *
    #     * Gets the character used for grouping separator. Different for French, etc.
    #     *
    #     * @return the grouping separator
    #     
    def getGroupingSeparator(self):
        return self._groupingSeparator

    #    *
    #     * Sets the character used for grouping separator. Different for French, etc.
    #     *
    #     * @param groupingSeparator the grouping separator
    #     
    def setGroupingSeparator(self, groupingSeparator):
        self._hashCode = 0
        self._groupingSeparator = groupingSeparator

    #    *
    #     * Gets the character used for decimal sign. Different for French, etc.
    #     *
    #     * @return the character used for decimal sign
    #     
    def getDecimalSeparator(self):
        return self._decimalSeparator

    #    *
    #     * Sets the character used for decimal sign. Different for French, etc.
    #     *
    #     * @param decimalSeparator the character used for decimal sign
    #     
    def setDecimalSeparator(self, decimalSeparator):
        self._hashCode = 0
        self._decimalSeparator = decimalSeparator

    #    *
    #     * Gets the character used for per mille sign. Different for Arabic, etc.
    #     *
    #     * @return the character used for per mille sign
    #     
    def getPerMill(self):
        return self._perMill

    #    *
    #     * Sets the character used for per mille sign. Different for Arabic, etc.
    #     *
    #     * @param perMill the character used for per mille sign
    #     
    def setPerMill(self, perMill):
        self._hashCode = 0
        self._perMill = perMill
        self._perMillText = perMill

    #    *
    #     * Gets the character used for percent sign. Different for Arabic, etc.
    #     *
    #     * @return the character used for percent sign
    #     
    def getPercent(self):
        return self._percent

    #    *
    #     * Sets the character used for percent sign. Different for Arabic, etc.
    #     *
    #     * @param percent the character used for percent sign
    #     
    def setPercent(self, percent):
        self._hashCode = 0
        self._percent = percent
        self._percentText = percent

    #    *
    #     * Gets the character used for a digit in a pattern.
    #     *
    #     * @return the character used for a digit in a pattern
    #     
    def getDigit(self):
        return self._digit

    #    *
    #     * Sets the character used for a digit in a pattern.
    #     *
    #     * @param digit the character used for a digit in a pattern
    #     
    def setDigit(self, digit):
        self._hashCode = 0
        self._digit = digit

    #    *
    #     * Gets the character used to separate positive and negative subpatterns
    #     * in a pattern.
    #     *
    #     * @return the pattern separator
    #     
    def getPatternSeparator(self):
        return self._patternSeparator

    #    *
    #     * Sets the character used to separate positive and negative subpatterns
    #     * in a pattern.
    #     *
    #     * @param patternSeparator the pattern separator
    #     
    def setPatternSeparator(self, patternSeparator):
        self._hashCode = 0
        self._patternSeparator = patternSeparator

    #    *
    #     * Gets the string used to represent infinity. Almost always left
    #     * unchanged.
    #     *
    #     * @return the string representing infinity
    #     
    def getInfinity(self):
        return self._infinity

    #    *
    #     * Sets the string used to represent infinity. Almost always left
    #     * unchanged.
    #     *
    #     * @param infinity the string representing infinity
    #     
    def setInfinity(self, infinity):
        self._hashCode = 0
        self._infinity = infinity

    #    *
    #     * Gets the string used to represent "not a number". Almost always left
    #     * unchanged.
    #     *
    #     * @return the string representing "not a number"
    #     
    def getNaN(self):
        return self._NaN

    #    *
    #     * Sets the string used to represent "not a number". Almost always left
    #     * unchanged.
    #     *
    #     * @param NaN the string representing "not a number"
    #     
    def setNaN(self, NaN):
        self._hashCode = 0
        self._NaN = NaN

    #    *
    #     * Gets the character used to represent minus sign. If no explicit
    #     * negative format is specified, one is formed by prefixing
    #     * minusSign to the positive format.
    #     *
    #     * @return the character representing minus sign
    #     
    def getMinusSign(self):
        return self._minusSign

    #    *
    #     * Sets the character used to represent minus sign. If no explicit
    #     * negative format is specified, one is formed by prefixing
    #     * minusSign to the positive format.
    #     *
    #     * @param minusSign the character representing minus sign
    #     
    def setMinusSign(self, minusSign):
        self._hashCode = 0
        self._minusSign = minusSign
        self._minusSignText = minusSign

    #    *
    #     * Returns the currency symbol for the currency of these
    #     * DecimalFormatSymbols in their locale.
    #     *
    #     * @return the currency symbol
    #     * @since 1.2
    #     
    def getCurrencySymbol(self):
        self._initializeCurrency(self._locale)
        return self._currencySymbol

    #    *
    #     * Sets the currency symbol for the currency of these
    #     * DecimalFormatSymbols in their locale.
    #     *
    #     * @param currency the currency symbol
    #     * @since 1.2
    #     
    def setCurrencySymbol(self, currency):
        self._initializeCurrency(self._locale)
        self._hashCode = 0
        self._currencySymbol = currency

    #    *
    #     * Returns the ISO 4217 currency code of the currency of these
    #     * DecimalFormatSymbols.
    #     *
    #     * @return the currency code
    #     * @since 1.2
    #     
    def getInternationalCurrencySymbol(self):
        self._initializeCurrency(self._locale)
        return self._intlCurrencySymbol

    #    *
    #     * Sets the ISO 4217 currency code of the currency of these
    #     * DecimalFormatSymbols.
    #     * If the currency code is valid (as defined by
    #     * {@link java.util.Currency#getInstance(java.lang.String) Currency.getInstance}),
    #     * this also sets the currency attribute to the corresponding Currency
    #     * instance and the currency symbol attribute to the currency's symbol
    #     * in the DecimalFormatSymbols' locale. If the currency code is not valid,
    #     * then the currency attribute is set to null and the currency symbol
    #     * attribute is not modified.
    #     *
    #     * @param currencyCode the currency code
    #     * @see #setCurrency
    #     * @see #setCurrencySymbol
    #     * @since 1.2
    #     
    def setInternationalCurrencySymbol(self, currencyCode):
        self._initializeCurrency(self._locale)
        self._hashCode = 0
        self._intlCurrencySymbol = currencyCode
        self._currency = None
        if currencyCode is not None:
            try:
                self._currency = java.util.Currency.getInstance(currencyCode)
                self._currencySymbol = self._currency.getSymbol()
            except IllegalArgumentException as e:
                pass

    #    *
    #     * Gets the currency of these DecimalFormatSymbols. May be null if the
    #     * currency symbol attribute was previously set to a value that's not
    #     * a valid ISO 4217 currency code.
    #     *
    #     * @return the currency used, or null
    #     * @since 1.4
    #     
    def getCurrency(self):
        self._initializeCurrency(self._locale)
        return self._currency

    #    *
    #     * Sets the currency of these DecimalFormatSymbols.
    #     * This also sets the currency symbol attribute to the currency's symbol
    #     * in the DecimalFormatSymbols' locale, and the international currency
    #     * symbol attribute to the currency's ISO 4217 currency code.
    #     *
    #     * @param currency the new currency to be used
    #     * @throws    NullPointerException if {@code currency} is null
    #     * @since 1.4
    #     * @see #setCurrencySymbol
    #     * @see #setInternationalCurrencySymbol
    #     
    def setCurrency(self, currency):
        if currency is None:
            raise NullPointerException()
        self._initializeCurrency(self._locale)
        self._hashCode = 0
        self._currency = currency
        self._intlCurrencySymbol = currency.getCurrencyCode()
        self._currencySymbol = currency.getSymbol(self._locale)


    #    *
    #     * Returns the monetary decimal separator.
    #     *
    #     * @return the monetary decimal separator
    #     * @since 1.2
    #     
    def getMonetaryDecimalSeparator(self):
        return self._monetarySeparator

    #    *
    #     * Sets the monetary decimal separator.
    #     *
    #     * @param sep the monetary decimal separator
    #     * @since 1.2
    #     
    def setMonetaryDecimalSeparator(self, sep):
        self._hashCode = 0
        self._monetarySeparator = sep

    #    *
    #     * Returns the string used to separate the mantissa from the exponent.
    #     * Examples: "x10^" for 1.23x10^4, "E" for 1.23E4.
    #     *
    #     * @return the exponent separator string
    #     * @see #setExponentSeparator(java.lang.String)
    #     * @since 1.6
    #     
    def getExponentSeparator(self):
        return self._exponentialSeparator

    #    *
    #     * Sets the string used to separate the mantissa from the exponent.
    #     * Examples: "x10^" for 1.23x10^4, "E" for 1.23E4.
    #     *
    #     * @param exp the exponent separator string
    #     * @throws    NullPointerException if {@code exp} is null
    #     * @see #getExponentSeparator()
    #     * @since 1.6
    #     
    def setExponentSeparator(self, exp):
        if exp is None:
            raise NullPointerException()
        self._hashCode = 0
        self._exponentialSeparator = exp

    #    *
    #     * Gets the character used for grouping separator for currencies.
    #     * May be different from {@code grouping separator} in some locales,
    #     * e.g, German in Austria.
    #     *
    #     * @return the monetary grouping separator
    #     * @since 15
    #     
    def getMonetaryGroupingSeparator(self):
        return self._monetaryGroupingSeparator

    #    *
    #     * Sets the character used for grouping separator for currencies.
    #     * Invocation of this method will not affect the normal
    #     * {@code grouping separator}.
    #     *
    #     * @param monetaryGroupingSeparator the monetary grouping separator
    #     * @see #setGroupingSeparator(char)
    #     * @since 15
    #     
    def setMonetaryGroupingSeparator(self, monetaryGroupingSeparator):
        self._hashCode = 0
        self._monetaryGroupingSeparator = monetaryGroupingSeparator

    #------------------------------------------------------------
    # BEGIN   Package Private methods ... to be made public later
    #------------------------------------------------------------

    #    *
    #     * Returns the character used to separate the mantissa from the exponent.
    #     
    def getExponentialSymbol(self):
        return self._exponential

    #    *
    #     * Sets the character used to separate the mantissa from the exponent.
    #     
    def setExponentialSymbol(self, exp):
        self._exponential = exp

    #    *
    #     * Gets the string used for per mille sign. Different for Arabic, etc.
    #     *
    #     * @return the string used for per mille sign
    #     * @since 13
    #     
    def getPerMillText(self):
        return self._perMillText

    #    *
    #     * Sets the string used for per mille sign. Different for Arabic, etc.
    #     *
    #     * Setting the {@code perMillText} affects the return value of
    #     * {@link #getPerMill()}, in which the first non-format character of
    #     * {@code perMillText} is returned.
    #     *
    #     * @param perMillText the string used for per mille sign
    #     * @throws NullPointerException if {@code perMillText} is null
    #     * @throws IllegalArgumentException if {@code perMillText} is an empty string
    #     * @see #getPerMill()
    #     * @see #getPerMillText()
    #     * @since 13
    #     
    def setPerMillText(self, perMillText):
        java.util.Objects.requireNonNull(perMillText)
        if len(perMillText) == 0:
            raise IllegalArgumentException("Empty argument string")

        self._hashCode = 0
        self._perMillText = perMillText
        self._perMill = self._findNonFormatChar(perMillText, '\u2030')

    #    *
    #     * Gets the string used for percent sign. Different for Arabic, etc.
    #     *
    #     * @return the string used for percent sign
    #     * @since 13
    #     
    def getPercentText(self):
        return self._percentText

    #    *
    #     * Sets the string used for percent sign. Different for Arabic, etc.
    #     *
    #     * Setting the {@code percentText} affects the return value of
    #     * {@link #getPercent()}, in which the first non-format character of
    #     * {@code percentText} is returned.
    #     *
    #     * @param percentText the string used for percent sign
    #     * @throws NullPointerException if {@code percentText} is null
    #     * @throws IllegalArgumentException if {@code percentText} is an empty string
    #     * @see #getPercent()
    #     * @see #getPercentText()
    #     * @since 13
    #     
    def setPercentText(self, percentText):
        java.util.Objects.requireNonNull(percentText)
        if len(percentText) == 0:
            raise IllegalArgumentException("Empty argument string")

        self._hashCode = 0
        self._percentText = percentText
        self._percent = self._findNonFormatChar(percentText, '%')

    #    *
    #     * Gets the string used to represent minus sign. If no explicit
    #     * negative format is specified, one is formed by prefixing
    #     * minusSignText to the positive format.
    #     *
    #     * @return the string representing minus sign
    #     * @since 13
    #     
    def getMinusSignText(self):
        return self._minusSignText

    #    *
    #     * Sets the string used to represent minus sign. If no explicit
    #     * negative format is specified, one is formed by prefixing
    #     * minusSignText to the positive format.
    #     *
    #     * Setting the {@code minusSignText} affects the return value of
    #     * {@link #getMinusSign()}, in which the first non-format character of
    #     * {@code minusSignText} is returned.
    #     *
    #     * @param minusSignText the character representing minus sign
    #     * @throws NullPointerException if {@code minusSignText} is null
    #     * @throws IllegalArgumentException if {@code minusSignText} is an
    #     *  empty string
    #     * @see #getMinusSign()
    #     * @see #getMinusSignText()
    #     * @since 13
    #     
    def setMinusSignText(self, minusSignText):
        java.util.Objects.requireNonNull(minusSignText)
        if len(minusSignText) == 0:
            raise IllegalArgumentException("Empty argument string")

        self._hashCode = 0
        self._minusSignText = minusSignText
        self._minusSign = self._findNonFormatChar(minusSignText, '-')

    #------------------------------------------------------------
    # END     Package Private methods ... to be made public later
    #------------------------------------------------------------

    #    *
    #     * Standard override.
    #     
    def clone(self):
        try:
            return super().clone()
            # other fields are bit-copied
        except CloneNotSupportedException as e:
            raise InternalError(e)

    #    *
    #     * Compares the specified object with this {@code DecimalFormatSymbols} for equality.
    #     * Returns true if the object is also a {@code DecimalFormatSymbols} and the two
    #     * {@code DecimalFormatSymbols} objects represent the same set of symbols.
    #     *
    #     * @implSpec This method performs an equality check with a notion of class
    #     * identity based on {@code getClass()}, rather than {@code instanceof}.
    #     * Therefore, in the equals methods in subclasses, no instance of this class
    #     * should compare as equal to an instance of a subclass.
    #     * @param  obj object to be compared for equality
    #     * @return {@code true} if the specified object is equal to this {@code DecimalFormatSymbols}
    #     * @see Object#equals(Object)
    #     
    def equals(self, obj):
        if self is obj:
            return True
        if obj is None or getClass() != type(obj):
            return False
        other = obj
        return (self._zeroDigit == other._zeroDigit and self._groupingSeparator == other._groupingSeparator and self._decimalSeparator == other._decimalSeparator and self._percent == other._percent and self._percentText == other._percentText and self._perMill == other._perMill and self._perMillText == other._perMillText and self._digit == other._digit and self._minusSign == other._minusSign and self._minusSignText == other._minusSignText and self._patternSeparator == other._patternSeparator and self._infinity == other._infinity and self._NaN == other._NaN and self.getCurrencySymbol() == other.getCurrencySymbol() and self._intlCurrencySymbol == other._intlCurrencySymbol and self._currency is other._currency and self._monetarySeparator == other._monetarySeparator and self._monetaryGroupingSeparator == other._monetaryGroupingSeparator and self._exponentialSeparator == other._exponentialSeparator and self._locale is other._locale)

    #    *
    #     * {@return the hash code for this {@code DecimalFormatSymbols}}
    #     *
    #     * @implSpec Non-transient instance fields of this class are used to calculate
    #     * a hash code value which adheres to the contract defined in {@link Objects#hashCode}.
    #     * @see Object#hashCode()
    #     
    def hashCode(self):
        if self._hashCode == 0:
            self._hashCode = java.util.Objects.hash(self._zeroDigit, self._groupingSeparator, self._decimalSeparator, self._percent, self._percentText, self._perMill, self._perMillText, self._digit, self._minusSign, self._minusSignText, self._patternSeparator, self._infinity, self._NaN, self.getCurrencySymbol(), self._intlCurrencySymbol, self._currency, self._monetarySeparator, self._monetaryGroupingSeparator, self._exponentialSeparator, self._locale)
        return self._hashCode

    #    *
    #     * Initializes the symbols from the FormatData resource bundle.
    #     
    def _initialize(self, locale):
        self._locale = locale

        # check for region override
        override = sun.util.locale.provider.CalendarDataUtility.findRegionOverride(locale) if locale.getUnicodeLocaleType("nu") is None else locale

        # get resource bundle data
        adapter = sun.util.locale.provider.LocaleProviderAdapter.getAdapter(java.text.spi.DecimalFormatSymbolsProvider.class, override)
        # Avoid potential recursions
        if not(isinstance(adapter, sun.util.locale.provider.ResourceBundleBasedAdapter)):
            adapter = sun.util.locale.provider.LocaleProviderAdapter.getResourceBundleBased()
        data = adapter.getLocaleResources(override).getDecimalFormatSymbolsData()
        numberElements = data[0]

        self._decimalSeparator = numberElements[0][0]
        self._groupingSeparator = numberElements[1][0]
        self._patternSeparator = numberElements[2][0]
        self._percentText = numberElements[3]
        self._percent = self._findNonFormatChar(self._percentText, '%')
        self._zeroDigit = numberElements[4][0] #different for Arabic,etc.
        self._digit = numberElements[5][0]
        self._minusSignText = numberElements[6]
        self._minusSign = self._findNonFormatChar(self._minusSignText, '-')
        self._exponential = numberElements[7][0]
        self._exponentialSeparator = numberElements[7] #string representation new since 1.6
        self._perMillText = numberElements[8]
        self._perMill = self._findNonFormatChar(self._perMillText, '\u2030')
        self._infinity = numberElements[9]
        self._NaN = numberElements[10]

        # monetary decimal/grouping separators may be missing in resource bundles
        self._monetarySeparator = self._decimalSeparator if len(numberElements) < 12 or len(numberElements[11]) == 0 else numberElements[11][0]
        self._monetaryGroupingSeparator = self._groupingSeparator if len(numberElements) < 13 or len(numberElements[12]) == 0 else numberElements[12][0]

        # maybe filled with previously cached values, or null.
        self._intlCurrencySymbol = str(data[1])
        self._currencySymbol = str(data[2])

    #    *
    #     * Obtains non-format single character from String
    #     
    def _findNonFormatChar(self, src, defChar):
        return chr(src.chars().filter(lambda c : Character.getType(c) != Character.FORMAT).findFirst().orElse(defChar))

    #    *
    #     * Lazy initialization for currency related fields
    #     
    def _initializeCurrency(self, locale):
        if self._currencyInitialized:
            return

        # Try to obtain the currency used in the locale's country.
        # Check for empty country string separately because it's a valid
        # country ID for Locale (and used for the C locale), but not a valid
        # ISO 3166 country code, and exceptions are expensive.
        if not locale.getCountry().isEmpty():
            try:
                self._currency = java.util.Currency.getInstance(locale)
            except IllegalArgumentException as e:
                # use default values below for compatibility
                pass

        if self._currency is not None:
            # get resource bundle data
            adapter = sun.util.locale.provider.LocaleProviderAdapter.getAdapter(java.text.spi.DecimalFormatSymbolsProvider.class, locale)
            # Avoid potential recursions
            if not(isinstance(adapter, sun.util.locale.provider.ResourceBundleBasedAdapter)):
                adapter = sun.util.locale.provider.LocaleProviderAdapter.getResourceBundleBased()
            data = adapter.getLocaleResources(locale).getDecimalFormatSymbolsData()
            self._intlCurrencySymbol = self._currency.getCurrencyCode()
            if data[1] is not None and data[1] is self._intlCurrencySymbol:
                self._currencySymbol = str(data[2])
            else:
                self._currencySymbol = self._currency.getSymbol(locale)
                data[1] = self._intlCurrencySymbol
                data[2] = self._currencySymbol
        else:
            # default values
            self._intlCurrencySymbol = "XXX"
            try:
                self._currency = java.util.Currency.getInstance(self._intlCurrencySymbol)
            except IllegalArgumentException as e:
                pass
            self._currencySymbol = "\u00A4"

        self._currencyInitialized = True

    #    *
    #     * Reads the default serializable fields, provides default values for objects
    #     * in older serial versions, and initializes non-serializable fields.
    #     * If {@code serialVersionOnStream}
    #     * is less than 1, initializes {@code monetarySeparator} to be
    #     * the same as {@code decimalSeparator} and {@code exponential}
    #     * to be 'E'.
    #     * If {@code serialVersionOnStream} is less than 2,
    #     * initializes {@code locale} to the root locale, and initializes
    #     * If {@code serialVersionOnStream} is less than 3, it initializes
    #     * {@code exponentialSeparator} using {@code exponential}.
    #     * If {@code serialVersionOnStream} is less than 4, it initializes
    #     * {@code perMillText}, {@code percentText}, and
    #     * {@code minusSignText} using {@code perMill}, {@code percent}, and
    #     * {@code minusSign} respectively.
    #     * If {@code serialVersionOnStream} is less than 5, it initializes
    #     * {@code monetaryGroupingSeparator} using {@code groupingSeparator}.
    #     * Sets {@code serialVersionOnStream} back to the maximum allowed value so that
    #     * default serialization will work properly if this object is streamed out again.
    #     * Initializes the currency from the intlCurrencySymbol field.
    #     *
    #     * @throws InvalidObjectException if {@code char} and {@code String}
    #     *      representations of either percent, per mille, and/or minus sign disagree.
    #     * @since  1.1.6
    #     
# JAVA TO PYTHON CONVERTER TASK: Java annotations have no direct Python equivalent:
# ORIGINAL LINE: @java.io.Serial private void readObject(java.io.ObjectInputStream stream) throws IOException, ClassNotFoundException
# JAVA TO PYTHON CONVERTER WARNING: Method 'throws' clauses are not available in Python:
    def _readObject(self, stream):
        stream.defaultReadObject()
        if self._serialVersionOnStream < 1:
            # Didn't have monetarySeparator or exponential field
            # use defaults.
            self._monetarySeparator = self._decimalSeparator
            self._exponential = 'E'
        if self._serialVersionOnStream < 2:
            # didn't have locale; use root locale
            self._locale = java.util.Locale.ROOT
        if self._serialVersionOnStream < 3:
            # didn't have exponentialSeparator. Create one using exponential
            self._exponentialSeparator = self._exponential
        if self._serialVersionOnStream < 4:
            # didn't have perMillText, percentText, and minusSignText.
            # Create one using corresponding char variations.
            self._perMillText = self._perMill
            self._percentText = self._percent
            self._minusSignText = self._minusSign
        else:
            # Check whether char and text fields agree
            if self._findNonFormatChar(self._perMillText, '\uFFFF') != self._perMill or self._findNonFormatChar(self._percentText, '\uFFFF') != self._percent or self._findNonFormatChar(self._minusSignText, '\uFFFF') != self._minusSign:
                raise java.io.InvalidObjectException("'char' and 'String' representations of either percent, " + "per mille, and/or minus sign disagree.")
        if self._serialVersionOnStream < 5:
            # didn't have monetaryGroupingSeparator. Create one using groupingSeparator
            self._monetaryGroupingSeparator = self._groupingSeparator

        self._serialVersionOnStream = java.text.DecimalFormatSymbols.CURRENT_SERIAL_VERSION

        if self._intlCurrencySymbol is not None:
            try:
                self._currency = java.util.Currency.getInstance(self._intlCurrencySymbol)
            except IllegalArgumentException as e:
                pass
            self._currencyInitialized = True

    #    *
    #     * Character used for zero.
    #     *
    #     * @serial
    #     * @see #getZeroDigit
    #     

    #    *
    #     * Character used for grouping separator.
    #     *
    #     * @serial
    #     * @see #getGroupingSeparator
    #     

    #    *
    #     * Character used for decimal sign.
    #     *
    #     * @serial
    #     * @see #getDecimalSeparator
    #     

    #    *
    #     * Character used for per mille sign.
    #     *
    #     * @serial
    #     * @see #getPerMill
    #     

    #    *
    #     * Character used for percent sign.
    #     * @serial
    #     * @see #getPercent
    #     

    #    *
    #     * Character used for a digit in a pattern.
    #     *
    #     * @serial
    #     * @see #getDigit
    #     

    #    *
    #     * Character used to separate positive and negative subpatterns
    #     * in a pattern.
    #     *
    #     * @serial
    #     * @see #getPatternSeparator
    #     

    #    *
    #     * String used to represent infinity.
    #     * @serial
    #     * @see #getInfinity
    #     

    #    *
    #     * String used to represent "not a number".
    #     * @serial
    #     * @see #getNaN
    #     

    #    *
    #     * Character used to represent minus sign.
    #     * @serial
    #     * @see #getMinusSign
    #     

    #    *
    #     * String denoting the local currency, e.g. "$".
    #     * @serial
    #     * @see #getCurrencySymbol
    #     

    #    *
    #     * ISO 4217 currency code denoting the local currency, e.g. "USD".
    #     * @serial
    #     * @see #getInternationalCurrencySymbol
    #     

    #    *
    #     * The decimal separator used when formatting currency values.
    #     * @serial
    #     * @since  1.1.6
    #     * @see #getMonetaryDecimalSeparator
    #     

    #    *
    #     * The character used to distinguish the exponent in a number formatted
    #     * in exponential notation, e.g. 'E' for a number such as "1.23E45".
    #     * <p>
    #     * Note that the public API provides no way to set this field,
    #     * even though it is supported by the implementation and the stream format.
    #     * The intent is that this will be added to the API in the future.
    #     *
    #     * @serial
    #     * @since  1.1.6
    #     

    #    *
    #     * The string used to separate the mantissa from the exponent.
    #     * Examples: "x10^" for 1.23x10^4, "E" for 1.23E4.
    #     * <p>
    #     * If both {@code exponential} and {@code exponentialSeparator}
    #     * exist, this {@code exponentialSeparator} has the precedence.
    #     *
    #     * @serial
    #     * @since 1.6
    #     

    #    *
    #     * The locale of these currency format symbols.
    #     *
    #     * @serial
    #     * @since 1.4
    #     

    #    *
    #     * String representation of per mille sign, which may include
    #     * formatting characters, such as BiDi control characters.
    #     * The first non-format character of this string is the same as
    #     * {@code perMill}.
    #     *
    #     * @serial
    #     * @since 13
    #     

    #    *
    #     * String representation of percent sign, which may include
    #     * formatting characters, such as BiDi control characters.
    #     * The first non-format character of this string is the same as
    #     * {@code percent}.
    #     *
    #     * @serial
    #     * @since 13
    #     

    #    *
    #     * String representation of minus sign, which may include
    #     * formatting characters, such as BiDi control characters.
    #     * The first non-format character of this string is the same as
    #     * {@code minusSign}.
    #     *
    #     * @serial
    #     * @since 13
    #     

    #    *
    #     * The grouping separator used when formatting currency values.
    #     *
    #     * @serial
    #     * @since 15
    #     

    # currency; only the ISO code is serialized.

    #    *
    #     * Cached hash code.
    #     

    # Proclaim JDK 1.1 FCS compatibility
# JAVA TO PYTHON CONVERTER TASK: Java annotations have no direct Python equivalent:
# ORIGINAL LINE: @java.io.Serial static final long serialVersionUID = 5772796243397350300L;
    SERIAL_VERSION_UID = 5772796243397350300

    # The internal serial version which says which version was written
    # - 0 (default) for version up to JDK 1.1.5
    # - 1 for version from JDK 1.1.6, which includes two new fields:
    #     monetarySeparator and exponential.
    # - 2 for version from J2SE 1.4, which includes locale field.
    # - 3 for version from J2SE 1.6, which includes exponentialSeparator field.
    # - 4 for version from Java SE 13, which includes perMillText, percentText,
    #      and minusSignText field.
    # - 5 for version from Java SE 15, which includes monetaryGroupingSeparator.
    CURRENT_SERIAL_VERSION = 5

    #    *
    #     * Describes the version of {@code DecimalFormatSymbols} present on the stream.
    #     * Possible values are:
    #     * <ul>
    #     * <li><b>0</b> (or uninitialized): versions prior to JDK 1.1.6.
    #     *
    #     * <li><b>1</b>: Versions written by JDK 1.1.6 or later, which include
    #     *      two new fields: {@code monetarySeparator} and {@code exponential}.
    #     * <li><b>2</b>: Versions written by J2SE 1.4 or later, which include a
    #     *      new {@code locale} field.
    #     * <li><b>3</b>: Versions written by J2SE 1.6 or later, which include a
    #     *      new {@code exponentialSeparator} field.
    #     * <li><b>4</b>: Versions written by Java SE 13 or later, which include
    #     *      new {@code perMillText}, {@code percentText}, and
    #     *      {@code minusSignText} field.
    #     * <li><b>5</b>: Versions written by Java SE 15 or later, which include
    #     *      new {@code monetaryGroupingSeparator} field.
    #     * * </ul>
    #     * When streaming out a {@code DecimalFormatSymbols}, the most recent format
    #     * (corresponding to the highest allowable {@code serialVersionOnStream})
    #     * is always written.
    #     *
    #     * @serial
    #     * @since  1.1.6
    #     
