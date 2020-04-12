# my database: postgresql://carinalewandowski:qwerty@127.0.0.1/test_db

# --------------------------------------------------------------------------
# sources:
# https://www.compose.com/articles/using-postgresql-through-sqlalchemy/
from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import ARRAY


db_string = "postgresql://iwmrbkqwyomjyv:d225ea16492b84cf1dbaafd0c9a805696d8077814197239d92cc4bb692d94cb2@ec2-18-210-51-239.compute-1.amazonaws.com/d6jlofmjviv3dl"
# db_string = "postgresql://carinalewandowski:qwerty@127.0.0.1/test_db"

db = create_engine(db_string)
base = declarative_base()

class Database(base):
    __tablename__ = 'courses_subset'
    course = Column(String, primary_key=True)
    title = Column(String)
    crosslistings = Column(ARRAY(String))
    prerequisites = Column(ARRAY(String))
    offered = Column(String)
    languages = Column(ARRAY(String))
    tags = Column(ARRAY(String))

    def setup():
        db_string = "postgresql://iwmrbkqwyomjyv:d225ea16492b84cf1dbaafd0c9a805696d8077814197239d92cc4bb692d94cb2@ec2-18-210-51-239.compute-1.amazonaws.com/d6jlofmjviv3dl"
        db = create_engine(db_string)
        base = declarative_base()
        Session = sessionmaker(db)
        session = Session()
        results = session.query(Database)
        return results

    def filter_langs(self, languages):
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

Session = sessionmaker(db)
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
    print("\n")