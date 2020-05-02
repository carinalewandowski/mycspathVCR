# --------------------------------------------------------------------------
#
# MyCSPath
# mycspath.py
# author: Carina Lewandowski
#
# --------------------------------------------------------------------------

from flask import Flask, request, make_response, redirect, url_for
from flask import render_template, session
from database import Database, Profiles, Paths
from CASClient import CASClient

app = Flask(__name__, template_folder='.')

# generated by os.urandom(24)
SECRET_KEY = b'2H\xe0\xac`\xa39\xd7\tn\x96K\xf8\x94b\x07\xd2O\x11\xc5\xa4x:6'
app.secret_key = SECRET_KEY

# connect to database
database = Database()
profiles = Profiles()
paths = Paths()
#db_tags = Tags()
#db_langs = Languages() 

# TESTING
# database = Database()
# results = session.query(database)
# tags = []
# tags.append("design")
# tags.append("systems")
# filtered_results = database.filter_tags(tags)
# results = []
# prerequisites = []
# for result in filtered_results:
#     results.append(result)
# for result in filtered_results:
#     prerequisites.append(result.prerequisites)
# unordered_path = database.make_bundles(results, prerequisites)
# for bundle in unordered_path:
#     print(bundle.course)
    # print(bundle.prereqs)

@app.route('/')
@app.route('/index')
def landing():
    html = render_template('index.html')
    response = make_response(html)
    return response

@app.route('/home', methods=['GET', 'POST'])
def home():
    casauth = CASClient()
    netid = casauth.authenticate().rstrip()
    #netid = "test"
    
    # get list of tags from db
    """ results = db_tags.setup()
    tags = []
    for result in results:
        tags.append(result.tag)
    tags.remove('applications')
    tags.remove('systems')
    tags.remove('theory')
    tags.sort()
    # create columns
    num_tags = len(tags)
    col_len = int(num_tags/3)
    i = 0
    tags1 = []
    tags2 = []
    tags3 = []
    while i < num_tags:
        j = 0
        while j < col_len:
            tags1.append(tags[i])
            j+=1
            i+=1
        j = 0
        while j < col_len:
            tags2.append(tags[i])
            j+=1
            i+=1
        j = 0
        while j < (num_tags - (2*col_len)):
            tags3.append(tags[i])
            j+=1
            i+=1
    # get list of languages from db
    results = db_langs.setup()
    langs = []
    for result in results:
        langs.append(result.lang)
    # create columns
    num_langs = len(langs)
    col_len = int(num_langs/2)
    i = 0
    langs1 = []
    langs2 = []
    while i < num_langs:
        j = 0
        while j < col_len:
            langs1.append(langs[i])
            j+=1
            i+=1
        j = 0
        while j < (num_langs - col_len):
            langs2.append(langs[i])
            j+=1
            i+=1 """
    tags1 = ['3D modeling', 'GUI programming', 'NLP', 'NP-completeness', 'animation', 'architecture', 'art', 'artificial intelligence', 'assembly language', 'astronomy', 'astrophysics', 'bioengineering', 'biology', 'business', 'chemistry', 'compilers', 'computation', 'computer architecture', 'computer vision', 'cryptocurrencies and blockchains', 'cryptography', 'data science/analysis', 'data structures']
    tags2 = ['database programming', 'deep learning', 'design', 'distributed systems', 'ecology', 'economics', 'electrical engineering', 'energy', 'environmental systems', 'finance', 'functional programming', 'general programming', 'geometry', 'graphics', 'healthcare', 'image processing', 'intellectual property', 'language', 'linear algebra', 'machine language', 'machine learning', 'mathematics', 'mechanical & aerospace engineering']
    tags3 = ['music', 'nanofabrication', 'network programming', 'networking', 'neuroscience', 'neural networks', 'operating systems', 'optics', 'optimization', 'physics', 'politics', 'probability', 'processors', 'psychology', 'public policy', 'quantitative modeling', 'quantum computing', 'robotics', 'security', 'server design', 'startups', 'statistics', 'system design', 'translation', 'web programming']
    langs1 = ['AJAX', 'AMPL', 'C', 'C++', 'ChucK', 'CSS', 'EES', 'Flask', 'Go', 'HTML', 'Java', 'JavaScript', 'Jinja2', 'Julia']
    langs2 = ['Machine Language', 'Mathematica', 'MATLAB', 'Max/MSP', 'OCalm', 'OpenFst', 'PHP', 'Python', 'R', 'SQL', 'Stata', 'Verilog', 'WEKA', 'Wolfram Language']
    html = render_template('home.html', netid=netid, tags1=tags1, tags2=tags2, tags3=tags3, langs1=langs1, langs2=langs2)
    response = make_response(html)
    return response

@app.route('/courseinfo')
def courseinfo():
    casauth = CASClient()
    netid = casauth.authenticate().rstrip()

    results = database.setup()
    html = render_template('courseinfo.html', results=results)
    response = make_response(html)
    return response

