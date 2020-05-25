# ----------------------------------------------------------------------------
# Copyright (c) 2018--, empress development team.
#
# Distributed under the terms of the Modified BSD License.
#
# ----------------------------------------------------------------------------
import unittest
import pandas as pd
from pandas.testing import assert_frame_equal
import empress.taxonomy_utils as tax_utils


class TestTaxonomyUtils(unittest.TestCase):

    def setUp(self):
        self.feature_metadata = pd.DataFrame(
            {
                "Taxonomy": [
                    (
                        "k__Bacteria; p__Bacteroidetes; c__Bacteroidia; "
                        "o__Bacteroidales; f__Bacteroidaceae; g__Bacteroides; "
                        "s__"
                    ),
                    (
                        "k__Bacteria; p__Proteobacteria; "
                        "c__Gammaproteobacteria; o__Pasteurellales; "
                        "f__Pasteurellaceae; g__; s__"
                    ),
                    (
                        "k__Bacteria; p__Bacteroidetes; c__Bacteroidia; "
                        "o__Bacteroidales; f__Bacteroidaceae; g__Bacteroides; "
                        "s__uniformis"
                    )
                ],
                "Confidence": [0.95, 0.8, 0]
            },
            index=["e", "h", "a"]
        )

    def test_split_taxonomy_no_tax_column(self):
        fm2 = self.feature_metadata.copy()
        fm2.columns = ["asdf", "ghjkl"]
        fm3 = tax_utils.split_taxonomy(fm2)
        assert_frame_equal(fm2, fm3)

    def test_split_taxonomy_multiple_tax_columns(self):
        bad_fm = self.feature_metadata.copy()
        bad_fm.columns = ["Taxonomy", "taxon"]
        # As with above, parentheses mess up regexes -- raw strings fix that
        with self.assertRaisesRegex(
            tax_utils.TaxonomyError,
            (
                "Multiple columns in the feature metadata have one of the "
                r"following names \(case insensitive\): "
                r"\('taxon', 'taxonomy'\). At most one feature metadata "
                "column can have a name from that list."
            )
        ):
            tax_utils.split_taxonomy(bad_fm)

    def test_split_taxonomy_invalid_level_column(self):
        bad_fm = self.feature_metadata.copy()
        bad_fm.columns = ["Taxonomy", "Level 20"]
        with self.assertRaisesRegex(
            tax_utils.TaxonomyError,
            (
                "The feature metadata contains a taxonomy column, but also "
                r"already contains column\(s\) starting with the text 'Level' "
                r"\(case insensitive\)."
            )
        ):
            tax_utils.split_taxonomy(bad_fm)

    def test_split_taxonomy_level_column_but_no_taxonomy_column(self):
        meh_fm = self.feature_metadata.copy()
        meh_fm.columns = ["I'm ambivalent!", "Level 20"]
        meh_fm2 = tax_utils.split_taxonomy(meh_fm)
        assert_frame_equal(meh_fm, meh_fm2)


if __name__ == "__main__":
    unittest.main()
