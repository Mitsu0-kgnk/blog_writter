import json
import pandas as pd
import tweepy
from requests_oauthlib import OAuth1Session
from time import sleep




class get_tweet():
    def trends(self):
        # API情報 
        CONSUMER_KEY = 'ImVGoxHYU0KEW1EjQSEfwj3wZ'
        CONSUMER_SECRET = 'vScInV6kgLV8W5xem6Iw7FbrLTIcXagdx3jSfC4mANki6x1d8k'
        ACCESS_TOKEN = '1175662253799956482-Q6ea6ShLamS4ubuIv1he7gCp7qry23'
        ACCESS_TOKEN_SECRET = 'ksQI9swPhKWYSLnI7RS9Mrv0wYHVGTnd6poPSC432gHp3'

        # Twitterオブジェクトの生成
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        api = tweepy.API(auth)

        #日本のWOEID
        woeid = 23424856
        #トレンド一覧取得
        trends = api.get_place_trends(woeid)


        #トレンド情報をデータフレーム化
        trends_df = pd.DataFrame(trends[0]['trends'])
        trends_df = trends_df.dropna(subset='tweet_volume')
        trends_df = trends_df.sort_values('tweet_volume',ascending=False)
        # トレンドキーワードをリスト化
        kwds_list = trends_df['name'].to_list()

        sleep(1)

        return kwds_list


