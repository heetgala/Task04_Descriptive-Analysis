import pandas as pd
import os

# Display current working directory
print("Current Working Directory:", os.getcwd())

# Change the working directory to where your CSV files are located
os.chdir("c:/Research/New folder/")

# List of dataset filenames to process
dataset_filenames = [
    "2024_fb_ads_president_scored_anon.csv",
    "2024_fb_posts_president_scored_anon.csv",
    "2024_tw_posts_president_scored_anon.csv"
]

# Loop through each dataset
for dataset_filename in dataset_filenames:
    print(f"\n\n====================== Analyzing: {dataset_filename} ======================\n")

    try:
        # Load the CSV file into a DataFrame
        dataset_df = pd.read_csv(dataset_filename)

        # Check if the DataFrame is empty
        if dataset_df.empty:
            print("The dataset is empty. Skipping.")
            continue

        # Display summary statistics for numeric columns
        print("Overall Summary (Numeric Columns):")
        print(dataset_df.describe(include=[float, int]))

        # Display basic stats for categorical (non-numeric) columns
        print("\nCategorical Summary:")
        for column in dataset_df.columns:
            if dataset_df[column].dtype == 'object':
                print(f"\nColumn: {column}")
                print(f"  Unique values: {dataset_df[column].nunique()}")
                print("  Most frequent value:")
                print(dataset_df[column].value_counts().head(1))

        # Group and summarize by 'page_id', if available
        if 'page_id' in dataset_df.columns:
            print("\nGrouped Summary by 'page_id' (First 3 Groups):")
            page_id_groups = dataset_df.groupby('page_id')
            for page_id_value, group_df in list(page_id_groups)[:3]:
                print(f"\nGroup: page_id = {page_id_value}")
                print(group_df.describe(include=[float, int]))

        # Group and summarize by 'page_id' and 'ad_id', if both are present
        if 'page_id' in dataset_df.columns and 'ad_id' in dataset_df.columns:
            print("\nGrouped Summary by 'page_id' and 'ad_id' (First 3 Groups):")
            page_ad_groups = dataset_df.groupby(['page_id', 'ad_id'])
            for (page_id_val, ad_id_val), group_df in list(page_ad_groups)[:3]:
                print(f"\nGroup: (page_id, ad_id) = ({page_id_val}, {ad_id_val})")
                print(group_df.describe(include=[float, int]))

    except FileNotFoundError:
        print(f"File '{dataset_filename}' not found. Skipping.")
    except Exception as error:
        print(f"An error occurred while processing '{dataset_filename}': {error}")
