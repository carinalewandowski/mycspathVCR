from flask import Flask, request, make_response, redirect, url_for
from flask import render_template, session
from database import Database
from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
app = Flask(__name__, template_folder='.')

# connect to database
database = Database()

@app.route('/')
def landing():
    html = render_template('index.html')
    response = make_response(html)
    return response

@app.route('/home', methods=['GET', 'POST'])
def home():
    html = render_template('home.html')
    response = make_response(html)
    return response

@app.route('/results', methods=['GET', 'POST'])
def results():
    if request.method == 'POST':
        tags = request.form.getlist('tag')
        for tag in tags:
            print(tag)

        results = database.filter_tags(tags)
        for result in results:
            print(result.title)
        print("here")
        
        html = render_template('results.html', results=results)
        response = make_response(html)
        return response

@app.route('/about')
def about():
    html = render_template('about.html')
    response = make_response(html)
    return response

@app.route('/saved')
def saved():
    html = render_template('saved.html')
    response = make_response(html)
    return response

@app.route('/profile')
def profiles():
    html = render_template('profile.html')
    response = make_response(html)
    return response

# from https://stackabuse.com/deploying-a-flask-application-to-heroku/
if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run()