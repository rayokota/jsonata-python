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
# * © Copyright IBM Corp. 2016, 2017 All Rights Reserved
# *   Project name: JSONata
# *   This project is licensed under the MIT License, see LICENSE
# 


from com.dashjoin.jsonata import Parser.Infix
from com.dashjoin.jsonata import Parser.Symbol
import com.dashjoin.jsonata.Utils
from com.dashjoin.jsonata.utils import Signature

#*
# * @module JSONata
# * @description JSON query and transformation language
# 
# JAVA TO PYTHON CONVERTER TASK: Java annotations have no direct Python equivalent:
# ORIGINAL LINE: @SuppressWarnings({"rawtypes", "unchecked"}) public class Jsonata
class Jsonata:

    def _initialize_instance_fields(self):
        # instance fields found by Java to Python Converter:
        self.errors = None
        self.environment = None
        self.ast = None
        self.timestamp = 0
        self.input = None
        self.validateInput = True
        self.parser = com.dashjoin.jsonata.Jsonata.getParser()


    # Start of Evaluator code

    class EntryCallback:
        def callback(self, expr, input, environment):
            pass

    class ExitCallback:
        def callback(self, expr, input, environment, result):
            pass

    class Frame:



        def __init__(self, enclosingEnvironment):
            # instance fields found by Java to Python Converter:
            self.bindings = java.util.LinkedHashMap()
            self.parent = None
            self.isParallelCall = False

            self.parent = enclosingEnvironment

# JAVA TO PYTHON CONVERTER TASK: Python does not allow method overloads:
        def bind(self, name, val):
            self.bindings[name] = val

# JAVA TO PYTHON CONVERTER TASK: Python does not allow method overloads:
        def bind(self, name, function):
            self.bind(name, function)
            if function.signature is not None:
                function.signature.setFunctionName(name)

# JAVA TO PYTHON CONVERTER TASK: Python does not allow method overloads:
        def bind(self, name, lambda_):
            self.bind(name, lambda_)
# JAVA TO PYTHON CONVERTER TASK: Python does not allow method overloads:
        def bind(self, name, lambda_):
            self.bind(name, lambda_)
# JAVA TO PYTHON CONVERTER TASK: Python does not allow method overloads:
        def bind(self, name, lambda_):
            self.bind(name, lambda_)

        def lookup(self, name):
            # Important: if we have a null value,
            # return it
            if name in self.bindings.keys():
                return self.bindings[name]
            if self.parent is not None:
                return self.parent.lookup(name)
            return None

        #        *
        #         * Sets the runtime bounds for this environment
        #         * 
        #         * @param timeout Timeout in millis
        #         * @param maxRecursionDepth Max recursion depth
        #         
        def setRuntimeBounds(self, timeout, maxRecursionDepth):
            Timebox(self, timeout, maxRecursionDepth)

        def setEvaluateEntryCallback(self, cb):
            self.bind("__evaluate_entry", cb)

        def setEvaluateExitCallback(self, cb):
            self.bind("__evaluate_exit", cb)

    staticFrame = None # = createFrame(null);

    #    *
    #     * Evaluate expression against input data
    #     * @param {Object} expr - JSONata expression
    #     * @param {Object} input - Input data to evaluate against
    #     * @param {Object} environment - Environment
    #     * @returns {*} Evaluated input data
    #     
# JAVA TO PYTHON CONVERTER TASK: Python does not allow method overloads:
    def evaluate(self, expr, input, environment):
        # Thread safety:
        # Make sure each evaluate is executed on an instance per thread
        return self.getPerThreadInstance()._evaluate(expr, input, environment)

    def _evaluate(self, expr, input, environment):
        result = None

        # Store the current input
        # This is required by Functions.functionEval for current $eval() input context
        self.input = input

        if self.parser.dbg:
            print("eval expr=" + expr + " type=" + expr.type) #+" input="+input);

        entryCallback = environment.lookup("__evaluate_entry")
        if entryCallback is not None:
            (entryCallback).callback(expr, input, environment)

        if expr.type is not None:
            if expr.type == "path":
                result = self.evaluatePath(expr, input, environment)
            elif expr.type == "binary":
                result = self.evaluateBinary(expr, input, environment)
            elif expr.type == "unary":
                result = self.evaluateUnary(expr, input, environment)
            elif expr.type == "name":
                result = self.evaluateName(expr, input, environment)
                if self.parser.dbg:
                    print("evalName " + result)
            elif expr.type == "string" or expr.type == "number" or expr.type == "value":
                result = self.evaluateLiteral(expr) #, input, environment);
            elif expr.type == "wildcard":
                result = self.evaluateWildcard(expr, input) #, environment);
            elif expr.type == "descendant":
                result = self.evaluateDescendants(expr, input) #, environment);
            elif expr.type == "parent":
                result = environment.lookup(expr.slot.label)
            elif expr.type == "condition":
                result = self.evaluateCondition(expr, input, environment)
            elif expr.type == "block":
                result = self.evaluateBlock(expr, input, environment)
            elif expr.type == "bind":
                result = self.evaluateBindExpression(expr, input, environment)
            elif expr.type == "regex":
                result = self.evaluateRegex(expr) #, input, environment);
            elif expr.type == "function":
                result = self.evaluateFunction(expr, input, environment, None)
            elif expr.type == "variable":
                result = self.evaluateVariable(expr, input, environment)
            elif expr.type == "lambda":
                result = self.evaluateLambda(expr, input, environment)
            elif expr.type == "partial":
                result = self.evaluatePartialApplication(expr, input, environment)
            elif expr.type == "apply":
                result = self.evaluateApplyExpression(expr, input, environment)
            elif expr.type == "transform":
                result = self.evaluateTransformExpression(expr, input, environment)

        if expr.predicate is not None:
            for ii, _ in enumerate(expr.predicate):
                result = self.evaluateFilter(expr.predicate[ii].expr, result, environment)

        if expr.type != "path" and expr.group is not None:
            result = self.evaluateGroupExpression(expr.group, result, environment)

        exitCallback = environment.lookup("__evaluate_exit")
        if exitCallback is not None:
            (exitCallback).callback(expr, input, environment, result)

        # mangle result (list of 1 element -> 1 element, empty list -> null)
        if result is not None and Utils.isSequence(result) and not(result).tupleStream:
            _result = result
            if expr.keepArray:
                _result.keepSingleton = True
            if _result.isEmpty():
                result = None
            elif _result.size() == 1:
                result = _result if _result.keepSingleton else _result.get(0)

        return result

    #    *
    #     * Evaluate path expression against input data
    #    * @param {Object} expr - JSONata expression
    #    * @param {Object} input - Input data to evaluate against
    #    * @param {Object} environment - Environment
    #    * @returns {*} Evaluated input data
    #    
    # async 
    def evaluatePath(self, expr, input, environment):
        inputSequence = None
        # expr is an array of steps
        # if the first step is a variable reference ($...), including root reference ($$),
        #   then the path is absolute rather than relative
        if isinstance(input, java.util.List) and expr.steps[0].type is not "variable":
            inputSequence = input
        else:
            # if input is not an array, make it so
            inputSequence = Utils.createSequence(input)

        resultSequence = None
        isTupleStream = False
        tupleBindings = None

        # evaluate each step in turn
        for ii, _ in enumerate(expr.steps):
            step = expr.steps[ii]

            if step.tuple is not None:
                isTupleStream = True

            # if the first step is an explicit array constructor, then just evaluate that (i.e. don"t iterate over a context array)
            if ii == 0 and step.consarray:
                resultSequence = self.evaluate(step, inputSequence, environment)
            else:
                if isTupleStream:
                    tupleBindings = self.evaluateTupleStep(step, inputSequence, tupleBindings, environment)
                else:
                    resultSequence = self.evaluateStep(step, inputSequence, environment, ii == len(expr.steps) - 1)

            if not isTupleStream and (resultSequence is None or len((resultSequence)) == 0):
                break

            if step.focus is None:
                inputSequence = resultSequence


        if isTupleStream:
            if expr.tuple is not None:
                # tuple stream is carrying ancestry information - keep this
                resultSequence = tupleBindings
            else:
                resultSequence = Utils.createSequence()
                for ii, _ in enumerate(tupleBindings):
                    (resultSequence).append(tupleBindings[ii]["@"])

        if expr.keepSingletonArray:

            # If we only got an ArrayList, convert it so we can set the keepSingleton flag
            if not(isinstance(resultSequence, com.dashjoin.jsonata.Utils.JList)):
                resultSequence = com.dashjoin.jsonata.Utils.JList(resultSequence)

            # if the array is explicitly constructed in the expression and marked to promote singleton sequences to array
            if (isinstance(resultSequence, com.dashjoin.jsonata.Utils.JList)) and (resultSequence).cons and not(resultSequence).sequence:
                resultSequence = Utils.createSequence(resultSequence)
            (resultSequence).keepSingleton = True

        if expr.group is not None:
            resultSequence = self.evaluateGroupExpression(expr.group,tupleBindings if isTupleStream else resultSequence, environment)

        return resultSequence

    def createFrameFromTuple(self, environment, tuple):
        frame = self.createFrame(environment)
        if tuple is not None:
            for prop in tuple.keys():
                frame.bind(prop, tuple[prop])
        return frame

    #    *
    #     * Evaluate a step within a path
    #    * @param {Object} expr - JSONata expression
    #    * @param {Object} input - Input data to evaluate against
    #    * @param {Object} environment - Environment
    #    * @param {boolean} lastStep - flag the last step in a path
    #    * @returns {*} Evaluated input data
    #    
    # async 
    def evaluateStep(self, expr, input, environment, lastStep):
        result = None
        if expr.type == "sort":
            result = self.evaluateSortExpression(expr, input, environment)
            if expr.stages is not None:
                result = self.evaluateStages(expr.stages, result, environment)
            return result

        result = Utils.createSequence()

        for ii, _ in enumerate((input)):
            res = self.evaluate(expr, (input)[ii], environment)
            if expr.stages is not None:
                for ss, _ in enumerate(expr.stages):
                    res = self.evaluateFilter(expr.stages[ss].expr, res, environment)
            if res is not None:
                (result).append(res)

        resultSequence = Utils.createSequence()
        if lastStep and len((result)) == 1 and (isinstance((result)[0], java.util.List)) and not Utils.isSequence((result)[0]):
            resultSequence = (result)[0]
        else:
            # flatten the sequence
            for res in result:
                if not(isinstance(res, java.util.List)) or (isinstance(res, com.dashjoin.jsonata.Utils.JList) and (res).cons):
                    # it's not an array - just push into the result sequence
                    resultSequence.append(res)
                else:
                    # res is a sequence - flatten it into the parent sequence
                    resultSequence.extend(res)

        return resultSequence

    # async 
    def evaluateStages(self, stages, input, environment):
        result = input
        for ss, _ in enumerate(stages):
            stage = stages[ss]
            if stage.type == "filter":
                result = self.evaluateFilter(stage.expr, result, environment)
            elif stage.type == "index":
                for ee, _ in enumerate((result)):
                    tuple = (result)[ee]
                    (tuple)["" + stage.value] = ee
        return result

    #    *
    #     * Evaluate a step within a path
    #    * @param {Object} expr - JSONata expression
    #    * @param {Object} input - Input data to evaluate against
    #    * @param {Object} tupleBindings - The tuple stream
    #    * @param {Object} environment - Environment
    #    * @returns {*} Evaluated input data
    #    
    # async 
    def evaluateTupleStep(self, expr, input, tupleBindings, environment):
        result = None
        if expr.type == "sort":
            if tupleBindings is not None:
                result = self.evaluateSortExpression(expr, tupleBindings, environment)
            else:
                sorted = self.evaluateSortExpression(expr, input, environment)
                result = Utils.createSequence()
                (result).tupleStream = True
                for ss, _ in enumerate((sorted)):
                    tuple = java.util.Map.of("@", sorted[ss], expr.index, ss)
                    result.append(tuple)
            if expr.stages is not None:
                result = self.evaluateStages(expr.stages, result, environment)
            return result

        result = Utils.createSequence()
        (result).tupleStream = True
        stepEnv = environment
        if tupleBindings is None:
            tupleBindings = input.stream().filter(lambda item : item is not None).map(lambda item : java.util.Map.of("@", item)).collect(java.util.stream.Collectors.toList())

        for ee, _ in enumerate(tupleBindings):
            stepEnv = self.createFrameFromTuple(environment, tupleBindings[ee])
            _res = self.evaluate(expr, tupleBindings[ee]["@"], stepEnv)
            # res is the binding sequence for the output tuple stream
            if _res is not None:
                res = None
                if not(isinstance(_res, java.util.List)):
                    res = []
                    res.append(_res)
                else:
                    res = _res
                for bb, _ in enumerate(res):
                    tuple = java.util.LinkedHashMap()
                    tuple.putAll(tupleBindings[ee])
                    #Object.assign(tuple, tupleBindings[ee])
                    if (isinstance(res, com.dashjoin.jsonata.Utils.JList)) and (res).tupleStream:
                        tuple.putAll(res[bb])
                    else:
                        if expr.focus is not None:
                            tuple[expr.focus] = res[bb]
                            tuple["@"] = tupleBindings[ee]["@"]
                        else:
                            tuple["@"] = res[bb]
                        if expr.index is not None:
                            tuple[expr.index] = bb
                        if expr.ancestor is not None:
                            tuple[expr.ancestor.label] = tupleBindings[ee]["@"]
                    result.append(tuple)

        if expr.stages is not None:
            result = self.evaluateStages(expr.stages, result, environment)

        return result

    #    *
    #     * Apply filter predicate to input data
    #    * @param {Object} predicate - filter expression
    #    * @param {Object} input - Input data to apply predicates against
    #    * @param {Object} environment - Environment
    #    * @returns {*} Result after applying predicates
    #    
    # async 
    def evaluateFilter(self, _predicate, input, environment):
        predicate = _predicate
        results = Utils.createSequence()
        if isinstance(input, com.dashjoin.jsonata.Utils.JList) and (input).tupleStream:
            (results).tupleStream = True
        if not(isinstance(input, java.util.List)):
            input = Utils.createSequence(input)
        if predicate.type == "number":
            index = (predicate.value).intValue() # round it down - was Math.floor
            if index < 0:
                # count in from end of array
                index = len((input)) + index
            item = (input)[index] if index < len((input)) else None
            if item is not None:
                if isinstance(item, java.util.List):
                    results = item
                else:
                    results.append(item)
        else:
            for index, _ in enumerate((input)):
                item = (input)[index]
                context = item
                env = environment
                if isinstance(input, com.dashjoin.jsonata.Utils.JList) and (input).tupleStream:
                    context = (item)["@"]
                    env = self.createFrameFromTuple(environment, item)
                res = self.evaluate(predicate, context, env)
                if Utils.isNumeric(res):
                    res = Utils.createSequence(res)
                if Utils.isArrayOfNumbers(res):
                    for ires in (res):
                        # round it down
                        ii = (ires).intValue() # Math.floor(ires);
                        if ii < 0:
                            # count in from end of array
                            ii = len((input)) + ii
                        if ii == index:
                            results.append(item)
                elif com.dashjoin.jsonata.Jsonata.boolize(res):
                    results.append(item)
        return results

    #    *
    #     * Evaluate binary expression against input data
    #    * @param {Object} expr - JSONata expression
    #    * @param {Object} input - Input data to evaluate against
    #    * @param {Object} environment - Environment
    #    * @returns {*} Evaluated input data
    #    
    # async 
    def evaluateBinary(self, _expr, input, environment):
        expr = _expr
        result = None
        lhs = self.evaluate(expr.lhs, input, environment)
        op = "" + expr.value

        if op == "and" or op == "or":

            #defer evaluation of RHS to allow short-circuiting
            evalrhs = CallableAnonymousInnerClass(self, input, environment, expr)

            try:
                return self.evaluateBooleanExpression(lhs, evalrhs, op)
            except Exception as err:
                if not(isinstance(err, JException)):
                    raise JException("Unexpected", expr.position)
                #err.position = expr.position
                #err.token = op
                raise (JException)err

        rhs = self.evaluate(expr.rhs, input, environment) #evalrhs();
        try:
            if op == "+" or op == "-" or op == "*" or op == "/" or op == "%":
                result = self.evaluateNumericExpression(lhs, rhs, op)
            elif op == "=" or op == "!=":
                result = self.evaluateEqualityExpression(lhs, rhs, op)
            elif op == "<" or op == "<=" or op == ">" or op == ">=":
                result = self.evaluateComparisonExpression(lhs, rhs, op)
            elif op == "&":
                result = self.evaluateStringConcat(lhs, rhs)
            elif op == "..":
                result = self.evaluateRangeExpression(lhs, rhs)
            elif op == "in":
                result = self.evaluateIncludesExpression(lhs, rhs)
            else:
                raise JException("Unexpected operator " + op, expr.position)
        except Exception as err:
            #err.position = expr.position
            #err.token = op
            raise err
        return result

    class CallableAnonymousInnerClass(java.util.concurrent.Callable):


        def __init__(self, outerInstance, input, environment, expr):
            self._outerInstance = outerInstance
            self._input = input
            self._environment = environment
            self._expr = expr

