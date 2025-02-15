import pandas as pd

# Load all CSV files into one DataFrame
files = ['eeg_data_focus.csv', 'eeg_data_relax.csv', 'eeg_data_left.csv', 'eeg_data_right.csv']

dataframes = []
for file in files:
    df = pd.read_csv(file)
    dataframes.append(df)

combined_df = pd.concat(dataframes, ignore_index=True)

# Save combined dataset
combined_df.to_csv('eeg_combined_data.csv', index=False)

print(f"Combined dataset saved as 'eeg_combined_data.csv'")