import pandas as pd
import numpy as np
import joblib
import urllib.request
import io
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, matthews_corrcoef
from xgboost import XGBClassifier
from imblearn.over_sampling import SMOTE
from scipy.io import arff

def download_uci_dataset():
    print("Downloading dataset from UCI Machine Learning Repository...")
    url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00327/Training%20Dataset.arff"
    
    # Download the ARFF file and decode the bytes to a string
    response = urllib.request.urlopen(url)
    content = response.read().decode('utf-8')
    
    # Pass the decoded string to arff using io.StringIO
    data, meta = arff.loadarff(io.StringIO(content))
    
    # Convert to Pandas DataFrame
    df = pd.DataFrame(data)
    
    # The UCI dataset decodes bytes to strings, we need to convert them to integers
    for col in df.columns:
        df[col] = df[col].astype(int)
        
    return df

def train_and_save_model():
    # 1. Load Dataset
    df = download_uci_dataset()
    print(f"Dataset loaded successfully with {len(df)} records.")
    
    # 2. Preprocessing & Splitting
    # The target column in the UCI dataset is 'Result'
    X = df.drop(columns=['Result'])
    
    # Map the target variable: Convert -1 (Legitimate) to 0, keep 1 (Phishing) as 1
    y = df['Result'].apply(lambda x: 0 if x == -1 else 1)
    
    # 3. Handle Class Imbalance using SMOTE
    print("Applying SMOTE to balance classes...")
    smote = SMOTE(random_state=42)
    X_resampled, y_resampled = smote.fit_resample(X, y)
    
    # 4. Train-Test Split (80/20)
    X_train, X_test, y_train, y_test = train_test_split(
        X_resampled, y_resampled, test_size=0.20, random_state=42, stratify=y_resampled
    )
    
    # 5. Define the Classifiers
    print("Initializing Random Forest and XGBoost classifiers...")
    rf_model = RandomForestClassifier(n_estimators=100, max_depth=15, random_state=42)
    
    # XGBoost needs specific parameter tuning for best results on this dataset
    xgb_model = XGBClassifier(
        n_estimators=100, 
        learning_rate=0.1, 
        max_depth=6, 
        random_state=42,
        use_label_encoder=False,
        eval_metric='logloss'
    )
    
    # 6. Build the Hybrid Voting Ensemble
    print("Training the Hybrid Voting Ensemble...")
    ensemble_model = VotingClassifier(
        estimators=[('rf', rf_model), ('xgb', xgb_model)],
        voting='soft' # Soft voting uses predicted probabilities for better accuracy
    )
    
    # Train the model
    ensemble_model.fit(X_train, y_train)
    
    # 7. Evaluate the Model
    print("\n--- Evaluating Model Performance ---")
    y_pred = ensemble_model.predict(X_test)
    
    acc = accuracy_score(y_test, y_pred)
    mcc = matthews_corrcoef(y_test, y_pred)
    
    print(f"Accuracy: {acc * 100:.2f}%")
    print(f"MCC Score: {mcc:.3f}\n")
    
    print("Classification Report:")
    print(classification_report(y_test, y_pred, target_names=["Legitimate", "Phishing"]))
    
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    
    # 8. Export the Trained Model
    model_filename = 'hybrid_ensemble_model.pkl'
    joblib.dump(ensemble_model, model_filename)
    print(f"\nSuccess! Model saved to your directory as '{model_filename}'.")

if __name__ == "__main__":
    train_and_save_model()