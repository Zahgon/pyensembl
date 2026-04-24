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

from sys import intern
from typechecks import is_string, is_integer

# Manually memoizing here, since our simple common.memoize function has
# noticable overhead in this instance.
NORMALIZE_CHROMOSOME_CACHE = {}


def normalize_chromosome(c):
    pass


def normalize_strand(strand):
    pass
