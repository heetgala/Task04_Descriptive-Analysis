import csv
import math
from collections import defaultdict
import os
print("Current Working Directory:", os.getcwd())
os.chdir("c:/Research/New folder/")
# List of dataset file names
dataset_file_paths = [
    "2024_fb_ads_president_scored_anon.csv",
    "2024_fb_posts_president_scored_anon.csv",
    "2024_tw_posts_president_scored_anon.csv"
]

# Utility to check if a value is numeric
def is_float(value):
    try:
        float(value)
        return True
    except:
        return False

# Compute basic statistics for numeric columns
def compute_basic_statistics(values):
    numeric_values = [float(val) for val in values if is_float(val)]
    count = len(numeric_values)
    if count == 0:
        return None
    mean_val = sum(numeric_values) / count
    min_val = min(numeric_values)
    max_val = max(numeric_values)
    std_dev = math.sqrt(sum((x - mean_val) ** 2 for x in numeric_values) / count)
    return {
        'count': count,
        'mean': round(mean_val, 2),
        'min': round(min_val, 2),
        'max': round(max_val, 2),
        'std_dev': round(std_dev, 2)
    }

# Count number of unique values in a column
def count_unique_values(values):
    return len(set(values))

# Analyze all columns for summary statistics
def analyze_column_statistics(rows, label=""):
    if not rows:
        print(f"\n{label} — No data.\n")
        return

    print(f"\n{label} — Numeric and Categorical Summary:")
    column_values = {col: [] for col in rows[0]}
    for row in rows:
        for col, val in row.items():
            column_values[col].append(val)

    for column_name, values in column_values.items():
        if all(is_float(val) or val.strip() == '' for val in values):
            stats = compute_basic_statistics(values)
            if stats:
                print(f"\nColumn: {column_name}")
                for stat_name, stat_val in stats.items():
                    print(f"  {stat_name}: {stat_val}")
        else:
            unique_count = count_unique_values(values)
            print(f"\nColumn: {column_name}")
            print(f"  unique values: {unique_count}")

# Group dataset rows by one or two columns
def group_rows_by_keys(rows, primary_key, secondary_key=None):
    grouped_data = defaultdict(list)
    for row in rows:
        if secondary_key:
            key = (row.get(primary_key), row.get(secondary_key))
        else:
            key = row.get(primary_key)
        grouped_data[key].append(row)
    return grouped_data

# MAIN SCRIPT
for dataset_path in dataset_file_paths:
    print(f"\n\n====================== Analyzing: {dataset_path} ======================\n")

    try:
        with open(dataset_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            data_rows = list(reader)

        if not data_rows:
            print("Empty dataset. Skipping.")
            continue

        print(f"Total rows loaded: {len(data_rows)}")

        # 1. Full dataset summary
        analyze_column_statistics(data_rows, label="Overall Dataset Summary")

        # 2. Grouped by 'page_id'
        if 'page_id' in data_rows[0]:
            page_groups = group_rows_by_keys(data_rows, 'page_id')
            print("\nGrouped by 'page_id' — Showing first 3 groups:")
            for i, (page_id_val, group) in enumerate(page_groups.items()):
                if i >= 3:
                    break
                print(f"\n--- Group: page_id = {page_id_val} ---")
                analyze_column_statistics(group, label=f"page_id = {page_id_val}")

        # 3. Grouped by 'page_id' and 'ad_id'
        if 'page_id' in data_rows[0] and 'ad_id' in data_rows[0]:
            page_ad_groups = group_rows_by_keys(data_rows, 'page_id', 'ad_id')
            print("\nGrouped by ('page_id', 'ad_id') — Showing first 3 groups:")
            for i, ((page_id_val, ad_id_val), group) in enumerate(page_ad_groups.items()):
                if i >= 3:
                    break
                print(f"\n--- Group: (page_id, ad_id) = ({page_id_val}, {ad_id_val}) ---")
                analyze_column_statistics(group, label=f"(page_id, ad_id) = ({page_id_val}, {ad_id_val})")

    except FileNotFoundError:
        print(f"File not found: {dataset_path}")
    except Exception as error:
        print(f"Error processing {dataset_path}: {error}")
