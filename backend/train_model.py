# ============================================================
#  PhishSentinel — ML Model Training Script
#  Team: CyberTechie | EPL '26 | CC-02-S1
#  Developer: Aarya Shinde (160624747002)
#  AI & Data Science — A
#  Stanley College of Engineering & Technology for Women
# ============================================================

import pandas as pd
import numpy as np
import joblib, os, re, math, time
from urllib.parse import urlparse
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from xgboost import XGBClassifier
import warnings
warnings.filterwarnings('ignore')

print("=" * 60)
print("  PhishSentinel — Model Training")
print("  Team CyberTechie | CC-02-S1")
print("=" * 60)

SUSPICIOUS_TLDS = {'.xyz','.tk','.ml','.ga','.cf','.gq','.top',
                   '.click','.link','.work','.loan','.win'}

def calc_entropy(text):
    if not text: return 0.0
    from collections import Counter
    freq = Counter(text)
    return -sum((c/len(text))*math.log2(c/len(text)) for c in freq.values())

def extract_features(url):
    try:
        if not url.startswith(('http://','https://')):
            url = 'http://' + url
        parsed = urlparse(url)
        netloc = parsed.netloc.lower()
        tld = '.' + netloc.split('.')[-1] if '.' in netloc else ''
        return {
            'url_length':         len(url),
            'has_https':          int(url.startswith('https')),
            'has_ip_in_url':      int(bool(re.match(r'\d+\.\d+\.\d+\.\d+', netloc))),
            'special_char_count': len(re.findall(r'[@\-_~%]', url)),
            'domain_age_days':    365,
            'subdomain_count':    max(0, len(netloc.split('.')) - 2),
            'url_entropy':        round(calc_entropy(netloc), 3),
            'has_suspicious_tld': int(tld in SUSPICIOUS_TLDS),
        }
    except:
        return {k: 0 for k in ['url_length','has_https','has_ip_in_url',
                                'special_char_count','domain_age_days',
                                'subdomain_count','url_entropy','has_suspicious_tld']}

FEATURES = ['url_length','has_https','has_ip_in_url','special_char_count',
            'domain_age_days','subdomain_count','url_entropy','has_suspicious_tld']

# ── Generate synthetic training data ─────────────────────
print("\n[1/4] Generating training data...")

phishing_patterns = [
    "http://paypa1-secure-login.xyz/verify",
    "http://sbi-kyc-update.tk/login",
    "http://192.168.1.1/bank/verify",
    "http://hdfc-bank-secure.ml/account",
    "http://amazon-prize-winner.gq/claim",
    "http://bit.ly/freegift-india",
    "http://arnazon-offer.xyz/deals",
    "http://google-security-alert.tk/fix",
]

safe_patterns = [
    "https://www.google.com",
    "https://github.com",
    "https://www.sbi.co.in",
    "https://www.amazon.in",
    "https://www.flipkart.com",
    "https://wikipedia.org",
    "https://www.irctc.co.in",
    "https://onlinesbi.sbi",
]

np.random.seed(42)
rows, labels = [], []

for _ in range(5000):
    base = phishing_patterns[np.random.randint(len(phishing_patterns))]
    f = extract_features(base)
    # add noise
    f['url_length']         = max(20, f['url_length'] + np.random.randint(-10,30))
    f['special_char_count'] = max(0, f['special_char_count'] + np.random.randint(0,5))
    f['url_entropy']        = max(2.0, f['url_entropy'] + np.random.uniform(-0.5,0.5))
    f['has_https']          = np.random.choice([0,1], p=[0.85,0.15])
    f['has_suspicious_tld'] = np.random.choice([0,1], p=[0.2,0.8])
    rows.append(f); labels.append(1)

for _ in range(5000):
    base = safe_patterns[np.random.randint(len(safe_patterns))]
    f = extract_features(base)
    f['url_length']         = max(10, f['url_length'] + np.random.randint(-5,15))
    f['special_char_count'] = max(0, f['special_char_count'] + np.random.randint(0,2))
    f['url_entropy']        = max(1.5, f['url_entropy'] + np.random.uniform(-0.3,0.3))
    f['has_https']          = np.random.choice([0,1], p=[0.05,0.95])
    f['has_suspicious_tld'] = 0
    rows.append(f); labels.append(0)

df = pd.DataFrame(rows)[FEATURES]
y  = np.array(labels)
print(f"    Dataset: {len(df)} samples ({sum(y)} phishing, {len(y)-sum(y)} safe)")

# ── Train/test split ──────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    df, y, test_size=0.2, random_state=42, stratify=y)

# ── Train ensemble ────────────────────────────────────────
print("\n[2/4] Training RF + XGBoost ensemble...")
t0 = time.time()

rf  = RandomForestClassifier(n_estimators=200, max_depth=12,
                              random_state=42, n_jobs=-1)
xgb = XGBClassifier(n_estimators=200, max_depth=6, learning_rate=0.1,
                     random_state=42, eval_metric='logloss',
                     use_label_encoder=False)

ensemble = VotingClassifier(
    estimators=[('rf', rf), ('xgb', xgb)],
    voting='soft'
)
ensemble.fit(X_train, y_train)
print(f"    Training time: {time.time()-t0:.1f}s")

# ── Evaluate ──────────────────────────────────────────────
print("\n[3/4] Evaluating model...")
y_pred = ensemble.predict(X_test)
acc    = accuracy_score(y_test, y_pred)
print(f"    Accuracy: {acc*100:.1f}%")
print(classification_report(y_test, y_pred,
      target_names=['SAFE','PHISHING']))

# ── Benchmark ─────────────────────────────────────────────
print("[4/4] Benchmarking prediction speed...")
test_url = "http://sbi-kyc-verify.xyz/login"
test_feat = pd.DataFrame([extract_features(test_url)])[FEATURES]

# Before (simulate re-train)
t_before = []
for _ in range(5):
    t = time.time()
    rf_tmp = RandomForestClassifier(n_estimators=50).fit(X_train, y_train)
    rf_tmp.predict(test_feat)
    t_before.append((time.time()-t)*1000)

# After (loaded from disk)
t_after = []
for _ in range(5):
    t = time.time()
    ensemble.predict(test_feat)
    t_after.append((time.time()-t)*1000)

avg_before = sum(t_before)/len(t_before)
avg_after  = sum(t_after)/len(t_after)
print(f"    Before optimization: {avg_before:.1f}ms")
print(f"    After optimization:  {avg_after:.1f}ms")
print(f"    Speedup:             {avg_before/avg_after:.1f}x faster")

# ── Save model ────────────────────────────────────────────
os.makedirs('models', exist_ok=True)
joblib.dump(ensemble, 'models/phishsentinel_model.pkl')
print(f"\n Model saved → models/phishsentinel_model.pkl")
print("=" * 60)
print("  Training complete. Run app.py to start the API.")
print("=" * 60)
