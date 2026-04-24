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

from memoized_property import memoized_property

from .common import memoize
from .exon import Exon
from .locus_with_genome import LocusWithGenome


def _merge_ranges(ranges):
    """
    Sort [(start, end)] inclusive-inclusive ranges and merge any that are
    adjacent or overlapping (end+1 == next start).
    """
    pass


class Transcript(LocusWithGenome):
    """
    Transcript encompasses the locus, exons, and sequence of a transcript.

    Lazily fetches sequence in case we"re constructing many Transcripts
    and not using the sequence, avoid the memory/performance overhead
    of fetching and storing sequences from a FASTA file.
    """

    def __init__(
        self,
        transcript_id,
        transcript_name,
        contig,
        start,
        end,
        strand,
        biotype,
        gene_id,
        genome,
        support_level=None,
    ):
        LocusWithGenome.__init__(
            self,
            contig=contig,
            start=start,
            end=end,
            strand=strand,
            biotype=biotype,
            genome=genome,
        )
        self.transcript_id = transcript_id
        self.transcript_name = transcript_name
        self.gene_id = gene_id
        self.support_level = support_level

    @property
    def id(self):
        """
        Alias for transcript_id necessary for backward compatibility.
        """
        pass

    @property
    def name(self):
        """
        Alias for transcript_name necessary for backward compatibility.
        """
        pass

    def __str__(self):
        return (
            "Transcript(transcript_id='%s',"
            " transcript_name='%s',"
            " gene_id='%s',"
            " biotype='%s',"
            " contig='%s',"
            " start=%d,"
            " end=%d, strand='%s', genome='%s')"
        ) % (
            self.transcript_id,
            self.name,
            self.gene_id,
            self.biotype,
            self.contig,
            self.start,
            self.end,
            self.strand,
            self.genome.reference_name,
        )

    def __len__(self):
        """
        Length of a transcript is the sum of its exon lengths
        """
        return sum(len(exon) for exon in self.exons)

    def __eq__(self, other):
        return (
            other.__class__ is Transcript
            and self.id == other.id
            and self.genome == other.genome
        )

    def __hash__(self):
        return hash(self.id)

    def to_dict(self):
        pass

    @property
    def gene(self):
        pass

    @property
    def gene_name(self):
        pass

    @property
    def exons(self):
        # need to look up exon_number alongside ID since each exon may
        # appear in multiple transcripts and have a different exon number
        # in each transcript.
        # Older or non-Ensembl GTFs may omit the exon_id attribute, in
        # which case we build Exon objects directly from the exon row
        # and synthesize a stable per-transcript ID.
        pass

    # possible annotations associated with transcripts
    _TRANSCRIPT_FEATURES = {"start_codon", "stop_codon", "UTR", "CDS"}

    @memoize
    def _transcript_feature_position_ranges(self, feature, required=True):
        """
        Find start/end chromosomal position range of features
        (such as start codon) for this transcript.
        """
        pass

    @memoize
    def _transcript_feature_positions(self, feature):
        """
        Get unique positions for feature, raise an error if feature is absent.
        """
        pass

    @memoize
    def _codon_positions(self, feature):
        """
        Parameters
        ----------
        feature : str
            Possible values are "start_codon" or "stop_codon"

        Returns list of three chromosomal positions.
        """
        pass

    @memoized_property
    def contains_start_codon(self):
        """
        Does this transcript have an annotated start_codon entry?
        """
        pass

    @memoized_property
    def contains_stop_codon(self):
        """
        Does this transcript have an annotated stop_codon entry?
        """
        pass

    @memoized_property
    def start_codon_complete(self):
        """
        Does the start codon span 3 genomic positions?
        """
        pass

    @memoized_property
    def start_codon_positions(self):
        """
        Chromosomal positions of nucleotides in start codon.
        """
        pass

    @memoized_property
    def stop_codon_positions(self):
        """
        Chromosomal positions of nucleotides in stop codon.
        """
        pass

    @memoized_property
    def exon_intervals(self):
        """List of (start,end) tuples for each exon of this transcript,
        in the order specified by the 'exon_number' column of the
        exon table.
        """
        pass

    def spliced_offset(self, position):
        """
        Convert from an absolute chromosomal position to the offset into
        this transcript"s spliced mRNA.

        Position must be inside some exon (otherwise raise exception).
        """
        pass

    @memoized_property
    def start_codon_unspliced_offsets(self):
        """
        Offsets from start of unspliced pre-mRNA transcript
        of nucleotides in start codon.
        """
        pass

    @memoized_property
    def stop_codon_unspliced_offsets(self):
        """
        Offsets from start of unspliced pre-mRNA transcript
        of nucleotides in stop codon.
        """
        pass

    def _contiguous_offsets(self, offsets):
        """
        Sorts the input list of integer offsets,
        ensures that values are contiguous.
        """
        pass

    @memoized_property
    def start_codon_spliced_offsets(self):
        """
        Offsets from start of spliced mRNA transcript
        of nucleotides in start codon.
        """
        pass

    @memoized_property
    def stop_codon_spliced_offsets(self):
        """
        Offsets from start of spliced mRNA transcript
        of nucleotides in stop codon.
        """
        pass

    @memoized_property
    def coding_sequence_position_ranges(self):
        """
        Return absolute chromosome position ranges for CDS fragments
        of this transcript, including the stop codon (which Ensembl
        encodes as a separate feature from the CDS).
        """
        pass

    @memoized_property
    def complete(self):
        """
        Consider a transcript complete if it has start and stop codons and
        a coding sequence whose length is divisible by 3
        """
        pass

    @memoized_property
    def sequence(self):
        """
        Spliced cDNA sequence of transcript
        (includes 5" UTR, coding sequence, and 3" UTR)
        """
        pass

    @memoized_property
    def first_start_codon_spliced_offset(self):
        """
        Offset of first nucleotide in start codon into the spliced mRNA
        (excluding introns)
        """
        pass

    @memoized_property
    def last_stop_codon_spliced_offset(self):
        """
        Offset of last nucleotide in stop codon into the spliced mRNA
        (excluding introns)
        """
        pass

    @memoized_property
    def coding_sequence(self):
        """
        cDNA coding sequence (from start codon to stop codon, without
        any introns)
        """
        pass

    @memoized_property
    def five_prime_utr_sequence(self):
        """
        cDNA sequence of 5' UTR
        (untranslated region at the beginning of the transcript)
        """
        pass

    @memoized_property
    def three_prime_utr_sequence(self):
        """
        cDNA sequence of 3' UTR
        (untranslated region at the end of the transcript)
        """
        pass

    @memoized_property
    def protein_id(self):
        pass

    @memoized_property
    def protein_sequence(self):
        pass
