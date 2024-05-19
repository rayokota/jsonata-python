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

from com.dashjoin.jsonata import Jsonata.Frame

#*
# * Configure max runtime / max recursion depth.
# * See Frame.setRuntimeBounds - usually not used directly
# 
class Timebox:

    def _initialize_instance_fields(self):
        # instance fields found by Java to Python Converter:
        self.timeout = 5000
        self.maxDepth = 100
        self.time = System.currentTimeMillis()
        self.depth = 0




    #    *
    #     * Protect the process/browser from a runnaway expression
    #     * i.e. Infinite loop (tail recursion), or excessive stack growth
    #     *
    #     * @param {Object} expr - expression to protect
    #     * @param {Number} timeout - max time in ms
    #     * @param {Number} maxDepth - max stack depth
    #     
# JAVA TO PYTHON CONVERTER TASK: There is no Python equivalent to multiple constructors:
# ORIGINAL LINE: public Timebox(com.dashjoin.jsonata.Jsonata.Frame expr)
    def __init__(self, expr):
        self(expr, 5000, 100)

# JAVA TO PYTHON CONVERTER TASK: There is no Python equivalent to multiple constructors:
# ORIGINAL LINE: public Timebox(com.dashjoin.jsonata.Jsonata.Frame expr, long timeout, int maxDepth)
    def __init__(self, expr, timeout, maxDepth):
        self._initialize_instance_fields()

        self.timeout = timeout
        self.maxDepth = maxDepth

        # register callbacks
# JAVA TO PYTHON CONVERTER TASK: Only expression lambdas are converted by Java to Python Converter:
        #        expr.setEvaluateEntryCallback((_exp, _input, _env)->
        #        {
        #            if (_env.isParallelCall)
        #                return
        #            depth++
        #            checkRunnaway()
        #        }
        #        )
# JAVA TO PYTHON CONVERTER TASK: Only expression lambdas are converted by Java to Python Converter:
        #        expr.setEvaluateExitCallback((_exp, _input, _env, _res)->
        #        {
        #            if (_env.isParallelCall)
        #                return
        #            depth--
        #            checkRunnaway()
        #        }
        #        )

    def checkRunnaway(self):
        if self.depth > self.maxDepth:
            # stack too deep
            raise JException("Stack overflow error: Check for non-terminating recursive function.  Consider rewriting as tail-recursive. Depth=" + str(self.depth) + " max=" + str(self.maxDepth),-1)
            #stack: new Error().stack,
            #code: "U1001"
            #}
        if System.currentTimeMillis() - self.time > self.timeout:
            # expression has run for too long
            raise JException("Expression evaluation timeout: Check for infinite loop",-1)
            #stack: new Error().stack,
            #code: "U1001"
            #}

