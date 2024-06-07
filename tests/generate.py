import io
import json
import pathlib
import re


class Generate:

    requires_3_11 = {
        ("FunctionFrommillis", "format_date_time", 66),
        ("FunctionTomillis", "case001", 0),
        ("FunctionTomillis", "case002", 0),
        ("FunctionTomillis", "case004", 0),
    }

    @staticmethod
    def main(args):

        verbose = len(args) > 0 and args[0].startswith("-v")

        gendir = "tests/gen"
        genpath = pathlib.Path(gendir)
        genpath.mkdir(exist_ok=True)
        suites = "jsonata/test/test-suite/groups"
        suitepath = pathlib.Path(suites)
        total = 0
        test_suites = 0
        list_suites = [f for f in suitepath.iterdir()]
        list_suites = sorted(list_suites, key=lambda x: x.name)
        for suite in list_suites:

            b = io.StringIO()
            b.write("import pytest\n")
            b.write("import sys\n")
            b.write("from tests import jsonata_test\n\n\n")
            # Pascal case
            cname = ''.join(word.title() for word in suite.name.split('-'))
            b.write("class Test" + cname + ":\n")

            cases = [f for f in suite.iterdir()]
            cases = sorted(cases, key=lambda x: x.name)
            count = 0
            for cas in cases:
                # Skip all non-JSON
                if not cas.name.endswith(".json"):
                    continue

                name = cas.name[0:len(cas.name) - 5]
                jname = name
                jname = jname.replace('-', '_')
                jname = jname.replace('.', '_')
                # Camel case to snake case
                jname = re.sub(r'(?<!^)(?=[A-Z])', '_', jname).lower()

                with open(cas, encoding="utf-8") as f:
                    json_case = json.load(f)
                if isinstance(json_case, list):
                    for i, c in enumerate(json_case):
                        b.write("    # " + Generate.s(c.get("expr")) + "\n")
                        if (cname, jname, i) in Generate.requires_3_11:
                            b.write("    @pytest.mark.skipif(sys.version_info < (3, 11), reason='requires Python 3.11+')\n")
                        b.write("    def test_" + jname + "_case_" + str(i) + "(self):\n")
                        b.write(
                            "        jsonata_test.TestJsonata().run_sub_case(\"jsonata/test/test-suite/groups/" +
                            suite.name + "/" + name + ".json\", " + str(
                                i) + ")\n\n")
                        count += 1
                        total += 1
                else:
                    b.write("    # " + Generate.s(json_case.get("expr")) + "\n")
                    if (cname, jname, 0) in Generate.requires_3_11:
                        b.write("    @pytest.mark.skipif(sys.version_info < (3, 11), reason='requires Python 3.11+')\n")
                    b.write("    def test_" + jname + "(self):\n")
                    b.write(
                        "        jsonata_test.TestJsonata().run_case(\"jsonata/test/test-suite/groups/" +
                        suite.name + "/" + name + ".json\")\n\n")
                    count += 1
                    total += 1
            with open(gendir + "/" + suite.name + "_test.py", "w", encoding="utf-8") as f:
                f.write(b.getvalue())
            if verbose:
                print(b)
            print("Generated suite '" + suite.name + "' tests=" + str(count))
            test_suites += 1
        print("Generated SUITES=" + str(test_suites) + " TOTAL=" + str(total))

    @staticmethod
    def s(o):
        if o is None:
            return str(None)
        s = str(o)
        s = s.replace('\n', ' ').replace("\\u", "u")
        try:
            s.encode("utf-8")
        except UnicodeEncodeError:
            s = "?"
        return s


if __name__ == '__main__':
    Generate.main([])
