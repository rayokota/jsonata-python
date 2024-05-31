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

# Derived from Javascript code under this license:
#*
# * © Copyright IBM Corp. 2016, 2018 All Rights Reserved
# *   Project name: JSONata
# *   This project is licensed under the MIT License, see LICENSE
# 


class Tokenizer:

    operators = HashMapAnonymousInnerClass()

    class HashMapAnonymousInnerClass(dict):
        def __init__(self):

            self.put(".", 75)
            self.put("[", 80)
            self.put("]", 0)
            self.put("{", 70)
            self.put("}", 0)
            self.put("(", 80)
            self.put(")", 0)
            self.put(",", 0)
            self.put("@", 80)
            self.put("#", 80)
            self.put(";", 80)
            self.put(":", 80)
            self.put("?", 20)
            self.put("+", 50)
            self.put("-", 50)
            self.put("*", 60)
            self.put("/", 60)
            self.put("%", 60)
            self.put("|", 20)
            self.put("=", 40)
            self.put("<", 40)
            self.put(">", 40)
            self.put("^", 40)
            self.put("**", 60)
            self.put("..", 20)
            self.put(":=", 10)
            self.put("!=", 40)
            self.put("<=", 40)
            self.put(">=", 40)
            self.put("~>", 40)
            self.put("and", 30)
            self.put("or", 25)
            self.put("in", 40)
            self.put("&", 50)
            self.put("!", 0)
            self.put("~", 0)


    escapes = HashMapAnonymousInnerClass2()

    class HashMapAnonymousInnerClass2(dict):
        def __init__(self):

            # JSON string escape sequences - see json.org
            self.put("\"", "\"")
            self.put("\\", "\\")
            self.put("/", "/")
            self.put("b", "\b")
            self.put("f", "\f")
            self.put("n", "\n")
            self.put("r", "\r")
            self.put("t", "\t")


    # Tokenizer (lexer) - invoked by the parser to return one token at a time

    def __init__(self, path):
        # instance fields found by Java to Python Converter:
        self.path = None
        self.position = 0
        self.length = 0
        self.depth = 0

        self.path = path
        self.length = len(path)

    class Token:

        def __init__(self):
            # instance fields found by Java to Python Converter:
            self.type = None
            self.value = None
            self.position = 0
            self.id = None

        #

    def create(self, type, value):
        t = Token()
        t.type = type
        t.value = value
        t.position = self.position
        return t

    def isClosingSlash(self, position):
        if self.path[position] == '/' and self.depth == 0:
            backslashCount = 0
            while self.path[position - (backslashCount + 1)] == '\\':
                backslashCount += 1
            if int(math.fmod(backslashCount, 2)) == 0:
                return True
        return False


    def scanRegex(self):
        # the prefix '/' will have been previously scanned. Find the end of the regex.
        # search for closing '/' ignoring any that are escaped, or within brackets
        start = self.position
        #int depth = 0
        pattern = None
        flags = None

        while self.position < self.length:
            currentChar = self.path[self.position]
            if self.isClosingSlash(self.position):
                # end of regex found
                pattern = self.path[start:self.position]
                if pattern == "":
                    raise JException("S0301", self.position)
                self.position += 1
                currentChar = self.path[self.position]
                # flags
                start = self.position
                while currentChar == 'i' or currentChar == 'm':
                    self.position += 1
                    currentChar = self.path[self.position]
                flags = self.path[start:self.position] + 'g'

                # Convert flags to Java Pattern flags
                _flags = 0
                if "i" in flags:
                    _flags |= java.util.regex.Pattern.CASE_INSENSITIVE
                if "m" in flags:
                    _flags |= java.util.regex.Pattern.MULTILINE
                return java.util.regex.Pattern.compile(pattern, _flags) # Pattern.CASE_INSENSITIVE | Pattern.MULTILINE | Pattern.DOTALL);
            if (currentChar == '(' or currentChar == '[' or currentChar == '{') and self.path[self.position - 1] != '\\':
                self.depth += 1
            if (currentChar == ')' or currentChar == ']' or currentChar == '}') and self.path[self.position - 1] != '\\':
                self.depth -= 1
            self.position += 1
        raise JException("S0302", self.position)

    def next(self, prefix):
        if self.position >= self.length:
            return None
        currentChar = self.path[self.position]
        # skip whitespace
        while self.position < self.length and " \t\n\r".find(currentChar) > -1:
            self.position += 1
            if self.position >= self.length:
                return None # Uli: JS relies on charAt returns null
            currentChar = self.path[self.position]
        # skip comments
        if currentChar == '/' and self.path[self.position + 1] == '*':
            commentStart = self.position
            self.position += 2
            currentChar = self.path[self.position]
            while not(currentChar == '*' and self.path[self.position + 1] == '/'):
                position += 1
