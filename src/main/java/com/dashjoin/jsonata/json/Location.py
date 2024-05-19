#******************************************************************************
# * Copyright (c) 2016 EclipseSource.
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
# * An immutable object that represents a location in the parsed text.
# 
class Location:

    #  *
    #   * The absolute character index, starting at 0.
    #   

    #  *
    #   * The line number, starting at 1.
    #   

    #  *
    #   * The column number, starting at 1.
    #   

    def __init__(self, offset, line, column):
        # instance fields found by Java to Python Converter:
        self.offset = 0
        self.line = 0
        self.column = 0

        self.offset = offset
        self.column = column
        self.line = line

    def toString(self):
        return str(self.line) + ":" + str(self.column)

    def hashCode(self):
        return self.offset

    def equals(self, obj):
        if self is obj:
            return True
        if obj is None:
            return False
        if getClass() != type(obj):
            return False
        other = obj
        return self.offset == other.offset and self.column == other.column and self.line == other.line
