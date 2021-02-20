import pandas as pd
import praw
from pprint import pprint
import warnings
from flask import Flask, render_template, request, redirect, url_for, session, flash
warnings.filterwarnings("ignore")
warnings.filterwarnings("ignore", category=DeprecationWarning) 

###############################################################################
# SQL server details
###############################################################################

app = Flask(__name__)
app.secret_key = 'wsb'
app.debug = True

my_client_id = 'R03GV48VhKDD-Q'
my_client_secret = '4hKPUsbnvFzGoSzJNCvLXjJZS-nxrw'
my_user_agent = 'sk_reddit_test'
reddit = praw.Reddit(client_id=my_client_id, client_secret=my_client_secret, user_agent=my_user_agent)
###############################################################################
# getting data 
###############################################################################
def getData(subr,query):
    subreddit = reddit.subreddit(subr)
    posts = subreddit.search(query)
    dataList = []
    for post in posts:
        if not post.stickied:
            postDict = {}
            postDict['headline'] = post.title
            postDict['ups'] = post.ups
            postDict['saved'] = post.saved
            postDict['view_count'] = post.view_count
            postDict['downs'] = post.downs
            dataList.append(postDict)
    return dataList

###############################################################################
# flask routes
###############################################################################
@app.route("/")
def main():
    return render_template("index.html")

@app.route("/searchredd", methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        subr = request.form['subr']
        query = request.form['query']
        data = getData(subr,query)
        print(subr,query)
        print(len(data))
        if not data:
            flash('Reddit has no opinion on this...')
            return redirect(url_for('main')) 
        else:
            return render_template("main.html",data=data,subr=subr,query=query)

###############################################################################
# run app
###############################################################################
if __name__ == "__main__":
    app.run()
