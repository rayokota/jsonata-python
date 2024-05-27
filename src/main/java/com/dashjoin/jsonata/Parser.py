import copy

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


from com.dashjoin.jsonata import Jsonata.Frame
from com.dashjoin.jsonata import Tokenizer.Token
from com.dashjoin.jsonata.utils import Signature

#var parseSignature = require('./signature')
# JAVA TO PYTHON CONVERTER TASK: Java annotations have no direct Python equivalent:
# ORIGINAL LINE: @SuppressWarnings({"unchecked"}) public class Parser
class Parser:


    # This parser implements the 'Top down operator precedence' algorithm developed by Vaughan R Pratt; http://dl.acm.org/citation.cfm?id=512931.
    # and builds on the Javascript framework described by Douglas Crockford at http://javascript.crockford.com/tdop/tdop.html
    # and in 'Beautiful Code', edited by Andy Oram and Greg Wilson, Copyright 2007 O'Reilly Media, Inc. 798-0-596-51004-6


    #var parser = function (source, recover) {


    def remainingTokens(self):
        remaining = []
        if self.node.id != "(end)":
            t = com.dashjoin.jsonata.Tokenizer.Token()
            t.type = self.node.type
            t.value = self.node.value
            t.position = self.node.position
            remaining.append(t)
        nxt = self.lexer.next(False)
        while nxt is not None:
            remaining.append(nxt)
            nxt = self.lexer.next(False)
        return remaining


    @staticmethod
    def clone(object):
        try:
            bOut = java.io.ByteArrayOutputStream()
            out = java.io.ObjectOutputStream(bOut)
            out.writeObject(object)
            out.close()

            in_ = java.io.ObjectInputStream(java.io.ByteArrayInputStream(bOut.toByteArray()))
            copy = in_.readObject()
            in_.close()

            return copy
        except Exception as e:
            raise RuntimeException(e)

    class Symbol(Cloneable):

        def _initialize_instance_fields(self):
            # instance fields found by Java to Python Converter:
            self.id = None
            self.type = None
            self.value = None
            self.bp = 0
            self.lbp = 0
            self.position = 0
            self.keepArray = False
            self.descending = False
            self.expression = None
            self.seekingParent = None
            self.errors = None
            self.steps = None
            self.slot = None
            self.nextFunction = None
            self.keepSingletonArray = False
            self.consarray = False
            self.level = 0
            self.focus = None
            self.token = None
            self.thunk = False
            self.procedure = None
            self.arguments = None
            self.body = None
            self.predicate = None
            self.stages = None
            self.input = None
            self.environment = None
            self.tuple = None
            self.expr = None
            self.group = None
            self.name = None
            self.lhs = None
            self.rhs = None
            self.lhsObject = None
            self.rhsObject = None
            self.rhsTerms = None
            self.terms = None
            self.condition = None
            self.then = None
            self._else = None
            self.expressions = None
            self.error = None
            self.signature = None
            self.pattern = None
            self.update = None
            self.delete = None
            self.label = None
            self.index = None
            self._jsonata_lambda = False
            self.ancestor = None



        #Symbol s





        # Procedure:

        # Infix attributes
        # where rhs = list of Symbol pairs
        # where rhs = list of Symbols

        # Ternary operator:


        # processAST error handling

        # Prefix attributes

        # Ancestor attributes


        def nud(self):
            # error - symbol has been invoked as a unary operator
# JAVA TO PYTHON CONVERTER WARNING: The original Java variable was marked 'final':
# ORIGINAL LINE: final JException _err = new JException("S0211", position, value);
            _err = JException("S0211", self.position, self.value)

            if outerInstance.recover:
                #                
                #                err.remaining = remainingTokens()
                #                err.type = "error"
                #                errors.add(err)
                #                return err
                #                
# JAVA TO PYTHON CONVERTER TASK: The following line could not be converted:
                return new Symbol("(error)")
                    #JException err = _err
            else:
                raise _err

        def led(self, left):
            raise Error("led not implemented")

        #class Symbol {
# JAVA TO PYTHON CONVERTER TASK: There is no Python equivalent to multiple constructors:
# ORIGINAL LINE: Symbol()
        def __init__(self, outerInstance):
            self._initialize_instance_fields()

            self._outerInstance = outerInstance

# JAVA TO PYTHON CONVERTER TASK: There is no Python equivalent to multiple constructors:
# ORIGINAL LINE: Symbol(String id)
        def __init__(self, outerInstance, id):
            self(outerInstance, id, 0)
            self._outerInstance = outerInstance

# JAVA TO PYTHON CONVERTER TASK: There is no Python equivalent to multiple constructors:
# ORIGINAL LINE: Symbol(String id, int bp)
        def __init__(self, outerInstance, id, bp):
            self._initialize_instance_fields()

            self._outerInstance = outerInstance

            self.id = id
            self.value = id
            self.bp = bp
            # use register(Symbol) ! Otherwise inheritance doesn't work
            #            Symbol s = symbolTable.get(id)
            #            //bp = bp != 0 ? bp : 0
            #            if (s != null) {
            #                if (bp >= s.lbp) {
            #                    s.lbp = bp
            #                }
            #            } else {
            #                s = new Symbol()
            #                s.value = s.id = id
            #                s.lbp = bp
            #                symbolTable.put(id, s)
            #            }
            #
            #
            #return s

        def create(self):
            # We want a shallow clone (do not duplicate outer class!)
            try:
                cl = copy.copy(self)
                #System.err.println("cloning "+this+" clone="+cl)
                return cl
            except CloneNotSupportedException as e:
                # never reached
                if outerInstance.dbg:
                    e.printStackTrace()
                return None

        def toString(self):
            return type(self).getSimpleName() + " " + self.id + " value=" + self.value

    def register(self, t):

        #if (t instanceof Infix || t instanceof InfixR) return

        s = self.symbolTable[t.id]
        if s is not None:
            if self.dbg:
                print("Symbol in table " + t.id + " " + type(s).getName() + " -> " + type(t).getName())
            #symbolTable.put(t.id, t)
            if t.bp >= s.lbp:
                if self.dbg:
                    print("Symbol in table " + t.id + " lbp=" + str(s.lbp) + " -> " + str(t.bp))
                s.lbp = t.bp
        else:
            s = t.create()
            s.value = s.id = t.id
            s.lbp = t.bp
            self.symbolTable[t.id] = s

    def handleError(self, err):
        if self.recover:
            err.remaining = self.remainingTokens()
            self.errors.append(err)
            #Symbol symbol = symbolTable.get("(error)")
            node = Symbol(self)
            # FIXME node.error = err
            #node.type = "(error)"
            return node
        else:
            raise err
    #}

