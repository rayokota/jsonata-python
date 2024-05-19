#******************************************************************************
# * Copyright (c) 2013, 2016 EclipseSource.
# *
# * Permission is hereby granted, free of charge, to any person obtaining a copy
# * of this software and associated documentation files (the "Software"), to deal
# * in the Software without restriction, including without limitation the rights
# * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# * copies of the Software, and to permit persons to whom the Software is
# * furnished to do so, subject to the following conditions:
# *
# * The above copyright notice and this permission notice shall be included in all
# * copies or substantial portions of the Software.
# *
# * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# * SOFTWARE.
# *****************************************************************************
#package com.eclipsesource.json



#*
# * A streaming parser for JSON text. The parser reports all events to a given handler.
# 
class JsonParser:

    MAX_NESTING_LEVEL = 1000
    MIN_BUFFER_SIZE = 10
    DEFAULT_BUFFER_SIZE = 1024


    #  
    #   * |                      bufferOffset
    #   *                        v
    #   * [a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t]        < input
    #   *                       [l|m|n|o|p|q|r|s|t|?|?]    < buffer
    #   *                          ^               ^
    #   *                       |  index           fill
    #   

    #  *
    #   * Creates a new JsonParser with the given handler. The parser will report all parser events to
    #   * this handler.
    #   *
    #   * @param handler
    #   *          the handler to process parser events
    #   
# JAVA TO PYTHON CONVERTER TASK: Java annotations have no direct Python equivalent:
# ORIGINAL LINE: @SuppressWarnings("unchecked") public JsonParser(JsonHandler<?, ?> handler)
    def __init__(self, handler):
        # instance fields found by Java to Python Converter:
        self._handler = None
        self._reader = None
        self._buffer = None
        self._bufferOffset = 0
        self._index = 0
        self._fill = 0
        self._line = 0
        self._lineOffset = 0
        self._current = 0
        self._captureBuffer = None
        self._captureStart = 0
        self._nestingLevel = 0

        if handler is None:
            raise NullPointerException("handler is null")
        self._handler = handler
        handler.parser = self

    #  *
    #   * Parses the given input string. The input must contain a valid JSON value, optionally padded
    #   * with whitespace.
    #   *
    #   * @param string
    #   *          the input string, must be valid JSON
    #   * @throws ParseException
    #   *           if the input is not valid JSON
    #   
# JAVA TO PYTHON CONVERTER TASK: Python does not allow method overloads:
    def parse(self, string):
        if string is None:
            raise NullPointerException("string is null")
        bufferSize = max(com.dashjoin.jsonata.json.JsonParser.MIN_BUFFER_SIZE, min(com.dashjoin.jsonata.json.JsonParser.DEFAULT_BUFFER_SIZE, len(string)))
        try:
            self.parse(java.io.StringReader(string), bufferSize)
        except java.io.IOException as exception:
            # StringReader does not throw IOException
            raise RuntimeException(exception)

    #  *
    #   * Reads the entire input from the given reader and parses it as JSON. The input must contain a
    #   * valid JSON value, optionally padded with whitespace.
    #   * <p>
    #   * Characters are read in chunks into a default-sized input buffer. Hence, wrapping a reader in an
    #   * additional <code>BufferedReader</code> likely won't improve reading performance.
    #   * </p>
    #   *
    #   * @param reader
    #   *          the reader to read the input from
    #   * @throws IOException
    #   *           if an I/O error occurs in the reader
    #   * @throws ParseException
    #   *           if the input is not valid JSON
    #   
# JAVA TO PYTHON CONVERTER WARNING: Method 'throws' clauses are not available in Python:
# ORIGINAL LINE: public void parse(java.io.Reader reader) throws java.io.IOException
# JAVA TO PYTHON CONVERTER TASK: Python does not allow method overloads:
    def parse(self, reader):
        self.parse(reader, com.dashjoin.jsonata.json.JsonParser.DEFAULT_BUFFER_SIZE)

    #  *
    #   * Reads the entire input from the given reader and parses it as JSON. The input must contain a
    #   * valid JSON value, optionally padded with whitespace.
    #   * <p>
    #   * Characters are read in chunks into an input buffer of the given size. Hence, wrapping a reader
    #   * in an additional <code>BufferedReader</code> likely won't improve reading performance.
    #   * </p>
    #   *
    #   * @param reader
    #   *          the reader to read the input from
    #   * @param buffersize
    #   *          the size of the input buffer in chars
    #   * @throws IOException
    #   *           if an I/O error occurs in the reader
    #   * @throws ParseException
    #   *           if the input is not valid JSON
    #   
