import jsonata
import pytest
from jsonata.regex_engine import RegexFlags

re2 = pytest.importorskip("re2")


def re2_regex_engine(pattern: str, flags: RegexFlags):
    """
    Adapts google-re2's Options-based compile() to the (pattern, RegexFlags)
    interface expected by Jsonata's regex_engine hook.
    """
    options = re2.Options()
    options.case_sensitive = not flags.case_insensitive
    options.one_line = not flags.multiline
    options.log_errors = False
    return re2.compile(pattern, options)


class TestRE2Engine:

    def test_match(self):
        expr = jsonata.Jsonata('$match("hello world", /o w/)', re2_regex_engine)
        assert expr.evaluate(None) == {"match": "o w", "index": 4, "groups": []}

    def test_match_case_insensitive_flag(self):
        expr = jsonata.Jsonata('$match("HELLO", /hello/i)', re2_regex_engine)
        result = expr.evaluate(None)
        assert result["match"] == "HELLO"

    def test_contains(self):
        expr = jsonata.Jsonata('$contains("hello", /ell/)', re2_regex_engine)
        assert expr.evaluate(None) is True

    def test_replace_with_string(self):
        expr = jsonata.Jsonata('$replace("abc123def", /[0-9]+/, "#")', re2_regex_engine)
        assert expr.evaluate(None) == "abc#def"

    def test_replace_with_function(self):
        expr = jsonata.Jsonata(
            '$replace("abc123", /[0-9]+/, function($m) { $m.match & "!" })', re2_regex_engine
        )
        assert expr.evaluate(None) == "abc123!"

    def test_split(self):
        expr = jsonata.Jsonata('$split("a1b2c3", /[0-9]/)', re2_regex_engine)
        assert expr.evaluate(None) == ["a", "b", "c", ""]

    def test_rejects_backreferences(self):
        # Proves RE2 is actually compiling the pattern rather than silently
        # falling back to stdlib re: backreferences can't run in RE2's
        # guaranteed-linear-time engine, so this must fail at parse time
        # (regex literals are compiled while the expression is constructed).
        with pytest.raises(re2.error):
            jsonata.Jsonata(r'$match("abab", /(a)\1/)', re2_regex_engine)

    def test_default_engine_still_stdlib_re(self):
        # No regex_engine argument -> falls back to stdlib re, which *does*
        # support backreferences. Confirms the default path is unaffected.
        expr = jsonata.Jsonata(r'$match("xaay", /(a)\1/)')
        assert expr.evaluate(None)["match"] == "aa"

    def test_eval_uses_enclosing_regex_engine(self):
        # $eval dynamically parses and evaluates a nested expression
        # (functions.py's function_eval); it must reuse the enclosing
        # expression's regex_engine rather than silently falling back to
        # stdlib re. Proven the same way as test_rejects_backreferences:
        # a backreference inside the $eval'd source must fail to compile
        # under RE2, surfaced as a D3120 "invalid expression" error.
        expr = jsonata.Jsonata(
            r"""$eval('$match("xaay", /(a)\\1/)')""", re2_regex_engine
        )
        with pytest.raises(jsonata.JException) as exc_info:
            expr.evaluate(None)
        assert exc_info.value.error == "D3120"
