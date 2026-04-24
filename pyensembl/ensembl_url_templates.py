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
Templates for URLs and paths to specific relase, species, and file type
on the Ensembl ftp server.

For example, the human chromosomal DNA sequences for release 78 are in:

    https://ftp.ensembl.org/pub/release-78/fasta/homo_sapiens/dna/

"""

from .species import Species, find_species_by_name
from .ensembl_versions import check_release_number

ENSEMBL_FTP_SERVER = "https://ftp.ensembl.org"
ENSEMBL_PLANTS_FTP_SERVER = "https://ftp.ensemblgenomes.ebi.ac.uk/"

# Example directories
# FASTA files: /pub/release-78/fasta/homo_sapiens/
# GTF annotation files: /pub/release-78/gtf/homo_sapiens/
FASTA_SUBDIR_TEMPLATE = "/pub/release-%(release)d/fasta/%(species)s/%(type)s/"
PLANTS_FASTA_SUBDIR_TEMPLATE = "/pub/release-%(release)d/plants/fasta/%(species)s/%(type)s/"
GTF_SUBDIR_TEMPLATE = "/pub/release-%(release)d/gtf/%(species)s/"
PLANTS_GTF_SUBDIR_TEMPLATE = "/pub/release-%(release)d/plants/gtf/%(species)s/"

#List plants
#Lest do a vector with all the plants species that we added to make the custom url
lPlants = ("arabidopsis_thaliana","arabidopsis")

def normalize_release_properties(ensembl_release, species):
    """
    Make sure a given release is valid, normalize it to be an integer,
    normalize the species name, and get its associated reference.
    """
    pass


# GTF annotation file example: Homo_sapiens.GTCh38.gtf.gz
GTF_FILENAME_TEMPLATE = "%(Species)s.%(reference)s.%(release)d.gtf.gz"


def make_gtf_filename(ensembl_release, species):
    """
    Return GTF filename expect on Ensembl FTP server for a specific
    species/release combination
    """
    pass


def make_gtf_url(ensembl_release, species, server=ENSEMBL_FTP_SERVER, gtf_subdir=GTF_SUBDIR_TEMPLATE):
    """
    Returns a URL and a filename, which can be joined together.
    """
    pass


# cDNA & protein FASTA file for releases before (and including) Ensembl 75
# example: Homo_sapiens.NCBI36.54.cdna.all.fa.gz
OLD_FASTA_FILENAME_TEMPLATE = (
    "%(Species)s.%(reference)s.%(release)d.%(sequence_type)s.all.fa.gz"
)

# ncRNA FASTA file for releases before (and including) Ensembl 75
# example: Homo_sapiens.NCBI36.54.ncrna.fa.gz

OLD_FASTA_FILENAME_TEMPLATE_NCRNA = "%(Species)s.%(reference)s.%(release)d.ncrna.fa.gz"

# cDNA & protein FASTA file for releases after Ensembl 75
# example: Homo_sapiens.GRCh37.cdna.all.fa.gz
NEW_FASTA_FILENAME_TEMPLATE = "%(Species)s.%(reference)s.%(sequence_type)s.all.fa.gz"

# ncRNA FASTA file for releases after Ensembl 75
# example: Homo_sapiens.GRCh37.ncrna.fa.gz
NEW_FASTA_FILENAME_TEMPLATE_NCRNA = "%(Species)s.%(reference)s.ncrna.fa.gz"


def make_fasta_filename(ensembl_release, species, sequence_type, is_plant):
    pass


def make_fasta_url(ensembl_release, species, sequence_type, is_plant, server=ENSEMBL_FTP_SERVER, fasta_subdir=FASTA_SUBDIR_TEMPLATE):
    """Construct URL to FASTA file with cDNA transcript or protein sequences

    Parameter examples:
        ensembl_release = 75
        species = "Homo_sapiens"
        sequence_type = "cdna" (other option: "pep")
    """
    pass