# JAVA TO PYTHON CONVERTER WARNING: Method 'throws' clauses are not available in Python:
# ORIGINAL LINE: public Object call() throws Exception
        def call(self):
            return outerInstance.evaluate(self._expr.rhs, self._input, self._environment)

    NULL_VALUE = ObjectAnonymousInnerClass()

    class ObjectAnonymousInnerClass(Object):
        def toString(self):
            return "null"

    #    *
    #     * Evaluate unary expression against input data
    #    * @param {Object} expr - JSONata expression
    #    * @param {Object} input - Input data to evaluate against
    #    * @param {Object} environment - Environment
    #    * @returns {*} Evaluated input data
    #    
    # async 
    def evaluateUnary(self, expr, input, environment):
        result = None

        if str("") + expr.value is "-":
            result = self.evaluate(expr.expression, input, environment)
            if result is None:
                result = None
            elif Utils.isNumeric(result):
                result = Utils.convertNumber(-(result).doubleValue())
            else:
                raise JException("D1002", expr.position, expr.value, result)
        elif str("") + expr.value is "[":
            # array constructor - evaluate each item
            result = com.dashjoin.jsonata.Utils.JList() # [];
            idx = 0
            for item in expr.expressions:
                environment.isParallelCall = idx > 0
                value = self.evaluate(item, input, environment)
                if value is not None:
                    if ("" + item.value) == "[":
                        (result).append(value)
                    else:
                        result = Functions.append(result, value)
                idx += 1
            if expr.consarray:
                if not(isinstance(result, com.dashjoin.jsonata.Utils.JList)):
                    result = com.dashjoin.jsonata.Utils.JList(result)
                #System.out.println("const "+result)
                (result).cons = True
        elif str("") + expr.value is "{":
            # object constructor - apply grouping
            result = self.evaluateGroupExpression(expr, input, environment)

        return result

    #    *
    #     * Evaluate name object against input data
    #    * @param {Object} expr - JSONata expression
    #    * @param {Object} input - Input data to evaluate against
    #    * @param {Object} environment - Environment
    #    * @returns {*} Evaluated input data
    #    
    def evaluateName(self, expr, input, environment):
        # lookup the "name" item in the input
        return Functions.lookup(input, str(expr.value))

    #    *
    #     * Evaluate literal against input data
    #     * @param {Object} expr - JSONata expression
    #     * @returns {*} Evaluated input data
    #     
    def evaluateLiteral(self, expr):
        return expr.value if expr.value is not None else com.dashjoin.jsonata.Jsonata.NULL_VALUE

    #    *
    #     * Evaluate wildcard against input data
    #    * @param {Object} expr - JSONata expression
    #    * @param {Object} input - Input data to evaluate against
    #    * @returns {*} Evaluated input data
    #    
    def evaluateWildcard(self, expr, input):
        results = Utils.createSequence()
        if (isinstance(input, com.dashjoin.jsonata.Utils.JList)) and (input).outerWrapper and (input).size() > 0:
            input = (input).get(0)
        if input is not None and isinstance(input, java.util.Map):
            for key in (input).keys():
                # Object.keys(input).forEach(Object (key) {
                value = (input)[key]
                if (isinstance(value, java.util.List)):
                    value = self.flatten(value, None)
                    results = Functions.append(results, value)
                else:
                    results.append(value)
        elif isinstance(input, java.util.List):
            # Java: need to handle List separately
            for value in (input):
                if (isinstance(value, java.util.List)):
                    value = self.flatten(value, None)
                    results = Functions.append(results, value)
                elif isinstance(value, java.util.Map):
                    # Call recursively do decompose the map
                    results.extend(self.evaluateWildcard(expr, value))
                else:
                    results.append(value)

        # result = normalizeSequence(results)
        return results

    #    *
    #     * Returns a flattened array
    #    * @param {Array} arg - the array to be flatten
    #    * @param {Array} flattened - carries the flattened array - if not defined, will initialize to []
    #    * @returns {Array} - the flattened array
    #    
    def flatten(self, arg, flattened):
        if flattened is None:
            flattened = []
        if isinstance(arg, java.util.List):
            for item in (arg):
                self.flatten(item, flattened)
        else:
            flattened.append(arg)
        return flattened

    #    *
    #     * Evaluate descendants against input data
    #    * @param {Object} expr - JSONata expression
    #    * @param {Object} input - Input data to evaluate against
    #    * @returns {*} Evaluated input data
    #    
    def evaluateDescendants(self, expr, input):
        result = None
        resultSequence = Utils.createSequence()
        if input is not None:
            # traverse all descendants of this object/array
            self.recurseDescendants(input, resultSequence)
            if len(resultSequence) == 1:
                result = resultSequence[0]
            else:
                result = resultSequence
        return result

    #    *
    #     * Recurse through descendants
    #    * @param {Object} input - Input data
    #    * @param {Object} results - Results
    #    
    def recurseDescendants(self, input, results):
        # this is the equivalent of //* in XPath
        if not(isinstance(input, java.util.List)):
            results.append(input)
        if isinstance(input, java.util.List):
            for member in (input):
                self.recurseDescendants(member, results)
        elif input is not None and isinstance(input, java.util.Map):
            #Object.keys(input).forEach(Object (key) {
            for key in (input).keys():
                self.recurseDescendants((input)[key], results)

    #    *
    #     * Evaluate numeric expression against input data
    #     * @param {Object} lhs - LHS value
    #     * @param {Object} rhs - RHS value
    #     * @param {Object} op - opcode
    #     * @returns {*} Result
    #     
    def evaluateNumericExpression(self, _lhs, _rhs, op):
        result = 0

        if _lhs is not None and not Utils.isNumeric(_lhs):
            raise JException("T2001", -1, op, _lhs)
        if _rhs is not None and not Utils.isNumeric(_rhs):
            raise JException("T2002", -1, op, _rhs)

        if _lhs is None or _rhs is None:
            # if either side is undefined, the result is undefined
            return None

        #System.out.println("op22 "+op+" "+_lhs+" "+_rhs)
        lhs = (_lhs).doubleValue()
        rhs = (_rhs).doubleValue()

        if op == "+":
            result = lhs + rhs
        elif op == "-":
            result = lhs - rhs
        elif op == "*":
            result = lhs * rhs
        elif op == "/":
            result = lhs / rhs
        elif op == "%":
            result = int(math.fmod(lhs, rhs))
        return Utils.convertNumber(result)

    #     *
    #      * Evaluate equality expression against input data
    #      * @param {Object} lhs - LHS value
    #      * @param {Object} rhs - RHS value
    #      * @param {Object} op - opcode
    #      * @returns {*} Result
    #      
    def evaluateEqualityExpression(self, lhs, rhs, op):
        result = None

        # type checks
        ltype = type(lhs).getSimpleName() if lhs is not None else None
        rtype = type(rhs).getSimpleName() if rhs is not None else None

        if ltype is None or rtype is None:
            # if either side is undefined, the result is false
            return False

        # JSON might come with integers,
        # convert all to double...
        # FIXME: semantically OK?
        if isinstance(lhs, Number):
            lhs = (lhs).doubleValue()
        if isinstance(rhs, Number):
            rhs = (rhs).doubleValue()

        if op == "=":
            result = lhs is rhs # isDeepEqual(lhs, rhs);
        elif op == "!=":
            result = lhs is not rhs # !isDeepEqual(lhs, rhs);
        return result

    #     *
    #      * Evaluate comparison expression against input data
    #      * @param {Object} lhs - LHS value
    #      * @param {Object} rhs - RHS value
    #      * @param {Object} op - opcode
    #      * @returns {*} Result
    #      
    def evaluateComparisonExpression(self, lhs, rhs, op):
        result = None

        # type checks
        lcomparable = lhs is None or isinstance(lhs, String) or isinstance(lhs, Number)
        rcomparable = rhs is None or isinstance(rhs, String) or isinstance(rhs, Number)

        # if either aa or bb are not comparable (string or numeric) values, then throw an error
        if not lcomparable or not rcomparable:
            raise JException("T2010", 0, op,lhs if lhs is not None else rhs)

        # if either side is undefined, the result is undefined
        if lhs is None or rhs is None:
            return None

        #if aa and bb are not of the same type
        if type(lhs) is not type(rhs):

            if isinstance(lhs, Number) and isinstance(rhs, Number):
                # Java : handle Double / Integer / Long comparisons
                # convert all to double -> loss of precision (64-bit long to double) be a problem here?
                lhs = (lhs).doubleValue()
                rhs = (rhs).doubleValue()

            else:

                raise JException("T2009", 0, lhs, rhs)

        _lhs = lhs

        if op == "<":
            result = _lhs.compareTo(rhs) < 0
        elif op == "<=":
            result = _lhs.compareTo(rhs) <= 0 #lhs <= rhs;
        elif op == ">":
            result = _lhs.compareTo(rhs) > 0 # lhs > rhs;
        elif op == ">=":
            result = _lhs.compareTo(rhs) >= 0 # lhs >= rhs;
        return result

    #     *
    #      * Inclusion operator - in
    #      *
    #      * @param {Object} lhs - LHS value
    #      * @param {Object} rhs - RHS value
    #      * @returns {boolean} - true if lhs is a member of rhs
    #      
    def evaluateIncludesExpression(self, lhs, rhs):
        result = False

        if lhs is None or rhs is None:
            # if either side is undefined, the result is false
            return False

        if not(isinstance(rhs, java.util.List)):
            _rhs = []
            _rhs.append(rhs)
            rhs = _rhs

        for i, _ in enumerate((rhs)):
            if (rhs)[i] is lhs:
                result = True
                break

        return result

    #    *
    #     * Evaluate boolean expression against input data
    #     * @param {Object} lhs - LHS value
    #     * @param {Function} evalrhs - Object to evaluate RHS value
    #     * @param {Object} op - opcode
    #     * @returns {*} Result
    #     
    # async 