# JAVA TO PYTHON CONVERTER TASK: Python does not allow method overloads:
    def advance(self):
        return self.advance(None)
# JAVA TO PYTHON CONVERTER TASK: Python does not allow method overloads:
    def advance(self, id):
        return self.advance(id, False)
# JAVA TO PYTHON CONVERTER TASK: Python does not allow method overloads:
    def advance(self, id, infix):
        if id is not None and self.node.id != id:
            code = None
            if self.node.id == "(end)":
                # unexpected end of buffer
                code = "S0203"
            else:
                code = "S0202"
            err = JException(code, self.node.position, id, self.node.value)
            return self.handleError(err)
        next_token = self.lexer.next(infix)
        if self.dbg:
            print("nextToken " + (next_token.type if next_token is not None else None))
        if next_token is None:
            self.node = self.symbolTable["(end)"]
            self.node.position = len(self.source)
            return self.node
        value = next_token.value
        type = next_token.type
        symbol = None
        match type:
            case type == "name" | "variable":
                symbol = self.symbolTable["(name)"]
            case "operator":
                symbol = self.symbolTable["" + value]
                if symbol is None:
                    return self.handleError(JException("S0204", next_token.position, value))
            case type == "string" | type == "number" | "value":
                symbol = self.symbolTable["(literal)"]
            case "regex":
                type = "regex"
                symbol = self.symbolTable["(regex)"]
                # istanbul ignore next 
            case other:
                return self.handleError(JException("S0205", next_token.position, value))

        self.node = symbol.create()
        #Token node = new Token(); //Object.create(symbol)
        self.node.value = value
        self.node.type = type
        self.node.position = next_token.position
        if self.dbg:
            print("advance " + self.node)
        return self.node

    # Pratt's algorithm
    def expression(self, rbp):
        left = None
        t = self.node
        self.advance(None, True)
        left = t.nud()
        while rbp < self.node.lbp:
            t = self.node
            self.advance(None, False)
            if self.dbg:
                print("t=" + t + ", left=" + left.type)
            left = t.led(left)
        return left

    class Terminal(Symbol):

        def __init__(self, outerInstance, id):
            super().__init__(outerInstance, id, 0)
            self._outerInstance = outerInstance
        def nud(self):
            return self

    #        
    #            var terminal = function (id) {
    #            var s = symbol(id, 0)
    #            s.nud = function () {
    #                return this
    #            }
    #        }
    #        

    # match infix operators
    # <expression> <operator> <expression>
    # left associative
    class Infix(Symbol):


# JAVA TO PYTHON CONVERTER TASK: There is no Python equivalent to multiple constructors:
# ORIGINAL LINE: Infix(String id)
        def __init__(self, outerInstance, id):
            self(outerInstance, id,0)
            self._outerInstance = outerInstance
# JAVA TO PYTHON CONVERTER TASK: There is no Python equivalent to multiple constructors:
# ORIGINAL LINE: Infix(String id, int bp)
        def __init__(self, outerInstance, id, bp):
            super().__init__(outerInstance, id,bp if bp != 0 else (Tokenizer.operators[id] if id is not None else 0))
            self._outerInstance = outerInstance

        def led(self, left):
            self.lhs = left
            self.rhs = outerInstance.expression(self.bp)
            self.type = "binary"
            return self


    class InfixAndPrefix(Infix):

        def _initialize_instance_fields(self):
            # instance fields found by Java to Python Converter:
            self.prefix = None




# JAVA TO PYTHON CONVERTER TASK: There is no Python equivalent to multiple constructors:
# ORIGINAL LINE: InfixAndPrefix(String id)
        def __init__(self, outerInstance, id):
            self(outerInstance, id,0)
            self._outerInstance = outerInstance

# JAVA TO PYTHON CONVERTER TASK: There is no Python equivalent to multiple constructors:
# ORIGINAL LINE: InfixAndPrefix(String id, int bp)
        def __init__(self, outerInstance, id, bp):
            self._initialize_instance_fields()

            super().__init__(outerInstance, id, bp)
            self._outerInstance = outerInstance

            self.prefix = Prefix(outerInstance, id)

        def nud(self):
            return self.prefix.nud()
            # expression(70)
            # type="unary"
            # return this

