from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Import our pymongo library

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def home():
    
    mars_info = mongo.db.listings.find_one()
  
    return render_template("index.html", mars_info=mars_info)


@app.route("/scrape")
def scraper():
    
    mars_info = mongo.db.listings

   
    mars_data_dict= scrape_mars.scrape()
    
    mars_info.update({}, mars_data_dict, upsert=True)
    
    return "Scraping completed"


if __name__ == "__main__":
    app.run(debug=True)
