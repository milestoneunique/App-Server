from flask import Flask,jsonify
from flask_cors import CORS
import requests
from lxml import html
import os

import numpy as np
app = Flask(__name__)
CORS(app)

@app.route('/')
def root():
	num = np.random.randint(100)
	d={"number":num}
	return jsonify(d)


@app.route('/gold')
def goldprice():
	page = requests.get("https://www.livechennai.com/gold_silverrate.asp")
	page_tree = html.fromstring(page.content)
	gold_price = page_tree.xpath("(//table[@class='table-price'])[2]//font")[1].text

	return jsonify({"price":float(gold_price)})


@app.route('/N-News')
def nationalNews():
	response = requests.get("https://newsapi.org/v2/top-headlines?country=in&apiKey=67919a9da672474aa169436ef82ce1f2").json()['articles']
	out = []
	for res in response:
		r = {}
		r['title'] = res['title']
		r['img'] = res['urlToImage']
		r['url'] = res['url']
		r['source'] = res['source']['name']
		out.append(r)

	return jsonify(out)

@app.route('/silver')
def silverprice():
	page = requests.get("https://www.livechennai.com/gold_silverrate.asp")
	page_tree = html.fromstring(page.content)
	silver_price = page_tree.xpath("(//table[@class='table-price'])[4]//font")[1].text
	return jsonify({"price":float(silver_price)})


port = int(os.environ.get("PORT", 5000))
app.run(debug=True,host='0.0.0.0',port=port)
