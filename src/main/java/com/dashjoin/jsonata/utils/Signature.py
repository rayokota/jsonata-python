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

# Derived from original JSONata4Java Signature code under this license:
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



from com.dashjoin.jsonata import Functions
from com.dashjoin.jsonata import JException
from com.dashjoin.jsonata import Utils

#*
# * Manages signature related functions
# 
class Signature:

    SERIAL_VERSION_UID = -450755246855587271

    class Param:

        def __init__(self):
            # instance fields found by Java to Python Converter:
            self.type = None
            self.regex = None
            self.context = False
            self.array = False
            self.subtype = None
            self.contextRegex = None


        def toString(self):
            return "Param " + self.type + " regex=" + self.regex + " ctx=" + self.context + " array=" + self.array



    def __init__(self, signature, function):
        # instance fields found by Java to Python Converter:
        self._param = Param()
        self._params = []
        self._prevParam = self._param
        self._regex = None
        self._signature = ""
        self.functionName = None

        self.functionName = function
        self.parseSignature(signature)

    def setFunctionName(self, functionName):
        self.functionName = functionName

    @staticmethod
    def main(args):
        s = Signature("<s-:s>", "test") #<s-(sf)(sf)n?:s>");
        print(s._params)

    def findClosingBracket(self, str, start, openSymbol, closeSymbol):
        # returns the position of the closing symbol (e.g. bracket) in a string
        # that balances the opening symbol at position start
        depth = 1
        position = start
        while position < len(str):
            position += 1
            symbol = str[position]
            if symbol == closeSymbol:
                depth -= 1
                if depth == 0:
                    # we're done
                    break # out of while loop
            elif symbol == openSymbol:
                depth += 1
        return position

    def getSymbol(self, value):
        symbol = None
        if value is None:
            symbol = "m"
        else:
            # first check to see if this is a function
            if com.dashjoin.jsonata.Utils.isFunction(value) or com.dashjoin.jsonata.Functions.isLambda(value) or (isinstance(value, java.util.regex.Pattern)):
                symbol = "f"
            elif isinstance(value, String):
                symbol = "s"
            elif isinstance(value, Number):
                symbol = "n"
            elif isinstance(value, Boolean):
                symbol = "b"
            elif isinstance(value, java.util.List):
                symbol = "a"
            elif isinstance(value, java.util.Map):
                symbol = "o"
            elif isinstance(value, javax.lang.model.type.NullType): # Uli: is this used???
                symbol = "l"
            else:
                # any value can be undefined, but should be allowed to match
                symbol = "m" # m for missing
        return symbol

    def next(self):
        self._params.append(self._param)
        self._prevParam = self._param
        self._param = Param()

    #    *
    #     * Parses a function signature definition and returns a validation function
    #     * 
    #     * @param {string}
    #     *                 signature - the signature between the <angle brackets>
    #     * @returns validation pattern
    #     
    def parseSignature(self, signature):
        # create a Regex that represents this signature and return a function that when
        # invoked,
        # returns the validated (possibly fixed-up) arguments, or throws a validation
        # error
        # step through the signature, one symbol at a time
        position = 1
        while position < len(signature):
            symbol = signature[position]
            if symbol == ':':
                # TODO figure out what to do with the return type
                # ignore it for now
                break

            if (symbol == 's') or (symbol == 'n') or (symbol == 'b') or (symbol == 'l') or (symbol == 'o'):
                    self._param.regex = ("[" + symbol + "m]")
                    self._param.type = ("" + symbol)
                    self.next()
            elif symbol == 'a':
                    # normally treat any value as singleton array
                    self._param.regex = ("[asnblfom]")
                    self._param.type = ("" + symbol)
                    self._param.array = (True)
                    self.next()
            elif symbol == 'f':
                    self._param.regex = ("f")
                    self._param.type = ("" + symbol)
                    self.next()
            elif symbol == 'j':
                    self._param.regex = ("[asnblom]")
                    self._param.type = ("" + symbol)
                    self.next()
            elif symbol == 'x':
                    self._param.regex = ("[asnblfom]")
                    self._param.type = ("" + symbol)
                    self.next()
            elif symbol == '-':
                    self._prevParam.context = True
                    self._prevParam.regex += "?"
            elif (symbol == '?') or (symbol == '+'):
                    self._prevParam.regex += symbol
            elif symbol == '(':
                    # search forward for matching ')'
                    endParen = self.findClosingBracket(signature, position, '(', ')')
                    choice = signature[position + 1:endParen]
                    if choice.find("<") == -1:
                        # no _parameterized types, simple regex
                        self._param.regex = ("[" + choice + "m]")
                    else:
                        # TODO harder
                        raise RuntimeException("Choice groups containing parameterized types are not supported")
                    self._param.type = ("(" + choice + ")")
                    position = endParen
                    self.next()
            elif symbol == '<':
                    test = self._prevParam.type
                    if test is not None:
                        type = test #.asText();
                        if type == "a" or type == "f":
                            # search forward for matching '>'
                            endPos = self.findClosingBracket(signature, position, '<', '>')
                            self._prevParam.subtype = signature[position + 1:endPos]
                            position = endPos
                        else:
                            raise RuntimeException("Type parameters can only be applied to functions and arrays")
                    else:
                        raise RuntimeException("Type parameters can only be applied to functions and arrays")
            position += 1 # end while processing symbols in signature

        regexStr = "^"
        for param in self._params:
            regexStr += "(" + param.regex + ")"
        regexStr += "$"

        self._regex = None
        try:
            self._regex = java.util.regex.Pattern.compile(regexStr)
            self._signature = regexStr
        except java.util.regex.PatternSyntaxException as pse:
            raise RuntimeException(pse.getLocalizedMessage())
        return self._regex

    def throwValidationError(self, badArgs, badSig, functionName):
        # to figure out where this went wrong we need apply each component of the
        # regex to each argument until we get to the one that fails to match
        partialPattern = "^"

        goodTo = 0
        for index, _ in enumerate(self._params):
            partialPattern += self._params[index].regex
            tester = java.util.regex.Pattern.compile(partialPattern)
            match_ = tester.matcher(badSig)
            if match_.matches() == False:
                # failed here
                raise com.dashjoin.jsonata.JException("T0410", -1, (goodTo + 1), functionName)
            goodTo = match_.end()
        # if it got this far, it's probably because of extraneous arguments (we
        # haven't added the trailing '$' in the regex yet.
        raise com.dashjoin.jsonata.JException("T0410", -1, (goodTo + 1), functionName)