# JAVA TO PYTHON CONVERTER WARNING: Method 'throws' clauses are not available in Python:
# ORIGINAL LINE: @Override public Object clone() throws CloneNotSupportedException
        def clone(self):
            c = super().clone()
            # IMPORTANT: make sure to allocate a new Prefix!!!
            (c).prefix = Prefix(self._outerInstance, (c).id)
            return c

    # match infix operators
    # <expression> <operator> <expression>
    # right associative
    class InfixR(Symbol):


        def __init__(self, outerInstance, id, bp):
            super().__init__(outerInstance, id, bp)
            self._outerInstance = outerInstance

        #abstract Object led()

    # match prefix operators
    # <operator> <expression>
    class Prefix(Symbol):

        #public List<Symbol[]> lhs

        def __init__(self, outerInstance, id):
            super().__init__(outerInstance, id)
            self._outerInstance = outerInstance
            #type = "unary"

        #Symbol _expression

        def nud(self):
            self.expression = outerInstance.expression(70)
            self.type = "unary"
            return self

    def __init__(self):
        # instance fields found by Java to Python Converter:
        self.dbg = False
        self.source = None
        self.recover = False
        self.node = None
        self.lexer = None
        self.symbolTable = {}
        self.errors = []
        self.ancestorLabel = 0
        self.ancestorIndex = 0
        self.ancestry = []


        self.register(Terminal(self, "(end)"))
        self.register(Terminal(self, "(name)"))
        self.register(Terminal(self, "(literal)"))
        self.register(Terminal(self, "(regex)"))
        self.register(Symbol(self, ":"))
        self.register(Symbol(self, ";"))
        self.register(Symbol(self, ","))
        self.register(Symbol(self, ")"))
        self.register(Symbol(self, "]"))
        self.register(Symbol(self, "}"))
        self.register(Symbol(self, "..")) # range operator
        self.register(Infix(self, ".")) # map operator
        self.register(Infix(self, "+")) # numeric addition
        self.register(InfixAndPrefix(self, "-")) # numeric subtraction
        # unary numeric negation

        self.register(InfixAnonymousInnerClass(self))
        # numeric multiplication
        self.register(Infix(self, "/")) # numeric division
        self.register(InfixAnonymousInnerClass2(self))
        # numeric modulus
        self.register(Infix(self, "=")) # equality
        self.register(Infix(self, "<")) # less than
        self.register(Infix(self, ">")) # greater than
        self.register(Infix(self, "!=")) # not equal to
        self.register(Infix(self, "<=")) # less than or equal
        self.register(Infix(self, ">=")) # greater than or equal
        self.register(Infix(self, "&")) # string concatenation

        self.register(InfixAnonymousInnerClass3(self))
        # Boolean AND
        self.register(InfixAnonymousInnerClass4(self))
        # Boolean OR
        self.register(InfixAnonymousInnerClass5(self))
        # is member of array
        # merged Infix: register(new Terminal("and")); // the 'keywords' can also be used as terminals (field names)
        # merged Infix: register(new Terminal("or")); //
        # merged Infix: register(new Terminal("in")); //
        # merged Infix: register(new Prefix("-")); // unary numeric negation
        self.register(Infix(self, "~>")) # function application

        self.register(InfixRAnonymousInnerClass(self))

        # field wildcard (single level)
        # merged with Infix *
        # register(new Prefix("*") {
        #     @Override Symbol nud() {
        #         type = "wildcard"
        #         return this
        #     }
        # })

        # descendant wildcard (multi-level)

        self.register(PrefixAnonymousInnerClass(self))

        # parent operator
        # merged with Infix %
        # register(new Prefix("%") {
        #     @Override Symbol nud() {
        #         type = "parent"
        #         return this
        #     }
        # })

        # function invocation
        self.register(InfixAnonymousInnerClass6(self, Tokenizer.operators["("]))

        # array constructor

        # merged: register(new Prefix("[") {        
        self.register(InfixAnonymousInnerClass7(self, Tokenizer.operators["["]))

        # order-by
        self.register(InfixAnonymousInnerClass8(self, Tokenizer.operators["^"]))

        self.register(InfixAnonymousInnerClass9(self, Tokenizer.operators["{"]))

        # bind variable
        self.register(InfixRAnonymousInnerClass2(self, Tokenizer.operators[":="]))

        # focus variable bind
        self.register(InfixAnonymousInnerClass10(self, Tokenizer.operators["@"]))

        # index (position) variable bind
        self.register(InfixAnonymousInnerClass11(self, Tokenizer.operators["#"]))

        # if/then/else ternary operator ?:
        self.register(InfixAnonymousInnerClass12(self, Tokenizer.operators["?"]))

        # object transformer
        self.register(PrefixAnonymousInnerClass2(self))

    class InfixAnonymousInnerClass(Infix):

        def __init__(self, outerInstance):
            super().__init__(outerInstance, "*")
            self._outerInstance = outerInstance

        # field wildcard (single level)
        def nud(self):
            outerInstance.type = "wildcard"
            return self

    class InfixAnonymousInnerClass2(Infix):

        def __init__(self, outerInstance):
            super().__init__(outerInstance, "%")
            self._outerInstance = outerInstance

        # parent operator
        def nud(self):
            outerInstance.type = "parent"
            return self

    class InfixAnonymousInnerClass3(Infix):

        def __init__(self, outerInstance):
            super().__init__(outerInstance, "and")
            self._outerInstance = outerInstance

        # allow as terminal
        def nud(self):
            return self

    class InfixAnonymousInnerClass4(Infix):

        def __init__(self, outerInstance):
            super().__init__(outerInstance, "or")
            self._outerInstance = outerInstance

        # allow as terminal
        def nud(self):
            return self

    class InfixAnonymousInnerClass5(Infix):

        def __init__(self, outerInstance):
            super().__init__(outerInstance, "in")
            self._outerInstance = outerInstance

        # allow as terminal
        def nud(self):
            return self

    class InfixRAnonymousInnerClass(InfixR):

        def __init__(self, outerInstance):
            super().__init__(outerInstance, "(error)", 10)
            self._outerInstance = outerInstance

        def led(self, left):
            raise UnsupportedOperationException("TODO", None)

    class PrefixAnonymousInnerClass(Prefix):

        def __init__(self, outerInstance):
            super().__init__(outerInstance, "**")
            self._outerInstance = outerInstance

        def nud(self):
            outerInstance.type = "descendant"
            return self

    class InfixAnonymousInnerClass6(Infix):

        def __init__(self, outerInstance, get):
            super().__init__(outerInstance, "(", get)
            self._outerInstance = outerInstance


        def led(self, left):
            # left is is what we are trying to invoke
            self.procedure = left
            self.type = "function"
            self.arguments = []
            if outerInstance.node.id != ")":
                while True:
                    if "operator" == outerInstance.node.type and outerInstance.node.id == "?":
                        # partial function application
                        self.type = "partial"
                        self.arguments.add(outerInstance.node)
                        outerInstance.advance("?")
                    else:
                        self.arguments.add(outerInstance.expression(0))
                    if outerInstance.node.id != ",":
                        break
                    outerInstance.advance(",")
            outerInstance.advance(")", True)
            # if the name of the function is 'function' or λ, then this is function definition (lambda function)
            if left.type == "name" and (left.value is "function" or left.value is "\u03BB"):
                # all of the args must be VARIABLE tokens
                #int index = 0
                for arg in outerInstance.arguments:
                    #this.arguments.forEach(function (arg, index) {
                    if arg.type != "variable":
                        return outerInstance.handleError(JException("S0208", arg.position, arg.value))
                    #index++
                self.type = "lambda"
                # is the next token a '<' - if so, parse the function signature
                if outerInstance.node.id == "<":
                    depth = 1
                    sig = "<"
                    while depth > 0 and outerInstance.node.id != "{" and outerInstance.node.id != "(end)":
                        tok = outerInstance.advance()
                        if tok.id == ">":
                            depth -= 1
                        elif tok.id == "<":
                            depth += 1
                        sig += tok.value
                    outerInstance.advance(">")
                    self.signature = com.dashjoin.jsonata.utils.Signature(sig, "lambda")
                # parse the function body
                outerInstance.advance("{")
                self.body = outerInstance.expression(0)
                outerInstance.advance("}")
            return self
        #})

        # parenthesis - block expression
        # Note: in Java both nud and led are in same class!
        #register(new Prefix("(") {

        def nud(self):
            if outerInstance.dbg:
                print("Prefix (")
            expressions = []
            while outerInstance.node.id != ")":
                expressions.append(self._outerInstance.expression(0))
                if outerInstance.node.id != ";":
                    break
                outerInstance.advance(";")
            outerInstance.advance(")", True)
            self.type = "block"
            self.expressions = expressions
            return self

    class InfixAnonymousInnerClass7(Infix):

        def __init__(self, outerInstance, get):
            super().__init__(outerInstance, "[", get)
            self._outerInstance = outerInstance


        def nud(self):
            a = []
            if outerInstance.node.id != "]":
                while True:
                    item = self._outerInstance.expression(0)
                    if outerInstance.node.id == "..":
                        # range operator
                        range = Symbol(self._outerInstance)
                        range.type = "binary"
                        range.value = ".."
                        range.position = outerInstance.node.position
                        range.lhs = item
                        outerInstance.advance("..")
                        range.rhs = outerInstance.expression(0)
                        item = range
                    a.append(item)
                    if outerInstance.node.id != ",":
                        break
                    outerInstance.advance(",")
            outerInstance.advance("]", True)
            self.expressions = a
            self.type = "unary"
            return self
        #})

        # filter - predicate or array index
        #register(new Infix("[", Tokenizer.operators.get("[")) {

        def led(self, left):
            if outerInstance.node.id == "]":
                # empty predicate means maintain singleton arrays in the output
                step = left
                while step is not None and step.type == "binary" and step.value is "[":
                    step = (step).lhs
                step.keepArray = True
                outerInstance.advance("]")
                return left
            else:
                self.lhs = left
                self.rhs = outerInstance.expression(Tokenizer.operators["]"])
                self.type = "binary"
                outerInstance.advance("]", True)
                return self

    class InfixAnonymousInnerClass8(Infix):

        def __init__(self, outerInstance, get):
            super().__init__(outerInstance, "^", get)
            self._outerInstance = outerInstance


        def led(self, left):
            outerInstance.advance("(")
            terms = []
            while True:
