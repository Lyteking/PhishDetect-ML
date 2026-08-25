from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import pandas as pd

from feature_extractor import extract_features

app = FastAPI(title="PhishDetect ML API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the new XGBoost model from the README implementation
try:
    xgb_model = joblib.load('XGBoostClassifier.pickle.dat')
    print("✅ XGBoost Model loaded successfully.")
except Exception as e:
    print(f"⚠️ Warning: Model file not found. {e}")
    xgb_model = None

class URLRequest(BaseModel):
    url: str

@app.post("/predict")
async def predict_phishing(request: URLRequest):
    url = request.url
    print(f"\n--- Scanning URL: {url} ---")
    
    try:
        # Extract the 17 features
        raw_features = extract_features(url)
        
        # Hardcoded Whitelist (Ultimate safeguard for major sites)
        safe_domains = ['google.com', 'github.com', 'youtube.com', 'facebook.com', 'twitter.com', 'apple.com']
        is_whitelisted = any(safe_domain in url.lower() for safe_domain in safe_domains)

        if is_whitelisted:
            is_phishing = False
            probability = 0.99
            print("✅ Domain is whitelisted as SAFE.")
            
        elif xgb_model:
            # Enforce 17 column order
            columns_order = [
                'have_ip', 'url_length', 'tiny_url', 'have_at', 'redirection', 
                'prefix_suffix', 'sub_domains', 'https_domain', 'suspicious_words', 
                'dns_record', 'domain_age', 'domain_end', 'web_traffic', 'iframe', 
                'mouse_over', 'right_click', 'web_forwards'
            ]
            
            feature_df = pd.DataFrame([raw_features], columns=columns_order)
            
            # Predict (0 = Safe, 1 = Phishing)
            prediction = xgb_model.predict(feature_df)[0]
            probabilities = xgb_model.predict_proba(feature_df)[0]
            
            is_phishing = bool(prediction == 1)
            probability = probabilities[1] if is_phishing else probabilities[0]
            
            print(f"🤖 Model Raw Prediction: {prediction} (0=Safe, 1=Phishing)")
            print(f"📊 Confidence: {probability * 100:.2f}%")
            
        else:
            # Fallback if model isn't loaded
            is_phishing = "login" in url or "update" in url
            probability = 0.98 if is_phishing else 0.85
            
        return {
            "url": url,
            "isPhishing": is_phishing,
            "confidence": float(probability),
            "features": raw_features,
            "timestamp": pd.Timestamp.now().isoformat()
        }
        
    except Exception as e:
        print(f"❌ Error during inference: {e}")
        raise HTTPException(status_code=500, detail=str(e))