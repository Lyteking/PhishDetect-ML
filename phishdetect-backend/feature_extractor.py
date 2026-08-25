import re
from urllib.parse import urlparse

def extract_features(url: str) -> dict:
    """
    Extracts 17 Features as per the README architecture.
    0 = Legitimate/Safe
    1 = Phishing/Suspicious
    """
    if not url.startswith('http://') and not url.startswith('https://'):
        url = 'http://' + url
        
    parsed = urlparse(url)
    domain = parsed.netloc.lower()
    path = parsed.path.lower()
    
    # --- 1 to 9: Address Bar Based Features ---
    # 1. IP Address in URL
    have_ip = 1 if re.search(r'\d+\.\d+\.\d+\.\d+', domain) else 0
    
    # 2. URL Length (Phishing URLs are often very long to hide the domain)
    url_length = 1 if len(url) >= 54 else 0
    
    # 3. TinyURL / Shortening Service
    shorteners = ['bit.ly', 'tinyurl', 'goo.gl', 't.co', 'ow.ly', 'is.gd', 'buff.ly', 'cutt.ly']
    tiny_url = 1 if any(s in domain for s in shorteners) else 0
    
    # 4. '@' Symbol (Used to ignore the first part of a URL)
    have_at = 1 if '@' in url else 0
    
    # 5. Redirecting '//' (Position of // after the initial https://)
    redirection = 1 if url.rfind('//') > 7 else 0
    
    # 6. Prefix/Suffix '-' in domain (Common in phishing to spoof brands)
    prefix_suffix = 1 if '-' in domain else 0
    
    # 7. Sub-domains (More than 1 subdomain = suspicious)
    dots = domain.replace('www.', '').count('.')
    sub_domains = 1 if dots > 1 else 0
    
    # 8. HTTPS token in domain (e.g., http://https-paypal.com)
    https_domain = 1 if 'https' in domain else 0
    
    # 9. Phishing Keywords in URL
    keywords = ['login', 'verify', 'update', 'secure', 'account', 'banking', 'auth', 'confirm']
    suspicious_words = 1 if any(kw in url.lower() for kw in keywords) else 0

    # --- 10 to 13: Domain Based Features (Simulated for speed) ---
    # 10. DNS Record (Assuming 0 for standard URLs, 1 if structural anomalies exist)
    dns_record = 1 if have_ip == 1 or prefix_suffix == 1 else 0
    # 11. Domain Age (Simulated: suspicious domains act "new")
    domain_age = 1 if suspicious_words == 1 and sub_domains == 1 else 0
    # 12. Domain End (Suspicious TLDs)
    sketchy_tlds = ['.xyz', '.top', '.info', '.club', '.tk']
    domain_end = 1 if any(domain.endswith(tld) for tld in sketchy_tlds) else 0
    # 13. Web Traffic (Simulated: unknown traffic for sketchy URLs)
    web_traffic = 1 if tiny_url == 1 or prefix_suffix == 1 else 0

    # --- 14 to 17: HTML & JS Based Features (Lexical fallback) ---
    # Since we aren't downloading the HTML, we flag these if the URL is highly obfuscated
    iframe = 1 if redirection == 1 else 0
    mouse_over = 1 if have_at == 1 else 0
    right_click = 0 # Assume safe by default
    web_forwards = 1 if redirection == 1 or tiny_url == 1 else 0

    # Compile the 17 features
    return {
        'have_ip': have_ip,
        'url_length': url_length,
        'tiny_url': tiny_url,
        'have_at': have_at,
        'redirection': redirection,
        'prefix_suffix': prefix_suffix,
        'sub_domains': sub_domains,
        'https_domain': https_domain,
        'suspicious_words': suspicious_words,
        'dns_record': dns_record,
        'domain_age': domain_age,
        'domain_end': domain_end,
        'web_traffic': web_traffic,
        'iframe': iframe,
        'mouse_over': mouse_over,
        'right_click': right_click,
        'web_forwards': web_forwards
    }