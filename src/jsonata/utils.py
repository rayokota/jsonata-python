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
# Derived from the following code:
#
#   Project name: jsonata-java
#   Copyright Dashjoin GmbH. https://dashjoin.com
#   Licensed under the Apache License, Version 2.0 (the "License")
#

import copy
import math
from typing import Any, Optional, Iterable

from jsonata import jexception


class Utils:
    class NullValue:
        def __repr__(self):
            return "null"

    NULL_VALUE = NullValue()

    @staticmethod
    def is_numeric(v: Optional[Any]) -> bool:
        if isinstance(v, bool):
            return False
        if isinstance(v, int):
            return True
        is_num = False
        if isinstance(v, float):
            is_num = not math.isnan(v)
            if is_num and not math.isfinite(v):
                raise jexception.JException("D1001", 0, v)
        return is_num

    @staticmethod
    def is_array_of_strings(v: Optional[Any]) -> bool:
        if isinstance(v, list):
            for o in v:
                if not isinstance(o, str):
                    return False
            return True
        return False

    @staticmethod
    def is_array_of_numbers(v: Optional[Any]) -> bool:
        if isinstance(v, list):
            for o in v:
                if not Utils.is_numeric(o):
                    return False
            return True
        return False

    @staticmethod
    def is_function(o: Optional[Any]) -> bool:
        from jsonata import jsonata
        return isinstance(o, jsonata.Jsonata.JFunctionCallable)

    NONE = object()

    @staticmethod
    def create_sequence(el: Optional[Any] = NONE) -> list:
        if el is not Utils.NONE:
            sequence = Utils.JList([el])
        else:
            sequence = Utils.JList()
        sequence.sequence = True
        return sequence

    @staticmethod
    def create_sequence_from_iter(it: Iterable) -> list:
        sequence = Utils.JList(it)
        sequence.sequence = True
        return sequence

    @staticmethod
    def is_deep_equal(lhs: Optional[Any], rhs: Optional[Any]) -> bool:
        if isinstance(lhs, list) and isinstance(rhs, list):
            if len(lhs) != len(rhs):
                return False
            for ii, _ in enumerate(lhs):
                if not Utils.is_deep_equal(lhs[ii], rhs[ii]):
                    return False
            return True
        elif isinstance(lhs, dict) and isinstance(rhs, dict):
            if lhs.keys() != rhs.keys():
                return False
            for key in lhs.keys():
                if not Utils.is_deep_equal(lhs[key], rhs[key]):
                    return False
            return True
        if lhs == rhs:
            if isinstance(lhs, bool) != isinstance(rhs, bool):
                return False
            return True
        return False

    class JList(list):
        sequence: bool
        outer_wrapper: bool
        tuple_stream: bool
        keep_singleton: bool
        cons: bool

        def __init__(self, c=()):
            super().__init__(c)
            # Jsonata specific flags
            self.sequence = False
            self.outer_wrapper = False
            self.tuple_stream = False
            self.keep_singleton = False
            self.cons = False

    class RangeList(list):
        a: int
        b: int
        size: int

        def __init__(self, left, right):
            super().__init__()
            self.a = left
            self.b = right
            self.size = self.b - self.a + 1

        def __len__(self):
            return self.size

        def __getitem__(self, index):
            if index < self.size:
                return Utils.convert_number(self.a + index)
            raise IndexError(index)

        def __iter__(self):
            return iter(range(self.a, self.b))

    @staticmethod
    def is_sequence(result: Optional[Any]) -> bool:
        return isinstance(result, Utils.JList) and result.sequence

    @staticmethod
    def convert_number(n: float) -> Optional[float]:
        # Use long if the number is not fractional
        if not Utils.is_numeric(n):
            return None
        if int(n) == float(n):
            v = int(n)
            if int(v) == v:
                return int(v)
            else:
                return v
        return float(n)

    @staticmethod
    def convert_value(val: Optional[Any]) -> Optional[Any]:
        return val if val is not Utils.NULL_VALUE else None

    #
    # Converts all occurrences of NULL_VALUE in the given object to None.
    #
    # The given object is not modified. Dicts and lists that contain a NULL_VALUE
    # (directly or nested) are copied; all other dicts and lists are returned as is,
    # so the result may share structure with the input.
    #
    @staticmethod
    def convert_nulls(val: Optional[Any]) -> Optional[Any]:
        if isinstance(val, dict):
            copied = None
            for key, v in val.items():
                converted = Utils.convert_nulls(v)
                if converted is not v:
                    if copied is None:
                        copied = copy.copy(val)
                    copied[key] = converted
            return copied if copied is not None else val
        if isinstance(val, list):
            copied = None
            for i, v in enumerate(val):
                converted = Utils.convert_nulls(v)
                if converted is not v:
                    if copied is None:
                        copied = copy.copy(val)
                    copied[i] = converted
            return copied if copied is not None else val
        return Utils.convert_value(val)
