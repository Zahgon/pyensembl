# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pickle

from functools import wraps


def dump_pickle(obj, filepath):
    pass


def load_pickle(filepath):
    pass


def _memoize_cache_key(args, kwargs):
    """Turn args tuple and kwargs dictionary into a hashable key.

    Expects that all arguments to a memoized function are either hashable
    or can be uniquely identified from type(arg) and repr(arg).
    """
    pass


def memoize(fn):
    """Simple reset-able memoization decorator for functions and methods,
    assumes that all arguments to the function can be hashed and
    compared.
    """
    pass