# JAVA TO PYTHON CONVERTER WARNING: Method 'throws' clauses are not available in Python:
# ORIGINAL LINE: Object evaluateBooleanExpression(Object lhs, java.util.concurrent.Callable evalrhs, String op) throws Exception
    def evaluateBooleanExpression(self, lhs, evalrhs, op):
        result = None

        lBool = com.dashjoin.jsonata.Jsonata.boolize(lhs)

        if op == "and":
            result = lBool and com.dashjoin.jsonata.Jsonata.boolize(evalrhs.call())
        elif op == "or":
            result = lBool or com.dashjoin.jsonata.Jsonata.boolize(evalrhs.call())
        return result

    @staticmethod
    def boolize(value):
        booledValue = Functions.toBoolean(value)
        return False if booledValue is None else booledValue

    #    *
    #     * Evaluate string concatenation against input data
    #     * @param {Object} lhs - LHS value
    #     * @param {Object} rhs - RHS value
    #     * @returns {string|*} Concatenated string
    #     
    def evaluateStringConcat(self, lhs, rhs):
        result = None

        lstr = ""
        rstr = ""
        if lhs is not None:
            lstr = Functions.string(lhs,None)
        if rhs is not None:
            rstr = Functions.string(rhs,None)

        result = lstr + rstr
        return result

    class GroupEntry:

        def __init__(self):
            # instance fields found by Java to Python Converter:
            self.data = None
            self.exprIndex = 0


    #    *
    #     * Evaluate group expression against input data
    #     * @param {Object} expr - JSONata expression
    #     * @param {Object} input - Input data to evaluate against
    #     * @param {Object} environment - Environment
    #     * @returns {{}} Evaluated input data
    #     
    # async 
    def evaluateGroupExpression(self, expr, _input, environment):
        result = java.util.LinkedHashMap()
        groups = java.util.LinkedHashMap()
        reduce = True if (isinstance(_input, com.dashjoin.jsonata.Utils.JList)) and (_input).tupleStream else False
        # group the input sequence by "key" expression
        if not(isinstance(_input, java.util.List)):
            _input = Utils.createSequence(_input)
        input = _input

        # if the array is empty, add an undefined entry to enable literal JSON object to be generated
        if len(input) == 0:
            input.append(None)

        for itemIndex, _ in enumerate(input):
            item = input[itemIndex]
            env = self.createFrameFromTuple(environment, item) if reduce else environment
            for pairIndex, _ in enumerate(expr.lhsObject):
                pair = expr.lhsObject[pairIndex]
                key = self.evaluate(pair[0],(item)["@"] if reduce else item, env)
                # key has to be a string
                if key is not None and not(isinstance(key, String)):
                    raise JException("T1003", expr.position, key)

                if key is not None:
                    entry = GroupEntry()
                    entry.data = item
                    entry.exprIndex = pairIndex
                    if groups.get(key) is not None:
                        # a value already exists in this slot
                        if groups.get(key).exprIndex is not pairIndex:
                            # this key has been generated by another expression in this group
                            # when multiple key expressions evaluate to the same key, then error D1009 must be thrown
                            raise JException("D1009", expr.position, key)

                        # append it as an array
                        groups.get(key).data = Functions.append(groups.get(key).data, item)
                    else:
                        groups.put(key, entry)

        # iterate over the groups to evaluate the "value" expression
        #let generators = /* await */ Promise.all(Object.keys(groups).map(/* async */ (key, idx) => {
        idx = 0
        for e in groups.entrySet():
            entry = e.getValue()
            context = entry.data
            env = environment
            if reduce:
                tuple = self.reduceTupleStream(entry.data)
                context = (tuple)["@"]
                (tuple).pop("@")
                env = self.createFrameFromTuple(environment, tuple)
            env.isParallelCall = idx > 0
            #return [key, /* await */ evaluate(expr.lhs[entry.exprIndex][1], context, env)]
            res = self.evaluate(expr.lhsObject[entry.exprIndex][1], context, env)
            if res is not None:
                result.put(e.getKey(), res)

            idx += 1

        #  for (let generator of generators) {
        #      var [key, value] = /* await */ generator
        #      if(typeof value !== "undefined") {
        #          result[key] = value
        #      }
        #  }

        return result

    def reduceTupleStream(self, _tupleStream):
        if not(isinstance(_tupleStream, java.util.List)):
            return _tupleStream
        tupleStream = _tupleStream

        result = java.util.LinkedHashMap()
        result.putAll(tupleStream[0])

        #Object.assign(result, tupleStream[0])
        for ii in range(1, len(tupleStream)):

            el = tupleStream[ii]
# JAVA TO PYTHON CONVERTER TASK: The following line could not be converted:
            for (var prop : el.keySet())

                #             for(const prop in tupleStream[ii]) {