# JAVA TO PYTHON CONVERTER WARNING: The original Java variable was marked 'final':
# ORIGINAL LINE: final Symbol term = new Symbol(outerInstance);
                term = Symbol(self._outerInstance)
                term.descending = False

                if outerInstance.node.id == "<":
                    # ascending sort
                    outerInstance.advance("<")
                elif outerInstance.node.id == ">":
                    # descending sort
                    term.descending = True
                    outerInstance.advance(">")
                else:
                    #unspecified - default to ascending
                    pass
                term.expression = self._outerInstance.expression(0)
                terms.append(term)
                if outerInstance.node.id != ",":
                    break
                outerInstance.advance(",")
            outerInstance.advance(")")
            self.lhs = left
            self.rhsTerms = terms
            self.type = "binary"
            return self

    class InfixAnonymousInnerClass9(Infix):

        def __init__(self, outerInstance, get):
            super().__init__(outerInstance, "{", get)
            self._outerInstance = outerInstance


        # merged register(new Prefix("{") {

        def nud(self):
            return outerInstance.objectParser(None)
        # })

        # register(new Infix("{", Tokenizer.operators.get("{")) {

        def led(self, left):
            return outerInstance.objectParser(left)

    class InfixRAnonymousInnerClass2(InfixR):

        def __init__(self, outerInstance, get):
            super().__init__(outerInstance, ":=", get)
            self._outerInstance = outerInstance


        def led(self, left):
            if left.type != "variable":
                return outerInstance.handleError(JException("S0212", left.position, left.value))
            self.lhs = left
            self.rhs = outerInstance.expression(Tokenizer.operators[":="] - 1) # subtract 1 from bindingPower for right associative operators
            self.type = "binary"
            return self

    class InfixAnonymousInnerClass10(Infix):

        def __init__(self, outerInstance, get):
            super().__init__(outerInstance, "@", get)
            self._outerInstance = outerInstance


        def led(self, left):
            self.lhs = left
            self.rhs = outerInstance.expression(Tokenizer.operators["@"])
            if self.rhs.type != "variable":
                return outerInstance.handleError(JException("S0214", self.rhs.position, "@"))
            self.type = "binary"
            return self

    class InfixAnonymousInnerClass11(Infix):

        def __init__(self, outerInstance, get):
            super().__init__(outerInstance, "#", get)
            self._outerInstance = outerInstance


        def led(self, left):
            self.lhs = left
            self.rhs = outerInstance.expression(Tokenizer.operators["#"])
            if self.rhs.type != "variable":
                return outerInstance.handleError(JException("S0214", self.rhs.position, "#"))
            self.type = "binary"
            return self

    class InfixAnonymousInnerClass12(Infix):

        def __init__(self, outerInstance, get):
            super().__init__(outerInstance, "?", get)
            self._outerInstance = outerInstance


        def led(self, left):
            self.type = "condition"
            self.condition = left
            self.then = outerInstance.expression(0)
            if outerInstance.node.id == ":":
                # else condition
                outerInstance.advance(":")
                self._else = outerInstance.expression(0)
            return self

    class PrefixAnonymousInnerClass2(Prefix):

        def __init__(self, outerInstance):
            super().__init__(outerInstance, "|")
            self._outerInstance = outerInstance


        def nud(self):
            self.type = "transform"
            self.pattern = self._outerInstance.expression(0)
            outerInstance.advance("|")
            self.update = self._outerInstance.expression(0)
            if outerInstance.node.id == ",":
                outerInstance.advance(",")
                self.delete = self._outerInstance.expression(0)
            outerInstance.advance("|")
            return self

    # tail call optimization
    # this is invoked by the post parser to analyse lambda functions to see
    # if they make a tail call.  If so, it is replaced by a thunk which will
    # be invoked by the trampoline loop during function application.
    # This enables tail-recursive functions to be written without growing the stack
    def tailCallOptimize(self, expr):
        result = None
        if expr.type == "function" and expr.predicate is None:
            thunk = Symbol(self)
            thunk.type = "lambda"
            thunk.thunk = True
            thunk.arguments = []
            thunk.position = expr.position
            thunk.body = expr
            result = thunk
        elif expr.type == "condition":
            # analyse both branches
            expr.then = self.tailCallOptimize(expr.then)
            if expr._else is not None:
                expr._else = self.tailCallOptimize(expr._else)
            result = expr
        elif expr.type == "block":
            # only the last expression in the block
            length = len(expr.expressions)
            if length > 0:
                if not(isinstance(expr.expressions, java.util.ArrayList)):
                    expr.expressions = list(expr.expressions)
                expr.expressions[length - 1] = self.tailCallOptimize(expr.expressions[length - 1])
            result = expr
        else:
            result = expr
        return result


    def seekParent(self, node, slot):
        match node.type:
            case node.type == "name" | "wildcard":
                slot.level -= 1
                if slot.level == 0:
                    if node.ancestor is None:
                        node.ancestor = slot
                    else:
                        # reuse the existing label
                        self.ancestry[int(slot.index)].slot.label = node.ancestor.label
                        node.ancestor = slot
                    node.tuple = True
            case "parent":
                slot.level += 1
            case "block":
                # look in last expression in the block
                if len(node.expressions) > 0:
                    node.tuple = True
                    slot = self.seekParent(node.expressions[-1], slot)
            case "path":
                # last step in path
                node.tuple = True
                index = len(node.steps) - 1
