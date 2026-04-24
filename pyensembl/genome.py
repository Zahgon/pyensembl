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
Contains the Genome class, with its millions of accessors and wrappers
around an arbitrary genomic database.
"""


from os import remove
from os.path import exists, getsize

from serializable import Serializable

from .download_cache import DownloadCache
from .database import Database
from .exon import Exon
from .gene import Gene
from .sequence_data import SequenceData
from .transcript import Transcript


def _parse_transcript_support_level(value):
    """
    Coerce a raw ``transcript_support_level`` attribute into an int or None.

    Recent Ensembl releases append text such as
    ``"1 (assigned to previous version 5)"`` after the numeric TSL, and
    older or missing entries can be ``None`` or the literal string ``"NA"``.
    Keep only the leading whitespace-separated token and return it as an
    int when it is a digit, otherwise None.
    """
    pass


class Genome(Serializable):
    """
    Bundles together the genomic annotation and sequence data associated with
    a particular genomic database source (e.g. a single Ensembl release) and
    provides a wide variety of helper methods for accessing this data.
    """

    def __init__(
        self,
        reference_name,
        annotation_name,
        annotation_version=None,
        gtf_path_or_url=None,
        transcript_fasta_paths_or_urls=None,
        protein_fasta_paths_or_urls=None,
        decompress_on_download=False,
        copy_local_files_to_cache=False,
        cache_directory_path=None,
    ):
        """
        Parameters
        ----------
        reference_name : str
            Name of genome assembly which annotations in GTF are aligned against
            (and from which sequence data is drawn)

        annotation_name : str
            Name of annotation source (e.g. "Ensembl)

        annotation_version : int or str
            Version of annotation database (e.g. 75)

        gtf_path_or_url : str
            Path or URL of GTF file

        transcript_fasta_paths_or_urls : list
            List of paths or URLs of FASTA files containing transcript sequences

        protein_fasta_paths_or_urls : list
            List of paths or URLs of FASTA files containing protein sequences

        decompress_on_download : bool
            If remote file is compressed, decompress the local copy?

        copy_local_files_to_cache : bool
            If genome data file is local use it directly or copy to cache first?

        cache_directory_path : None
            Where to place downloaded and cached files for this genome,
            by default inferred from reference name, annotation name,
            annotation version, and global cache dir for pyensembl.
        """
        if transcript_fasta_paths_or_urls is None:
            transcript_fasta_paths_or_urls = []
        elif isinstance(transcript_fasta_paths_or_urls, str):
            transcript_fasta_paths_or_urls = [transcript_fasta_paths_or_urls]

        if protein_fasta_paths_or_urls is None:
            protein_fasta_paths_or_urls = []
        elif isinstance(protein_fasta_paths_or_urls, str):
            protein_fasta_paths_or_urls = [protein_fasta_paths_or_urls]

        self.reference_name = reference_name
        self.annotation_name = annotation_name
        self.annotation_version = annotation_version
        self.decompress_on_download = decompress_on_download
        self.copy_local_files_to_cache = copy_local_files_to_cache
        self.cache_directory_path = cache_directory_path
        self._gtf_path_or_url = gtf_path_or_url
        self._transcript_fasta_paths_or_urls = transcript_fasta_paths_or_urls
        self._protein_fasta_paths_or_urls = protein_fasta_paths_or_urls

        self.download_cache = DownloadCache(
            reference_name=self.reference_name,
            annotation_name=self.annotation_name,
            annotation_version=self.annotation_version,
            decompress_on_download=self.decompress_on_download,
            copy_local_files_to_cache=self.copy_local_files_to_cache,
            install_string_function=self.install_string,
            cache_directory_path=cache_directory_path,
        )
        self._init_lazy_fields()

    @property
    def requires_gtf(self):
        pass

    @property
    def requires_transcript_fasta(self):
        pass

    @property
    def requires_protein_fasta(self):
        pass

    def to_dict(self):
        """
        Returns a dictionary of the essential fields of this Genome.
        """
        pass

    def _init_lazy_fields(self):
        """
        Member data that gets loaded or constructed on demand
        """
        pass

    def _get_cached_path(
        self, field_name, path_or_url, download_if_missing=False, overwrite=False
    ):
        """
        Get the local path for a possibly remote file, invoking either
        a download or install error message if it's missing.
        """
        pass

    def _get_gtf_path(self, download_if_missing=False, overwrite=False):
        pass

    def _get_transcript_fasta_paths(self, download_if_missing=False, overwrite=False):
        pass

    def _get_protein_fasta_paths(self, download_if_missing=False, overwrite=False):
        # get the path for peptide FASTA files containing
        # this genome's protein sequences
        pass

    def _set_local_paths(self, download_if_missing=True, overwrite=False):
        pass

    def required_local_files(self):
        paths = []
        if self._gtf_path_or_url:
            paths.append(self.download_cache.cached_path(self._gtf_path_or_url))
        if self._transcript_fasta_paths_or_urls:
            paths.extend(
                [
                    self.download_cache.cached_path(path_or_url)
                    for path_or_url in self._transcript_fasta_paths_or_urls
                ]
            )
        if self._protein_fasta_paths_or_urls:
            paths.extend(
                [
                    self.download_cache.cached_path(path_or_url)
                    for path_or_url in self._protein_fasta_paths_or_urls
                ]
            )
        return paths

    def required_local_files_exist(self, empty_files_ok=False):
        for path in self.required_local_files():
            if not exists(path):
                return False
            if not empty_files_ok:
                if getsize(path) == 0:
                    return False
        return True

    def download(self, overwrite=False):
        """
        Download data files needed by this Genome instance.

        Parameters
        ----------
        overwrite : bool, optional
            Download files regardless whether local copy already exists.
        """
        pass

    def index(self, overwrite=False):
        """
        Assuming that all necessary data for this Genome has been downloaded,
        generate the GTF database and save efficient representation of
        FASTA sequence files.
        """
        pass

    @property
    def db(self):
        pass

    @property
    def protein_sequences(self):
        pass

    @property
    def transcript_sequences(self):
        pass

    def install_string(self):
        """
        Add every missing file to the install string shown to the user
        in an error message.
        """
        pass

    def __str__(self):
        transcript_fasta_paths_or_urls = (
            ",".join(self._transcript_fasta_paths_or_urls)
            if self._transcript_fasta_paths_or_urls is not None
            else None
        )
        protein_fasta_paths_or_urls = (
            ",".join(self._protein_fasta_paths_or_urls)
            if self._protein_fasta_paths_or_urls is not None
            else None
        )
        return (
            "Genome(reference_name=%s, "
            "annotation_name=%s, "
            "annotation_version=%s, "
            "gtf_path_or_url=%s, "
            "transcript_fasta_paths_or_urls=%s, "
            "protein_fasta_paths_or_urls=%s)"
            % (
                self.reference_name,
                self.annotation_name,
                self.annotation_version,
                self._gtf_path_or_url,
                transcript_fasta_paths_or_urls,
                protein_fasta_paths_or_urls,
            )
        )

    def __repr__(self):
        return str(self)

    def _fields(self):
        pass

    def __eq__(self, other):
        return other.__class__ is Genome and self._fields() == other._fields()

    def __hash__(self):
        return hash(self._fields())

    def clear_cache(self):
        """
        Clear any in-memory cached values
        """
        pass

    def delete_index_files(self):
        """
        Delete all data aside from source GTF and FASTA files
        """
        pass

    def _all_feature_values(
        self, column, feature, distinct=True, contig=None, strand=None
    ):
        """
        Cached lookup of all values for a particular feature property from
        the database, caches repeated queries in memory and
        stores them as a CSV.

        Parameters
        ----------

        column : str
            Name of property (e.g. exon_id)

        feature : str
            Type of entry (e.g. exon)

        distinct : bool, optional
            Keep only unique values

        contig : str, optional
            Restrict query to particular contig

        strand : str, optional
            Restrict results to "+" or "-" strands

        Returns a list constructed from query results.
        """
        pass

    def transcript_sequence(self, transcript_id):
        """Return cDNA nucleotide sequence of transcript, or None if
        transcript doesn't have cDNA sequence.
        """
        pass

    def protein_sequence(self, protein_id):
        """Return cDNA nucleotide sequence of transcript, or None if
        transcript doesn't have cDNA sequence.
        """
        pass

    def genes_at_locus(self, contig, position, end=None, strand=None):
        pass

    def transcripts_at_locus(self, contig, position, end=None, strand=None):
        pass

    def exons_at_locus(self, contig, position, end=None, strand=None):
        pass

    def gene_ids_at_locus(self, contig, position, end=None, strand=None):
        pass

    def gene_names_at_locus(self, contig, position, end=None, strand=None):
        pass

    def exon_ids_at_locus(self, contig, position, end=None, strand=None):
        pass

    def transcript_ids_at_locus(self, contig, position, end=None, strand=None):
        pass

    def transcript_names_at_locus(self, contig, position, end=None, strand=None):
        pass

    def protein_ids_at_locus(self, contig, position, end=None, strand=None):
        pass

    ###################################################
    #
    #         Methods which return Locus objects
    #         containing (contig, start, stop, strand)
    #         of various genomic entities
    #
    ###################################################

    def locus_of_gene_id(self, gene_id):
        """
        Given a gene ID returns Locus with: chromosome, start, stop, strand
        """
        pass

    def loci_of_gene_names(self, gene_name):
        """
        Given a gene name returns list of Locus objects with fields:
            chromosome, start, stop, strand
        You can get multiple results since a gene might have multiple copies
        in the genome.
        """
        pass

    def locus_of_transcript_id(self, transcript_id):
        pass

    def locus_of_exon_id(self, exon_id):
        """
        Given an exon ID returns Locus
        """
        pass

    ###################################################
    #
    #                  Contigs
    #
    ###################################################

    def contigs(self):
        """
        Returns all contig names for any gene in the genome
        (field called "seqname" in Ensembl GTF files)
        """
        pass

    ###################################################
    #
    #             Gene Info Objects
    #
    ###################################################

    def genes(self, contig=None, strand=None):
        """
        Returns all Gene objects in the database. Can be restricted to a
        particular contig/chromosome and strand by the following arguments:

        Parameters
        ----------
        contig : str
            Only return genes on the given contig.

        strand : str
            Only return genes on this strand.
        """
        pass

    def gene_by_id(self, gene_id):
        """
        Construct a Gene object for the given gene ID.
        """
        pass

    def genes_by_name(self, gene_name):
        """
        Get all the unqiue genes with the given name (there might be multiple
        due to copies in the genome), return a list containing a Gene object
        for each distinct ID.
        """
        pass

    def gene_by_protein_id(self, protein_id):
        """
        Get the gene ID associated with the given protein ID,
        return its Gene object
        """
        pass

    ###################################################
    #
    #             Gene Names
    #
    ###################################################

    def _query_gene_name(self, property_name, property_value, feature_type):
        pass

    def gene_names(self, contig=None, strand=None):
        """
        Return all genes in the database,
        optionally restrict to a chromosome and/or strand.
        """
        pass

    def gene_name_of_gene_id(self, gene_id):
        pass

    def gene_name_of_transcript_id(self, transcript_id):
        pass

    def gene_name_of_transcript_name(self, transcript_name):
        pass

    def gene_name_of_exon_id(self, exon_id):
        pass

    ###################################################
    #
    #             Gene IDs
    #
    ###################################################

    def _query_gene_ids(self, property_name, value, feature="gene"):
        pass

    def gene_ids(self, contig=None, strand=None):
        """
        What are all the gene IDs
        (optionally restrict to a given chromosome/contig and/or strand)
        """
        pass

    def gene_ids_of_gene_name(self, gene_name):
        """
        What are the gene IDs associated with a given gene name?
        (due to copy events, there might be multiple genes per name)
        """
        pass

    def gene_id_of_protein_id(self, protein_id):
        """
        What is the gene ID associated with a given protein ID?
        """
        pass

    ###################################################
    #
    #             Transcript Info Objects
    #
    ###################################################

    def transcripts(self, contig=None, strand=None):
        """
        Construct Transcript object for every transcript entry in
        the database. Optionally restrict to a particular
        chromosome using the `contig` argument.
        """
        pass

    def transcript_by_id(self, transcript_id):
        """Construct Transcript object with given transcript ID"""
        pass

    def transcripts_by_name(self, transcript_name):
        pass

    def transcript_by_protein_id(self, protein_id):
        pass

    ###################################################
    #
    #            Transcript Names
    #
    ###################################################

    def _query_transcript_names(self, property_name, value):
        pass

    def transcript_names(self, contig=None, strand=None):
        """
        What are all the transcript names in the database
        (optionally, restrict to a given chromosome and/or strand)
        """
        pass

    def transcript_names_of_gene_name(self, gene_name):
        pass

    def transcript_name_of_transcript_id(self, transcript_id):
        pass

    ###################################################
    #
    #            Transcript IDs
    #
    ###################################################

    def _query_transcript_ids(self, property_name, value, feature="transcript"):
        pass

    def transcript_ids(self, contig=None, strand=None):
        pass

    def transcript_ids_of_gene_id(self, gene_id):
        pass

    def transcript_ids_of_gene_name(self, gene_name):
        pass

    def transcript_ids_of_transcript_name(self, transcript_name):
        pass

    def transcript_ids_of_exon_id(self, exon_id):
        pass

    def transcript_id_of_protein_id(self, protein_id):
        """
        What is the transcript ID associated with a given protein ID?
        """
        pass

    ###################################################
    #
    #             Exon Info Objects
    #
    ###################################################

    def exons(self, contig=None, strand=None):
        """
        Create exon object for all exons in the database, optionally
        restrict to a particular chromosome using the `contig` argument.
        """
        pass

    def exon_by_id(self, exon_id):
        """Construct an Exon object from its ID by looking up the exon"s
        properties in the given Database.
        """
        pass

    ###################################################
    #
    #                Exon IDs
    #
    ###################################################

    def _query_exon_ids(self, property_name, value):
        pass

    def exon_ids(self, contig=None, strand=None):
        pass

    def exon_ids_of_gene_id(self, gene_id):
        pass

    def exon_ids_of_gene_name(self, gene_name):
        pass

    def exon_ids_of_transcript_name(self, transcript_name):
        pass

    def exon_ids_of_transcript_id(self, transcript_id):
        pass

    ###################################################
    #
    #             Protein IDs
    #
    ###################################################

    def protein_ids(self, contig=None, strand=None):
        """
        What are all the protein IDs
        (optionally restrict to a given chromosome and/or strand)
        """
        pass
