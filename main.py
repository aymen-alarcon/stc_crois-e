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

def preprocess_data(df):
    from sklearn.preprocessing import StandardScaler
    import matplotlib.pyplot as plt
    import seaborn as sns

    df = df.drop_duplicates()
    df = df.dropna()
    df = df.drop(columns=['Student_ID'])

    df = pd.get_dummies(df, drop_first=True)
    
    scaler = StandardScaler()
    numerical_features = df.select_dtypes(include=[np.number]).columns
    df[numerical_features] = scaler.fit_transform(df[numerical_features])

    # plt.figure(figsize=(6, 4))
    # df['Mental_Health_Risk'].value_counts().plot(kind='bar')
    # plt.title('Distribution of Mental Health Risk')
    # plt.show()

    correlation_matrix = df.corr()
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
    plt.show()

    return df


def train_model(df):
    from sklearn.model_selection import train_test_split
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.metrics import confusion_matrix, mean_squared_error, mean_absolute_error

    features = ["Years_of_Study", "Age", "Gender_Male", "Gender_Other", "Family_History_Yes", "Work_Experience_Yes", "Online_Learning_Yes"]
    target = ["Mental_health_risk"]

    X = df[features]
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_test, y_pred)
    print(mse)
    print(rmse)
    print(mae)
    print(confusion_matrix(y_test, y_pred))

    return model, X_test, y_test
train_model(preprocess_data(extract_dataset()))