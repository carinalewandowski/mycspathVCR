# my database: postgresql://iwmrbkqwyomjyv:d225ea16492b84cf1dbaafd0c9a805696d8077814197239d92cc4bb692d94cb2@ec2-18-210-51-239.compute-1.amazonaws.com/d6jlofmjviv3dl
# --------------------------------------------------------------------------
#
# MyCSPath
# database.py
# author: Carina Lewandowski
#
# --------------------------------------------------------------------------


# --------------------------------------------------------------------------
# sources:
# https://www.compose.com/articles/using-postgresql-through-sqlalchemy/
# --------------------------------------------------------------------------

from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import ARRAY, INTEGER, JSON

# PostgreSQL URL
db_string = "postgresql://iwmrbkqwyomjyv:d225ea16492b84cf1dbaafd0c9a805696d8077814197239d92cc4bb692d94cb2@ec2-18-210-51-239.compute-1.amazonaws.com/d6jlofmjviv3dl"

# connect to database
db = create_engine(db_string)
base = declarative_base()
Session = sessionmaker(db)
session = Session()

class Bundle:
    def __init__(self, course, prereqs):
        self.course = course
        self.prereqs = prereqs

# --------------------------------------------------------------------------
# COURSES DATABASE
# --------------------------------------------------------------------------

class Database(base):
    __tablename__ = 'courses_subset'
    course = Column(String, primary_key=True)
    title = Column(String)
    crosslistings = Column(ARRAY(String))
    prerequisites = Column(ARRAY(String))
    offered = Column(String)
    languages = Column(ARRAY(String))
    tags = Column(ARRAY(String))

    def setup(self):
        db_string = "postgresql://iwmrbkqwyomjyv:d225ea16492b84cf1dbaafd0c9a805696d8077814197239d92cc4bb692d94cb2@ec2-18-210-51-239.compute-1.amazonaws.com/d6jlofmjviv3dl"
        db = create_engine(db_string)
        base = declarative_base()
        Session = sessionmaker(db)
        session = Session()
        results = session.query(Database)
        return results

    def filter_langs(self, languages):
        results = session.query(Database)
        filtered_ar = []
        for language in languages:
            filtered_results = results.filter(Database.languages.contains({language}))
            for result in filtered_results:
                if result not in filtered_ar:
                    filtered_ar.append(result)
        return filtered_ar

    def filter_tags(self, tags):
        results = session.query(Database)
        filtered_ar = []
        for tag in tags:
            filtered_results = results.filter(Database.tags.contains({tag}))
            for result in filtered_results:
                if result not in filtered_ar:
                    filtered_ar.append(result)
        return filtered_ar

    def merge_results(self, results_langs, results_tags):
        merged_results = []
        for entry in results_langs:
            if entry not in merged_results:
                merged_results.append(entry)
        for entry in results_tags:
            if entry not in merged_results:
                merged_results.append(entry)
        return merged_results

    def make_bundles(self, results, prereqs):
        # a list of bundles (courses w/ corresponding list of prereqs)
        unordered_path = []
        # results is a list of db entries for selected courses
        for result in results:
            c_prereqs = result.prerequisites
            not_taken = []
            for c_prereq in c_prereqs:
                if c_prereq not in prereqs:
                    not_taken.append(c_prereq)
            bundle = Bundle(result.course, not_taken)
            unordered_path.append(bundle)
        return unordered_path
    
    # removed duplicate prerequisites
    def remove_duplicate_prereqs(self, bundles):
        # build dict pq: courses
        pq_dict = {}
        for bundle in bundles:
            for pq in bundle.prereqs:
                # if pq already mapped, add the corresponding course to value list
                if pq in pq_dict:
                    value_list = pq_dict[pq]
                    value_list.append(bundle.course)
                    pq_dict[pq] = value_list
                # if pq not mapped, create entry with corresponding course 
                else:
                    value_list = []
                    value_list.append(bundle.course)
                    pq_dict[pq] = value_list
        for bundle in bundles:
            new_pq_list = []
            for pq in bundle.prereqs:
                if pq in pq_dict:
                    courses = pq_dict[pq]
                    pq_str = pq + " (needed for "
                    courses_left = len(courses)
                    for course in courses:
                        if courses_left > 1:
                            pq_str+= course +", "
                            courses_left-=1
                        else:
                            pq_str+= course + ")"
                    new_pq_list.append(pq_str)
                pq_dict.pop(pq, None)
            bundle.prereqs = new_pq_list
        return bundles
    
    # remove courses that are prereqs for other courses
    def remove_duplicate_courses(self, bundles):
        for bundle in bundles:
            for comp in bundles:
                if not bundle == comp:
                    prereqs = comp.prereqs
                    for pq in prereqs:
                        if bundle.course in pq[0:7]:
                            bundle.course = ''
        return bundles


            
                    
        


    # takes list of courses and returns corresponding list of db entries
    def make_result_list(self, courses):
        result_list = []
        results = session.query(Database)
        for course in courses:
            print("searching for: " + course)
            result = results.filter(Database.course == course)[0]
            print("appending result with course code: " + result.course)
            result_list.append(result)
        return result_list