# JAVA TO PYTHON CONVERTER WARNING: An assignment within expression was extracted from the following statement:
# ORIGINAL LINE: slot = seekParent(node.steps.get(index--), slot);
                slot = self.seekParent(node.steps[index], slot)
                index -= 1
                while slot.level > 0 and index >= 0:
                    # check previous steps
# JAVA TO PYTHON CONVERTER WARNING: An assignment within expression was extracted from the following statement:
# ORIGINAL LINE: slot = seekParent(node.steps.get(index--), slot);
                    slot = self.seekParent(node.steps[index], slot)
                    index -= 1
            case other:
                # error - can't derive ancestor
                raise JException("S0217", node.position, node.type)
        return slot


    def pushAncestry(self, result, value):
        if value is None:
            return # Added NPE check
        if value.seekingParent is not None or value.type == "parent":
            slots = value.seekingParent if (value.seekingParent is not None) else []
            if value.type == "parent":
                slots.append(value.slot)
            if result.seekingParent is None:
                result.seekingParent = slots
            else:
                result.seekingParent.extend(slots)

    def resolveAncestry(self, path):
        index = len(path.steps) - 1
        laststep = path.steps[index]
        slots = laststep.seekingParent if (laststep.seekingParent is not None) else []
        if laststep.type == "parent":
            slots.append(laststep.slot)
        for is_, _ in enumerate(slots):
            slot = slots[is_]
            index = len(path.steps) - 2
            while slot.level > 0:
                if index < 0:
                    if path.seekingParent is None:
                        path.seekingParent = list(java.util.Arrays.asList(slot))
                    else:
                        path.seekingParent.append(slot)
                    break
                # try previous step