# JAVA TO PYTHON CONVERTER WARNING: An assignment within expression was extracted from the following statement:
# ORIGINAL LINE: currentChar = path.charAt(++position);
                currentChar = self.path[self.position]
                if self.position >= self.length:
                    # no closing tag
                    raise JException("S0106", commentStart)
            self.position += 2
            currentChar = self.path[self.position]
            return self.next(prefix) # need this to swallow any following whitespace
        # test for regex
        if prefix != True and currentChar == '/':
            self.position += 1
            return self.create("regex", self.scanRegex())
        # handle double-char operators
        haveMore = self.position < len(self.path) - 1 # Java: position+1 is valid
        if currentChar == '.' and haveMore and self.path[self.position + 1] == '.':
            # double-dot .. range operator
            self.position += 2
            return self.create("operator", "..")
        if currentChar == ':' and haveMore and self.path[self.position + 1] == '=':
            # := assignment
            self.position += 2
            return self.create("operator", ":=")
        if currentChar == '!' and haveMore and self.path[self.position + 1] == '=':
            # !=
            self.position += 2
            return self.create("operator", "!=")
        if currentChar == '>' and haveMore and self.path[self.position + 1] == '=':
            # >=
            self.position += 2
            return self.create("operator", ">=")
        if currentChar == '<' and haveMore and self.path[self.position + 1] == '=':
            # <=
            self.position += 2
            return self.create("operator", "<=")
        if currentChar == '*' and haveMore and self.path[self.position + 1] == '*':
            # **  descendant wildcard
            self.position += 2
            return self.create("operator", "**")
        if currentChar == '~' and haveMore and self.path[self.position + 1] == '>':
            # ~>  chain function
            self.position += 2
            return self.create("operator", "~>")
        # test for single char operators
        if com.dashjoin.jsonata.Tokenizer.operators["" + currentChar] is not None:
            self.position += 1
            return self.create("operator", currentChar)
        # test for string literals
        if currentChar == '"' or currentChar == '\'':
            quoteType = currentChar
            # double quoted string literal - find end of string
            self.position += 1
            qstr = ""
            while self.position < self.length:
                currentChar = self.path[self.position]
                if currentChar == '\\':
                    self.position += 1
                    currentChar = self.path[self.position]
                    if com.dashjoin.jsonata.Tokenizer.escapes["" + currentChar] is not None:
                        qstr += com.dashjoin.jsonata.Tokenizer.escapes["" + currentChar]
                    elif currentChar == 'u':
                        #  u should be followed by 4 hex digits
                        octets = self.path[self.position + 1:(self.position + 1) + 4]
                        if octets.matches("^[0-9a-fA-F]+$"):
                            codepoint = Integer.parseInt(octets, 16)
                            qstr += chr(codepoint)
                            self.position += 4
                        else:
                            raise JException("S0104", self.position)
                    else:
                        # illegal escape sequence
                        raise JException("S0301", self.position, currentChar)

                elif currentChar == quoteType:
                    self.position += 1
                    return self.create("string", qstr)
                else:
                    qstr += currentChar
                self.position += 1
            raise JException("S0101", self.position)
        # test for numbers
        numregex = java.util.regex.Pattern.compile("^-?(0|([1-9][0-9]*))(\\.[0-9]+)?([Ee][-+]?[0-9]+)?")
        match_ = numregex.matcher(self.path[self.position:])
        if match_.find():
            num = float(match_.group(0))
            if not Double.isNaN(num) and Double.isFinite(num):
                self.position += match_.group(0).length()
                # If the number is integral, use long as type
                return self.create("number", Utils.convertNumber(num))
            else:
                raise JException("S0102", self.position) #, match.group[0]);

        # test for quoted names (backticks)
        name = None
        if currentChar == '`':
            # scan for closing quote
            self.position += 1
            end = self.path.find('`', self.position)
            if end != -1:
                name = self.path[self.position:end]
                self.position = end + 1
                return self.create("name", name)
            self.position = self.length
            raise JException("S0105", self.position)
        # test for names
        i = self.position
        ch = '\0'
        while True:
            #if (i>=length) return null; // Uli: JS relies on charAt returns null

            ch = self.path[i] if i < self.length else chr(0)
            if i == self.length or " \t\n\r".find(ch) > -1 or "" + ch in com.dashjoin.jsonata.Tokenizer.operators.keys():
                if self.path[self.position] == '$':
                    # variable reference
                    _name = self.path[self.position + 1:i]
                    self.position = i
                    return self.create("variable", _name)
                else:
                    _name = self.path[self.position:i]
                    self.position = i
                    match _name:
                        case _name == "or" | _name == "in" | "and":
                            return self.create("operator", _name)
                        case "true":
                            return self.create("value", True)
                        case "false":
                            return self.create("value", False)
                        case "null":
                            return self.create("value", None)
                        case other:
                            if self.position == self.length and _name == "":
                                # whitespace at end of input
                                return None
                            return self.create("name", _name)
            else:
                i += 1
