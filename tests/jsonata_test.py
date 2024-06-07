import json
import jsonata
import math
import pathlib
import traceback


class TestJsonata:
    testFiles = 0
    testCases = 0
    groupDir = "jsonata/test/test-suite/groups/"
    debug = False
    ignoreOverrides = False

    def eval_expr(self, expr, data, bindings, expected, code):
        success = True
        try:
            if TestJsonata.debug:
                print("Expr=" + str(expr) + " Expected=" + str(expected) + " ErrorCode=" + str(code))
            if TestJsonata.debug:
                print(str(data))

            binding_frame = None
            if bindings is not None:
                # If we have bindings, create a binding env with the settings
                binding_frame = jsonata.Jsonata.Frame(None)
                for k, v in bindings.items():
                    binding_frame.bind(k, v)

            jsonata_expr = jsonata.Jsonata(expr)
            if binding_frame is not None:
                binding_frame.set_runtime_bounds(500000 if TestJsonata.debug else 10000, 303)
            result = jsonata_expr.evaluate(data, binding_frame)
            if code is not None:
                success = False

            if expected is not None and expected != result:
                # if ((""+expected).equals(""+result))
                #     System.out.println("Value equals failed, stringified equals = true. Result = "+result)
                # else
                success = False

            if expected is None and result is not None:
                success = False

            if TestJsonata.debug and success:
                print("--Result = " + str(result))

            if not success:
                print("--Expr=" + str(expr) + " Expected=" + str(expected) + " ErrorCode=" + str(code))
                print("--Data=" + str(data))
                print("--Result = " + str(result) + " Class=" + str(type(result) if result is not None else None))
                print("--Expect = " + str(expected) + " ExpectedError=" + str(code))
                print("WRONG RESULT")

            # assertEquals("Must be equal", expected, ""+result)
        except Exception as t:
            if code is None:
                print("--Expr=" + str(expr) + " Expected=" + str(expected) + " ErrorCode=" + str(code))
                print("--Data=" + str(data))

                if isinstance(t, jsonata.JException):
                    je = t
                    print("--Exception     = " + str(je.error) + "  --> " + str(je))
                else:
                    print("--Exception     = " + str(t))

                print("--ExpectedError = " + str(code) + " Expected=" + str(expected))
                print("WRONG RESULT (exception)")
                success = False
            if TestJsonata.debug and success:
                print("--Exception = " + str(t))
            if not success:
                print(traceback.format_exc())
                # TODO fix - remove
                # raise t
        return success

    def to_json(self, json_str):
        return json.loads(json_str)

    def read_json(self, name):
        with open(name, encoding="utf-8") as f:
            return json.load(f)

    def test_simple(self):
        self.eval_expr("42", None, None, 42, None)
        self.eval_expr("(3*(4-2)+1.01e2)/-2", None, None, -53.5, None)

    def test_path(self):
        data = self.read_json("jsonata/test/test-suite/datasets/dataset0.json")
        print(str(data))
        self.eval_expr("foo.bar", data, None, 42, None)

    def run_case(self, name):
        if not self.run_test_suite(name):
            raise Exception()

    def run_sub_case(self, name, sub_nr):
        cases = self.read_json(name)
        if not self.run_test_case(name + "_" + str(sub_nr), cases[sub_nr]):
            raise Exception()

    def run_test_suite(self, name):

        # System.out.println("Running test "+name)
        TestJsonata.testFiles += 1

        success = True

        test_case = self.read_json(name)
        if isinstance(test_case, list):
            # some cases contain a list of test cases
            # loop over the case definitions
            for testDef in test_case:
                print("Running sub-test")
                success &= self.run_test_case(name, testDef)
        else:
            success &= self.run_test_case(name, test_case)
        return success

    def replace_nulls(self, o):
        if isinstance(o, list):
            index = 0
            for i in o:
                if i is None:
                    o[index] = jsonata.Utils.NULL_VALUE
                else:
                    self.replace_nulls(i)
                index += 1
        if isinstance(o, dict):
            for k, v in o.items():
                if v is None:
                    o[k] = jsonata.Utils.NULL_VALUE
                else:
                    self.replace_nulls(v)

    testOverrides = None

    @staticmethod
    def get_test_overrides():
        if TestJsonata.testOverrides is not None:
            return TestJsonata.testOverrides

        with open("tests/test-overrides.json", encoding="utf-8") as f:
            TestJsonata.testOverrides = json.load(f)
        return TestJsonata.testOverrides

    def get_override_for_test(self, name):
        if TestJsonata.ignoreOverrides:
            return None

        tos = TestJsonata.get_test_overrides()
        for to in tos.get("override"):
            if name.find(to.get("name")) >= 0:
                return to
        return None

    def run_test_case(self, name, test_def):

        TestJsonata.testCases += 1
        if TestJsonata.debug:
            print("\nRunning test " + name)

        expr = test_def.get("expr")

        if expr is None:
            expr_file = test_def.get("expr-file")
            file_name = name[0:name.rfind("/")] + "/" + expr_file
            with open(file_name, 'r', encoding="utf-8") as f:
                expr = f.read()

        dataset = test_def.get("dataset")
        bindings = test_def.get("bindings")
        result = test_def.get("result")

        # if (result == null)
        #   if (testDef.containsKey("result"))
        #     result = Jsonata.NULL_VALUE

        # replaceNulls(result)

        code = test_def.get("code")

        if isinstance(test_def.get("error"), dict):
            code = test_def.get("error").get("code")

        # System.out.println(""+bindings)

        data = test_def.get("data")
        if data is None and dataset is not None:
            data = self.read_json("jsonata/test/test-suite/datasets/" + dataset + ".json")

        to = self.get_override_for_test(name)
        if to is not None:
            print("OVERRIDE used : " + to.get("name") + " for " + name + " reason=" + to.get("reason"))
            if to.get("alternateResult") is not None:
                result = to.get("alternateResult")
            if to.get("alternateCode") is not None:
                code = to.get("alternateCode")
        res = False
        if TestJsonata.debug and expr == "(  $inf := function(){$inf()};  $inf())":
            print("DEBUG MODE: skipping infinity test: " + str(expr), end='\n')
            res = True
        else:
            res = self.eval_expr(expr, data, bindings, result, code)

        if to is not None:
            # There is an override/alternate result for this defined...
            if not res and to.get("ignoreError") is not None and to.get("ignoreError"):
                print("Test " + name + " failed, but override allows failure")
                res = True

        return res

    def run_test_group(self, group):

        path = pathlib.Path(TestJsonata.groupDir, group)
        print("Run group " + path.name)
        files = [f for f in path.iterdir()]
        files = sorted(files, key=lambda x: x.name)
        success = True
        count = 0
        good = 0
        for f in files:
            name = f.name
            if name.endswith(".json"):
                res = self.run_test_suite(TestJsonata.groupDir + group + "/" + name)
                success &= res

                count += 1
                if res:
                    good += 1
        success_percentage = math.trunc(100 * good / float(count))
        print("Success: " + str(good) + " / " + str(count) + " = " + str(math.trunc(100 * good / float(count))) + "%")
        assert good == count
        # assertEquals("100% test runs must succeed", 100, success_percentage)
        return success

    # For local dev: @Test
    def run_sub_suite(self):
        # runTestSuite("jsonata/test/test-suite/groups/boolean-expresssions/test.jsonx")
        # runTestSuite("jsonata/test/test-suite/groups/boolean-expresssions/case017.json")
        # runTestSuite("jsonata/test/test-suite/groups/fields/case000.json")
        # runTestGroup("fields")
        # runTestGroup("comments")
        # runTestGroup("comparison-operators")
        # runTestGroup("boolean-expresssions")
        # runTestGroup("array-constructor")
        # runTestGroup("transform")
        # runTestGroup("function-substring")
        # runTestGroup("wildcards")
        # runTestSuite("jsonata/test/test-suite/groups/function-substring/case012.json")
        # runTestSuite("jsonata/test/test-suite/groups/transform/case030.json")
        # runTestSuite("jsonata/test/test-suite/groups/array-constructor/case006.json")
        # Filter:
        # runTestSuite("jsonata/test/test-suite/groups/array-constructor/case017.json")
        s = "jsonata/test/test-suite/groups/wildcards/case003.json"
        s = "jsonata/test/test-suite/groups/flattening/large.json"
        s = "jsonata/test/test-suite/groups/function-sum/case006.json"
        s = "jsonata/test/test-suite/groups/function-substring/case016.json"
        s = "jsonata/test/test-suite/groups/null/case001.json"
        s = "jsonata/test/test-suite/groups/context/case003.json"
        s = "jsonata/test/test-suite/groups/object-constructor/case008.json"
        self.run_test_suite(s)
        # String g = "function-applications"; // partly
        # String g = "higher-order-functions"; // works!
        # String g = "hof-map"
        # String g = "joins"
        # String g = "function-join"; // looks good
        # String g = "descendent-operator"; // nearly
        # String g = "object-constructor"
        # String g = "flattening"
        # String g = "parent-operator"
        # String g = "function-substring"; // nearly - unicode encoding issues
        # String g = "function-substringBefore"; // works!
        # String g = "function-substringAfter"; // works!
        # String g = "function-sum"; // works! rounding error delta
        # String g = "function-max"; // nearly - [-1,-5] second unary wrong!!!
        # String g = "function-average"; // nearly - [-1,-5] second unary wrong!!!
        # String g = "function-pad"; // nearly - unicode
        # String g = "function-trim"; // works!
        # String g = "function-contains"; // works NO regexp
        # String g = "function-join"; // works NO regexp
        # runTestGroup(g)

        # runAllTestGroups()

    def run_all_test_groups(self):
        path = pathlib.Path(TestJsonata.groupDir)
        groups = [f for f in path.iterdir()]
        groups = sorted(groups, key=lambda x: x.name)
        for g in groups:
            name = g.name
            print("@Test")
            print("public void runTestGroup_" + name.replace("-", "_") + "() {")
            print("\trunTestGroup(\"" + name + "\");")
            print("}")
            # runTestGroup(name)

        print("Total test files=" + str(TestJsonata.testFiles) + " cases=" + str(TestJsonata.testCases))
