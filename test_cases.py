import unittest
import pandas as pd
import os
from scraper import map_data  

class TestDataMapping(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Create mock test files
        """
        # Mock Raw Data (with duplicates)
        raw_data = pd.DataFrame({
            "lookup_key": ["A1", "A2", "A2", "A3"]
        })
        raw_data.to_csv("test_raw_data.csv", index=False)

        # Mock Reference Data
        reference_data = pd.DataFrame({
            "lookup_key": ["A1", "A2", "A3", "A4"],
            "Name": ["Alpha", "Beta", "Gamma", "Delta"],
            "Value": [100, 200, 300, 400]
        })
        reference_data.to_excel("test_reference_data.xlsx", index=False)

        # Run mapping
        map_data(
            raw_file="test_raw_data.csv",
            reference_file="test_reference_data.xlsx",
            lookup_column="lookup_key",
            output_file="test_mapped_output.csv"
        )

    def test_only_matching_rows_fetched(self):
        """
        Should only fetch rows that match raw dataset
        """
        output_df = pd.read_csv("test_mapped_output.csv")
        self.assertTrue(all(output_df["lookup_key"].isin(["A1", "A2", "A3"])))

    def test_all_reference_columns_present(self):
        """
        Output should contain all columns from reference file
        """
        output_df = pd.read_csv("test_mapped_output.csv")
        expected_columns = ["lookup_key", "Name", "Value"]
        self.assertListEqual(list(output_df.columns), expected_columns)

    def test_row_count_matches_unique_values(self):
        """
        Row count should match number of unique raw lookup values
        """
        output_df = pd.read_csv("test_mapped_output.csv")
        self.assertEqual(len(output_df), 3)  # A1, A2, A3

    def test_no_duplicates_in_output(self):
        """
        Output should not contain duplicates even if raw had duplicates
        """
        output_df = pd.read_csv("test_mapped_output.csv")
        self.assertEqual(len(output_df["lookup_key"].unique()), len(output_df))

    @classmethod
    def tearDownClass(cls):
        """
        Clean up test files
        """
        files_to_remove = [
            "test_raw_data.csv",
            "test_reference_data.xlsx",
            "test_mapped_output.csv",
            "unmatched_records.csv",
            "mapping_summary.csv"
        ]
        for file in files_to_remove:
            if os.path.exists(file):
                os.remove(file)


if __name__ == "__main__":
    unittest.main()
