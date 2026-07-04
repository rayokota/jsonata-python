import re

import jsonata
import pytest

re2 = pytest.importorskip("re2")


class RE2Engine:
    """
    Adapts google-re2's Options-based compile() to the re.compile(pattern, flags)
    interface expected by Jsonata's regex_engine hook.
    """

    @staticmethod
    def compile(pattern, flags=0):
        options = re2.Options()
        options.case_sensitive = not bool(flags & re.IGNORECASE)
        options.one_line = not bool(flags & re.MULTILINE)
        options.log_errors = False
        return re2.compile(pattern, options)


class TestRE2Engine:

    def test_match(self):
        expr = jsonata.Jsonata('$match("hello world", /o w/)', RE2Engine)
        assert expr.evaluate(None) == {"match": "o w", "index": 4, "groups": []}

    def test_match_case_insensitive_flag(self):
        expr = jsonata.Jsonata('$match("HELLO", /hello/i)', RE2Engine)
        result = expr.evaluate(None)
        assert result["match"] == "HELLO"

    def test_contains(self):
        expr = jsonata.Jsonata('$contains("hello", /ell/)', RE2Engine)
        assert expr.evaluate(None) is True

    def test_replace_with_string(self):
        expr = jsonata.Jsonata('$replace("abc123def", /[0-9]+/, "#")', RE2Engine)
        assert expr.evaluate(None) == "abc#def"

    def test_replace_with_function(self):
        expr = jsonata.Jsonata(
            '$replace("abc123", /[0-9]+/, function($m) { $m.match & "!" })', RE2Engine
        )
        assert expr.evaluate(None) == "abc123!"

    def test_split(self):
        expr = jsonata.Jsonata('$split("a1b2c3", /[0-9]/)', RE2Engine)
        assert expr.evaluate(None) == ["a", "b", "c", ""]

    def test_rejects_backreferences(self):
        # Proves RE2 is actually compiling the pattern rather than silently
        # falling back to stdlib re: backreferences can't run in RE2's
        # guaranteed-linear-time engine, so this must fail at parse time
        # (regex literals are compiled while the expression is constructed).
        with pytest.raises(re2.error):
            jsonata.Jsonata(r'$match("abab", /(a)\1/)', RE2Engine)

    def test_default_engine_still_stdlib_re(self):
        # No regex_engine argument -> falls back to stdlib re, which *does*
        # support backreferences. Confirms the default path is unaffected.
        expr = jsonata.Jsonata(r'$match("xaay", /(a)\1/)')
        assert expr.evaluate(None)["match"] == "aa"