# JAVA TO PYTHON CONVERTER WARNING: An assignment within expression was extracted from the following statement:
# ORIGINAL LINE: var step = path.steps.get(index--);
                step = path.steps[index]
                index -= 1
                # multiple contiguous steps that bind the focus should be skipped
                while index >= 0 and step.focus is not None and path.steps[index].focus is not None:
# JAVA TO PYTHON CONVERTER WARNING: An assignment within expression was extracted from the following statement:
# ORIGINAL LINE: step = path.steps.get(index--);
                    step = path.steps[index]
                    index -= 1
                slot = self.seekParent(step, slot)

    # post-parse stage
    # the purpose of this is to add as much semantic value to the parse tree as possible
    # in order to simplify the work of the evaluator.
    # This includes flattening the parts of the AST representing location paths,
    # converting them to arrays of steps which in turn may contain arrays of predicates.
    # following this, nodes containing '.' and '[' should be eliminated from the AST.
    def processAST(self, expr):
        result = expr
        if expr is None:
            return None
        if self.dbg:
            print(" > processAST type=" + expr.type + " value='" + expr.value + "'")
        expr.type if match expr.type is not None else "(null)":
            case "binary":
                    match "" + expr.value:
                        case ".":
                            lstep = self.processAST((expr).lhs)

                            if lstep.type == "path":
                                result = lstep
                            else:
                                result = Infix(self, None)
                                result.type = "path"
                                result.steps = list(java.util.Arrays.asList(lstep))
                                #result = {type: 'path', steps: [lstep]}
                            if lstep.type == "parent":
                                result.seekingParent = list(java.util.Arrays.asList(lstep.slot))
                            rest = self.processAST((expr).rhs)
                            if rest.type == "function" and rest.procedure.type == "path" and len(rest.procedure.steps) == 1 and rest.procedure.steps[0].type == "name" and result.steps[-1].type == "function":
                                # next function in chain of functions - will override a thenable
                                result.steps[-1].nextFunction = rest.procedure.steps[0].value
                            if rest.type == "path":
                                result.steps.extend(rest.steps)
                            else:
                                if rest.predicate is not None:
                                    rest.stages = rest.predicate
                                    rest.predicate = None
                                    #delete rest.predicate
                                result.steps.append(rest)
                            # any steps within a path that are string literals, should be changed to 'name'
                            for step in result.steps:
                                if step.type == "number" or step.type == "value":
                                    # don't allow steps to be numbers or the values true/false/null
                                    raise JException("S0213", step.position, step.value)
                                #System.out.println("step "+step+" type="+step.type)
                                if step.type == "string":
                                    step.type = "name"
                                # for (var lit : step.steps) {
                                #     System.out.println("step2 "+lit+" type="+lit.type)
                                #     lit.type = "name"
                                # }

                            # any step that signals keeping a singleton array, should be flagged on the path
                            if result.steps.stream().filter(lambda step : step.keepArray == True).count() > 0:
                                result.keepSingletonArray = True
                            # if first step is a path constructor, flag it for special handling
                            firststep = result.steps[0]
                            if firststep.type == "unary" and ("" + firststep.value) == "[":
                                firststep.consarray = True
                            # if the last step is an array constructor, flag it so it doesn't flatten
                            laststep = result.steps[-1]
                            if laststep.type == "unary" and ("" + laststep.value) == "[":
                                laststep.consarray = True
                            self.resolveAncestry(result)
                        case "[":
                            if self.dbg:
                                print("binary [")
                            # predicated step
                            # LHS is a step or a predicated step
                            # RHS is the predicate expr
                            result = self.processAST((expr).lhs)
                            step = result
                            type = "predicate"
                            if result.type == "path":
                                step = result.steps[-1]
                                type = "stages"
                            if step.group is not None:
                                raise JException("S0209", expr.position)
                            # if (typeof step[type] === 'undefined') {
                            #     step[type] = []
                            # }
                            if type == "stages":
                                if step.stages is None:
                                    step.stages = []
                            else:
                                if step.predicate is None:
                                    step.predicate = []

                            predicate = self.processAST((expr).rhs)
                            if predicate.seekingParent is not None:
# JAVA TO PYTHON CONVERTER WARNING: The original Java variable was marked 'final':
# ORIGINAL LINE: final var _step = step;
                                _step = step
# JAVA TO PYTHON CONVERTER TASK: Only expression lambdas are converted by Java to Python Converter:
                                #                                predicate.seekingParent.forEach(slot ->
                                #                                {
                                #                                    if(slot.level == 1)
                                #                                    {
                                #                                        seekParent(_step, slot)
                                #                                    }
                                #                                    else
                                #                                    {
                                #                                        slot.level--
                                #                                    }
                                #                                }
                                #                                )
                                self.pushAncestry(step, predicate)
                            s = Symbol(self)
                            s.type = "filter"
                            s.expr = predicate
                            s.position = expr.position

                            # FIXED:
                            # this logic is required in Java to fix
                            # for example test: flattening case 045
                            # otherwise we lose the keepArray flag
                            if expr.keepArray:
                                step.keepArray = True

                            if type == "stages":
                                step.stages.append(s)
                            else:
                                step.predicate.append(s)
                            #step[type].push({type: 'filter', expr: predicate, position: expr.position})
                        case "{":
                            # group-by
                            # LHS is a step or a predicated step
                            # RHS is the object constructor expr
                            result = self.processAST(expr.lhs)
                            if result.group is not None:
                                raise JException("S0210", expr.position)
                            # object constructor - process each pair
                            result.group = Symbol(self)
                            result.group.lhsObject = expr.rhsObject.stream().map(lambda pair : [self.processAST(pair[0]), self.processAST(pair[1])]).collect(java.util.stream.Collectors.toList())
                            result.group.position = expr.position

                        case "^":
                            # order-by
                            # LHS is the array to be ordered
                            # RHS defines the terms
                            result = self.processAST(expr.lhs)
                            if result.type != "path":
                                _res = Symbol(self)
                                _res.type = "path"
                                _res.steps = []
                                _res.steps.append(result)
                                result = _res
                            sortStep = Symbol(self)
                            sortStep.type = "sort"
                            sortStep.position = expr.position
