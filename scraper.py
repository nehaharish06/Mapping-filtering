import pandas as pd
import logging
import sys
import os
import time

# =====================================
# LOGGING CONFIGURATION
# =====================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("mapping_log.log"),   #  writes to file
        logging.StreamHandler(sys.stdout)         #  prints to console
    ]
)

def map_data(raw_file, reference_file, lookup_column, output_file):
    try:
        start_time = time.time()
        logging.info("===== Data Mapping Process Started =====")

        # =====================================
        # VALIDATION CHECKS
        # =====================================
        if not os.path.exists(raw_file):
            raise FileNotFoundError(f"{raw_file} not found.")
        if not os.path.exists(reference_file):
            raise FileNotFoundError(f"{reference_file} not found.")

        # Load Raw Data
        raw_df = pd.read_csv(raw_file, dtype=str)

        if lookup_column not in raw_df.columns:
            raise KeyError(f"{lookup_column} not found in raw file.")

        if raw_df.empty:
            raise ValueError("Raw file is empty.")

        total_raw_records = len(raw_df)

        # Remove duplicates
        unique_keys = raw_df[lookup_column].drop_duplicates()
        duplicate_count = total_raw_records - len(unique_keys)

        logging.info(f"Total Raw Records: {total_raw_records}")
        logging.info(f"Unique Lookup Values: {len(unique_keys)}")
        logging.info(f"Duplicate Values Removed: {duplicate_count}")

        # Load Reference Data
        reference_df = pd.read_excel(reference_file, dtype=str)

        if lookup_column not in reference_df.columns:
            raise KeyError(f"{lookup_column} not found in reference file.")

        # =====================================
        # FILTER MATCHING RECORDS
        # =====================================
        mapped_df = reference_df[
            reference_df[lookup_column].isin(unique_keys)
        ]

        # Save mapped output
        mapped_df.to_csv(output_file, index=False)

        # =====================================
        # UNMATCHED RECORDS
        # =====================================
        unmatched_values = set(unique_keys) - set(reference_df[lookup_column])
        unmatched_df = pd.DataFrame(unmatched_values, columns=[lookup_column])
        unmatched_df.to_csv("unmatched_records.csv", index=False)

        # =====================================
        # SUMMARY REPORT
        # =====================================
        summary_data = {
            "Total Raw Records": total_raw_records,
            "Unique Lookup Values": len(unique_keys),
            "Duplicate Values Removed": duplicate_count,
            "Total Matches Found": len(mapped_df),
            "Unmatched Values": len(unmatched_values),
            "Match Rate (%)": round((len(mapped_df) / len(unique_keys)) * 100, 2)
        }

        summary_df = pd.DataFrame([summary_data])
        summary_df.to_csv("mapping_summary.csv", index=False)

        # =====================================
        # PERFORMANCE METRICS
        # =====================================
        end_time = time.time()
        execution_time = round(end_time - start_time, 2)

        logging.info(f"Matched Rows: {len(mapped_df)}")
        logging.info(f"Unmatched Values: {len(unmatched_values)}")
        logging.info(f"Execution Time: {execution_time} seconds")
        logging.info("===== Data Mapping Process Completed Successfully =====")

    except Exception as e:
        logging.error(f"Error occurred: {e}")

# =====================================
# RUN SCRIPT
# =====================================
if __name__ == "__main__":
    map_data(
        raw_file="raw_data.csv",
        reference_file="reference_data.xlsx",
        lookup_column="lookup_key",
        output_file="mapped_output.csv"
    )