# JAVA TO PYTHON CONVERTER TASK: The following line could not be converted:
                result.put(prop, Functions.append(result.get(prop), el.get(prop)));

                #               result[prop] = fn.append(result[prop], tupleStream[ii][prop])
        return result

    #    *
    #     * Evaluate range expression against input data
    #     * @param {Object} lhs - LHS value
    #     * @param {Object} rhs - RHS value
    #     * @returns {Array} Resultant array
    #     
    def evaluateRangeExpression(self, lhs, rhs):
        result = None

        if lhs is not None and (not(isinstance(lhs, Long)) and not(isinstance(lhs, Integer))):
            raise JException("T2003", -1, lhs)
        if rhs is not None and (not(isinstance(rhs, Long)) and not(isinstance(rhs, Integer))):
            raise JException("T2004", -1, rhs)

        if rhs is None or lhs is None:
            # if either side is undefined, the result is undefined
            return result

        _lhs = (lhs).longValue()
        _rhs = (rhs).longValue()

        if _lhs > _rhs:
            # if the lhs is greater than the rhs, return undefined
            return result

        # limit the size of the array to ten million entries (1e7)
        # this is an implementation defined limit to protect against
        # memory and performance issues.  This value may increase in the future.
        size = _rhs - _lhs + 1
        if size > 1e7:
            raise JException("D2014", -1, size)

        return Utils.RangeList(_lhs, _rhs)

    #    *
    #     * Evaluate bind expression against input data
    #     * @param {Object} expr - JSONata expression
    #     * @param {Object} input - Input data to evaluate against
    #     * @param {Object} environment - Environment
    #     * @returns {*} Evaluated input data
    #     
    # async 
    def evaluateBindExpression(self, expr, input, environment):
        # The RHS is the expression to evaluate
        # The LHS is the name of the variable to bind to - should be a VARIABLE token (enforced by parser)
        value = self.evaluate(expr.rhs, input, environment)
        environment.bind("" + expr.lhs.value, value)
        return value

    #    *
    #     * Evaluate condition against input data
    #     * @param {Object} expr - JSONata expression
    #     * @param {Object} input - Input data to evaluate against
    #     * @param {Object} environment - Environment
    #     * @returns {*} Evaluated input data
    #     
    # async 
    def evaluateCondition(self, expr, input, environment):
        result = None
        condition = self.evaluate(expr.condition, input, environment)
        if com.dashjoin.jsonata.Jsonata.boolize(condition):
            result = self.evaluate(expr.then, input, environment)
        elif expr._else is not None:
            result = self.evaluate(expr._else, input, environment)
        return result

    #     *
    #      * Evaluate block against input data
    #      * @param {Object} expr - JSONata expression
    #      * @param {Object} input - Input data to evaluate against
    #      * @param {Object} environment - Environment
    #      * @returns {*} Evaluated input data
    #      
    # async 
    def evaluateBlock(self, expr, input, environment):
        result = None
        # create a new frame to limit the scope of variable assignments
        # TODO, only do this if the post-parse stage has flagged this as required
        frame = self.createFrame(environment)
        # invoke each expression in turn
        # only return the result of the last one
        for ex in expr.expressions:
            result = self.evaluate(ex, input, frame)

        return result

    #     *
    #      * Prepare a regex
    #      * @param {Object} expr - expression containing regex
    #      * @returns {Function} Higher order Object representing prepared regex
    #      
    def evaluateRegex(self, expr):
        # Note: in Java we just use the compiled regex Pattern
        # The apply functions need to take care to evaluate
        return expr.value

    #     *
    #      * Evaluate variable against input data
    #      * @param {Object} expr - JSONata expression
    #      * @param {Object} input - Input data to evaluate against
    #      * @param {Object} environment - Environment
    #      * @returns {*} Evaluated input data
    #      
    def evaluateVariable(self, expr, input, environment):
        # lookup the variable value in the environment
        result = None
        # if the variable name is empty string, then it refers to context value
        if expr.value is "":
            # Empty string == "$" !
            result = (input).get(0) if isinstance(input, com.dashjoin.jsonata.Utils.JList) and (input).outerWrapper else input
        else:
            result = environment.lookup(str(expr.value))
            if self.parser.dbg:
                print("variable name=" + expr.value + " val=" + result)
        return result

    #     *
    #      * sort / order-by operator
    #      * @param {Object} expr - AST for operator
    #      * @param {Object} input - Input data to evaluate against
    #      * @param {Object} environment - Environment
    #      * @returns {*} Ordered sequence
    #      
    # async 
    def evaluateSortExpression(self, expr, input, environment):
        result = None

        # evaluate the lhs, then sort the results in order according to rhs expression
        lhs = input
        isTupleSort = True if (isinstance(input, com.dashjoin.jsonata.Utils.JList) and (input).tupleStream) else False

        # sort the lhs array
        # use comparator function
        comparator = ComparatorAnonymousInnerClass(self, expr, environment, isTupleSort)

        #  var focus = {
        #      environment: environment,
        #      input: input
        #  }
        #  // the `focus` is passed in as the `this` for the invoked function
        #  result = /* await */ fn.sort.apply(focus, [lhs, comparator])

        result = Functions.sort(lhs, comparator)
        return result

    class ComparatorAnonymousInnerClass(java.util.Comparator):


        def __init__(self, outerInstance, expr, environment, isTupleSort):
            self._outerInstance = outerInstance
            self._expr = expr
            self._environment = environment
            self._isTupleSort = isTupleSort


        def compare(self, a, b):

            # expr.terms is an array of order-by in priority order
            comp = 0
            index = 0
            while comp == 0 and index < len(self._expr.terms):
                term = self._expr.terms[index]
                #evaluate the sort term in the context of a
                context = a
                env = self._environment
                if self._isTupleSort:
                    context = (a)["@"]
                    env = outerInstance.createFrameFromTuple(self._environment, a)
                aa = outerInstance.evaluate(term.expression, context, env)

                #evaluate the sort term in the context of b
                context = b
                env = self._environment
                if self._isTupleSort:
                    context = (b)["@"]
                    env = outerInstance.createFrameFromTuple(self._environment, b)
                bb = outerInstance.evaluate(term.expression, context, env)

                # type checks
                #  var atype = typeof aa
                #  var btype = typeof bb
                # undefined should be last in sort order
                if aa is None:
                    # swap them, unless btype is also undefined
                    comp = 0 if (bb is None) else 1
                    index += 1
                    continue
                if bb is None:
                    comp = -1
                    index += 1
                    continue

                # if aa or bb are not string or numeric values, then throw an error
                if not(isinstance(aa, Number) or isinstance(aa, String)) or not(isinstance(bb, Number) or isinstance(bb, String)):
                    raise JException("T2008", self._expr.position, aa, bb)

                #if aa and bb are not of the same type
                sameType = False
                if isinstance(aa, Number) and isinstance(bb, Number):
                    sameType = True
                elif type(aa).isAssignableFrom(type(bb)) or type(bb).isAssignableFrom(type(aa)):
                    sameType = True

                if not sameType:
                    raise JException("T2007", self._expr.position, aa, bb)
                if aa is bb:
                    # both the same - move on to next term
                    index += 1
                    continue
                elif (aa).compareTo(bb) < 0:
                    comp = -1
                else:
                    comp = 1
                if term.descending == True:
                    comp = -comp
                index += 1
            # only swap a & b if comp equals 1
            # return comp == 1
            return comp

    #     *
    #      * create a transformer function
    #      * @param {Object} expr - AST for operator
    #      * @param {Object} input - Input data to evaluate against
    #      * @param {Object} environment - Environment
    #      * @returns {*} tranformer function
    #      
    def evaluateTransformExpression(self, expr, input, environment):
        # create a Object to implement the transform definition
# JAVA TO PYTHON CONVERTER TASK: Only expression lambdas are converted by Java to Python Converter:
        #        JFunctionCallable transformer = (_input, args) ->
        #        {
        #        // /* async */ Object (obj) { // signature <(oa):o>
        #
        #            var obj = ((List)args).get(0)
        #
        #            // undefined inputs always return undefined
        #            if(obj == null)
        #            {
        #                return null
        #            }
        #
        #            // this Object returns a copy of obj with changes specified by the pattern/operation
        #            Object result = Functions.functionClone(obj)
        #
        #            var _matches = evaluate(expr.pattern, result, environment)
        #            if(_matches != null)
        #            {
        #                if(!(_matches instanceof List))
        #                {
        #                    _matches = new ArrayList<>(List.of(_matches))
        #                }
        #                List matches = (List)_matches
        #                for(var ii = 0; ii < matches.size(); ii++)
        #                {
        #                    var @match = matches.get(ii)
        #                    // evaluate the update value for each match
        #                    var update = evaluate(expr.update, @match, environment)
        #                    // update must be an object
        #                    //var updateType = typeof update
        #                    //if(updateType != null) 
        #
        #                    if (update != null)
        #                    {
        #                    if(!(update instanceof Map))
        #                    {
        #                            // throw type error
        #                            throw new JException("T2011", expr.update.position, update)
        #                        }
        #                        // merge the update
        #                        for(var prop : ((Map)update).keySet())
        #                        {
        #                            ((Map)@match).put(prop, ((Map)update).get(prop))
        #                        }
        #                    }
        #
        #                    // delete, if specified, must be an array of strings (or single string)
        #                    if(expr.delete != null)
        #                    {
        #                        var deletions = evaluate(expr.delete, @match, environment)
        #                        if(deletions != null)
        #                        {
        #                            var val = deletions
        #                            if (!(deletions instanceof List))
        #                            {
        #                                deletions = new ArrayList<>(List.of(deletions))
        #                            }
        #                            if (!Utils.isArrayOfStrings(deletions))
        #                            {
        #                                // throw type error
        #                                throw new JException("T2012", expr.delete.position, val)
        #                            }
        #                            List _deletions = (List)deletions
        #                            for (var jj = 0; jj < _deletions.size(); jj++)
        #                            {
        #                                if(@match instanceof Map)
        #                                {
        #                                ((Map)@match).remove(_deletions.get(jj))
        #                                    //delete match[deletions[jj]]
        #                                }
        #                            }
        #                        }
        #                    }
        #                }
        #            }
        #
        #            return result
        #        }

        return JFunction(transformer, "<(oa):o>")

    chainAST = None # = new Parser().parse("function($f, $g) { function($x){ $g($f($x)) } }");

    @staticmethod
    def chainAST():
        if com.dashjoin.jsonata.Jsonata.chainAST is None:
            # only create on demand
            com.dashjoin.jsonata.Jsonata.chainAST = (Parser()).parse("function($f, $g) { function($x){ $g($f($x)) } }")
        return com.dashjoin.jsonata.Jsonata.chainAST

    #     *
    #      * Apply the Object on the RHS using the sequence on the LHS as the first argument
    #      * @param {Object} expr - JSONata expression
    #      * @param {Object} input - Input data to evaluate against
    #      * @param {Object} environment - Environment
    #      * @returns {*} Evaluated input data
    #      
    # async 
    def evaluateApplyExpression(self, expr, input, environment):
        result = None


        lhs = self.evaluate(expr.lhs, input, environment)

        # Map null to NULL_VALUE before applying to functions
        # TODO: fix more generically!
        if lhs is None:
            lhs = Jsonata.NULL_VALUE

        if expr.rhs.type == "function":
            #Symbol applyTo = new Symbol(); applyTo.context = lhs
            # this is a Object _invocation_; invoke it with lhs expression as the first argument
            result = self.evaluateFunction(expr.rhs, input, environment, lhs)
        else:
            func = self.evaluate(expr.rhs, input, environment)

            if not self.isFunctionLike(func) and not self.isFunctionLike(lhs):
                raise JException("T2006", expr.position, func)

            if self.isFunctionLike(lhs):
                # this is Object chaining (func1 ~> func2)
                # λ($f, $g) { λ($x){ $g($f($x)) } }
                chain = self.evaluate(com.dashjoin.jsonata.Jsonata.chainAST(), None, environment)
                args = []
                args.append(lhs)
                args.append(func) # == [lhs, func]
                result = self.apply(chain, args, None, environment)
            else:
                args = []
                args.append(lhs) # == [lhs]
                result = self.apply(func, args, None, environment)


        return result

    def isFunctionLike(self, o):
        return Utils.isFunction(o) or Functions.isLambda(o) or (isinstance(o, java.util.regex.Pattern))

    CURRENT = ThreadLocal()

    #    *
    #     * Returns a per thread instance of this parsed expression.
    #     * 
    #     * @return
    #     
    def getPerThreadInstance(self):
        threadInst = com.dashjoin.jsonata.Jsonata.CURRENT.get()
        # Fast path
        if threadInst is not None:
            return threadInst

