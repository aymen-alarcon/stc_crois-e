import pandas as pd
import numpy as np

def extract_dataset():
    import kagglehub
    import os

    path = kagglehub.dataset_download("maqdadali/mental-health-risk-prediction-dataset-students")

    print("Dataset downloaded to:", path)
    print("Files:", os.listdir(path))

    df = pd.read_csv(os.path.join(path, "student_mental_health.csv"))
    print("Dataset shape:", df.shape)
    print("Dataset columns:", df.columns)
    print(df.head())
    print(df.info())
    return df
extract_dataset()

def preprocess_data(df):
    from sklearn.preprocessing import StandardScaler

    df = df.drop_duplicates()
    df = df.dropna()

    df = pd.get_dummies(df, drop_first=True)
    
    scaler = StandardScaler()
    numerical_features = df.select_dtypes(include=[np.number]).columns
    df[numerical_features] = scaler.fit_transform(df[numerical_features])

    print(df.shape)
    print(df.info())

    return df
preprocess_data(extract_dataset())