# JAVA TO PYTHON CONVERTER TASK: Only expression lambdas are converted by Java to Python Converter:
                            #                        sortStep.terms = expr.rhsTerms.stream().map(terms ->
                            #                        {
                            #                            Symbol expression = processAST(terms.expression)
                            #                            pushAncestry(sortStep, expression)
                            #                            Symbol res = new Symbol()
                            #                            res.descending = terms.descending
                            #                            res.expression = expression
                            #                            return res
                            #                        }
                            #                        ).collect(Collectors.toList())
                            result.steps.append(sortStep)
                            self.resolveAncestry(result)
                        case ":=":
                            result = Symbol(self)
                            result.type = "bind"
                            result.value = expr.value
                            result.position = expr.position
                            result.lhs = self.processAST(expr.lhs)
                            result.rhs = self.processAST(expr.rhs)
                            self.pushAncestry(result, result.rhs)
                        case "@":
                            result = self.processAST(expr.lhs)
                            step = result
                            if result.type == "path":
                                step = result.steps[-1]
                            # throw error if there are any predicates defined at this point
                            # at this point the only type of stages can be predicates
                            if step.stages is not None or step.predicate is not None:
                                raise JException("S0215", expr.position)
                            # also throw if this is applied after an 'order-by' clause
                            if step.type == "sort":
                                raise JException("S0216", expr.position)
                            if expr.keepArray:
                                step.keepArray = True
                            step.focus = expr.rhs.value
                            step.tuple = True
                        case "#":
                            result = self.processAST(expr.lhs)
                            step = result
                            if result.type == "path":
                                step = result.steps[-1]
                            else:
                                _res = Symbol(self)
                                _res.type = "path"
                                _res.steps = []
                                _res.steps.append(result)
                                result = _res
                                if step.predicate is not None:
                                    step.stages = step.predicate
                                    step.predicate = None
                            if step.stages is None:
                                step.index = expr.rhs.value # name of index variable = String
                            else:
                                _res = Symbol(self)
                                _res.type = "index"
                                _res.value = expr.rhs.value
                                _res.position = expr.position
                                step.stages.append(_res)
                            step.tuple = True
                        case "~>":
                            result = Symbol(self)
                            result.type = "apply"
                            result.value = expr.value
                            result.position = expr.position
                            result.lhs = self.processAST(expr.lhs)
                            result.rhs = self.processAST(expr.rhs)
                        case other:
                            _result = Infix(self, None)
                            _result.type = expr.type
                            _result.value = expr.value
                            _result.position = expr.position
                            _result.lhs = self.processAST((expr).lhs)
                            _result.rhs = self.processAST((expr).rhs)
                            self.pushAncestry(_result, _result.lhs)
                            self.pushAncestry(_result, _result.rhs)
                            result = _result

            case "unary":
                    result = Symbol(self)
                    result.type = expr.type
                    result.value = expr.value
                    result.position = expr.position
                    # expr.value might be Character!
                    exprValue = "" + expr.value
                    if exprValue == "[":
                        if self.dbg:
                            print("unary [ " + result)
                        # array constructor - process each item
# JAVA TO PYTHON CONVERTER WARNING: The original Java variable was marked 'final':
# ORIGINAL LINE: final Symbol _result = result;
                        _result = result
# JAVA TO PYTHON CONVERTER TASK: Only expression lambdas are converted by Java to Python Converter:
                        #                    result.expressions = expr.expressions.stream().map(item ->
                        #                    {
                        #                        Symbol value = processAST(item)
                        #                        pushAncestry(_result, value)
                        #                        return value
                        #                    }
                        #                    ).collect(Collectors.toList())
                    elif exprValue == "{":
                        # object constructor - process each pair
                        #throw new Error("processAST {} unimpl")
# JAVA TO PYTHON CONVERTER WARNING: The original Java variable was marked 'final':
# ORIGINAL LINE: final Symbol _result = result;
                        _result = result
# JAVA TO PYTHON CONVERTER TASK: Only expression lambdas are converted by Java to Python Converter:
                        #                    result.lhsObject = expr.lhsObject.stream().map(pair ->
                        #                    {
                        #                        Symbol key = processAST(pair[0])
                        #                        pushAncestry(_result, key)
                        #                        Symbol value = processAST(pair[1])
                        #                        pushAncestry(_result, value)
                        #                        return new Symbol[] {key, value}
                        #                    }
                        #                    ).collect(Collectors.toList())
                    else:
                        # all other unary expressions - just process the expression
                        result.expression = self.processAST(expr.expression)
                        # if unary minus on a number, then pre-process
                        if exprValue == "-" and result.expression.type == "number":
                            result = result.expression
                            result.value = Utils.convertNumber(-(result.value).doubleValue())
                            if self.dbg:
                                print("unary - value=" + result.value)
                        else:
                            self.pushAncestry(result, result.expression)

            case (expr.type if expr.type is not None else "(null)" == "function") | "partial":
                result = Symbol(self)
                result.type = expr.type
                result.name = expr.name
                result.value = expr.value
                result.position = expr.position
# JAVA TO PYTHON CONVERTER WARNING: The original Java variable was marked 'final':
# ORIGINAL LINE: final Symbol _result = result;
                _result = result