# JAVA TO PYTHON CONVERTER TASK: Synchronized blocks are not converted by Java to Python Converter:
        synchronized(self)
            threadInst = com.dashjoin.jsonata.Jsonata.CURRENT.get()
            if threadInst is None:
                threadInst = Jsonata(self)
                com.dashjoin.jsonata.Jsonata.CURRENT.set(threadInst)
            return threadInst

    #     *
    #      * Evaluate Object against input data
    #      * @param {Object} expr - JSONata expression
    #      * @param {Object} input - Input data to evaluate against
    #      * @param {Object} environment - Environment
    #      * @returns {*} Evaluated input data
    #      
    # async 
    def evaluateFunction(self, expr, input, environment, applytoContext):
        result = None

        # this.current is set by getPerThreadInstance() at this point

        # create the procedure
        # can"t assume that expr.procedure is a lambda type directly
        # could be an expression that evaluates to a Object (e.g. variable reference, parens expr etc.
        # evaluate it generically first, then check that it is a function.  Throw error if not.
        proc = self.evaluate(expr.procedure, input, environment)

        if proc is None and (expr).procedure.type is "path" and environment.lookup(str(expr.procedure.steps[0].value)) is not None:
            # help the user out here if they simply forgot the leading $
            raise JException("T1005", expr.position, (expr).procedure.steps[0].value)

        evaluatedArgs = []

        if applytoContext is not None:
            evaluatedArgs.append(applytoContext)
        # eager evaluation - evaluate the arguments
        for jj, _ in enumerate(expr.arguments):
            arg = self.evaluate(expr.arguments[jj], input, environment)
            if Utils.isFunction(arg) or Functions.isLambda(arg):
                # wrap this in a closure
                # Java: not required, already a JFunction
                #  const closure = /* async */ Object (...params) {
                #      // invoke func
                #      return /* await */ apply(arg, params, null, environment)
                #  }
                #  closure.arity = getFunctionArity(arg)

                # JFunctionCallable fc = (ctx,params) ->
                #     apply(arg, params, null, environment)

                # JFunction cl = new JFunction(fc, "<o:o>")

                #Object cl = apply(arg, params, null, environment)
                evaluatedArgs.append(arg)
            else:
                evaluatedArgs.append(arg)
        # apply the procedure
        procName = expr.procedure.steps[0].value if expr.procedure.type is "path" else expr.procedure.value

        # Error if proc is null
        if proc is None:
            raise JException("T1006", expr.position, procName)

        try:
            if isinstance(proc, com.dashjoin.jsonata.Parser.Symbol):
                (proc).token = procName
                (proc).position = expr.position
            result = self.apply(proc, evaluatedArgs, input, environment)
        except JException as jex:
            if jex.location < 0:
                # add the position field to the error
                jex.location = expr.position
            if jex.current is None:
                # and the Object identifier
                jex.current = expr.token
            raise jex
        except Exception as err:
            if not(isinstance(err, RuntimeException)):
                raise RuntimeException(err)
            #err.printStackTrace()
            raise err
            # new JException(err, "Error calling function "+procName, expr.position, null, null); //err
        return result

    #     *
    #      * Apply procedure or function
    #      * @param {Object} proc - Procedure
    #      * @param {Array} args - Arguments
    #      * @param {Object} input - input
    #      * @param {Object} environment - environment
    #      * @returns {*} Result of procedure
    #      
    # async 
    def apply(self, proc, args, input, environment):
        result = self.applyInner(proc, args, input, environment)
        while Functions.isLambda(result) and (result).thunk == True:
            # trampoline loop - this gets invoked as a result of tail-call optimization
            # the Object returned a tail-call thunk
            # unpack it, evaluate its arguments, and apply the tail call
            next = self.evaluate((result).body.procedure, (result).input, (result).environment)
            if (result).body.procedure.type is "variable":
                if isinstance(next, com.dashjoin.jsonata.Parser.Symbol): # Java: not if JFunction
                    (next).token = (result).body.procedure.value
            if isinstance(next, com.dashjoin.jsonata.Parser.Symbol): # Java: not if JFunction
                (next).position = (result).body.procedure.position
            evaluatedArgs = []
            for ii, _ in enumerate((result).body.arguments):
                evaluatedArgs.append(self.evaluate((result).body.arguments[ii], (result).input, (result).environment))

            result = self.applyInner(next, evaluatedArgs, input, environment)
        return result

    #     *
    #      * Apply procedure or function
    #      * @param {Object} proc - Procedure
    #      * @param {Array} args - Arguments
    #      * @param {Object} input - input
    #      * @param {Object} environment - environment
    #      * @returns {*} Result of procedure
    #      
    # async 
    def applyInner(self, proc, args, input, environment):
        result = None
        try:
            validatedArgs = args
            if proc is not None:
                validatedArgs = self.validateArguments(proc, args, input)

            if Functions.isLambda(proc):
                result = self.applyProcedure(proc, validatedArgs) # FIXME: need in Java??? else if (proc && proc._jsonata_Object == true) {
            #                 var focus = {
            #                     environment: environment,
            #                     input: input
            #                 }
            #                 // the `focus` is passed in as the `this` for the invoked function
            #                 result = proc.implementation.apply(focus, validatedArgs)
            #                 // `proc.implementation` might be a generator function
            #                 // and `result` might be a generator - if so, yield
            #                 if (isIterable(result)) {
            #                     result = result.next().value
            #                 }
            #                 if (isPromise(result)) {
            #                     result = /await/ result
            #                 } 
            #             } 
            elif isinstance(proc, JFunction):
                # typically these are functions that are returned by the invocation of plugin functions
                # the `input` is being passed in as the `this` for the invoked function
                # this is so that functions that return objects containing functions can chain
                # e.g. /* await */ (/* await */ $func())

                # handling special case of Javascript:
                # when calling a function with fn.apply(ctx, args) and args = [undefined]
                # Javascript will convert to undefined (without array)
                if isinstance(validatedArgs, java.util.List) and len((validatedArgs)) == 1 and (validatedArgs)[0] is None:
                    #validatedArgs = null
                    pass

                result = (proc).call(input, validatedArgs)
                #  if (isPromise(result)) {
                #      result = /* await */ result
                #  }
            elif isinstance(proc, JLambda):
                # System.err.println("Lambda "+proc)
                _args = validatedArgs
                if isinstance(proc, Fn0):
                    result = (proc).get()
                elif isinstance(proc, Fn1):
                    result = (proc).apply(None if len(_args) <= 0 else _args[0])
                elif isinstance(proc, Fn2):
                    result = (proc).apply(None if len(_args) <= 0 else _args[0],None if len(_args) <= 1 else _args[1])
            elif isinstance(proc, java.util.regex.Pattern):
                _res = []
                for s in validatedArgs:
                    #System.err.println("PAT "+proc+" input "+s)
                    if (proc).matcher(s).find():
                        #System.err.println("MATCH")
                        _res.append(s)
                result = _res
            else:
                print("Proc not found " + proc)
                raise JException("T1006", 0)
        except JException as err:
            #  if(proc) {
            #      if (typeof err.token == "undefined" && typeof proc.token !== "undefined") {
            #          err.token = proc.token
            #      }
            #      err.position = proc.position
            #  }
            raise err
        return result

    #     *
    #      * Evaluate lambda against input data
    #      * @param {Object} expr - JSONata expression
    #      * @param {Object} input - Input data to evaluate against
    #      * @param {Object} environment - Environment
    #      * @returns {{lambda: boolean, input: *, environment: *, arguments: *, body: *}} Evaluated input data
    #      
    def evaluateLambda(self, expr, input, environment):
        # make a Object (closure)
        procedure = com.dashjoin.jsonata.Parser.Symbol(self.parser)

        procedure._jsonata_lambda = True
        procedure.input = input
        procedure.environment = environment
        procedure.arguments = expr.arguments
        procedure.signature = expr.signature
        procedure.body = expr.body

        if expr.thunk == True:
            procedure.thunk = True

        # procedure.apply = /* async */ function(self, args) {
        #     return /* await */ apply(procedure, args, input, !!self ? self.environment : environment)
        # }
        return procedure

    #     *
    #      * Evaluate partial application
    #      * @param {Object} expr - JSONata expression
    #      * @param {Object} input - Input data to evaluate against
    #      * @param {Object} environment - Environment
    #      * @returns {*} Evaluated input data
    #      
    # async 
    def evaluatePartialApplication(self, expr, input, environment):
        # partially apply a function
        result = None
        # evaluate the arguments
        evaluatedArgs = []
        for ii, _ in enumerate(expr.arguments):
            arg = expr.arguments[ii]
            if arg.type is "operator" and (arg.value is "?"):
                evaluatedArgs.append(arg)
            else:
                evaluatedArgs.append(self.evaluate(arg, input, environment))
        # lookup the procedure
        proc = self.evaluate(expr.procedure, input, environment)
        if proc is not None and expr.procedure.type == "path" and environment.lookup(str(expr.procedure.steps[0].value)) is not None:
            # help the user out here if they simply forgot the leading $
            raise JException("T1007", expr.position, expr.procedure.steps[0].value)
        if Functions.isLambda(proc):
            result = self.partialApplyProcedure(proc, evaluatedArgs)
        elif Utils.isFunction(proc):
            result = self.partialApplyNativeFunction(proc, evaluatedArgs)
            #  } else if (typeof proc === "function") {
            #      result = partialApplyNativeFunction(proc, evaluatedArgs)
        else:
            raise JException("T1008", expr.position,expr.procedure.steps[0].value if expr.procedure.type == "path" else expr.procedure.value)
        return result

    #     *
    #      * Validate the arguments against the signature validator (if it exists)
    #      * @param {Function} signature - validator function
    #      * @param {Array} args - Object arguments
    #      * @param {*} context - context value
    #      * @returns {Array} - validated arguments
    #      
    def validateArguments(self, signature, args, context):
        validatedArgs = args
        if Utils.isFunction(signature):
            validatedArgs = (signature).validate(args, context)
        elif Functions.isLambda(signature):
            sig = ((signature).signature)
            if sig is not None:
                validatedArgs = sig.validate(args, context)
        return validatedArgs

    #     *
    #      * Apply procedure
    #      * @param {Object} proc - Procedure
    #      * @param {Array} args - Arguments
    #      * @returns {*} Result of procedure
    #      
    # async 
    def applyProcedure(self, _proc, _args):
        args = _args
        proc = _proc
        result = None
        env = self.createFrame(proc.environment)
        for i, _ in enumerate(proc.arguments):
            if i >= len(args):
                break
            env.bind("" + proc.arguments[i].value, args[i])
        if isinstance(proc.body, com.dashjoin.jsonata.Parser.Symbol):
            result = self.evaluate(proc.body, proc.input, env)
        else:
            raise Error("Cannot execute procedure: " + proc + " " + proc.body)
        #  if (typeof proc.body === "function") {
        #      // this is a lambda that wraps a native Object - generated by partially evaluating a native
        #      result = /* await */ applyNativeFunction(proc.body, env)
        return result

    #     *
    #      * Partially apply procedure
    #      * @param {Object} proc - Procedure
    #      * @param {Array} args - Arguments
    #      * @returns {{lambda: boolean, input: *, environment: {bind, lookup}, arguments: Array, body: *}} Result of partially applied procedure
    #      
    def partialApplyProcedure(self, proc, args):
        # create a closure, bind the supplied parameters and return a Object that takes the remaining (?) parameters
        # Note Uli: if no env, bind to default env so the native functions can be found
        env = self.createFrame(proc.environment if proc.environment is not None else self.environment)
        unboundArgs = []
        index = 0
        for param in proc.arguments:
            #         proc.arguments.forEach(Object (param, index) {
            arg = args[index] if index < len(args) else None
            if (arg is None) or (isinstance(arg, com.dashjoin.jsonata.Parser.Symbol) and ("operator" == (arg).type and "?" == (arg).value)):
                unboundArgs.append(param)
            else:
                env.bind(str(param.value), arg)
            index += 1
        procedure = com.dashjoin.jsonata.Parser.Symbol(self.parser)
        procedure._jsonata_lambda = True
        procedure.input = proc.input
        procedure.environment = env
        procedure.arguments = unboundArgs
        procedure.body = proc.body

        return procedure

    #     *
    #      * Partially apply native function
    #      * @param {Function} native - Native function
    #      * @param {Array} args - Arguments
    #      * @returns {{lambda: boolean, input: *, environment: {bind, lookup}, arguments: Array, body: *}} Result of partially applying native function
    #      
    def partialApplyNativeFunction(self, _native, args):
        # create a lambda Object that wraps and invokes the native function
        # get the list of declared arguments from the native function
        # this has to be picked out from the toString() value


        #var body = "function($a,$c) { $substring($a,0,$c) }"

        sigArgs = []
        partArgs = []
        i = 0
        while i < _native.getNumberOfArgs():
            argName = "$" + chr(('a' + i))
            sigArgs.append(argName)
            if i >= len(args) or args[i] is None:
                partArgs.append(argName)
            else:
                partArgs.append(args[i])
            i += 1

        body = "function(" + String.join(", ", sigArgs) + "){"
        body += "$" + _native.functionName + "(" + String.join(", ", sigArgs) + ") }"

        if self.parser.dbg:
            print("partial trampoline = " + body)

        #  var sigArgs = getNativeFunctionArguments(_native)
        #  sigArgs = sigArgs.stream().map(sigArg -> {
        #      return "$" + sigArg
        #  }).toList()
        #  var body = "function(" + String.join(", ", sigArgs) + "){ _ }"

        bodyAST = self.parser.parse(body)
        #bodyAST.body = _native

        partial = self.partialApplyProcedure(bodyAST, args)
        return partial

    #     *
    #      * Apply native function
    #      * @param {Object} proc - Procedure
    #      * @param {Object} env - Environment
    #      * @returns {*} Result of applying native function
    #      
    # async 
    def applyNativeFunction(self, proc, env):
        # Not called in Java - JFunction call directly calls native function
        return None

    #     *
    #      * Get native Object arguments
    #      * @param {Function} func - Function
    #      * @returns {*|Array} Native Object arguments
    #      
    def getNativeFunctionArguments(self, func):
        # Not called in Java
        return None

    #     *
    #      * Creates a Object definition
    #      * @param {Function} func - Object implementation in Javascript
    #      * @param {string} signature - JSONata Object signature definition
    #      * @returns {{implementation: *, signature: *}} Object definition
    #      
    @staticmethod
