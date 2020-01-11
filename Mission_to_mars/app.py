from flask import Flask,render_template,redirect
from flask_pymongo import PyMongo
import scraper

app = Flask(__name__)

# set up local host to connect to mongo

mongo = PyMongo(app,uri="mongodb://localhost:27017/mars_app")

@app.route("/")
def index():
    mars =mongo.db.mars.find_one()
    return render_template("index.html", mars = mars)

@app.route("/scrape")
def scrape():
    mars =mongo.db.mars
    mars_data = scraper.scrape_all()
    mars.update({},mars_data,upsert=True)
    return redirect("/",code=302)

if __name__ =="__main__":
    app.run(debug=True)
