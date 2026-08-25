import pandas as pd
import numpy as np
from xgboost import XGBClassifier
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, matthews_corrcoef
import re
from urllib.parse import urlparse

# --- 1. The 17-Feature Extraction Logic ---
def extract_17_features(url: str) -> dict:
    if not isinstance(url, str):
        url = str(url)
    if not url.startswith('http://') and not url.startswith('https://'):
        url = 'http://' + url
        
    try:
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
    except Exception:
        # Fallback for heavily obfuscated/malformed URLs that break urlparse
        domain = url.split('://')[-1].split('/')[0].lower()
        
    have_ip = 1 if re.search(r'\d+\.\d+\.\d+\.\d+', domain) else 0
    url_length = 1 if len(url) >= 54 else 0
    shorteners = ['bit.ly', 'tinyurl', 'goo.gl', 't.co', 'ow.ly', 'is.gd', 'buff.ly', 'cutt.ly']
    tiny_url = 1 if any(s in domain for s in shorteners) else 0
    have_at = 1 if '@' in url else 0
    redirection = 1 if url.rfind('//') > 7 else 0
    prefix_suffix = 1 if '-' in domain else 0
    
    dots = domain.replace('www.', '').count('.')
    sub_domains = 1 if dots > 1 else 0
    https_domain = 1 if 'https' in domain else 0
    
    keywords = ['login', 'verify', 'update', 'secure', 'account', 'banking', 'auth', 'confirm', 'service']
    suspicious_words = 1 if any(kw in url.lower() for kw in keywords) else 0

    dns_record = 1 if have_ip == 1 or prefix_suffix == 1 else 0
    domain_age = 1 if suspicious_words == 1 and sub_domains == 1 else 0
    sketchy_tlds = ['.xyz', '.top', '.info', '.club', '.tk', '.dev', '.site', '.online']
    domain_end = 1 if any(domain.endswith(tld) for tld in sketchy_tlds) else 0
    web_traffic = 1 if tiny_url == 1 or prefix_suffix == 1 else 0

    iframe = 1 if redirection == 1 else 0
    mouse_over = 1 if have_at == 1 else 0
    right_click = 0
    web_forwards = 1 if redirection == 1 or tiny_url == 1 else 0

    return {
        'have_ip': have_ip, 'url_length': url_length, 'tiny_url': tiny_url,
        'have_at': have_at, 'redirection': redirection, 'prefix_suffix': prefix_suffix,
        'sub_domains': sub_domains, 'https_domain': https_domain, 'suspicious_words': suspicious_words,
        'dns_record': dns_record, 'domain_age': domain_age, 'domain_end': domain_end,
        'web_traffic': web_traffic, 'iframe': iframe, 'mouse_over': mouse_over,
        'right_click': right_click, 'web_forwards': web_forwards
    }

def train_model():
    print("1. Loading the new URL dataset...")
    try:
        df = pd.read_csv('URL dataset.csv')
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return

    # 2. Balance the dataset (50,000 of each to keep training fast and prevent bias)
    print("2. Balancing dataset to 50,000 Phishing and 50,000 Legitimate URLs...")
    df_phish = df[df['type'] == 'phishing'].sample(n=50000, random_state=42, replace=True)
    df_legit = df[df['type'] == 'legitimate'].sample(n=50000, random_state=42)
    
    df_balanced = pd.concat([df_phish, df_legit])
    # Shuffle
    df_balanced = df_balanced.sample(frac=1, random_state=42).reset_index(drop=True)

    print("3. Extracting 17 features from 100,000 URLs (this may take a minute)...")
    features_list = df_balanced['url'].apply(extract_17_features).tolist()
    X = pd.DataFrame(features_list)
    
    # Map labels: 1 = Phishing, 0 = Legitimate
    y = df_balanced['type'].map({'phishing': 1, 'legitimate': 0})

    print("4. Training the XGBoost Model...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42, stratify=y)

    model = XGBClassifier(
        n_estimators=150, 
        learning_rate=0.1, 
        max_depth=6, 
        use_label_encoder=False, 
        eval_metric='logloss',
        random_state=42
    )
    
    model.fit(X_train, y_train)

    print("\n--- 5. Evaluating Model Performance ---")
    y_pred = model.predict(X_test)
    print(f"Accuracy: {accuracy_score(y_test, y_pred) * 100:.2f}%")
    print(f"MCC Score: {matthews_corrcoef(y_test, y_pred):.3f}\n")
    print(classification_report(y_test, y_pred, target_names=["Legitimate", "Phishing"]))

    # Save the model
    joblib.dump(model, 'XGBoostClassifier.pickle.dat')
    print("✅ Model successfully trained on real data and saved as 'XGBoostClassifier.pickle.dat'")

if __name__ == "__main__":
    train_model()