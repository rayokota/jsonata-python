class Generate:

    @staticmethod
# JAVA TO PYTHON CONVERTER WARNING: Method 'throws' clauses are not available in Python:
# ORIGINAL LINE: public static void main(String[] args) throws java.io.IOException
    def main(args):

        verbose = len(args) > 0 and args[0].startswith("-v")

        (java.io.File("src/test/java/com/dashjoin/jsonata/gen")).mkdirs()
        suites = java.io.File("jsonata/test/test-suite/groups")
        total = 0
        testSuites = 0
        listSuites = suites.listFiles()
        listSuites.sort()
        for suite in listSuites:

            b = StringBuffer()
            b.append("package com.dashjoin.jsonata.gen;\n")
            b.append("import org.junit.jupiter.api.Test;\n")
            b.append("import com.dashjoin.jsonata.JsonataTest;\n")
            b.append("public class " + suite.getName().replace('-', '_') + "Test {\n")

            cases = suite.listFiles()
            cases.sort()
            count = 0
            for cas in cases:
                # Skip all non-JSON
                if not cas.getName().endsWith(".json"):
                    continue

                name = cas.getName().substring(0, cas.getName().length() - 5)
                jname = name.replace('-', '_')

                jsonCase = (JsonataTest()).readJson(cas.getAbsolutePath())
                if isinstance(jsonCase, java.util.List):
                    for i, _ in enumerate((jsonCase)):
                        b.append("// " + com.dashjoin.jsonata.Generate.s(((jsonCase)[i])["expr"]) + "\n")
                        b.append("@Test public void " + jname.replace('.', '_') + "_case_" + str(i) + "() throws Exception { \n")
                        b.append("  new JsonataTest().runSubCase(\"jsonata/test/test-suite/groups/" + suite.getName() + "/" + name + ".json\", " + str(i) + ");\n")
                        b.append("}\n")
                        count += 1
                        total += 1
                else:
                    b.append("// " + com.dashjoin.jsonata.Generate.s((jsonCase)["expr"]) + "\n")
                    b.append("@Test public void " + jname.replace('.', '_') + "() throws Exception { \n")
                    b.append("  new JsonataTest().runCase(\"jsonata/test/test-suite/groups/" + suite.getName() + "/" + name + ".json\");\n")
                    b.append("}\n")
                    count += 1
                    total += 1
            b.append("}\n")
            java.nio.file.Files.write(java.nio.file.Path.of("src/test/java/com/dashjoin/jsonata/gen/" + suite.getName().replace('-', '_') + "Test.java"), str(b).getBytes())
            if verbose:
                print(b)
            print("Generated suite '" + suite.getName() + "' tests=" + str(count))
            testSuites += 1
        print("Generated SUITES=" + str(testSuites) + " TOTAL=" + str(total))

    @staticmethod
    def s(o):
        if o is None:
            return None
        s = str(o)
        return s.replace('\n', ' ').replace("\\u", "u")