# JAVA TO PYTHON CONVERTER WARNING: Method 'throws' clauses are not available in Python:
# ORIGINAL LINE: public void parse(java.io.Reader reader, int buffersize) throws java.io.IOException
# JAVA TO PYTHON CONVERTER TASK: Python does not allow method overloads:
    def parse(self, reader, buffersize):
        if reader is None:
            raise NullPointerException("reader is null")
        if buffersize <= 0:
            raise IllegalArgumentException("buffersize is zero or negative")
        self._reader = reader
        self._buffer = ['\0' for _ in range(buffersize)]
        self._bufferOffset = 0
        self._index = 0
        self._fill = 0
        self._line = 1
        self._lineOffset = 0
        self._current = 0
        self._captureStart = -1
        self._read()
        self._skipWhiteSpace()
        self._readValue()
        self._skipWhiteSpace()
        if not self._isEndOfText():
            raise self._error("Unexpected character")

# JAVA TO PYTHON CONVERTER WARNING: Method 'throws' clauses are not available in Python:
# ORIGINAL LINE: private void readValue() throws java.io.IOException
    def _readValue(self):
        if self._current == 'n':
            self._readNull()
        elif self._current == 't':
            self._readTrue()
        elif self._current == 'f':
            self._readFalse()
        elif self._current == '"':
            self._readString()
        elif self._current == '[':
            self._readArray()
        elif self._current == '{':
            self._readObject()
        elif (self._current == '-') or (self._current == '0') or (self._current == '1') or (self._current == '2') or (self._current == '3') or (self._current == '4') or (self._current == '5') or (self._current == '6') or (self._current == '7') or (self._current == '8') or (self._current == '9'):
            self._readNumber()
        else:
            raise self._expected("value")

# JAVA TO PYTHON CONVERTER WARNING: Method 'throws' clauses are not available in Python:
# ORIGINAL LINE: private void readArray() throws java.io.IOException
    def _readArray(self):
        array = self._handler.startArray()
        self._read()
        nestingLevel += 1
# JAVA TO PYTHON CONVERTER WARNING: An assignment within expression was extracted from the following statement:
# ORIGINAL LINE: if (++nestingLevel > MAX_NESTING_LEVEL)
        if self._nestingLevel > com.dashjoin.jsonata.json.JsonParser.MAX_NESTING_LEVEL:
            raise self._error("Nesting too deep")
        self._skipWhiteSpace()
        if self._readChar(']'):
            self._nestingLevel -= 1
            self._handler.endArray(array)
            return
        loop_condition = True
        while loop_condition:
            self._skipWhiteSpace()
            self._handler.startArrayValue(array)
            self._readValue()
            self._handler.endArrayValue(array)
            self._skipWhiteSpace()
            loop_condition = self._readChar(',')
        if not self._readChar(']'):
            raise self._expected("',' or ']'")
        self._nestingLevel -= 1
        self._handler.endArray(array)

# JAVA TO PYTHON CONVERTER WARNING: Method 'throws' clauses are not available in Python:
# ORIGINAL LINE: private void readObject() throws java.io.IOException
    def _readObject(self):
        object = self._handler.startObject()
        self._read()
        nestingLevel += 1
# JAVA TO PYTHON CONVERTER WARNING: An assignment within expression was extracted from the following statement:
# ORIGINAL LINE: if (++nestingLevel > MAX_NESTING_LEVEL)
        if self._nestingLevel > com.dashjoin.jsonata.json.JsonParser.MAX_NESTING_LEVEL:
            raise self._error("Nesting too deep")
        self._skipWhiteSpace()
        if self._readChar('}'):
            self._nestingLevel -= 1
            self._handler.endObject(object)
            return
        loop_condition = True
        while loop_condition:
            self._skipWhiteSpace()
            self._handler.startObjectName(object)
            name = self._readName()
            self._handler.endObjectName(object, name)
            self._skipWhiteSpace()
            if not self._readChar(':'):
                raise self._expected("':'")
            self._skipWhiteSpace()
            self._handler.startObjectValue(object, name)
            self._readValue()
            self._handler.endObjectValue(object, name)
            self._skipWhiteSpace()
            loop_condition = self._readChar(',')
        if not self._readChar('}'):
            raise self._expected("',' or '}'")
        self._nestingLevel -= 1
        self._handler.endObject(object)

