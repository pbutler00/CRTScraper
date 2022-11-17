from flask import Blueprint, render_template, request, g
import sqlite3
import datetime

DATABASE = 'C:/Users/jackd/Desktop/FrontEnd 11-16 V2/data.db'

views = Blueprint("views", __name__)

def get_db():
    db = getattr(g, '__data', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@views.route("/", methods = ["GET", "POST"])
@views.route("/home", methods = ["GET", "POST"])
def home():
    return render_template("frontend.html")

@views.route("/about")
def about():
    return render_template("about.html")

@views.route("/graphs")
def graphs():
    return render_template("graphs.html")

@views.route("/recent")
def recent():
    return render_template("recent.html")

@views.route("/results", methods = ["GET", "POST"])
def results():
    if request.method == "POST":

        keywords = []
        fields = []
        counter = 1
        while (request.form.get("kw"+str(counter)+"")):
            keywords.append(request.form.get("kw"+str(counter)+""))
            fields.append(request.form.get("fields"+str(counter)+""))
            counter += 1

        andors = []
        counter = 1
        while (request.form.get("andor"+str(counter)+"")):
            andors.append(request.form.get("andor"+str(counter)+""))
            counter += 1

        andors = andors[:len(keywords) - 1]

        counter = len(keywords)
        seperate_searches = []
        for i in range(counter):
            if fields[i] == "Title":
                seperate_searches.append(query_db("SELECT * FROM data WHERE Title LIKE '%"+ keywords[i] +"%'"))
            elif fields[i] == "Author":
                seperate_searches.append(query_db("SELECT * FROM data WHERE Author LIKE '%"+ keywords[i] +"%'"))
            elif fields[i] == "Text":
                seperate_searches.append(query_db("SELECT * FROM data WHERE Text LIKE '%"+ keywords[i] +"%'"))
            elif fields[i] == "Keywords":
                seperate_searches.append(query_db("SELECT * FROM data WHERE Keywords LIKE '%"+ keywords[i] +"%'"))
            elif fields[i] == "all fields":
                seperate_searches.append(query_db("SELECT * FROM data WHERE Title LIKE '%"+ keywords[i] +"%'") + 
                                         query_db("SELECT * FROM data WHERE Author LIKE '%"+ keywords[i] +"%'") +
                                         query_db("SELECT * FROM data WHERE Text LIKE '%"+ keywords[i] +"%'") +
                                         query_db("SELECT * FROM data WHERE Keywords LIKE '%"+ keywords[i] +"%'"))
        
        whole_search = []
        if (len(keywords) > 1):
            for index in range(len(andors)):
                item = andors[index]
                if item == 'and':
                    for row in seperate_searches[index+1]:
                        if row in seperate_searches[0]:
                            whole_search.append(row)
                    for row in seperate_searches[0]:
                        if row not in seperate_searches[index+1] and row in whole_search:
                            whole_search.remove(row)

                elif item == 'or':
                    for row in seperate_searches[0]:
                        whole_search.append(row)
                    for row in seperate_searches[index+1]:
                        if row not in seperate_searches[0]:
                            whole_search.append(row)

                elif item == 'not':
                    for row in seperate_searches[0]:
                        if row not in seperate_searches[index+1]:
                            whole_search.append(row)
        else:
            whole_search = seperate_searches[0]

        start = request.form.get("from")
        start_dt = datetime.date(int(start[0:4]), int(start[5:7]), int(start[8:]))
        end = request.form.get("to")
        end_dt = datetime.date(int(end[0:4]), int(end[5:7]), int(end[8:]))

        for row in whole_search:
            date = row['Date']
            slash1= date.find('/')
            slash2 = date.rfind('/')
            dt_obj = datetime.date(int(date[slash2 + 1:]), int(date[:slash1]), int(date[slash1 + 1: slash2]))
            if (dt_obj < start_dt) or (dt_obj > end_dt):
                whole_search.remove(row)
        
        whole_search_V2 = []
        all_sources = request.form.get("all")
        cnn = request.form.get("cnn")
        fox = request.form.get("fox")
        wapo  = request.form.get("wapo")
        msnbc = request.form.get("msnbc")
        nytimes = request.form.get("nytimes")

        if (all_sources):
            whole_search_V2 = whole_search
        else:
            for row in whole_search:
                if (cnn):
                    if (row['Source'] == 'www.cnn.com'):
                        whole_search_V2.append(row)
                if (fox):
                    if (row['Source'] == 'www.foxnews.com'):
                        whole_search_V2.append(row)
                if (wapo):
                    if (row['Source'] == 'www.washingtonpost.com'):
                        whole_search_V2.append(row)
                if (msnbc):
                    if (row['Source'] == 'www.msnbc.com'):
                        whole_search_V2.append(row)
                if (nytimes):
                    if (row['Source'] == 'www.nytimes.com'):
                        whole_search_V2.append(row)

        whole_search_V3 = []
        article_type = request.form.get("type")

        if (article_type == "all"):
            whole_search_V3 = whole_search_V2
        else:
            for row in whole_search_V2:
                if (article_type == "oped"):
                    if (row['Opinion'] == "Opinion"):
                        whole_search_V3.append(row)
                if (article_type == "journalistic"):
                    if (row['Opinion'] == "Non-Opinion"):
                        whole_search_V3.append(row)
                if (article_type == "non-text"):
                    if (row['Format'] == "Non-Text"):
                        whole_search_V3.append(row)
        
        explicit_inclusion = request.form.get("appearance")

        if (explicit_inclusion):
            for row in whole_search_V3:
                if (row['CRTinText'] == "CRT doesn't appear"):
                    whole_search_V3.remove(row)


        return render_template("results.html", seperate_searches = seperate_searches, rows = whole_search_V3)
