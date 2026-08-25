from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np
import shap
import lime
import lime.lime_tabular

from feature_extractor import extract_features

app = FastAPI(title="PhishDetect ML API with XAI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

FEATURE_NAMES = [
    'have_ip', 'url_length', 'tiny_url', 'have_at', 'redirection', 
    'prefix_suffix', 'sub_domains', 'https_domain', 'suspicious_words', 
    'dns_record', 'domain_age', 'domain_end', 'web_traffic', 'iframe', 
    'mouse_over', 'right_click', 'web_forwards'
]

try:
    xgb_model = joblib.load('XGBoostClassifier.pickle.dat')
    print("✅ XGBoost Model loaded successfully.")
    
    shap_explainer = shap.TreeExplainer(xgb_model)
    
    dummy_training_data = np.random.randint(2, size=(100, 17))
    lime_explainer = lime.lime_tabular.LimeTabularExplainer(
        training_data=dummy_training_data,
        feature_names=FEATURE_NAMES,
        class_names=['Legitimate', 'Phishing'],
        mode='classification'
    )
    
except Exception as e:
    print(f"⚠️ Warning: Model file not found or failed to load. {e}")
    xgb_model = None

class URLRequest(BaseModel):
    url: str

def predict_proba_wrapper(features_matrix):
    feature_df = pd.DataFrame(features_matrix, columns=FEATURE_NAMES)
    return xgb_model.predict_proba(feature_df)

@app.post("/predict")
async def predict_phishing(request: URLRequest):
    url = request.url
    print(f"\n--- Scanning URL: {url} ---")
    
    try:
        raw_features = extract_features(url)
        
        # safe_domains = ['google.com', 'github.com', 'youtube.com', 'facebook.com', 'twitter.com', 'apple.com']
        # is_whitelisted = any(safe_domain in url.lower() for safe_domain in safe_domains)
        is_whitelisted = False # Force everything to go through the ML model!

        if is_whitelisted:
            print("✅ Domain is whitelisted as SAFE.")
            return {
                "url": url,
                "isPhishing": False,
                "confidence": 0.99,
                "features": raw_features,
                "xai_diagnostics": {
                    "shap_values": {feature: 0.0 for feature in FEATURE_NAMES},
                    "lime_top_features": {"Whitelisted Domain": 1.0}
                },
                "timestamp": pd.Timestamp.now().isoformat()
            }
            
        elif xgb_model:
            feature_df = pd.DataFrame([raw_features], columns=FEATURE_NAMES)
            
            prediction = xgb_model.predict(feature_df)[0]
            probabilities = xgb_model.predict_proba(feature_df)[0]
            
            is_phishing = bool(prediction == 1)
            phishing_prob = float(probabilities[1]) 
            
            print(f"🤖 Model Raw Prediction: {prediction} (0=Safe, 1=Phishing)")
            print(f"📊 Confidence (Phishing Probability): {phishing_prob * 100:.2f}%")
            
            shap_values = shap_explainer.shap_values(feature_df)
            shap_dict = {FEATURE_NAMES[i]: float(shap_values[0][i]) for i in range(17)}
            
            lime_exp = lime_explainer.explain_instance(
                data_row=feature_df.iloc[0].values, 
                predict_fn=predict_proba_wrapper,
                num_features=5 
            )
            lime_dict = {feature: float(weight) for feature, weight in lime_exp.as_list()}
            
            return {
                "url": url,
                "isPhishing": is_phishing,
                "confidence": float(probabilities[1] if is_phishing else probabilities[0]),
                "features": raw_features,
                "xai_diagnostics": {
                    "shap_values": shap_dict,
                    "lime_top_features": lime_dict
                },
                "timestamp": pd.Timestamp.now().isoformat()
            }
            
        else:
            is_phishing = "login" in url or "update" in url
            probability = 0.98 if is_phishing else 0.85
            return {
                "url": url,
                "isPhishing": is_phishing,
                "confidence": float(probability),
                "features": raw_features,
                "xai_diagnostics": {},
                "timestamp": pd.Timestamp.now().isoformat()
            }
            
    except Exception as e:
        print(f"❌ Error during inference: {e}")
        raise HTTPException(status_code=500, detail=str(e))