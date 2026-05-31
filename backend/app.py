# ============================================================
#  PhishSentinel — Flask Backend API
#  Team: CyberTechie | EPL '26 | CC-02-S1
#  Developer: Aarya Shinde (160624747002)
#  AI & Data Science — A
#  Stanley College of Engineering & Technology for Women
# ============================================================

from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib, os, re, math
import pandas as pd
import numpy as np
from urllib.parse import urlparse
import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)
CORS(app)

# ── Load model on startup ────────────────────────────────
MODEL_PATH = 'models/phishsentinel_model.pkl'
model = None

def load_model():
    global model
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
        print("Model loaded from disk")
    else:
        print("Model not found — run train_model.py first")

load_model()

# ── Feature extraction ───────────────────────────────────
SUSPICIOUS_TLDS = {'.xyz','.tk','.ml','.ga','.cf','.gq','.top',
                   '.click','.link','.work','.loan','.win','.download'}

def calc_entropy(text):
    if not text: return 0.0
    from collections import Counter
    freq = Counter(text)
    return -sum((c/len(text))*math.log2(c/len(text)) for c in freq.values())

def extract_url_features(url: str) -> dict:
    try:
        if not url.startswith(('http://','https://')):
            url = 'http://' + url
        parsed = urlparse(url)
        netloc = parsed.netloc.lower()
        tld = '.' + netloc.split('.')[-1] if '.' in netloc else ''
        return {
            'url_length':          len(url),
            'has_https':           int(url.startswith('https')),
            'has_ip_in_url':       int(bool(re.match(r'\d+\.\d+\.\d+\.\d+', netloc))),
            'special_char_count':  len(re.findall(r'[@\-_~%]', url)),
            'domain_age_days':     365,  # placeholder — use WhoisXML API in production
            'subdomain_count':     max(0, len(netloc.split('.')) - 2),
            'url_entropy':         round(calc_entropy(netloc), 3),
            'has_suspicious_tld':  int(tld in SUSPICIOUS_TLDS),
        }
    except Exception as e:
        return {'url_length':50,'has_https':0,'has_ip_in_url':0,
                'special_char_count':3,'domain_age_days':30,
                'subdomain_count':1,'url_entropy':3.5,'has_suspicious_tld':0}

FEATURES = ['url_length','has_https','has_ip_in_url','special_char_count',
            'domain_age_days','subdomain_count','url_entropy','has_suspicious_tld']

BRAND_MAP = {
    'paypa': 'paypal.com', 'paypal': 'paypal.com',
    'sbi': 'onlinesbi.sbi', 'sbionline': 'onlinesbi.sbi',
    'hdfc': 'hdfcbank.com', 'icici': 'icicibank.com',
    'amazon': 'amazon.in', 'amaz': 'amazon.in',
    'flipkart': 'flipkart.com', 'google': 'google.com',
    'facebook': 'facebook.com', 'instagram': 'instagram.com',
    'paytm': 'paytm.com', 'phonepe': 'phonepe.com',
    'aadhaar': 'uidai.gov.in', 'irctc': 'irctc.co.in',
}

def get_safe_alternative(url: str):
    url_lower = url.lower()
    for keyword, real_url in BRAND_MAP.items():
        if keyword in url_lower and real_url not in url_lower:
            return real_url
    return None

SHAP_EXPLANATIONS = {
    'url_length':         ('URL Length',         'Unusually long URL'),
    'has_https':          ('HTTPS Status',        'No SSL certificate found'),
    'has_ip_in_url':      ('IP in URL',           'Raw IP address detected in URL'),
    'special_char_count': ('Special Characters',  'High number of suspicious characters'),
    'domain_age_days':    ('Domain Age',          'Domain registered recently'),
    'subdomain_count':    ('Subdomain Depth',     'Excessive subdomains detected'),
    'url_entropy':        ('URL Entropy',         'High randomness score in URL'),
    'has_suspicious_tld': ('Domain Extension',    'High-risk domain extension detected'),
}

