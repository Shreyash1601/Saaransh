from flask import Flask, jsonify,request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def getText():
    url=request.json["url"]
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    text_elements = soup.find_all(['p','pre', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    extracted_text = ' '.join([element.get_text() for element in text_elements])
    return extracted_text


@app.route("/")
def welcome():
    return "Welcome to Saaransh backend!!!"

@app.route("/getdata",methods=['POST','GET'])
def getData():
    text=getText()
    Webtext=jsonify({
        "text":text
    })
    Webtext.headers.add("Access-Control-Allow-Origin","*")
    return Webtext
@app.route("/getsummaryp",methods=['POST','GET'])
def get_summary():
    text=getText()
    openai_api_key = "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"
    URL = "https://api.openai.com/v1/chat/completions"
    payload = {"model": "gpt-3.5-turbo", "temperature" : 1.0, "messages" : [{"role": "user", "content": f"Summarize the following text give answer in maximum 50 words: {text}"}]}
    headers = {"Content-Type": "application/json","Authorization": f"Bearer {openai_api_key}"}
    response = requests.post(URL, json=payload, headers=headers)
    response_data = response.json()
    result= jsonify({
        "summaryP":response_data['choices'][0]['message']['content']
        })
    result.headers.add("Access-Control-Allow-Origin","*")
    return result


@app.route("/getsummarypoints",methods=['POST','GET'])
def get_major_points():
    text=getText()
    openai_api_key = "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"
    URL = "https://api.openai.com/v1/chat/completions"
    payload = {"model": "gpt-3.5-turbo", "temperature" : 1.0, "messages" : [{"role": "user", "content": f"Provide major points around 4-5 for the following text: {text}"}]}
    headers = {"Content-Type": "application/json","Authorization": f"Bearer {openai_api_key}"}
    response = requests.post(URL, headers=headers, json=payload)
    response = response.json()
    print(response['choices'][0]['message']['content'])
    summaryPoints=jsonify({
        "summarypoints":response['choices'][0]['message']['content']
        })
    summaryPoints.headers.add("Access-Control-Allow-Origin","*")
    return summaryPoints
    







if __name__=="__main__":
    app.run(debug=True)