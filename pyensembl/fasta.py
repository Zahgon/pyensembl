# Copyright (c) 2015-2016. Mount Sinai School of Medicine
#
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

"""
The worse sin in bioinformatics is to write your own FASTA parser.
Unfortunately, small errors creep in to different FASTA files on the
Ensembl FTP server that no proper FASTA parser lets you skip over.
"""


from gzip import GzipFile
import logging


logger = logging.getLogger(__name__)


def _parse_header_id(line):
    """
    Pull the transcript or protein identifier from the header line
    which starts with '>'
    """
    pass


class FastaParser(object):
    """
    FastaParser object consumes lines of a FASTA file incrementally
    while building up a dictionary mapping sequence identifiers to sequences.
    """

    def __init__(self):
        self.current_id = None
        self.current_lines = []

    def read_file(self, fasta_path):
        """
        Read the contents of a FASTA file into a dictionary
        """
        pass

    def iterate_over_file(self, fasta_path):
        """
        Generator that yields identifiers paired with sequences.
        """
        pass

    def _open(self, fasta_path):
        """
        Open either a text file or compressed gzip file as a stream of bytes.
        """
        pass

    def _current_entry(self):
        # when we hit a new entry, if this isn't the first
        # entry of the file then put the last one in the dictionary
        pass

    def _read_header(self, line):
        pass


def parse_fasta_dictionary(fasta_path):
    """
    Given a path to a FASTA (or compressed FASTA) file, returns a dictionary
    mapping its sequence identifiers to sequences.

    Parameters
    ----------
    fasta_path : str
        Path to the FASTA file.

    Returns dictionary from string identifiers to string sequences.
    """
    pass