# ── Input validation ─────────────────────────────────────
def validate_url(url: str):
    if not url or not url.strip():
        return False, "URL cannot be empty."
    url = url.strip()[:2048]
    if not url.startswith(('http://','https://')):
        url = 'http://' + url
    try:
        parsed = urlparse(url)
        if not parsed.netloc:
            return False, "No domain found in URL."
    except:
        return False, "URL could not be parsed."
    return True, url

# ── Safe prediction wrapper ──────────────────────────────
def safe_predict(features_df):
    try:
        if model is None:
            return {'label':'UNKNOWN','confidence':0,'error':'Model not loaded'}
        pred  = model.predict(features_df)[0]
        proba = model.predict_proba(features_df)[0]
        conf  = round(float(max(proba))*100, 1)
        return {'label':'PHISHING' if pred==1 else 'SAFE',
                'confidence':conf,'error':None}
    except Exception as e:
        return {'label':'UNKNOWN','confidence':0,'error':str(e)}

# ── Routes ───────────────────────────────────────────────
@app.route('/', methods=['GET'])
def health():
    return jsonify({'status':'PhishSentinel API running',
                    'team':'CyberTechie','version':'1.0',
                    'endpoints':['/predict-url','/predict-email',
                                 '/predict-message','/predict-bulk']})

@app.route('/predict-url', methods=['POST'])
def predict_url():
    try:
        data = request.get_json(force=True)
        if not data or 'url' not in data:
            return jsonify({'error':'Missing field: url'}), 400

        valid, result = validate_url(data['url'])
        if not valid:
            return jsonify({'error': result}), 422

        url = result
        features = extract_url_features(url)
        features_df = pd.DataFrame([features])[FEATURES]
        prediction = safe_predict(features_df)

        # Build SHAP-style reasons
        reasons = []
        f = features
        if f['has_https'] == 0:
            reasons.append({'feature':'HTTPS Status','display':'No HTTPS certificate found','score':0.71})
        if f['has_ip_in_url'] == 1:
            reasons.append({'feature':'IP in URL','display':'Raw IP address detected','score':0.68})
        if f['has_suspicious_tld'] == 1:
            reasons.append({'feature':'Domain Extension','display':'High-risk domain extension','score':0.65})
        if f['url_entropy'] > 3.8:
            reasons.append({'feature':'URL Entropy','display':f'High URL entropy score: {f["url_entropy"]}','score':0.53})
        if f['special_char_count'] > 4:
            reasons.append({'feature':'Special Characters','display':f'{f["special_char_count"]} suspicious characters','score':0.41})
        if f['url_length'] > 75:
            reasons.append({'feature':'URL Length','display':f'Unusually long URL: {f["url_length"]} chars','score':0.22})
        if f['subdomain_count'] > 2:
            reasons.append({'feature':'Subdomain Depth','display':f'Excessive subdomains: {f["subdomain_count"]}','score':0.38})

        risk_score = min(int(prediction['confidence'] * 0.95), 99) if prediction['label']=='PHISHING' else int(100 - prediction['confidence'])

        return jsonify({
            'label':            prediction['label'],
            'confidence':       prediction['confidence'],
            'risk_score':       risk_score,
            'shap_reasons':     reasons,
            'domain_info':      features,
            'safe_alternative': get_safe_alternative(url),
            'what_to_do': [
                'Do NOT click this link',
                'Do NOT enter any passwords or OTP',
                'Report at cybercrime.gov.in or call 1930',
                'Forward this warning to whoever sent you the link',
                'Share PhishSentinel with them'
            ] if prediction['label']=='PHISHING' else [],
            'privacy_note': 'This URL was analyzed in memory and never stored.',
        })
    except Exception as e:
        return jsonify({'error':'Unexpected server error'}), 500

