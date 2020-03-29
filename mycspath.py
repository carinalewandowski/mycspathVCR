from flask import Flask, request, make_response, redirect, url_for
from flask import render_template, session
app = Flask(__name__, template_folder='.')

@app.route('/')
def landing():
    html = render_template('index.html')
    response = make_response(html)
    return response

@app.route('/home')
def home():
    html = render_template('home.html')
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