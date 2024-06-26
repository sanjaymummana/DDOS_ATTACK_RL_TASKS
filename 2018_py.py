# -*- coding: utf-8 -*-
"""2018-PY.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1_gkOfcFfORyIFD9e94dJnFLMJXxWzM-E
"""

import pandas as pd
import os

# List of file paths for the CSE-CIC-IDS2018 dataset
file_paths = ['/content/Friday-02-03-2018_TrafficForML_CICFlowMeter.csv','/content/Friday-16-02-2018_TrafficForML_CICFlowMeter.csv',
              '/content/Friday-23-02-2018_TrafficForML_CICFlowMeter.csv','/content/Thursday-01-03-2018_TrafficForML_CICFlowMeter.csv',
              '/content/Thursday-15-02-2018_TrafficForML_CICFlowMeter.csv','/content/Thursday-22-02-2018_TrafficForML_CICFlowMeter.csv',
              '/content/Wednesday-14-02-2018_TrafficForML_CICFlowMeter.csv','/content/Wednesday-21-02-2018_TrafficForML_CICFlowMeter.csv',
              '/content/Wednesday-28-02-2018_TrafficForML_CICFlowMeter.csv',
              "D:\canada dataset\Thuesday-20-02-2018_TrafficForML_CICFlowMeter.csv"]

# Verify file paths
existing_files = [file for file in file_paths if os.path.exists(file)]

# Print the existing files to verify
print("Existing files:", existing_files)

# Initialize an empty dictionary to store DataFrames
dataframes = {}

# Read each CSV file into a separate DataFrame
for file_path in existing_files:
    try:
        # Extract the file name to use as the DataFrame key
        file_name = os.path.basename(file_path).split('.')[0]
        # Read the CSV file into a DataFrame and store it in the dictionary
        dataframes[file_name] = pd.read_csv(file_path, encoding='ISO-8859-1')
        print(f"Successfully read {file_path}")
    except Exception as e:
        print(f"Error reading {file_path}: {e}")

# Concatenate all DataFrames into a single DataFrame
if dataframes:
    combined_data = pd.concat(dataframes.values(), ignore_index=True)
    # Write the combined data to a new CSV file
    combined_csv_path = r"D:\Canada dataset\CSE-CIC-IDS2018_combined.csv"
    combined_data.to_csv(combined_csv_path, index=False)
    print(f"Combined data has been written to {combined_csv_path}")
else:
    print("No files to combine.")

import pandas as pd
import numpy as np
from sklearn.feature_selection import mutual_info_classif

# Load the CSE-CIC-IDS2018 dataset
cse_cic_ids2018 = pd.read_csv('/content/D:\Canada dataset\CSE-CIC-IDS2018_combined.csv', low_memory=False)

# Display the column names
print(cse_cic_ids2018.columns)

# Specify the label column
label_column = 'Label'  # Adjust this if the label column has a different name

# Step 2: Determine the total dimensions
dim_cse_cic_ids2018 = cse_cic_ids2018.shape
print(f'Total Dimensions: {dim_cse_cic_ids2018}')

# Step 3: Count genuine and malicious samples
genuine_cse_cic_ids2018 = cse_cic_ids2018[cse_cic_ids2018[label_column] == 'BENIGN'].shape[0]
malicious_cse_cic_ids2018 = cse_cic_ids2018.shape[0] - genuine_cse_cic_ids2018

print(f'Genuine Samples: {genuine_cse_cic_ids2018}')
print(f'Malicious Samples: {malicious_cse_cic_ids2018}')

# Step 4: Calculate the percentage of TCP SYN Flood attacks
tcp_syn_flood_cse_cic_ids2018 = cse_cic_ids2018[cse_cic_ids2018[label_column].str.contains('Syn', case=False, na=False)].shape[0]
percent_tcp_syn_flood_cse_cic_ids2018 = (tcp_syn_flood_cse_cic_ids2018 / malicious_cse_cic_ids2018) * 100

print(f'TCP SYN Flood %: {percent_tcp_syn_flood_cse_cic_ids2018:.2f}%')

# Step 5: Ensure all feature columns are numeric
features_cse_cic_ids2018 = cse_cic_ids2018.drop(columns=[label_column])

# Convert all non-numeric columns to NaN
features_cse_cic_ids2018 = features_cse_cic_ids2018.apply(pd.to_numeric, errors='coerce')

# Replace infinity values with NaN
features_cse_cic_ids2018.replace([np.inf, -np.inf], np.nan, inplace=True)

# Fill NaN values with zeros
features_cse_cic_ids2018 = features_cse_cic_ids2018.fillna(0)

# Convert labels to strings to ensure consistency
labels_cse_cic_ids2018 = cse_cic_ids2018[label_column].astype(str)

# Compute information gain
info_gain_cse_cic_ids2018 = mutual_info_classif(features_cse_cic_ids2018, labels_cse_cic_ids2018)

# Create DataFrame
info_gain_df_cse_cic_ids2018 = pd.DataFrame({
    'Feature': features_cse_cic_ids2018.columns,
    'Information Gain': info_gain_cse_cic_ids2018
}).sort_values(by='Information Gain', ascending=False)

print("Top features by information gain for CSE-CIC-IDS2018:")
print(info_gain_df_cse_cic_ids2018.head())