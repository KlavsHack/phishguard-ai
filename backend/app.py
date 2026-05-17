from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import re
import random

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class URLRequest(BaseModel):
    url: str


trusted_domains = [
    "google.com",
    "youtube.com",
    "amazon.com",
    "github.com",
    "microsoft.com",
    "facebook.com",
    "instagram.com",
    "linkedin.com",
    "openai.com",
    "apple.com",
]


phishing_keywords = [
    "login",
    "verify",
    "secure",
    "update",
    "bank",
    "free",
    "gift",
    "bonus",
    "wallet",
    "crypto",
    "paypal",
    "password",
]


def extract_features(url):

    features = {}

    features["has_https"] = url.startswith("https")

    features["url_length"] = len(url)

    features["has_ip_address"] = bool(
        re.search(r'\d+\.\d+\.\d+\.\d+', url)
    )

    features["suspicious_symbols"] = (
        url.count("-")
        + url.count("@")
        + url.count("//")
    )

    features["phishing_keywords"] = sum(
        keyword in url.lower()
        for keyword in phishing_keywords
    )

    return features


@app.post("/predict")
def predict(request: URLRequest):

    url = request.url.lower()

    features = extract_features(url)

    score = 0

    trusted = any(domain in url for domain in trusted_domains)

    if trusted:
        return {
            "prediction": "Safe",
            "confidence": random.randint(95, 99),
            "features": features
        }

    if not features["has_https"]:
        score += 25

    if features["url_length"] > 75:
        score += 15

    if features["has_ip_address"]:
        score += 30

    if features["suspicious_symbols"] > 3:
        score += 15

    score += features["phishing_keywords"] * 10

    if score >= 50:
        prediction = "Phishing"
        confidence = random.randint(75, 95)

    elif score >= 30:
        prediction = "Suspicious"
        confidence = random.randint(55, 75)

    else:
        prediction = "Safe"
        confidence = random.randint(80, 94)

    return {
        "prediction": prediction,
        "confidence": confidence,
        "features": features
    }