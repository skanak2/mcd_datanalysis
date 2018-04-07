import tweepy
import csv
import pickle
import psycopg2
import pandas as pd
####input your credentials here
consumer_key = 'C8F7iCj6dgci3MPGagTH0PYdC'
consumer_secret = 'NAr6hi17LIqHYrreZWf14aGbdw365ue49LGCJbLxjF6sgmXKJG'
access_token = '144087624-KKzNAWjccMEYpYr6Zf9USlccOBrNJZ9nHNMe8HmL'
access_token_secret = 'HFHCC6hqQVwb3MKyxwgUvYYEKrCey6ey4zs83FxMxL2Ud'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)
#####United Airlines
# Open/Create a file to append data
csvFile = open('ua.csv', 'a')
#Use csv Writer
csvWriter = csv.writer(csvFile)
try:
    conn = psycopg2.connect("dbname='alltweetsdata' user='skanak2' host='testdb.cqybmhselzg1.eu-west-1.rds.amazonaws.com' password='1monalisa2'")
except:
    print ("I am unable to connect to the database")


cur = conn.cursor()
for tweet in tweepy.Cursor(api.search,q="#mcdonalds",count=100,
                           lang="en",
                           since="2018-03-26").items():
    print (tweet.created_at, tweet.text)
    createdat=str(tweet.created_at)
    csvWriter.writerow([tweet.created_at, tweet.text.encode('utf-8')])
    try:
        cur.execute("INSERT INTO mcdtweets (tweet_id, text, screen_name, author_id, created_at) VALUES (%s, %s, %s, %s, %s);",(tweet.id, tweet.text, tweet.author.screen_name, tweet.author.id, tweet.created_at))
    except:
        print ("hello")
    conn.commit()
cur.close()
conn.close()