@app.route('/predict-email', methods=['POST'])
def predict_email():
    try:
        data = request.get_json(force=True)
        if not data or 'text' not in data:
            return jsonify({'error':'Missing field: text'}), 400
        text = data['text'].strip()
        if len(text) < 10:
            return jsonify({'error':'Email text too short'}), 422

        t = text.lower()
        urgency   = [w for w in ['urgent','immediately','asap','expires','24 hours','act now','suspended','final warning'] if w in t]
        threat    = [w for w in ['suspended','terminate','delete','locked','legal action','unauthorized'] if w in t]
        financial = [w for w in ['bank','otp','password','credit card','account number','pin','verify'] if w in t]
        phishing  = [w for w in ['click here','verify your','confirm your','update your','login now'] if w in t]
        links     = len(re.findall(r'https?://', text))

        score = len(urgency)*12 + len(threat)*15 + len(financial)*10 + len(phishing)*12 + (links*8 if links>2 else 0)
        is_phishing = score >= 25
        confidence  = min(45 + score*0.7, 99)

        return jsonify({
            'label':      'PHISHING EMAIL' if is_phishing else 'LEGITIMATE',
            'confidence': round(confidence, 1),
            'risk_score': min(score, 99),
            'analysis': {
                'urgency_triggers':   urgency[:3],
                'threat_language':    threat[:3],
                'financial_triggers': financial[:3],
                'phishing_phrases':   phishing[:3],
                'external_links':     links,
            },
            'privacy_note': 'Analyzed in memory — never stored.'
        })
    except Exception as e:
        return jsonify({'error':'Unexpected server error'}), 500

@app.route('/predict-message', methods=['POST'])
def predict_message():
    try:
        data = request.get_json(force=True)
        if not data or 'message' not in data:
            return jsonify({'error':'Missing field: message'}), 400
        message = data['message'].strip()
        urls = re.findall(r'https?://[^\s]+|www\.[^\s]+|[a-zA-Z0-9-]+\.[a-zA-Z]{2,}(?:/[^\s]*)?', message)
        if not urls:
            return jsonify({'error':'No URLs found in message','urls_found':0})

        results = []
        for url in urls[:10]:
            valid, cleaned = validate_url(url)
            if valid:
                features = extract_url_features(cleaned)
                features_df = pd.DataFrame([features])[FEATURES]
                pred = safe_predict(features_df)
                results.append({'url':url,'label':pred['label'],'confidence':pred['confidence']})

        phishing_count = sum(1 for r in results if r['label']=='PHISHING')
        return jsonify({
            'urls_found':     len(urls),
            'urls_analyzed':  len(results),
            'phishing_count': phishing_count,
            'safe_count':     len(results)-phishing_count,
            'results':        results,
            'summary': f'Found {len(results)} links — {phishing_count} PHISHING, {len(results)-phishing_count} SAFE'
        })
    except Exception as e:
        return jsonify({'error':'Unexpected server error'}), 500

@app.route('/predict-bulk', methods=['POST'])
def predict_bulk():
    try:
        data = request.get_json(force=True)
        if not data or 'urls' not in data:
            return jsonify({'error':'Missing field: urls'}), 400
        urls = data['urls'][:10]
        results = []
        for url in urls:
            valid, cleaned = validate_url(url)
            if valid:
                features = extract_url_features(cleaned)
                features_df = pd.DataFrame([features])[FEATURES]
                pred = safe_predict(features_df)
                alt = get_safe_alternative(cleaned)
                results.append({
                    'url':url,'label':pred['label'],
                    'confidence':pred['confidence'],
                    'risk_score': min(int(pred['confidence']*0.95),99) if pred['label']=='PHISHING' else int(100-pred['confidence']),
                    'safe_alternative':alt
                })
        phishing = sum(1 for r in results if r['label']=='PHISHING')
        return jsonify({'total':len(results),'phishing':phishing,'safe':len(results)-phishing,'results':results})
    except Exception as e:
        return jsonify({'error':'Unexpected server error'}), 500

@app.errorhandler(400)
def bad_request(e):
    return jsonify({'error':'Bad request','detail':str(e)}), 400

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error':'Endpoint not found'}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({'error':'Internal server error. Try again.'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
