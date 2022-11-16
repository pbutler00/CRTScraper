from flask import Blueprint, render_template, request, g
import sqlite3

DATABASE = 'C:/Users/jackd/Desktop/FrontEnd 11-15/data.db'

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
        for index in range(len(andors)):
            item = andors[index]
            if item == 'and':
                for row in seperate_searches[index+1]:
                    if row in seperate_searches[0]:
                        whole_search.append(row)

            elif item == 'or':
                for row in seperate_searches[index+1]:
                    if row not in seperate_searches[0]:
                        whole_search.append(row)

            elif item == 'not':
                for row in seperate_searches[0]:
                    if row not in seperate_searches[index+1]:
                        whole_search.append(row)

        start = request.form.get("from")
        end = request.form.get("to")

        all_sources = request.form.get("all")
        cnn = request.form.get("cnn")
        fox = request.form.get("fox")
        wapo  = request.form.get("wapo")
        msnbc = request.form.get("msnbc")
        nytimes = request.form.get("nytimes")

        article_type = request.form.get("type")
        return render_template("results.html", whole_search = whole_search)