# JAVA TO PYTHON CONVERTER TASK: Python does not allow method overloads:
    def defineFunction(func, signature):
        return com.dashjoin.jsonata.Jsonata.defineFunction(func, signature, func)
    @staticmethod
# JAVA TO PYTHON CONVERTER TASK: Python does not allow method overloads:
    def defineFunction(func, signature, funcImplMethod):
        fn = JFunction(func, signature, Functions.class, None, funcImplMethod)
        com.dashjoin.jsonata.Jsonata.staticFrame.bind(func, fn)
        return fn

    @staticmethod
# JAVA TO PYTHON CONVERTER TASK: Python does not allow method overloads:
    def function(name, signature, clazz, instance, methodName):
        return JFunction(name, signature, clazz, instance, methodName)

    @staticmethod
# JAVA TO PYTHON CONVERTER TASK: Python does not allow method overloads:
    def function(name, func, signature):
        return JFunction(func.getJFunctionCallable(), signature)
    @staticmethod
# JAVA TO PYTHON CONVERTER TASK: Python does not allow method overloads:
    def function(name, func, signature):
        return JFunction(func.getJFunctionCallable(), signature)
    @staticmethod
# JAVA TO PYTHON CONVERTER TASK: Python does not allow method overloads:
    def function(name, func, signature):
        return JFunction(func.getJFunctionCallable(), signature)
    @staticmethod
# JAVA TO PYTHON CONVERTER TASK: Python does not allow method overloads:
    def function(name, func, signature):
        return JFunction(func.getJFunctionCallable(), signature)
    @staticmethod
# JAVA TO PYTHON CONVERTER TASK: Python does not allow method overloads:
    def function(name, func, signature):
        return JFunction(func.getJFunctionCallable(), signature)
    @staticmethod
# JAVA TO PYTHON CONVERTER TASK: Python does not allow method overloads:
    def function(name, func, signature):
        return JFunction(func.getJFunctionCallable(), signature)
    @staticmethod
# JAVA TO PYTHON CONVERTER TASK: Python does not allow method overloads:
    def function(name, func, signature):
        return JFunction(func.getJFunctionCallable(), signature)
    @staticmethod
# JAVA TO PYTHON CONVERTER TASK: Python does not allow method overloads:
    def function(name, func, signature):
        return JFunction(func.getJFunctionCallable(), signature)
    @staticmethod
# JAVA TO PYTHON CONVERTER TASK: Python does not allow method overloads:
    def function(name, func, signature):
        return JFunction(func.getJFunctionCallable(), signature)
    @staticmethod
# JAVA TO PYTHON CONVERTER TASK: Python does not allow method overloads:
    def function(name, func, signature):
        return JFunction(func.getJFunctionCallable(), signature)

    #     *
    #      * parses and evaluates the supplied expression
    #      * @param {string} expr - expression to evaluate
    #      * @returns {*} - result of evaluating the expression
    #      
    # async  
    #Object functionEval(String expr, Object focus) {
    # moved to Functions !
    #}

    #     *
    #      * Clones an object
    #      * @param {Object} arg - object to clone (deep copy)
    #      * @returns {*} - the cloned object
    #      
    #Object functionClone(Object arg) {
    # moved to Functions !
    #}

    #     *
    #      * Create frame
    #      * @param {Object} enclosingEnvironment - Enclosing environment
    #      * @returns {{bind: bind, lookup: lookup}} Created frame
    #      
# JAVA TO PYTHON CONVERTER TASK: Python does not allow method overloads:
    def createFrame(self):
        return self.createFrame(None)
# JAVA TO PYTHON CONVERTER TASK: Python does not allow method overloads:
    def createFrame(self, enclosingEnvironment):
        return Frame(enclosingEnvironment)

        # The following logic is in class Frame:
        #  var bindings = {}
        #  return {
        #      bind: Object (name, value) {
        #          bindings[name] = value
        #      },
        #      lookup: Object (name) {
        #          var value
        #          if(bindings.hasOwnProperty(name)) {
        #              value = bindings[name]
        #          } else if (enclosingEnvironment) {
        #              value = enclosingEnvironment.lookup(name)
        #          }
        #          return value
        #      },
        #      timestamp: enclosingEnvironment ? enclosingEnvironment.timestamp : null,
        #      async: enclosingEnvironment ? enclosingEnvironment./* async */ : false,
        #      isParallelCall: enclosingEnvironment ? enclosingEnvironment.isParallelCall : false,
        #      global: enclosingEnvironment ? enclosingEnvironment.global : {
        #          ancestry: [ null ]
        #      }
        #  }

    class JLambda:
        pass

    class FnVarArgs(JLambda, java.util.function.Function):
        def getJFunctionCallable(self):
            return lambda outerInstance.input, args : apply(args)
    class Fn0(JLambda, java.util.function.Supplier):
        def getJFunctionCallable(self):
            return lambda outerInstance.input, args : get()
    class Fn1(JLambda, java.util.function.Function):
        def getJFunctionCallable(self):
            return lambda outerInstance.input, args : apply(args.get(0))
    class Fn2(JLambda, java.util.function.BiFunction):
        def getJFunctionCallable(self):
            return lambda outerInstance.input, args : apply(args.get(0), args.get(1))
    class Fn3(JLambda):
        def apply(self, a, b, c):
            pass
        def getJFunctionCallable(self):
            return lambda outerInstance.input, args : self.apply(args.get(0), args.get(1), args.get(2))
    class Fn4(JLambda):
        def apply(self, a, b, c, d):
            pass
        def getJFunctionCallable(self):
            return lambda outerInstance.input, args : self.apply(args.get(0), args.get(1), args.get(2), args.get(3))
    class Fn5(JLambda):
        def apply(self, a, b, c, d, e):
            pass
        def getJFunctionCallable(self):
            return lambda outerInstance.input, args : self.apply(args.get(0), args.get(1), args.get(2), args.get(3), args.get(4))
    class Fn6(JLambda):
        def apply(self, a, b, c, d, e, f):
            pass
        def getJFunctionCallable(self):
            return lambda outerInstance.input, args : self.apply(args.get(0), args.get(1), args.get(2), args.get(3), args.get(4), args.get(5))
    class Fn7(JLambda):
        def apply(self, a, b, c, d, e, f, g):
            pass
        def getJFunctionCallable(self):
            return lambda outerInstance.input, args : self.apply(args.get(0), args.get(1), args.get(2), args.get(3), args.get(4), args.get(5), args.get(6))
    class Fn8(JLambda):
        def apply(self, a, b, c, d, e, f, g, h):
            pass
        def getJFunctionCallable(self):
            return lambda outerInstance.input, args : self.apply(args.get(0), args.get(1), args.get(2), args.get(3), args.get(4), args.get(5), args.get(6), args.get(7))

    #    *
    #     * JFunction callable Lambda interface
    #     
    class JFunctionCallable:
# JAVA TO PYTHON CONVERTER WARNING: Method 'throws' clauses are not available in Python:
# ORIGINAL LINE: Object call(Object input, java.util.List args) throws Throwable;
        def call(self, input, args):
            pass

    class JFunctionSignatureValidation:
        def validate(self, args, context):
            pass

    #    *
    #     * JFunction definition class
    #     
    class JFunction(JFunctionCallable, JFunctionSignatureValidation):

        def _initialize_instance_fields(self):
            # instance fields found by Java to Python Converter:
            self.function = None
            self.functionName = None
            self.signature = None
            self.method = None
            self.methodInstance = None


# JAVA TO PYTHON CONVERTER TASK: There is no Python equivalent to multiple constructors:
# ORIGINAL LINE: public JFunction(JFunctionCallable function, String signature)
        def __init__(self, function, signature):
            self._initialize_instance_fields()

            self.function = function
            if signature is not None:
                # use classname as default, gets overwritten once the function is registered
                self.signature = com.dashjoin.jsonata.utils.Signature(signature, type(function).getName())