# JAVA TO PYTHON CONVERTER WARNING: Method 'throws' clauses are not available in Python:
# ORIGINAL LINE: private String readName() throws java.io.IOException
    def _readName(self):
        if self._current != '"':
            raise self._expected("name")
        return self._readStringInternal()

# JAVA TO PYTHON CONVERTER WARNING: Method 'throws' clauses are not available in Python:
# ORIGINAL LINE: private void readNull() throws java.io.IOException
    def _readNull(self):
        self._handler.startNull()
        self._read()
        self._readRequiredChar('u')
        self._readRequiredChar('l')
        self._readRequiredChar('l')
        self._handler.endNull()

# JAVA TO PYTHON CONVERTER WARNING: Method 'throws' clauses are not available in Python:
# ORIGINAL LINE: private void readTrue() throws java.io.IOException
    def _readTrue(self):
        self._handler.startBoolean()
        self._read()
        self._readRequiredChar('r')
        self._readRequiredChar('u')
        self._readRequiredChar('e')
        self._handler.endBoolean(True)

# JAVA TO PYTHON CONVERTER WARNING: Method 'throws' clauses are not available in Python:
# ORIGINAL LINE: private void readFalse() throws java.io.IOException
    def _readFalse(self):
        self._handler.startBoolean()
        self._read()
        self._readRequiredChar('a')
        self._readRequiredChar('l')
        self._readRequiredChar('s')
        self._readRequiredChar('e')
        self._handler.endBoolean(False)

# JAVA TO PYTHON CONVERTER WARNING: Method 'throws' clauses are not available in Python:
# ORIGINAL LINE: private void readRequiredChar(char ch) throws java.io.IOException
    def _readRequiredChar(self, ch):
        if not self._readChar(ch):
            raise self._expected("'" + ch + "'")

# JAVA TO PYTHON CONVERTER WARNING: Method 'throws' clauses are not available in Python:
# ORIGINAL LINE: private void readString() throws java.io.IOException
    def _readString(self):
        self._handler.startString()
        self._handler.endString(self._readStringInternal())

# JAVA TO PYTHON CONVERTER WARNING: Method 'throws' clauses are not available in Python:
# ORIGINAL LINE: private String readStringInternal() throws java.io.IOException
    def _readStringInternal(self):
        self._read()
        self._startCapture()
        while self._current != '"':
            if self._current == '\\':
                self._pauseCapture()
                self._readEscape()
                self._startCapture()
            elif self._current < 0x20:
                raise self._expected("valid string character")
            else:
                self._read()
        string = self._endCapture()
        self._read()
        return string

# JAVA TO PYTHON CONVERTER WARNING: Method 'throws' clauses are not available in Python:
# ORIGINAL LINE: private void readEscape() throws java.io.IOException
    def _readEscape(self):
        self._read()
        if (self._current == '"') or (self._current == '/') or (self._current == '\\'):
            self._captureBuffer.append(chr(self._current))
        elif self._current == 'b':
            self._captureBuffer.append('\b')
        elif self._current == 'f':
            self._captureBuffer.append('\f')
        elif self._current == 'n':
            self._captureBuffer.append('\n')
        elif self._current == 'r':
            self._captureBuffer.append('\r')
        elif self._current == 't':
            self._captureBuffer.append('\t')
        elif self._current == 'u':
            hexChars = ['\0' for _ in range(4)]
            for i in range(0, 4):
                self._read()
                if not self._isHexDigit():
                    raise self._expected("hexadecimal digit")
                hexChars[i] = chr(self._current)
            self._captureBuffer.append(chr(Integer.parseInt(str(hexChars), 16)))
        else:
            raise self._expected("valid escape sequence")
        self._read()

# JAVA TO PYTHON CONVERTER WARNING: Method 'throws' clauses are not available in Python:
# ORIGINAL LINE: private void readNumber() throws java.io.IOException
    def _readNumber(self):
        self._handler.startNumber()
        self._startCapture()
        self._readChar('-')
        firstDigit = self._current
        if not self._readDigit():
            raise self._expected("digit")
        if firstDigit != '0':
            while self._readDigit():
                pass
        self._readFraction()
        self._readExponent()
        self._handler.endNumber(self._endCapture())

