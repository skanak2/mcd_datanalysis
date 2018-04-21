# -*- coding: utf-8 -*-


from datetime import datetime, timedelta

import tweepy
import csv
import pickle
import psycopg2
import pandas as pd


yesterday = datetime.now() - timedelta(days=1)
year=yesterday.strftime('%y')
month=yesterday.strftime('%m')
date=yesterday.strftime('%d')
yesterday_date=("20"+str(year)+"-"+str(month)+"-"+str(date))
consumer_key = 'C8F7iCj6dgci3MPGagTH0PYdC'
consumer_secret = 'NAr6hi17LIqHYrreZWf14aGbdw365ue49LGCJbLxjF6sgmXKJG'
access_token = '144087624-KKzNAWjccMEYpYr6Zf9USlccOBrNJZ9nHNMe8HmL'
access_token_secret = 'HFHCC6hqQVwb3MKyxwgUvYYEKrCey6ey4zs83FxMxL2Ud'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)

# Open/Create a file to append dataa
csvFile = open('ua.csv', 'a')

csvWriter = csv.writer(csvFile)
try:
    conn = psycopg2.connect("dbname='alltweetsdata' user='skanak2' host='testdb.cqybmhselzg1.eu-west-1.rds.amazonaws.com' password='1monalisa2'")
except:
    print ("I am unable to connect to the database")


cur = conn.cursor()
alltweets=list
pos=0
neg=0
neu=0
for tweet in tweepy.Cursor(api.search,q="#mcdonalds",count=100,
                           lang="en",
                           since=str(yesterday_date),).items():
    """print (tweet.created_at, tweet.text)"""
    grap = (tweet.text).lower()
#check if a tweet is positive or not
    if (u'good'in grap or u'awesome' in grap or u'🙌🏽' in grap or u'💕'in grap or u'🤣' in grap or u'imlovinit' in grap or u'star' in grap or u'🍟' in grap or u'not acceptable'  in grap or u'🙄' in grap  or u'favourite' in grap or u'💯' in grap):
        pos = pos + 1
    elif (u'bad' in grap or u'misery' in grap or u'pain' in grap or u'wtf' in grap or u'heartbreaking' in grap or u'☹' in grap or u'imnotlovinit' in grap or u'wth' in grap or u'😢' in grap or u'😭' in grap ):
        neg = neg + 1
    else:
        neu = neu + 1
    createdat=str(tweet.created_at)
    csvWriter.writerow([tweet.created_at, tweet.text.encode('utf-8')])
    #insert all tweets in table
    try:
        cur.execute("INSERT INTO mcdtweets (tweet_id, text, screen_name, author_id, created_at) VALUES (%s, %s, %s, %s, %s);",(tweet.id, tweet.text, tweet.author.screen_name, tweet.author.id, tweet.created_at))
    except:
        print ("already exists")
    conn.commit()

#after getting all results of a day, insert into results table
cur.execute("INSERT INTO mcdresults(date, positive, negative, neutral) VALUES (%s, %s, %s, %s);",(datetime.now().date(), pos, neg,neu))

print ("already exists")
conn.commit()

cur.close()
conn.close()






print ("Hello #McDonalds according to today's Sentiment analysis "+str(pos)+" people liked you, "+str(neg)+" disliked you and "+str(neu)+
       " people are Neutral.")
#this is to send a tweet mentioning all details
status_update=" Hello #McDonalds according to today's Sentiment analysis "+str(pos)+" people liked you, "+str(neg)+" disliked you and "+str(neu)+" people are Neutral."
api.update_status(status_update)

with open("logformcd.txt", "a") as myfile:
    myfile.write(str(datetime.now())+"\n")