# JAVA TO PYTHON CONVERTER TASK: Java annotations have no direct Python equivalent:
# ORIGINAL LINE: @SuppressWarnings({"rawtypes", "unchecked"}) public Object validate(Object _args, Object context)
    def validate(self, _args, context):

        result = []

        args = _args
        suppliedSig = ""
        for arg in args:
            suppliedSig += self.getSymbol(arg)

        isValid = self._regex.matcher(suppliedSig)
        if isValid is not None and isValid.matches():
            validatedArgs = []
            argIndex = 0
            index = 0
            for _param in self._params:
                param = _param
                arg = args[argIndex] if argIndex < len(args) else None
                match_ = isValid.group(index + 1)
                if "" == match_:
                    if param.context and param.regex is not None:
                        # substitute context value for missing arg
                        # first check that the context value is the right type
                        contextType = self.getSymbol(context)
                        # test contextType against the regex for this arg (without the trailing ?)
                        if java.util.regex.Pattern.matches(param.regex, contextType):
                            #if (param.contextRegex.test(contextType)) {
                            validatedArgs.append(context)
                        else:
                            # context value not compatible with this argument
                            raise com.dashjoin.jsonata.JException("T0411",-1, context, argIndex + 1)
                    else:
                        validatedArgs.append(arg)
                        argIndex += 1
                else:
                    # may have matched multiple args (if the regex ends with a '+'
                    # split into single tokens
                    singles = match_.split("")
                    for single in singles:
                        #match.split('').forEach(function (single) {
                        if param.type == "a":
                            if single == "m":
                                # missing (undefined)
                                arg = None
                            else:
                                arg = args[argIndex] if argIndex < len(args) else None
                                arrayOK = True
                                # is there type information on the contents of the array?
                                if param.subtype is not None:
                                    if single != "a" and match_ != param.subtype:
                                        arrayOK = False
                                    elif single == "a":
                                        argArr = arg
                                        if len(argArr) > 0:
                                            itemType = self.getSymbol(argArr[0])
                                            if itemType != "" + param.subtype[0]:
                                                arrayOK = False
                                            else:
                                                # make sure every item in the array is this type
                                                for o in argArr:
                                                    if self.getSymbol(o) != itemType:
                                                        arrayOK = False
                                                        break
                                if not arrayOK:
                                    raise com.dashjoin.jsonata.JException("T0412", -1, arg, param.subtype)
                                # the function expects an array. If it's not one, make it so
                                if single != "a":
                                    _arg = []
                                    _arg.append(arg)
                                    arg = _arg
                            validatedArgs.append(arg)
                            argIndex += 1
                        else:
                            validatedArgs.append(arg)
                            argIndex += 1
            return validatedArgs
        self.throwValidationError(args, suppliedSig, self.functionName)
        return None # dead code -> compiler happy

    def getNumberOfArgs(self):
        return len(self._params)

    #    *
    #     * Returns the minimum # of arguments.
    #     * I.e. the # of all non-optional arguments.
    #     
    def getMinNumberOfArgs(self):
        res = 0
        for p in self._params:
            if (not "?") in p.regex:
                res += 1
        return res
    #
    #    ArrayNode validate(String functionName, ExprListContext args, ExpressionsVisitor expressionVisitor) {
    #        ArrayNode result = JsonNodeFactory.instance.arrayNode()
    #        String suppliedSig = ""
    #        for (Iterator<ExprContext> it = args.expr().iterator(); it.hasNext();) {
    #            ExprContext arg = it.next()
    #            suppliedSig += getSymbol(arg)
    #        }
    #        Matcher isValid = _regex.matcher(suppliedSig)
    #        if (isValid != null) {
    #            ArrayNode validatedArgs = JsonNodeFactory.instance.arrayNode()
    #            int argIndex = 0
    #            int index = 0
    #            for (Iterator<JsonNode> it = _params.iterator(); it.hasNext();) {
    #                ObjectNode param = (ObjectNode) it.next()
    #                JsonNode arg = expressionVisitor.visit(args.expr(argIndex))
    #                String match = isValid.group(index + 1)
    #                if ("".equals(match)) {
    #                    boolean useContext = (param.get("context") != null && param.get("context").asBoolean())
    #                    if (useContext) {
    #                        // substitute context value for missing arg
    #                        // first check that the context value is the right type
    #                        JsonNode context = expressionVisitor.getVariable("$")
    #                        String contextType = getSymbol(context)
    #                        // test contextType against the regex for this arg (without the trailing ?)
    #                        if (Pattern.matches(param.get("regex").asText(), contextType)) {
    #                            validatedArgs.add(context)
    #                        } else {
    #                            // context value not compatible with this argument
    #                            throw new EvaluateRuntimeException("Context value is not a compatible type with argument \""
    #                                + argIndex + 1 + "\" of function \"" + functionName + "\"")
    #                        }
    #                    } else {
    #                        validatedArgs.add(arg)
    #                        argIndex++
    #                    }
    #                } else {
    #                    // may have matched multiple args (if the regex ends with a '+'
    #                    // split into single tokens
    #                    String[] singles = match.split("")
    #                    for (String single : singles) {
    #                        if ("a".equals(param.get("type").asText())) {
    #                            if ("m".equals(single)) {
    #                                // missing (undefined)
    #                                arg = null
    #                            } else {
    #                                arg = expressionVisitor.visit(args.expr(argIndex))
    #                                boolean arrayOK = true
    #                                // is there type information on the contents of the array?
    #                                String subtype = "undefined"
    #                                JsonNode testSubType = param.get("subtype")
    #                                if (testSubType != null) {
    #                                    subtype = testSubType.asText()
    #                                    if ("a".equals(single) == false && match.equals(subtype) == false) {
    #                                        arrayOK = false
    #                                    } else if ("a".equals(single)) {
    #                                        ArrayNode argArray = (ArrayNode) arg
    #                                        if (argArray.size() > 0) {
    #                                            String itemType = getSymbol(argArray.get(0))
    #                                            if (itemType.equals(subtype) == false) { // TODO recurse further
    #                                                arrayOK = false
    #                                            } else {
    #                                                // make sure every item in the array is this type
    #                                                ArrayNode differentItems = JsonNodeFactory.instance.arrayNode()
    #                                                for (Object val : argArray) {
    #                                                    if (itemType.equals(getSymbol(val)) == false) {
    #                                                        differentItems.add(expressionVisitor.visit((ExprListContext) val))
    #                                                    }
    #                                                }
    #                                                
    #                                                arrayOK = (differentItems.size() == 0)
    #                                            }
    #                                        }
    #                                    }
    #                                }
    #                                if (!arrayOK) {
    #                                    JsonNode type = s_arraySignatureMapping.get(subtype)
    #                                    if (type == null) {
    #                                        type = JsonNodeFactory.instance.nullNode()
    #                                    }
    #                                    throw new EvaluateRuntimeException("Argument \"" + (argIndex + 1) + "\" of function \""
    #                                        + functionName + "\" must be an array of \"" + type.asText() + "\"")
    #                                }
    #                                // the function expects an array. If it's not one, make it so
    #                                if ("a".equals(single) == false) {
    #                                    ArrayNode wrappedArg = JsonNodeFactory.instance.arrayNode()
    #                                    wrappedArg.add(arg)
    #                                    arg = wrappedArg
    #                                }
    #                            }
    #                            validatedArgs.add(arg)
    #                            argIndex++
    #                        } else {
    #                            validatedArgs.add(arg)
    #                            argIndex++
    #                        }
    #                    }
    #                }
    #                index++
    #            }
    #            return validatedArgs
    #        }
    #        throwValidationError(args, suppliedSig, functionName)
    #        // below just for the compiler as a runtime exception is thrown above
    #        return result
    #    }
    #
