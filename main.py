from flask import Flask, jsonify,request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/")
def welcome():
    return "Hello World!"

@app.route("/getdata",methods=['POST','GET'])
def getData():
    url=request.json["url"]
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    text_elements = soup.find_all(['p','pre', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    extracted_text = ' '.join([element.get_text() for element in text_elements])
    return jsonify({
        "result":extracted_text
    })







if __name__=="__main__":
    app.run(debug=True)