#
# Copyright Robert Yokota
#
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import re
from dataclasses import dataclass
from typing import Any, Callable, Optional, Protocol


@dataclass
class RegexFlags:
    """
    Flags parsed from a JSONata regex literal's /pattern/flags suffix.
    Engines translate these into their own native flag representation.
    """

    case_insensitive: bool = False
    multiline: bool = False


class CompiledPattern(Protocol):
    """
    Structural type for a compiled regex: matches stdlib `re.Pattern`
    as well as whatever a pluggable regex_engine returns (e.g. a
    `google-re2` pattern object).
    """

    def search(self, string: str) -> Optional[Any]: ...
    def finditer(self, string: str) -> Any: ...
    def sub(self, repl: Any, string: str, count: int = 0) -> str: ...
    def split(self, string: str, maxsplit: int = 0) -> list[str]: ...


# Compiles a pattern into a CompiledPattern. Used for JSONata regex literals.
RegexEngine = Callable[[str, RegexFlags], CompiledPattern]


def default_regex_engine(pattern: str, flags: RegexFlags) -> re.Pattern:
    """
    The built-in stdlib `re`-backed engine; this is jsonata-python's default.
    """
    py_flags = 0
    if flags.case_insensitive:
        py_flags |= re.IGNORECASE
    if flags.multiline:
        py_flags |= re.MULTILINE
    return re.compile(pattern, py_flags)