@app.route('/results', methods=['GET', 'POST'])
def results():
    casauth = CASClient()
    netid = casauth.authenticate().rstrip()

    if request.method == 'POST':
        langs = request.form.getlist('lang')
        tags = request.form.getlist('tag')

        if not (len(langs) or len(tags)):
            results = database.get_all()
            total = 0
            msg = "Looks like you didn't select any filters, so here is our complete list of courses."
        else:
            results_tags = database.filter_tags(tags)
            results_langs = database.filter_langs(langs)
            results = database.merge_results(results_langs, results_tags)
            msg = "The following courses matched at least one of your selections!"
        
        html = render_template('results.html', results=results, msg=msg)
        response = make_response(html)
        return response

@app.route('/path', methods=['GET', 'POST'])
def path():
    casauth = CASClient()
    netid = casauth.authenticate().rstrip()

    if request.method == 'POST':
        courses = request.form.getlist('courses')
        prereqs = request.form.getlist('prereqs')
        for course in courses:
            print(course)
        for pq in prereqs:
            print(pq)
        result_list = database.make_result_list(courses)
        for result in result_list:
            print(result.course)

        bundles = database.make_bundles(result_list, prereqs)
        for bundle in bundles:
            print(bundle.course)
            print(bundle.prereqs)
        
        new_bundles = database.remove_duplicate_prereqs(bundles)
        for bundle in new_bundles:
            print(bundle.course)
            print("------------")
            print(bundle.prereqs)
            print("\n")
        
        more_bundles = database.remove_duplicate_courses(new_bundles)
        for bundle in more_bundles:
            print(bundle.course)
            print("------------")
            print(bundle.prereqs)
            print("\n")

        html = render_template('path.html', bundles=bundles)
        response = make_response(html)
        return response

@app.route('/about')
def about():
    casauth = CASClient()
    netid = casauth.authenticate().rstrip()

    html = render_template('about.html')
    response = make_response(html)
    return response

@app.route('/tutorial')
def tutorial():
    casauth = CASClient()
    netid = casauth.authenticate().rstrip()

    html = render_template('tutorial.html')
    response = make_response(html)
    return response

@app.route('/saved', methods=['GET', 'POST'])
def saved():
    casauth = CASClient()
    netid = casauth.authenticate().rstrip()
    #netid = 'test'

    # add new path to db
    if request.method == 'POST':
        path = request.form.getlist('dragged')
        title = request.form.get('title')
        print(title)
        for item in path:
            print(item)
        print("here")
        paths.add_to_dict(netid, title, path)

    # render saved paths on page
    result = paths.get_row(netid)
    current_dict = {}
    if result is not None:
        current_dict = result.paths
        for title, path in current_dict.items():
            print(title + ":")
            print("------------")
            for course in path:
                print(course)

    html = render_template('saved.html', current_dict=current_dict)
    response = make_response(html)
    return response

@app.route('/delete_path', methods=['GET', 'POST'])
def delete_path():
    casauth = CASClient()
    netid = casauth.authenticate().rstrip()
    #netid = 'test'
    
    if request.method == 'POST':
        # get title of path to remove
        title = request.form.get('title')
        print("title: " + title)
        # get row in db matching current netid
        row = paths.get_row(netid)
        current_dict = row.paths
        # remove 
        paths.remove_row(row)
        print("row removed")
        # update
        removed = current_dict.pop(title, None)
        print(removed)
        paths.add_row(netid, current_dict)


    return redirect('/saved')

@app.route('/profile')
def profile():
    casauth = CASClient()
    netid = casauth.authenticate().rstrip()
    #netid = "test"
    if not profiles.check_exists(netid):
        html = render_template('profile.html')
        response = make_response(html)
        return response
    else:
        profile = profiles.get_row(netid)
        html = render_template('profile_saved.html', profile=profile)
        response = make_response(html)
        return response

@app.route('/profile_saved', methods=['GET', 'POST'])
def profile_saved():
    casauth = CASClient()
    netid = casauth.authenticate().rstrip()
    #netid = "test"
    if request.method == 'POST':
        btn_type = request.form.get('btn_type')
        if btn_type == 'Save':
        # get fields from edit form
            name = request.form.get('Name')
            print(name)
            class_yr = request.form.get('Class Year')
            degree = request.form.get('Degree')
            concentration = request.form.get('Concentration')
            goals = request.form.get('Goals')
            # remove existing row
            if profiles.check_exists(netid):
                profile = profiles.get_row(netid)
                profiles.remove_row(profile)
            # add updated row
            profiles.add_profile(netid, name, class_yr, degree, concentration, goals)
        # get new row
        profile = profiles.get_row(netid)

        html = render_template('profile_saved.html', profile=profile)
        response = make_response(html)
        return response

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    casauth = CASClient()
    netid = casauth.authenticate().rstrip()
    #netid = "test"
    if request.method == 'POST':
        profile = profiles.get_row(netid)
        html = render_template('edit_profile.html', profile=profile)
        response = make_response(html)
        return response



# from https://stackabuse.com/deploying-a-flask-application-to-heroku/
if __name__ == '__main__':
    app.run()