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

import logging
from os.path import split, join, exists, splitext
import sqlite3

import datacache
from typechecks import require_integer, require_string
from gtfparse import read_gtf, create_missing_features

from .common import memoize
from .normalization import normalize_chromosome, normalize_strand
from .locus import Locus

# any time we update the database schema, increment this version number
DATABASE_SCHEMA_VERSION = 3


logger = logging.getLogger(__name__)


class Database(object):
    """
    Wrapper around sqlite3 database so that the rest of the
    library doesn't have to worry about constructing the .db file or
    writing SQL queries directly.
    """

    def __init__(
        self,
        gtf_path,
        install_string=None,
        cache_directory_path=None,
        restrict_gtf_columns=None,
        restrict_gtf_features=None,
    ):
        """
        Parameters
        ----------
        gtf_path : str
            Path to GTF annotation file

        install_string : str
            Message to tell user if database connection is requested before
            database is created.

        cache_directory_path : str
            Path to directory where database should be written. If omitted
            then use path of GTF file.

        restrict_gtf_columns : list/set of str or None
            If provided then extract only these columns before creating
            a database.

        restrict_gtf_features : list/set of str or None
            If provided then only create tables for these features.

        """
        self.gtf_path = gtf_path
        self.restrict_gtf_columns = restrict_gtf_columns
        self.restrict_gtf_features = restrict_gtf_features
        self.gtf_directory_path, self.gtf_filename = split(self.gtf_path)
        self.gtf_base_filename = splitext(self.gtf_filename)[0]

        # if cache directory isn't given then put cached files
        # alongside the GTF
        if cache_directory_path:
            self.cache_directory_path = cache_directory_path
        else:
            self.cache_directory_path = self.gtf_directory_path

        self.install_string = install_string
        self._connection = None
        # dictionary mapping table names to sets of columns
        self._columns = {}
        self._query_cache = {}

    def __eq__(self, other):
        return other.__class__ is Database and self.gtf_path == other.gtf_path

    def __str__(self):
        return "Database(gtf_path=%s)" % (self.gtf_path,)

    def __hash__(self):
        return hash((self.gtf_path))

    @property
    def local_db_filename(self):
        pass

    @property
    def local_db_path(self):
        pass

    def _all_possible_indices(self, column_names):
        """
        Create list of tuples containing all possible index groups
        we might want to create over tables in this database.

        If a set of genome annotations is missing some column we want
        to index on, we have to drop any indices which use that column.

        A specific table may later drop some of these indices if they're
        missing  values for that feature or are the same as the table's primary key.
        """
        pass

    # mapping from database tables to their primary keys
    # sadly exon IDs *are* not unique, so can't be in this dict
    PRIMARY_KEY_COLUMNS = {"gene": "gene_id", "transcript": "transcript_id"}

    def _get_primary_key(self, feature_name, feature_df):
        """Name of primary key for a feature table (e.g. "gene" -> "gene_id")

        Since we're potentially going to run this code over unseen data,
        make sure that the primary is unique and never null.

        If a feature doesn't have a primary key, return None.
        """
        pass

    def _feature_indices(self, all_index_groups, primary_key, feature_df):
        """Choose subset of index group tuples from `all_index_groups` which are
        applicable to a particular feature (not same as its primary key, have
        non-null values).
        """
        pass

    def create(self, overwrite=False):
        """
        Create the local database (including indexing) if it's not
        already set up. If `overwrite` is True, always re-create
        the database from scratch.

        Returns a connection to the database.
        """
        pass

    def _get_connection(self):
        pass

    @property
    def connection(self):
        """
        Get a connection to the database or raise an exception
        """
        pass

    def connect_or_create(self, overwrite=False):
        """
        Return a connection to the database if it exists, otherwise create it.
        Overwrite the existing database if `overwrite` is True.
        """
        pass

    def columns(self, table_name):
        pass

    def column_exists(self, table_name, column_name):
        pass

    def column_values_at_locus(
        self,
        column_name,
        feature,
        contig,
        position,
        end=None,
        strand=None,
        distinct=False,
        sorted=False,
    ):
        """
        Get the non-null values of a column from the database
        at a particular range of loci
        """
        pass

    def distinct_column_values_at_locus(
        self, column, feature, contig, position, end=None, strand=None
    ):
        """
        Gather all the distinct values for a property/column at some specified
        locus.

        Parameters
        ----------
        column : str
            Which property are we getting the values of.

        feature : str
            Which type of entry (e.g. transcript, exon, gene) is the property
            associated with?

        contig : str
            Chromosome or unplaced contig name

        position : int
            Chromosomal position

        end : int, optional
            End position of a range, if unspecified assume we're only looking
            at the single given position.

        strand : str, optional
            Either the positive ('+') or negative strand ('-'). If unspecified
            then check for values on either strand.
        """
        pass

    def run_sql_query(self, sql, required=False, query_params=[]):
        """
        Given an arbitrary SQL query, run it against the database
        and return the results.

        Parameters
        ----------
        sql : str
            SQL query

        required : bool
            Raise an error if no results found in the database

        query_params : list
            For each '?' in the query there must be a corresponding value in
            this list.
        """
        pass

    @memoize
    def query(
        self,
        select_column_names,
        filter_column,
        filter_value,
        feature,
        distinct=False,
        required=False,
    ):
        """
        Construct a SQL query and run against the sqlite3 database,
        filtered both by the feature type and a user-provided column/value.
        """
        pass

    def query_one(
        self,
        select_column_names,
        filter_column,
        filter_value,
        feature,
        distinct=False,
        required=False,
    ):
        pass

    @memoize
    def query_feature_values(
        self, column, feature, distinct=True, contig=None, strand=None
    ):
        """
        Run a SQL query against the sqlite3 database, filtered
        only on the feature type.
        """
        pass

    def query_distinct_on_contig(self, column_name, feature, contig):
        pass

    def query_loci(self, filter_column, filter_value, feature):
        """
        Query for loci satisfying a given filter and feature type.


        Parameters
        ----------
        filter_column : str
            Name of column to filter results by.

        filter_value : str
            Only return loci which have this value in the their filter_column.

        feature : str
            Feature names such as 'transcript', 'gene', and 'exon'

        Returns list of Locus objects
        """
        pass

    def query_locus(self, filter_column, filter_value, feature):
        """
        Query for unique locus, raises error if missing or more than
        one locus in the database.

        Parameters
        ----------
        filter_column : str
            Name of column to filter results by.

        filter_value : str
            Only return loci which have this value in the their filter_column.

        feature : str
            Feature names such as 'transcript', 'gene', and 'exon'

        Returns single Locus object.
        """
        pass

    def _load_gtf_as_dataframe(self, usecols=None, features=None):
        """
        Parse this genome source's GTF file and load it as a Pandas DataFrame
        """
        pass