# --------------------------------------------------------------------------
# PROFILES DATABASE
# --------------------------------------------------------------------------

class Profiles(base):
    __tablename__ = 'profiles'
    netid = Column(String, primary_key=True)
    user_name = Column(String)
    class_yr = Column(INTEGER)
    degree = Column(String)
    concentration = Column(String)
    goals = Column(String)

    # add a new profile to the db
    def add_profile(self, netid, user_name, class_yr, degree, concentration, goals):
        profile = Profiles(netid=netid,
        user_name=user_name, 
        class_yr=class_yr, 
        degree=degree, 
        concentration=concentration, 
        goals=goals)
        session.add(profile)
        session.commit()

    # check if a user already created a profile
    def check_exists(self, netid):
        results = session.query(Profiles)
        for result in results:
            if result.netid == netid:
                return True
        return False

    def get_row(self, netid):
        results = session.query(Profiles)
        for result in results:
            if result.netid == netid:
                return result
        return None
    def remove_row(self, profile):
        session.delete(profile)
        session.commit()

# --------------------------------------------------------------------------
# PATHS DATABASE
# --------------------------------------------------------------------------

class Paths(base):
    __tablename__ = 'paths'
    netid = Column(String, primary_key=True)
    paths = Column(JSON)

    def add_to_dict(self, netid, title, path):
        result = self.get_row(netid)
        current_dict = {}
        # if row already exists w netid
        if result is not None:
            current_dict = result.paths
            current_dict[title] = path
            # delete current row
            self.remove_row(result)
            # add updated row
            row = Paths(netid=netid,
            paths=current_dict)
            session.add(row)
            session.commit()
        else:
            current_dict[title] = path
            # add updated row
            row = Paths(netid=netid,
            paths=current_dict)
            session.add(row)
            session.commit()

    def remove_row(self, result):
        session.delete(result)
        session.commit()
    
    def get_row(self, netid):
        results = session.query(Paths)
        for result in results:
            if result.netid == netid:
                return result
        return None


""" Session = sessionmaker(db)
session = Session()

# Read title
results = session.query(Database)
for r in results:  
    print(r.title)
print("\n")

# Read tags
for r in results:
    print(r.title)
    print("------------------------------------")
    for topic in r.tags:
        print(topic)
    print("\n")

# selected languages
languages = []
languages.append("Java")

# selected tags
tags = []
# tags.append("machine learning")
# tags.append("security")
# tags.append("statistics")
tags.append("applications")
tags.append("artificial intelligence")
tags.append("security")

filtered_ar = []
# filter by language
for language in languages:
    filtered_results = results.filter(Database.languages.contains({language}))
    for result in filtered_results:
        if result not in filtered_ar:
            filtered_ar.append(result)
            print("results matching language: " + result.title)
    results = filtered_results
    filtered_ar2 = []
    # additionally filter by tags
    for tag in tags:
        filtered_results = results.filter(Database.tags.contains({tag}))
        for result in filtered_results:
            if result not in filtered_ar2:
                filtered_ar2.append(result)

# filtered_results = results.filter(Database.tags.contains({tag}))
print("PRINTING FILTERED RESULTS!\n")
for r in filtered_ar2:
    print(r.title)
    print("------------------------------------")
    for topic in r.tags:
        print(topic)
    print("\n") """