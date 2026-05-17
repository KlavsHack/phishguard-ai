import re
import requests
import whois
import tldextract
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from datetime import datetime


def has_ip(url):
    pattern = r"https?://(\d{1,3}\.){3}\d{1,3}"
    return 1 if re.search(pattern, url) else 0


def url_length(url):
    return len(url)


def has_at_symbol(url):
    return 1 if "@" in url else 0


def count_subdomains(url):
    ext = tldextract.extract(url)
    return len(ext.subdomain.split('.')) if ext.subdomain else 0


def has_https(url):
    return 1 if url.startswith("https") else 0


def domain_age(domain):
    try:
        domain_info = whois.whois(domain)
        creation_date = domain_info.creation_date

        if isinstance(creation_date, list):
            creation_date = creation_date[0]

        age = (datetime.now() - creation_date).days
        return age

    except:
        return 0


def external_scripts(url):
    try:
        response = requests.get(url, timeout=5)

        soup = BeautifulSoup(response.text, "html.parser")

        scripts = soup.find_all("script")

        external = 0

        for script in scripts:
            src = script.get("src")

            if src and "http" in src:
                external += 1

        return external

    except:
        return 0


def extract_features(url):

    parsed = urlparse(url)

    domain = parsed.netloc

    features = [
        has_ip(url),
        url_length(url),
        has_at_symbol(url),
        count_subdomains(url),
        has_https(url),
        domain_age(domain),
        external_scripts(url)
    ]

    return features