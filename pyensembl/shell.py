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
Manipulate pyensembl's local cache.

    %(prog)s {install, delete, delete-sequence-cache} [--release XXX --species human...]

To install particular Ensembl human release(s):
    %(prog)s install --release 75 77

To install particular Ensembl mouse release(s):
    %(prog)s install --release 75 77 --species mouse

To delete all downloaded and cached data for a particular Ensembl release:
    %(prog)s delete-all-files --release 75 --species human

To delete only cached data related to transcript and protein sequences:
    %(prog)s delete-index-files --release 75

To list all installed genomes:
    %(prog)s list

To install a genome from source files:
    %(prog)s install \
 --reference-name "GRCh38" \
 --gtf URL_OR_PATH \
 --transcript-fasta URL_OR_PATH \
 --protein-fasta URL_OR_PATH
"""

import argparse
import logging.config
from importlib import resources
import os

from .ensembl_release import EnsemblRelease
from .ensembl_versions import MAX_ENSEMBL_RELEASE
from .genome import Genome
from .species import Species
from .version import __version__

logging.config.fileConfig(str(resources.files("pyensembl") / "logging.conf"))
logger = logging.getLogger(__name__)


parser = argparse.ArgumentParser(usage=__doc__)

parser.add_argument(
    "--version", 
    action="version",
    version='%(prog)s {version}'.format(version=__version__)
)

parser.add_argument(
    "--overwrite",
    default=False,
    action="store_true",
    help="Force download and indexing even if files already exist locally",
)


release_group = parser.add_argument_group("Ensembl release options")
release_group.add_argument(
    "--release",
    type=int,
    nargs="+",
    default=[],
    help="Ensembl release version(s) (default=%d)" % MAX_ENSEMBL_RELEASE,
)

release_group.add_argument(
    "--species",
    default=[],
    nargs="+",
    help="Which species to download Ensembl data for (default=human)",
)

release_group.add_argument(
    "--custom-mirror",
    default=None,
    help="URL and directory to use instead of the default Ensembl FTP server",
)

path_group = parser.add_argument_group("Custom genome options")

path_group.add_argument(
    "--reference-name",
    type=str,
    default=None,
    help="Name of the reference, e.g. GRCh38",
)

path_group.add_argument(
    "--annotation-name", default=None, help="Name of annotation source (e.g. refseq)"
)

path_group.add_argument(
    "--annotation-version", default=None, help="Version of annotation database"
)

path_group.add_argument(
    "--gtf",
    type=str,
    default=None,
    help="URL or local path to a GTF file containing annotations.",
)

path_group.add_argument(
    "--transcript-fasta",
    type=str,
    action="append",
    default=[],
    help="URL or local path to a FASTA files containing the transcript "
    "data. This option can be specified multiple times for multiple "
    "FASTA files.",
)

path_group.add_argument(
    "--protein-fasta",
    type=str,
    default=[],
    action="append",
    help="URL or local path to a FASTA file containing protein data.",
)

path_group.add_argument(
    "--shared-prefix",
    default="",
    help="Add this prefix to URLs or paths specified by --gtf, --transcript-fasta, --protein-fasta",
)

parser.add_argument(
    "action",
    type=lambda arg: arg.lower().strip(),
    choices=(
        "install",
        "delete-all-files",
        "delete-index-files",
        "list",
    ),
    help=(
        '"install" will download and index any data that is  not '
        'currently downloaded or indexed. "delete-all-files" will delete all data '
        'associated with a genome annotation. "delete-index-files" deletes '
        "all files other than the original GTF and FASTA files for a genome. "
        '"list" will show you all installed Ensembl genomes.'
    ),
)


def collect_all_installed_ensembl_releases():
    pass


def all_combinations_of_ensembl_genomes(args):
    """
    Use all combinations of species and release versions specified by the
    commandline arguments to return a list of EnsemblRelease or Genome objects.
    The results will typically be of type EnsemblRelease unless the
    --custom-mirror argument was given.
    """
    pass


def collect_selected_genomes(args):
    # If specific genome source URLs are provided, use those
    pass


def run():
    pass
