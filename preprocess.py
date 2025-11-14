import pandas as pd
import numpy as np
import os
import argparse
import logging
from sklearn.model_selection import train_test_split

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def clean_data(df):
    logging.info("Starting data cleaning...")
    df.replace('?', np.nan, inplace=True)
    df.dropna(subset=['race', 'gender'], inplace=True) # Minimal drop for sample data
    
    cols_to_drop = [] # No irrelevant columns in sample data
    df.drop(columns=cols_to_drop, inplace=True, errors='ignore')

    df = df[df['gender'] != 'Unknown/Invalid']
    
    numeric_cols = ['time_in_hospital', 'num_lab_procedures', 'num_medications', 'number_inpatient']
    for col in numeric_cols:
        df[col] = df[col].fillna(df[col].median())

    logging.info(f"Cleaned dataset shape: {df.shape}")
    return df

def feature_engineer(df):
    logging.info("Starting feature engineering and encoding...")

    df['target'] = df['readmitted'].apply(lambda x: 1 if x == '<30' else 0)
    df.drop(columns=['readmitted'], inplace=True)
    
    categorical_cols = df.select_dtypes(include=['object']).columns
    df = pd.get_dummies(df, columns=categorical_cols, drop_first=True)

    logging.info(f"Feature engineered dataset shape: {df.shape}")
    return df

def split_and_save_data(df, base_output_dir):
    logging.info("Splitting data into train, validation, and test sets...")

    X = df.drop('target', axis=1)
    y = df['target']

    # 60/20/20 split
    X_train_val, X_test, y_train_val, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    X_train, X_val, y_train, y_val = train_test_split(
        X_train_val, y_train_val, test_size=0.25, random_state=42, stratify=y_train_val
    )

    train_df = pd.concat([y_train, X_train], axis=1)
    val_df = pd.concat([y_val, X_val], axis=1)
    test_df = pd.concat([y_test, X_test], axis=1)

    os.makedirs(base_output_dir, exist_ok=True)
    
    train_df.to_csv(os.path.join(base_output_dir, 'train.csv'), index=False, header=True)
    val_df.to_csv(os.path.join(base_output_dir, 'validation.csv'), index=False, header=True)
    test_df.to_csv(os.path.join(base_output_dir, 'test.csv'), index=False, header=True)

    logging.info(f"Train data saved: {train_df.shape}")
    logging.info(f"Validation data saved: {val_df.shape}")
    logging.info(f"Test data saved: {test_df.shape}")
    
def main():
    parser = argparse.ArgumentParser(description="Data Preprocessing script.")
    parser.add_argument('--input-path', type=str, default='data/diabetic_data.csv')
    parser.add_argument('--output-dir', type=str, default='data/processed')
    args = parser.parse_args()
    
    if not os.path.exists(args.input_path):
        logging.error(f"Input file not found at {args.input-path}")
        return

    df = pd.read_csv(args.input_path)
    df_cleaned = clean_data(df)
    df_features = feature_engineer(df_cleaned)
    
    split_and_save_data(df_features, args.output_dir)
    logging.info("Data Preprocessing script finished.")

if __name__ == "__main__":
    main()