# JAVA TO PYTHON CONVERTER TASK: Only expression lambdas are converted by Java to Python Converter:
                #                result.arguments = expr.arguments.stream().map(arg ->
                #                {
                #                    Symbol argAST = processAST(arg)
                #                    pushAncestry(_result, argAST)
                #                    return argAST
                #                }
                #                ).collect(Collectors.toList())
                result.procedure = self.processAST(expr.procedure)
            case "lambda":
                result = Symbol(self)
                result.type = expr.type
                result.arguments = expr.arguments
                result.signature = expr.signature
                result.position = expr.position
                body = self.processAST(expr.body)
                result.body = self.tailCallOptimize(body)
            case "condition":
                result = Symbol(self)
                result.type = expr.type
                result.position = expr.position
                result.condition = self.processAST(expr.condition)
                self.pushAncestry(result, result.condition)
                result.then = self.processAST(expr.then)
                self.pushAncestry(result, result.then)
                if expr._else is not None:
                    result._else = self.processAST(expr._else)
                    self.pushAncestry(result, result._else)
            case "transform":
                result = Symbol(self)
                result.type = expr.type
                result.position = expr.position
                result.pattern = self.processAST(expr.pattern)
                result.update = self.processAST(expr.update)
                if expr.delete is not None:
                    result.delete = self.processAST(expr.delete)
            case "block":
                result = Symbol(self)
                result.type = expr.type
                result.position = expr.position
                # array of expressions - process each one
# JAVA TO PYTHON CONVERTER WARNING: The original Java variable was marked 'final':
# ORIGINAL LINE: final Symbol __result = result;
                __result = result
# JAVA TO PYTHON CONVERTER TASK: Only expression lambdas are converted by Java to Python Converter:
                #                result.expressions = expr.expressions.stream().map(item ->
                #                {
                #                    Symbol part = processAST(item)
                #                    pushAncestry(__result, part)
                #                    if (part.consarray || (part.type.equals("path") && part.steps.get(0).consarray))
                #                    {
                #                        __result.consarray = true
                #                    }
                #                    return part
                #                }
                #                ).collect(Collectors.toList())
                # TODO scan the array of expressions to see if any of them assign variables
                # if so, need to mark the block as one that needs to create a new frame
            case "name":
                result = Symbol(self)
                result.type = "path"
                result.steps = []
                result.steps.append(expr)
                if expr.keepArray:
                    result.keepSingletonArray = True
            case "parent":
                result = Symbol(self)
                result.type = "parent"
                result.slot = Symbol(self)
# JAVA TO PYTHON CONVERTER WARNING: An assignment within expression was extracted from the following statement:
# ORIGINAL LINE: result.slot.label = "!"+ancestorLabel++;
                result.slot.label = "!" + str(self.ancestorLabel)
                self.ancestorLabel += 1
                result.slot.level = 1
# JAVA TO PYTHON CONVERTER WARNING: An assignment within expression was extracted from the following statement:
# ORIGINAL LINE: result.slot.index = ancestorIndex++;
                result.slot.index = self.ancestorIndex
                self.ancestorIndex += 1
                #slot: { label: '!' + ancestorLabel++, level: 1, index: ancestorIndex++ } }
                self.ancestry.append(result)
            case (expr.type if expr.type is not None else "(null)" == "string") | (expr.type if expr.type is not None else "(null)" == "number") | (expr.type if expr.type is not None else "(null)" == "value") | (expr.type if expr.type is not None else "(null)" == "wildcard") | (expr.type if expr.type is not None else "(null)" == "descendant") | (expr.type if expr.type is not None else "(null)" == "variable") | "regex":
                result = expr
            case "operator":
                # the tokens 'and' and 'or' might have been used as a name rather than an operator
                if expr.value is "and" or expr.value is "or" or expr.value is "in":
                    expr.type = "name"
                    result = self.processAST(expr)
                elif ("" + expr.value) == "?":
                    # partial application
                    result = expr
                else:
                    raise JException("S0201", expr.position, expr.value)
            case "error":
                result = expr
                if expr.lhs is not None:
                    result = self.processAST(expr.lhs)
            case other:
                code = "S0206"
                # istanbul ignore else 
                if expr.id == "(end)":
                    code = "S0207"
                err = JException(code, expr.position, expr.value)
                if self.recover:
                    self.errors.append(err)
                    ret = Symbol(self)
                    ret.type = "error"
                    ret.error = err
                    return ret
                else:
                    #err.stack = (new Error()).stack
                    raise err
        if expr.keepArray:
            result.keepArray = True
        return result

    def objectParser(self, left):

        res = Infix(self, "{") if left is not None else Prefix(self, "{")

        a = []
        if self.node.id != "}":
            while True:
                n = Parser.this.expression(0)
                self.advance(":")
                v = Parser.this.expression(0)
                pair = [n, v]
                a.append(pair) # holds an array of name/value expression pairs
                if self.node.id != ",":
                    break
                self.advance(",")
        self.advance("}", True)
        if left is None:
            # NUD - unary prefix form
            (res).lhsObject = a
            (res).type = "unary"
        else:
            # LED - binary infix form
            (res).lhs = left
            (res).rhsObject = a
            (res).type = "binary"
        return res

    def parse(self, jsonata):
        self.source = jsonata

        # now invoke the tokenizer and the parser and return the syntax tree
        self.lexer = Tokenizer(self.source)
        self.advance()
        # parse the tokens
        expr = self.expression(0)
        if self.node.id != "(end)":
            err = JException("S0201", self.node.position, self.node.value)
            self.handleError(err)

        expr = self.processAST(expr)

        if expr.type == "parent" or expr.seekingParent is not None:
            # error - trying to derive ancestor at top level
            raise JException("S0217", expr.position, expr.type)

        if len(self.errors) > 0:
            expr.errors = self.errors

        return expr
