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


class JException(RuntimeException):

    def _initialize_instance_fields(self):
        # instance fields found by Java to Python Converter:
        self.error = None
        self.location = 0
        self.current = None
        self.expected = None
        self.type = None
        self.remaining = None


    SERIAL_VERSION_UID = -3354943281127831704


# JAVA TO PYTHON CONVERTER TASK: There is no Python equivalent to multiple constructors:
# ORIGINAL LINE: public JException(String error)
    def __init__(self, error):
        self(error, -1, None, None)
# JAVA TO PYTHON CONVERTER TASK: There is no Python equivalent to multiple constructors:
# ORIGINAL LINE: public JException(String error, int location)
    def __init__(self, error, location):
        self(error, location, None, None)
# JAVA TO PYTHON CONVERTER TASK: There is no Python equivalent to multiple constructors:
# ORIGINAL LINE: public JException(String error, int location, Object currentToken)
    def __init__(self, error, location, currentToken):
        self(error, location, currentToken, None)
# JAVA TO PYTHON CONVERTER TASK: There is no Python equivalent to multiple constructors:
# ORIGINAL LINE: public JException(String error, int location, Object currentToken, Object expected)
    def __init__(self, error, location, currentToken, expected):
        self(None, error, location, currentToken, expected)
# JAVA TO PYTHON CONVERTER TASK: There is no Python equivalent to multiple constructors:
# ORIGINAL LINE: public JException(Throwable cause, String error, int location, Object currentToken, Object expected)
    def __init__(self, cause, error, location, currentToken, expected):
        self._initialize_instance_fields()

        super().__init__(com.dashjoin.jsonata.JException.msg(error, location, currentToken, expected), cause)
        self.error = error
        self.location = location
        self.current = currentToken
        self.expected = expected

    #    *
    #     * Returns the error code, i.e. S0201
    #     * @return
    #     
    def getError(self):
        return self.error

    #    *
    #     * Returns the error location (in characters)
    #     * @return
    #     
    def getLocation(self):
        return self.location

    #    *
    #     * Returns the current token
    #     * @return
    #     
    def getCurrent(self):
        return self.current

    #    *
    #     * Returns the expected token
    #     * @return
    #     
    def getExpected(self):
        return self.expected

    #    *
    #     * Returns the error message with error details in the text.
    #     * Example: Syntax error: ")" {code=S0201 position=3}
    #     * @return
    #     
    def getDetailedErrorMessage(self):
        return com.dashjoin.jsonata.JException.msg(self.error, self.location, self.current, self.expected, True)

    #    *
    #     * Generate error message from given error code
    #     * Codes are defined in Jsonata.errorCodes
    #     * 
    #     * Fallback: if error code does not exist, return a generic message
    #     * 
    #     * @param error
    #     * @param location
    #     * @param arg1
    #     * @param arg2
    #     * @return
    #     
    @staticmethod
# JAVA TO PYTHON CONVERTER TASK: Python does not allow method overloads:
    def msg(error, location, arg1, arg2):
        return com.dashjoin.jsonata.JException.msg(error, location, arg1, arg2, False)

    #    *
    #     * Generate error message from given error code
    #     * Codes are defined in Jsonata.errorCodes
    #     * 
    #     * Fallback: if error code does not exist, return a generic message
    #     * 
    #     * @param error
    #     * @param location
    #     * @param arg1
    #     * @param arg2
    #     * @param details True = add error details as text, false = don't add details (use getters to retrieve details)
    #     * @return
    #     
    @staticmethod
# JAVA TO PYTHON CONVERTER TASK: Python does not allow method overloads:
    def msg(error, location, arg1, arg2, details):
        message = Jsonata.errorCodes[error]

        if message is None:
            # unknown error code
            return "JSonataException " + error + (" {code=unknown position=" + location + " arg1=" + arg1 + " arg2=" + arg2 + "}" if details else "")

        formatted = message
        try:
            # Replace any {{var}} with Java format "%1$s"
            formatted = formatted.replaceFirst("\\{\\{\\w+\\}\\}", java.util.regex.Matcher.quoteReplacement("\"%1$s\""))
            formatted = formatted.replaceFirst("\\{\\{\\w+\\}\\}", java.util.regex.Matcher.quoteReplacement("\"%2$s\""))

            formatted = String.format(formatted, arg1, arg2)
        except java.util.IllegalFormatException as ex:
            ex.printStackTrace()
            # ignore
        if details:
            formatted = formatted + " {code=" + error
            if location >= 0:
                formatted += " position=" + str(location)
            formatted += "}"
        return formatted

    # Recover