# JAVA TO PYTHON CONVERTER TASK: There is no Python equivalent to multiple constructors:
# ORIGINAL LINE: public JFunction(String functionName, String signature, Class clz, Object instance, String implMethodName)
        def __init__(self, functionName, signature, clz, instance, implMethodName):
            self._initialize_instance_fields()

            self.functionName = functionName
            self.signature = com.dashjoin.jsonata.utils.Signature(signature, functionName)
            self.method = Functions.getFunction(clz, implMethodName)
            self.methodInstance = instance
            if self.method is None:
                System.err.println("Function not implemented: " + functionName + " impl=" + implMethodName)

        def call(self, input, args):
            try:
                if self.function is not None:
                    return self.function.call(input, args)
                else:
                    return Functions.call(self.methodInstance, self.method, args)
            except JException as e:
                raise e
            except java.lang.reflect.InvocationTargetException as e:
                raise RuntimeException(e.getTargetException())
            except Throwable as e:
                if isinstance(e, RuntimeException):
                    raise (RuntimeException)e
                raise RuntimeException(e)
                #throw new JException(e, "T0410", -1, args, functionName)

        def validate(self, args, context):
            if self.signature is not None:
                return self.signature.validate(args, context)
            else:
                return args

        def getNumberOfArgs(self):
            return self.method.getParameterTypes().length if self.method is not None else 0

    # Function registration
    @staticmethod
    def registerFunctions():
        com.dashjoin.jsonata.Jsonata.defineFunction("sum", "<a<n>:n>")
        com.dashjoin.jsonata.Jsonata.defineFunction("count", "<a:n>")
        com.dashjoin.jsonata.Jsonata.defineFunction("max", "<a<n>:n>")
        com.dashjoin.jsonata.Jsonata.defineFunction("min", "<a<n>:n>")
        com.dashjoin.jsonata.Jsonata.defineFunction("average", "<a<n>:n>")
        com.dashjoin.jsonata.Jsonata.defineFunction("string", "<x-b?:s>")
        com.dashjoin.jsonata.Jsonata.defineFunction("substring", "<s-nn?:s>")
        com.dashjoin.jsonata.Jsonata.defineFunction("substringBefore", "<s-s:s>")
        com.dashjoin.jsonata.Jsonata.defineFunction("substringAfter", "<s-s:s>")
        com.dashjoin.jsonata.Jsonata.defineFunction("lowercase", "<s-:s>")
        com.dashjoin.jsonata.Jsonata.defineFunction("uppercase", "<s-:s>")
        com.dashjoin.jsonata.Jsonata.defineFunction("length", "<s-:n>")
        com.dashjoin.jsonata.Jsonata.defineFunction("trim", "<s-:s>")
        com.dashjoin.jsonata.Jsonata.defineFunction("pad", "<s-ns?:s>")
        com.dashjoin.jsonata.Jsonata.defineFunction("match", "<s-f<s:o>n?:a<o>>")
        com.dashjoin.jsonata.Jsonata.defineFunction("contains", "<s-(sf):b>") # TODO <s-(sf<s:o>):b>
        com.dashjoin.jsonata.Jsonata.defineFunction("replace", "<s-(sf)(sf)n?:s>") # TODO <s-(sf<s:o>)(sf<o:s>)n?:s>
        com.dashjoin.jsonata.Jsonata.defineFunction("split", "<s-(sf)n?:a<s>>") # TODO <s-(sf<s:o>)n?:a<s>>
        com.dashjoin.jsonata.Jsonata.defineFunction("join", "<a<s>s?:s>")
        com.dashjoin.jsonata.Jsonata.defineFunction("formatNumber", "<n-so?:s>")
        com.dashjoin.jsonata.Jsonata.defineFunction("formatBase", "<n-n?:s>")
        com.dashjoin.jsonata.Jsonata.defineFunction("formatInteger", "<n-s:s>")
        com.dashjoin.jsonata.Jsonata.defineFunction("parseInteger", "<s-s:n>")
        com.dashjoin.jsonata.Jsonata.defineFunction("number", "<(nsb)-:n>")
        com.dashjoin.jsonata.Jsonata.defineFunction("floor", "<n-:n>")
        com.dashjoin.jsonata.Jsonata.defineFunction("ceil", "<n-:n>")
        com.dashjoin.jsonata.Jsonata.defineFunction("round", "<n-n?:n>")
        com.dashjoin.jsonata.Jsonata.defineFunction("abs", "<n-:n>")
        com.dashjoin.jsonata.Jsonata.defineFunction("sqrt", "<n-:n>")
        com.dashjoin.jsonata.Jsonata.defineFunction("power", "<n-n:n>")
        com.dashjoin.jsonata.Jsonata.defineFunction("random", "<:n>")
        com.dashjoin.jsonata.Jsonata.defineFunction("boolean", "<x-:b>", "toBoolean")
        com.dashjoin.jsonata.Jsonata.defineFunction("not", "<x-:b>")
        com.dashjoin.jsonata.Jsonata.defineFunction("map", "<af>")
        com.dashjoin.jsonata.Jsonata.defineFunction("zip", "<a+>")
        com.dashjoin.jsonata.Jsonata.defineFunction("filter", "<af>")
        com.dashjoin.jsonata.Jsonata.defineFunction("single", "<af?>")
        com.dashjoin.jsonata.Jsonata.defineFunction("reduce", "<afj?:j>", "foldLeft") # TODO <f<jj:j>a<j>j?:j>
        com.dashjoin.jsonata.Jsonata.defineFunction("sift", "<o-f?:o>")
        com.dashjoin.jsonata.Jsonata.defineFunction("keys", "<x-:a<s>>")
        com.dashjoin.jsonata.Jsonata.defineFunction("lookup", "<x-s:x>")
        com.dashjoin.jsonata.Jsonata.defineFunction("append", "<xx:a>")
        com.dashjoin.jsonata.Jsonata.defineFunction("exists", "<x:b>")
        com.dashjoin.jsonata.Jsonata.defineFunction("spread", "<x-:a<o>>")
        com.dashjoin.jsonata.Jsonata.defineFunction("merge", "<a<o>:o>")
        com.dashjoin.jsonata.Jsonata.defineFunction("reverse", "<a:a>")
        com.dashjoin.jsonata.Jsonata.defineFunction("each", "<o-f:a>")
        com.dashjoin.jsonata.Jsonata.defineFunction("error", "<s?:x>")
        com.dashjoin.jsonata.Jsonata.defineFunction("assert", "<bs?:x>", "assertFn")
        com.dashjoin.jsonata.Jsonata.defineFunction("type", "<x:s>")
        com.dashjoin.jsonata.Jsonata.defineFunction("sort", "<af?:a>")
        com.dashjoin.jsonata.Jsonata.defineFunction("shuffle", "<a:a>")
        com.dashjoin.jsonata.Jsonata.defineFunction("distinct", "<x:x>")
        com.dashjoin.jsonata.Jsonata.defineFunction("base64encode", "<s-:s>")
        com.dashjoin.jsonata.Jsonata.defineFunction("base64decode", "<s-:s>")
        com.dashjoin.jsonata.Jsonata.defineFunction("encodeUrlComponent", "<s-:s>")
        com.dashjoin.jsonata.Jsonata.defineFunction("encodeUrl", "<s-:s>")
        com.dashjoin.jsonata.Jsonata.defineFunction("decodeUrlComponent", "<s-:s>")
        com.dashjoin.jsonata.Jsonata.defineFunction("decodeUrl", "<s-:s>")
        com.dashjoin.jsonata.Jsonata.defineFunction("eval", "<sx?:x>", "functionEval")
        com.dashjoin.jsonata.Jsonata.defineFunction("toMillis", "<s-s?:n>", "dateTimeToMillis")
        com.dashjoin.jsonata.Jsonata.defineFunction("fromMillis", "<n-s?s?:s>", "dateTimeFromMillis")
        com.dashjoin.jsonata.Jsonata.defineFunction("clone", "<(oa)-:o>", "functionClone")

        com.dashjoin.jsonata.Jsonata.defineFunction("now", "<s?s?:s>")
        com.dashjoin.jsonata.Jsonata.defineFunction("millis", "<:n>")

        #  environment.bind("now", defineFunction(function(picture, timezone) {
        #      return datetime.fromMillis(timestamp.getTime(), picture, timezone)
        #  }, "<s?s?:s>"))
        #  environment.bind("millis", defineFunction(function() {
        #      return timestamp.getTime()
        #  }, "<:n>"))


    #     *
    #      * Error codes
    #      *
    #      * Sxxxx    - Static errors (compile time)
    #      * Txxxx    - Type errors
    #      * Dxxxx    - Dynamic errors (evaluate time)
    #      *  01xx    - tokenizer
    #      *  02xx    - parser
    #      *  03xx    - regex parser
    #      *  04xx    - Object signature parser/evaluator
    #      *  10xx    - evaluator
    #      *  20xx    - operators
    #      *  3xxx    - functions (blocks of 10 for each function)
    #      
    errorCodes = HashMapAnonymousInnerClass()

    class HashMapAnonymousInnerClass(dict):
        def __init__(self):

            self.put("S0101", "String literal must be terminated by a matching quote")
            self.put("S0102", "Number out of range: {{token}}")
            self.put("S0103", "Unsupported escape sequence: \\{{token}}")
            self.put("S0104", "The escape sequence \\u must be followed by 4 hex digits")
            self.put("S0105", "Quoted property name must be terminated with a backquote (`)")
            self.put("S0106", "Comment has no closing tag")
            self.put("S0201", "Syntax error: {{token}}")
            self.put("S0202", "Expected {{value}}, got {{token}}")
            self.put("S0203", "Expected {{value}} before end of expression")
            self.put("S0204", "Unknown operator: {{token}}")
            self.put("S0205", "Unexpected token: {{token}}")
            self.put("S0206", "Unknown expression type: {{token}}")
            self.put("S0207", "Unexpected end of expression")
            self.put("S0208", "Parameter {{value}} of Object definition must be a variable name (start with $)")
            self.put("S0209", "A predicate cannot follow a grouping expression in a step")
            self.put("S0210", "Each step can only have one grouping expression")
            self.put("S0211", "The symbol {{token}} cannot be used as a unary operator")
            self.put("S0212", "The left side of := must be a variable name (start with $)")
            self.put("S0213", "The literal value {{value}} cannot be used as a step within a path expression")
            self.put("S0214", "The right side of {{token}} must be a variable name (start with $)")
            self.put("S0215", "A context variable binding must precede any predicates on a step")
            self.put("S0216", "A context variable binding must precede the \"order-by\" clause on a step")
            self.put("S0217", "The object representing the \"parent\" cannot be derived from this expression")
            self.put("S0301", "Empty regular expressions are not allowed")
            self.put("S0302", "No terminating / in regular expression")
            self.put("S0402", "Choice groups containing parameterized types are not supported")
            self.put("S0401", "Type parameters can only be applied to functions and arrays")
            self.put("S0500", "Attempted to evaluate an expression containing syntax error(s)")
            self.put("T0410", "Argument {{index}} of Object {{token}} does not match Object signature")
            self.put("T0411", "Context value is not a compatible type with argument {{index}} of Object {{token}}")
            self.put("T0412", "Argument {{index}} of Object {{token}} must be an array of {{type}}")
            self.put("D1001", "Number out of range: {{value}}")
            self.put("D1002", "Cannot negate a non-numeric value: {{value}}")
            self.put("T1003", "Key in object structure must evaluate to a string; got: {{value}}")
            self.put("D1004", "Regular expression matches zero length string")
            self.put("T1005", "Attempted to invoke a non-function. Did you mean ${{{token}}}?")
            self.put("T1006", "Attempted to invoke a non-function")
            self.put("T1007", "Attempted to partially apply a non-function. Did you mean ${{{token}}}?")
            self.put("T1008", "Attempted to partially apply a non-function")
            self.put("D1009", "Multiple key definitions evaluate to same key: {{value}}")
            self.put("T1010", "The matcher Object argument passed to Object {{token}} does not return the correct object structure")
            self.put("T2001", "The left side of the {{token}} operator must evaluate to a number")
            self.put("T2002", "The right side of the {{token}} operator must evaluate to a number")
            self.put("T2003", "The left side of the range operator (..) must evaluate to an integer")
            self.put("T2004", "The right side of the range operator (..) must evaluate to an integer")
            self.put("D2005", "The left side of := must be a variable name (start with $)") # defunct - replaced by S0212 parser error
            self.put("T2006", "The right side of the Object application operator ~> must be a function")
            self.put("T2007", "Type mismatch when comparing values {{value}} and {{value2}} in order-by clause")
            self.put("T2008", "The expressions within an order-by clause must evaluate to numeric or string values")
            self.put("T2009", "The values {{value}} and {{value2}} either side of operator {{token}} must be of the same data type")
            self.put("T2010", "The expressions either side of operator {{token}} must evaluate to numeric or string values")
            self.put("T2011", "The insert/update clause of the transform expression must evaluate to an object: {{value}}")
            self.put("T2012", "The delete clause of the transform expression must evaluate to a string or array of strings: {{value}}")
            self.put("T2013", "The transform expression clones the input object using the $clone() function.  This has been overridden in the current scope by a non-function.")
            self.put("D2014", "The size of the sequence allocated by the range operator (..) must not exceed 1e6.  Attempted to allocate {{value}}.")
            self.put("D3001", "Attempting to invoke string Object on Infinity or NaN")
            self.put("D3010", "Second argument of replace Object cannot be an empty string")
            self.put("D3011", "Fourth argument of replace Object must evaluate to a positive number")
            self.put("D3012", "Attempted to replace a matched string with a non-string value")
            self.put("D3020", "Third argument of split Object must evaluate to a positive number")
            self.put("D3030", "Unable to cast value to a number: {{value}}")
            self.put("D3040", "Third argument of match Object must evaluate to a positive number")
            self.put("D3050", "The second argument of reduce Object must be a Object with at least two arguments")
            self.put("D3060", "The sqrt Object cannot be applied to a negative number: {{value}}")
            self.put("D3061", "The power Object has resulted in a value that cannot be represented as a JSON number: base={{value}}, exponent={{exp}}")
            self.put("D3070", "The single argument form of the sort Object can only be applied to an array of strings or an array of numbers.  Use the second argument to specify a comparison function")
            self.put("D3080", "The picture string must only contain a maximum of two sub-pictures")
            self.put("D3081", "The sub-picture must not contain more than one instance of the \"decimal-separator\" character")
            self.put("D3082", "The sub-picture must not contain more than one instance of the \"percent\" character")
            self.put("D3083", "The sub-picture must not contain more than one instance of the \"per-mille\" character")
            self.put("D3084", "The sub-picture must not contain both a \"percent\" and a \"per-mille\" character")
            self.put("D3085", "The mantissa part of a sub-picture must contain at least one character that is either an \"optional digit character\" or a member of the \"decimal digit family\"")
            self.put("D3086", "The sub-picture must not contain a passive character that is preceded by an active character and that is followed by another active character")
            self.put("D3087", "The sub-picture must not contain a \"grouping-separator\" character that appears adjacent to a \"decimal-separator\" character")
            self.put("D3088", "The sub-picture must not contain a \"grouping-separator\" at the end of the integer part")
            self.put("D3089", "The sub-picture must not contain two adjacent instances of the \"grouping-separator\" character")
            self.put("D3090", "The integer part of the sub-picture must not contain a member of the \"decimal digit family\" that is followed by an instance of the \"optional digit character\"")
            self.put("D3091", "The fractional part of the sub-picture must not contain an instance of the \"optional digit character\" that is followed by a member of the \"decimal digit family\"")
            self.put("D3092", "A sub-picture that contains a \"percent\" or \"per-mille\" character must not contain a character treated as an \"exponent-separator\"")
            self.put("D3093", "The exponent part of the sub-picture must comprise only of one or more characters that are members of the \"decimal digit family\"")
            self.put("D3100", "The radix of the formatBase Object must be between 2 and 36.  It was given {{value}}")
            self.put("D3110", "The argument of the toMillis Object must be an ISO 8601 formatted timestamp. Given {{value}}")
            self.put("D3120", "Syntax error in expression passed to Object eval: {{value}}")
            self.put("D3121", "Dynamic error evaluating the expression passed to Object eval: {{value}}")
            self.put("D3130", "Formatting or parsing an integer as a sequence starting with {{value}} is not supported by this implementation")
            self.put("D3131", "In a decimal digit pattern, all digits must be from the same decimal group")
            self.put("D3132", "Unknown component specifier {{value}} in date/time picture string")
            self.put("D3133", "The \"name\" modifier can only be applied to months and days in the date/time picture string, not {{value}}")
            self.put("D3134", "The timezone integer format specifier cannot have more than four digits")
            self.put("D3135", "No matching closing bracket \"]\" in date/time picture string")
            self.put("D3136", "The date/time picture string is missing specifiers required to parse the timestamp")
            self.put("D3137", "{{{message}}}")
            self.put("D3138", "The $single() Object expected exactly 1 matching result.  Instead it matched more.")
            self.put("D3139", "The $single() Object expected exactly 1 matching result.  Instead it matched 0.")
            self.put("D3140", "Malformed URL passed to ${{{functionName}}}(): {{value}}")
            self.put("D3141", "{{{message}}}")


    #     *
    #      * lookup a message template from the catalog and substitute the inserts.
    #      * Populates `err.message` with the substituted message. Leaves `err.message`
    #      * untouched if code lookup fails.
    #      * @param {string} err - error code to lookup
    #      * @returns {undefined} - `err` is modified in place
    #      
    def populateMessage(self, err):
        #  var template = errorCodes[err.code]
        #  if(typeof template !== "undefined") {
        #      // if there are any handlebars, replace them with the field references
        #      // triple braces - replace with value
        #      // double braces - replace with json stringified value
        #      var message = template.replace(/\{\{\{([^}]+)}}}/g, function() {
        #          return err[arguments[1]]
        #      })
        #      message = message.replace(/\{\{([^}]+)}}/g, function() {
        #          return JSON.stringify(err[arguments[1]])
        #      })
        #      err.message = message
        #  }
        # Otherwise retain the original `err.message`
        return err


    @staticmethod
    def _static_initializer():
        com.dashjoin.jsonata.Jsonata.staticFrame = Frame(None)
        com.dashjoin.jsonata.Jsonata.registerFunctions()

    _static_initializer()

    #     *
    #      * JSONata
    #      * @param {Object} expr - JSONata expression
    #      * @returns Evaluated expression
    #      * @throws JException An exception if an error occured.
    #      
    @staticmethod
    def jsonata(expression):
        return Jsonata(expression)

    #    *
    #     * Internal constructor
    #     * @param expr
    #     
