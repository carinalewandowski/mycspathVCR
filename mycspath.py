from flask import Flask
app = Flask(__name__)

@app.route('/')
def welcome():
    return 'Welcome to myCOSPath.'

# from https://stackabuse.com/deploying-a-flask-application-to-heroku/
if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)