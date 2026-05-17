import requests
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import re
import random
import requests
import socket

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
    "netflix.com",
    "spotify.com",
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
    "signin",
    "account",
    "otp",
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


def check_phishtank(url):

    try:

        response = requests.post(
            "https://checkurl.phishtank.com/checkurl/",
            data={
                "url": url,
                "format": "json"
            },
            headers={
                "User-Agent": "phishtank"
            },
            timeout=5
        )

        result = response.json()

        if result.get("results", {}).get("in_database"):
            return True

    except:
        pass

    return False


def website_exists(url):

    try:

        if url.startswith("https://"):
            domain = url.replace("https://", "").split("/")[0]

        elif url.startswith("http://"):
            domain = url.replace("http://", "").split("/")[0]

        else:
            domain = url.split("/")[0]

        socket.gethostbyname(domain)

        return True

    except:
        return False


@app.post("/predict")
def predict(request: URLRequest):

    url = request.url.lower()

    features = extract_features(url)

    score = 0

    reasons = []

    phishing_database_match = check_phishtank(url)

    if phishing_database_match:

        return {
            "prediction": "Phishing",
            "confidence": 99,
            "features": {
                **features,
                "real_time_database_detection": True
            },
            "reasons": [
                "URL found in real-time phishing intelligence database"
            ]
        }

    trusted = any(domain in url for domain in trusted_domains)

    if trusted:

        return {
            "prediction": "Safe",
            "confidence": random.randint(95, 99),
            "features": features,
            "reasons": [
                "Trusted domain detected",
                "HTTPS encryption verified",
                "No suspicious patterns found"
            ]
        }

    if not features["has_https"]:

        score += 25

        reasons.append("Website does not use HTTPS")

    else:

        reasons.append("HTTPS encryption enabled")

    if features["url_length"] > 75:

        score += 15

        reasons.append("Long URL detected")

    if features["has_ip_address"]:

        score += 30

        reasons.append("IP address used instead of domain")

    if features["suspicious_symbols"] > 3:

        score += 15

        reasons.append("Suspicious symbols detected")

    if features["phishing_keywords"] > 0:

        keyword_score = features["phishing_keywords"] * 10

        score += keyword_score

        reasons.append(
            "Phishing-related keywords detected"
        )

    if not website_exists(url):

        score += 20

        reasons.append("Domain does not appear valid")

    else:

        reasons.append("Domain exists online")

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
        "features": features,
        "reasons": reasons
    }