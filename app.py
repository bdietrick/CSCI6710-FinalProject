from flask import Flask, render_template, jsonify, json, request, redirect, url_for
import os
import util

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/items', methods=['GET'])
def get_items():
    return render_template('items.html')

@app.route('/item', methods=['GET'])
def get_item():
    return render_template('item.html')

@app.route('/createitem', methods=['GET','POST'])
def create_item():
    return render_template('createitem.html')

@app.route('/articles', methods=['GET'])
def get_articles():
    return render_template('articles.html')

@app.route('/article', methods=['GET'])
def get_article():
    return render_template('article.html')

@app.route('/createarticle', methods=['GET','POST'])
def create_article():
    return render_template('createarticle.html')

if __name__ == '__main__':
    app.debug = True
    ip = '127.0.0.1'
    port = 5000
    app.run(host=ip, port=port)
