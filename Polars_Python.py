import polars as pl
import os

# Display current working directory
print("Current Working Directory:", os.getcwd())

# Change the working directory to where your CSV files are located
os.chdir("c:/Research/New folder/")
# List of dataset file names to process
dataset_file_names = [
    "2024_fb_ads_president_scored_anon.csv",
    "2024_fb_posts_president_scored_anon.csv",
    "2024_tw_posts_president_scored_anon.csv"
]

# Loop through each dataset
for dataset_name in dataset_file_names:
    print(f"\n\n====================== Analyzing: {dataset_name} ======================\n")

    try:
        # Load the dataset into a Polars DataFrame
        dataset_df = pl.read_csv(dataset_name)

        # Skip if dataset is empty
        if dataset_df.is_empty():
            print("The dataset is empty. Skipping.")
            continue

        # Summary statistics for numeric columns
        print("Overall Summary (Numeric Columns):")
        print(dataset_df.describe())

        # Summary for categorical columns (count of unique values only)
        print("\nCategorical Summary (Unique Value Counts Only):")
        for column_name in dataset_df.columns:
            if dataset_df[column_name].dtype == pl.Utf8:
                try:
                    unique_value_count = dataset_df[column_name].n_unique()
                    print(f"  {column_name}: {unique_value_count} unique values")
                except Exception as error:
                    print(f"  {column_name}: Could not count unique values. Skipped. Error: {error}")

        # Grouped summary by 'page_id'
        if 'page_id' in dataset_df.columns:
            print("\nGrouped Summary by 'page_id' (First 3 Groups):")
            unique_page_ids = dataset_df['page_id'].unique().to_list()
            for page_id_val in unique_page_ids[:3]:
                page_group_df = dataset_df.filter(pl.col('page_id') == page_id_val)
                print(f"\nGroup: page_id = {page_id_val}")
                print(page_group_df.describe())

        # Grouped summary by ('page_id', 'ad_id')
        if 'page_id' in dataset_df.columns and 'ad_id' in dataset_df.columns:
            print("\nGrouped Summary by ('page_id', 'ad_id') (First 3 Groups):")
            unique_pairs_df = dataset_df.select(['page_id', 'ad_id']).unique()
            unique_pairs = unique_pairs_df.rows()
            for page_id_val, ad_id_val in unique_pairs[:3]:
                pair_group_df = dataset_df.filter(
                    (pl.col('page_id') == page_id_val) & (pl.col('ad_id') == ad_id_val)
                )
                print(f"\nGroup: (page_id, ad_id) = ({page_id_val}, {ad_id_val})")
                print(pair_group_df.describe())

    except FileNotFoundError:
        print(f"File '{dataset_name}' not found. Skipping.")
    except Exception as error:
        print(f"An error occurred while processing '{dataset_name}': {error}")
