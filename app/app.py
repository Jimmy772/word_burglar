from flask import Flask, render_template, request
import requests
import json

app = Flask(__name__)

URL = "http://localhost:5005/webhooks/rest/webhook"

def get_json(text):
    params = {
        "sender": "user",
        "message": text
    }
    r = requests.post(url=URL, data=json.dumps(params))
    response = r.json()
    response_text = response[0]["text"]
    as_json = json.loads(response_text)
    placeholder = 'https://th.bing.com/th/id/OIP.nqeqmr8ye-hJ1hoWebqf0QAAAA?rs=1&pid=ImgDetMain'
    as_json['image_urls'] = [placeholder if value is None else
                             value for value in as_json["image_urls"]]
    return as_json

# edit this code
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_books', methods=['POST'])
def get_books():
    if request.method == 'POST':
        text = str(request.form['text'])
        result = get_json(text)
        return render_template('index.html', result=result, zip=zip)
    
if __name__ == '__main__':
    app.run(debug=True)