# JAVA TO PYTHON CONVERTER WARNING: Method 'throws' clauses are not available in Python:
# ORIGINAL LINE: private boolean readFraction() throws java.io.IOException
    def _readFraction(self):
        if not self._readChar('.'):
            return False
        if not self._readDigit():
            raise self._expected("digit")
        while self._readDigit():
            pass
        return True

# JAVA TO PYTHON CONVERTER WARNING: Method 'throws' clauses are not available in Python:
# ORIGINAL LINE: private boolean readExponent() throws java.io.IOException
    def _readExponent(self):
        if not self._readChar('e') and not self._readChar('E'):
            return False
        if not self._readChar('+'):
            self._readChar('-')
        if not self._readDigit():
            raise self._expected("digit")
        while self._readDigit():
            pass
        return True

# JAVA TO PYTHON CONVERTER WARNING: Method 'throws' clauses are not available in Python:
# ORIGINAL LINE: private boolean readChar(char ch) throws java.io.IOException
    def _readChar(self, ch):
        if chr(self._current) != ch:
            return False
        self._read()
        return True

# JAVA TO PYTHON CONVERTER WARNING: Method 'throws' clauses are not available in Python:
# ORIGINAL LINE: private boolean readDigit() throws java.io.IOException
    def _readDigit(self):
        if not self._isDigit():
            return False
        self._read()
        return True

# JAVA TO PYTHON CONVERTER WARNING: Method 'throws' clauses are not available in Python:
# ORIGINAL LINE: private void skipWhiteSpace() throws java.io.IOException
    def _skipWhiteSpace(self):
        while self._isWhiteSpace():
            self._read()

# JAVA TO PYTHON CONVERTER WARNING: Method 'throws' clauses are not available in Python:
# ORIGINAL LINE: private void read() throws java.io.IOException
    def _read(self):
        if self._index == self._fill:
            if self._captureStart != -1:
                self._captureBuffer.append(self._buffer, self._captureStart, self._fill - self._captureStart)
                self._captureStart = 0
            self._bufferOffset += self._fill
            self._fill = self._reader.read(self._buffer, 0, len(self._buffer))
            self._index = 0
            if self._fill == -1:
                self._current = -1
                self._index += 1
                return
        if self._current == '\n':
            self._line += 1
            self._lineOffset = self._bufferOffset + self._index
# JAVA TO PYTHON CONVERTER WARNING: An assignment within expression was extracted from the following statement:
# ORIGINAL LINE: current = buffer[index++];
        self._current = self._buffer[self._index]
        self._index += 1

    def _startCapture(self):
        if self._captureBuffer is None:
            self._captureBuffer = StringBuilder()
        self._captureStart = self._index - 1

    def _pauseCapture(self):
        end = self._index if self._current == -1 else self._index - 1
        self._captureBuffer.append(self._buffer, self._captureStart, end - self._captureStart)
        self._captureStart = -1

    def _endCapture(self):
        start = self._captureStart
        end = self._index - 1
        self._captureStart = -1
        if self._captureBuffer.length() > 0:
            self._captureBuffer.append(self._buffer, start, end - start)
            captured = str(self._captureBuffer)
            self._captureBuffer.setLength(0)
            return captured
        return str(self._buffer, start, end - start)

    def getLocation(self):
        offset = self._bufferOffset + self._index - 1
        column = offset - self._lineOffset + 1
        return Location(offset, self._line, column)

    def _expected(self, expected):
        if self._isEndOfText():
            return self._error("Unexpected end of input")
        return self._error("Expected " + expected)

    def _error(self, message):
        return ParseException(message, self.getLocation())

    def _isWhiteSpace(self):
        return self._current == ' ' or self._current == '\t' or self._current == '\n' or self._current == '\r'

    def _isDigit(self):
        return self._current >= '0' and self._current <= '9'

    def _isHexDigit(self):
        return self._current >= '0' and self._current <= '9' or self._current >= 'a' and self._current <= 'f' or self._current >= 'A' and self._current <= 'F'

    def _isEndOfText(self):
        return self._current == -1