# JAVA TO PYTHON CONVERTER TASK: There is no Python equivalent to multiple constructors:
# ORIGINAL LINE: Jsonata(String expr)
    def __init__(self, expr):
        self._initialize_instance_fields()

        try:
            self.ast = self.parser.parse(expr) #, optionsRecover);
            self.errors = self.ast.errors
            self.ast.errors = None #delete ast.errors;
        except JException as err:
            # insert error message into structure
            #populateMessage(err); // possible side-effects on `err`
            raise err
        self.environment = self.createFrame(com.dashjoin.jsonata.Jsonata.staticFrame)

        self.timestamp = System.currentTimeMillis() # will be overridden on each call to evalute()

        # Note: now and millis are implemented in Functions
        #  environment.bind("now", defineFunction(function(picture, timezone) {
        #      return datetime.fromMillis(timestamp.getTime(), picture, timezone)
        #  }, "<s?s?:s>"))
        #  environment.bind("millis", defineFunction(function() {
        #      return timestamp.getTime()
        #  }, "<:n>"))

        # FIXED: options.RegexEngine not implemented in Java
        #  if(options && options.RegexEngine) {
        #      jsonata.RegexEngine = options.RegexEngine
        #  } else {
        #      jsonata.RegexEngine = RegExp
        #  }

        # Set instance for this thread
        com.dashjoin.jsonata.Jsonata.CURRENT.set(self)

    #    *
    #     * Creates a clone of the given Jsonata instance.
    #     * Package-private copy constructor used to create per thread instances.
    #     * 
    #     * @param other
    #     
# JAVA TO PYTHON CONVERTER TASK: There is no Python equivalent to multiple constructors:
# ORIGINAL LINE: Jsonata(Jsonata other)
    def __init__(self, other):
        self._initialize_instance_fields()

        self.ast = other.ast
        self.environment = other.environment
        self.timestamp = other.timestamp

    #    *
    #     * Flag: validate input objects to comply with JSON types
    #     

    #    *
    #     * Checks whether input validation is active
    #     
    def isValidateInput(self):
        return self.validateInput

    #    *
    #     * Enable or disable input validation
    #     * @param validateInput
    #     
    def setValidateInput(self, validateInput):
        self.validateInput = validateInput

# JAVA TO PYTHON CONVERTER TASK: Python does not allow method overloads:
    def evaluate(self, input):
        return self.evaluate(input,None)

    # async 
# JAVA TO PYTHON CONVERTER TASK: Python does not allow method overloads:
    def evaluate(self, input, bindings):
        # throw if the expression compiled with syntax errors
        if self.errors is not None:
            raise JException("S0500", 0)

        exec_env = None
        if bindings is not None:
            #var exec_env
            # the variable bindings have been passed in - create a frame to hold these
            exec_env = self.createFrame(self.environment)
            for v in bindings.bindings.keys():
                exec_env.bind(v, bindings.lookup(v))
        else:
            exec_env = self.environment
        # put the input document into the environment as the root object
        exec_env.bind("$", input)

        # capture the timestamp and put it in the execution environment
        # the $now() and $millis() functions will return this value - whenever it is called
        self.timestamp = System.currentTimeMillis()
        #exec_env.timestamp = timestamp

        # if the input is a JSON array, then wrap it in a singleton sequence so it gets treated as a single input
        if (isinstance(input, java.util.List)) and not Utils.isSequence(input):
            input = Utils.createSequence(input)
            (input).outerWrapper = True

        if self.validateInput:
            Functions.validateInput(input)

        it = None
        try:
            it = self.evaluate(self.ast, input, exec_env)
            #  if (typeof callback === "function") {
            #      callback(null, it)
            #  }
            it = Utils.convertNulls(it)
            return it
        except Exception as err:
            # insert error message into structure
            self.populateMessage(err) # possible side-effects on `err`
            raise err

    def assign(self, name, value):
        self.environment.bind(name, value)

# JAVA TO PYTHON CONVERTER TASK: Python does not allow method overloads:
    def registerFunction(self, name, implementation):
        self.environment.bind(name, implementation)

# JAVA TO PYTHON CONVERTER TASK: Python does not allow method overloads:
    def registerFunction(self, name, implementation):
        self.environment.bind(name, implementation)

# JAVA TO PYTHON CONVERTER TASK: Python does not allow method overloads:
    def registerFunction(self, name, implementation):
        self.environment.bind(name, implementation)

# JAVA TO PYTHON CONVERTER TASK: Python does not allow method overloads:
    def registerFunction(self, name, implementation):
        self.environment.bind(name, implementation)

    def getErrors(self):
        return self.errors

    PARSER = ThreadLocal()
    @staticmethod
# JAVA TO PYTHON CONVERTER TASK: Synchronized methods are not converted by Java to Python Converter:
# ORIGINAL LINE: final static synchronized Parser getParser()
    def getParser():
        p = com.dashjoin.jsonata.Jsonata.PARSER.get()
        if p is not None:
            return p
        com.dashjoin.jsonata.Jsonata.PARSER.set(p := Parser())
        return p
